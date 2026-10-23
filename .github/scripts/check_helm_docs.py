#!/usr/bin/env python3
"""Run the wiki's Helm examples without accessing a Kubernetes cluster.

Requires Helm 3, curl, and PyYAML. Omit --chart-version to check the latest
stable release; pass a published version to reproduce a specific check.
"""

import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile

import yaml


ROOT = Path(__file__).resolve().parents[2]
GUIDE = ROOT / 'docs/source/content/user_documentation/helm'


def run(command, directory, env):
    print('+ ' + ' '.join(command), flush=True)
    return subprocess.run(command, cwd=directory, env=env, check=True,
                          text=True, capture_output=True, timeout=180).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chart-version', default='')
    args = parser.parse_args()
    if args.chart_version and not re.fullmatch(r'\d+\.\d+\.\d+', args.chart_version):
        parser.error('--chart-version must be an exact stable version such as X.Y.Z')

    page = (GUIDE / 'installation.md').read_text()
    snippets = dict(re.findall(
        r'<!-- helm-docs-check: (\w+) -->\s*```bash\n(.*?)\n```', page, re.S))
    if set(snippets) != {'download', 'render', 'lint'}:
        raise RuntimeError('Installation guide must mark its download, render, and lint examples')

    with tempfile.TemporaryDirectory(prefix='basyx-helm-docs-') as temporary:
        directory = Path(temporary)
        env = dict(os.environ, KUBECONFIG=os.devnull,
                   HELM_CACHE_HOME=str(directory / 'cache'),
                   HELM_CONFIG_HOME=str(directory / 'config'),
                   HELM_DATA_HOME=str(directory / 'data'),
                   BASYX_NAMESPACE='basyx-evaluation')
        helm_version = run(['helm', 'version', '--short'], directory, env)
        if not helm_version.startswith('v3.'):
            raise RuntimeError('These documentation examples require Helm 3')
        run(['helm', 'repo', 'add', 'basyx', 'https://eclipse-basyx.github.io/charts'], directory, env)
        run(['helm', 'repo', 'update'], directory, env)
        selection = ['--version', args.chart_version] if args.chart_version else []
        metadata = yaml.safe_load(run(['helm', 'show', 'chart', 'basyx/basyx', *selection], directory, env))
        version = str(metadata['version'])
        if not re.fullmatch(r'\d+\.\d+\.\d+', version):
            raise RuntimeError('Expected a stable chart release')
        env['BASYX_CHART_VERSION'] = version
        print(f'Checking chart {version}, appVersion {metadata.get("appVersion")}', flush=True)
        overlay = (GUIDE / 'examples/values.cluster.yaml').read_text()
        overlay = overlay.replace('YOUR_INGRESS_CLASS', 'nginx')
        overlay = overlay.replace('YOUR_CLUSTER_ISSUER', 'platform-issuer')
        (directory / 'values.cluster.yaml').write_text(overlay)

        # Execute the actual documented commands rather than a parallel example.
        for name in ['download', 'render', 'lint']:
            output = run(['bash', '-euo', 'pipefail', '-c', snippets[name]], directory, env)
            print(output, flush=True)

        resources = [x for x in yaml.safe_load_all((directory / 'rendered.yaml').read_text()) if x]
        by_kind_name = {(x['kind'], x['metadata']['name']): x for x in resources}
        for name in ['basyx-aas-environment', 'basyx-aas-web-ui']:
            by_kind_name['Deployment', name]
        by_kind_name['Cluster', 'basyx-database']
        initializer = by_kind_name['Job', 'basyx-configuration']
        events = initializer['metadata']['annotations']['helm.sh/hook'].split(',')
        if 'post-install' not in events or 'pre-upgrade' not in events:
            raise RuntimeError('Initializer lifecycle changed; review the installation and upgrade guidance')
        print(f'PASS: documented download, render, lint, and startup contract for chart {version}')


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(exc.stdout or '')
        print(exc.stderr or '')
        raise SystemExit(exc.returncode)
