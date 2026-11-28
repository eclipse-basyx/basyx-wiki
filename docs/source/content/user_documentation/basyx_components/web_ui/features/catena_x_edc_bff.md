# Catena-X EDC BFF

> **As a** system administrator  
> **I want to** connect the BaSyx AAS Web UI to the Eclipse Dataspace Connector (EDC) of my company  
> **so that** users can browse partner data and manage the EDC without the browser ever seeing the EDC credentials.

## Feature Overview

The **Catena-X EDC BFF** (backend for frontend) is a small Node.js server that ships with the BaSyx AAS Web UI. It sits between the browser and a [Tractus-X EDC](https://github.com/eclipse-tractusx/tractusx-edc) and is used by:

- the **[CatenaXplorer](./modules/catenaxplorer.md)**, which loads Digital Twin Registry (DTR) descriptors and Submodels of business partners through the EDC (read-only), and
- the **[Eclipse Dataspace Connector](./modules/eclipse_dataspace_connector.md)** module, which manages assets, policies and contracts of your EDC and fetches data from and sends data to business partners.

The basic security rule: **the browser only knows an EDC proxy ID.** The EDC Management API URL, its API key, the Endpoint Data References (EDRs) and the authorization for the data planes of the partners stay in the BFF.

```text
Browser
  -> http(s)://<web-ui-host>/api/catena-x/edc/<proxyId>/...
  -> nginx of the aas-web-ui container (port 3000)
  -> Catena-X EDC BFF (port 3001, not published)
  -> consumer EDC Management API and provider data planes
```

---

## Deployment

The BFF is disabled by default. There are three ways to run it.

### Integrated in the Web UI Container

The `eclipsebasyx/aas-gui` image contains the compiled BFF. With `CX_EDC_BFF_ENABLED=true`, the container starts it next to nginx on `127.0.0.1:${CX_EDC_BFF_PORT}` (default `3001`) and nginx forwards `/api/catena-x/edc/` to it.

```yaml
services:
  aas-web-ui:
    image: eclipsebasyx/aas-gui
    ports:
      - "3000:3000"            # publish only the UI port, never 3001
    volumes:
      - ./basyx-infra.yml:/basyx-infra.yml
    environment:
      CX_EDC_BFF_ENABLED: "true"
      CX_EDC_BFF_AUTH_MODE: "none"
      CX_EDC_DEFAULT_MANAGEMENT_URL: "https://consumer-edc.example.com/management"
      CX_EDC_DEFAULT_API_KEY: "${CX_EDC_DEFAULT_API_KEY}"
      CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES: "https://provider-edc.example.com/api/v1/dsp"
      CX_EDC_ALLOWED_DATA_PLANE_ADDRESSES: "https://provider-dataplane.example.com/api/public"
      # Only for the Eclipse Dataspace Connector module:
      CX_EDC_DEFAULT_ALLOW_MANAGEMENT_WRITES: "true"
```

A complete example, including `.env` and `basyx-infra.yml`, is the [CatenaXplorer EDC Standalone example](https://github.com/eclipse-basyx/basyx-aas-web-ui/tree/main/examples/CatenaXplorerEdcStandalone).

### Separate BFF Container

The Dockerfile of the Web UI has a build target `edc-bff-stage` that contains only the BFF. Run it as a separate container and point the Web UI to it with `CX_EDC_BFF_UPSTREAM_URL`. Without `CX_EDC_BFF_ENABLED=true`, the Web UI forwards to `http://catena-x-edc-bff:3001` by default.

### Local Development

For running the BFF next to the Vite dev server (`pnpm bff:build`, `pnpm bff:start`, `pnpm bff:dev`), see [Catena-X EDC BFF Local Development](https://github.com/eclipse-basyx/basyx-aas-web-ui/blob/main/Docs/CatenaXEdcBffDevelopment.md) in the Web UI repository.

```{warning}
`CX_EDC_BFF_AUTH_MODE=none`, as in the example above, trusts every request that reaches the Web UI. Use it only when access to the Web UI is controlled by the deployment, e.g. an internal network, VPN or a protected ingress, or switch to [`jwt`](#authentication).
```

---

## Infrastructure Configuration

The Web UI finds the BFF through an infrastructure with the `catena-x` template. Its `catenaX` section names the BFF proxy and the business partners. It contains **no** credentials.

```yaml
infrastructures:
  default: catena-x-edc

  catena-x-edc:
    name: Catena-X EDC
    template: catena-x
    components: {}
    catenaX:
      accessMode: edc
      edc:
        proxyId: default
        defaultPartnerId: provider-a
        partners:
          - id: provider-a
            name: Provider A
            counterPartyId: "BPNL000000000001"
            counterPartyAddress: "https://provider-edc.example.com/api/v1/dsp"
    security:
      type: none
```

| Field | Description |
| --- | --- |
| `catenaX.accessMode` | `edc` reaches DTR and Submodels of partners through the EDC; `direct` uses the `digitalTwinRegistry` and `submodelService` endpoints of the infrastructure without an EDC |
| `catenaX.edc.proxyId` | ID of the EDC proxy in the BFF, see [Multiple EDC proxies](#multiple-edc-proxies). Without it, the Web UI uses the proxy `default` |
| `catenaX.edc.partners` | Business partners, each with `id`, optional `name`, `counterPartyId` (the BPN of the partner) and `counterPartyAddress` (its DSP endpoint) |
| `catenaX.edc.defaultPartnerId` | Partner selected by default; without it the first partner |
| `catenaX.edc.defaultCounterPartyId`, `defaultCounterPartyAddress` | Older way to configure a single partner, still supported |

`components` may be omitted for an infrastructure that only uses the EDC.

The DSP address of every partner must start with one of the prefixes in `CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES`. With `ENDPOINT_CONFIG_AVAILABLE=true`, users can also manage partners in **Settings → Manage Infrastructures**; these changes are stored in the browser, while credentials and allowlists remain BFF settings.

---

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `CX_EDC_BFF_ENABLED` | Starts the BFF inside the Web UI container (Web UI image only) | `false` |
| `CX_EDC_BFF_UPSTREAM_URL` | URL nginx forwards `/api/catena-x/edc/` to (Web UI image only) | `http://127.0.0.1:<CX_EDC_BFF_PORT>` if integrated, otherwise `http://catena-x-edc-bff:3001` |
| `CX_EDC_BFF_PORT` | Port of the BFF | `3001` |
| `CX_EDC_BFF_AUTH_MODE` | `jwt` or `none`, see [Authentication](#authentication) | `jwt` |
| `CX_EDC_BFF_AUTH_JWKS_URL` | JWKS URL of the identity provider; required for `jwt` | - |
| `CX_EDC_BFF_AUTH_ISSUER` | Expected issuer of the token (optional) | - |
| `CX_EDC_BFF_AUTH_AUDIENCE` | Expected audience of the token (optional) | - |
| `CX_EDC_BFF_REQUIRED_ROLES` | Comma-separated roles or scopes; the token needs one of them (optional) | - |
| `CX_EDC_DEFAULT_MANAGEMENT_URL` | Management API URL of your (consumer) EDC, ending with `/management` | - |
| `CX_EDC_DEFAULT_API_KEY` | Management API key of your EDC | - |
| `CX_EDC_DEFAULT_API_KEY_HEADER` | Header of the API key | `X-Api-Key` |
| `CX_EDC_DEFAULT_PARTICIPANT_ID` | Your own participant ID, shown in the status (optional) | - |
| `CX_EDC_DEFAULT_DSP_ENDPOINT` | Your own DSP endpoint (optional, metadata only) | - |
| `CX_EDC_DEFAULT_DATA_PLANE_PROXY_URL` | Data plane proxy URL (optional, metadata only) | - |
| `CX_EDC_DEFAULT_ALLOW_MANAGEMENT_WRITES` | Allows creating, updating and deleting assets, policies and contracts through the `default` proxy, see [Management writes](#management-writes) | `false` |
| `CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES` | Comma-separated DSP endpoint prefixes of partners, or `*` | - |
| `CX_EDC_ALLOWED_DATA_PLANE_ADDRESSES` | Comma-separated data plane endpoint prefixes of partners, or `*`. **Required** to reach any data plane, see [Allowlists](#allowlists) | - |
| `CX_EDC_ALLOW_INSECURE_COUNTER_PARTY_ADDRESSES` | Allows `http:` DSP and data plane addresses, for local testing only | `false` |
| `CX_EDC_REQUEST_TIMEOUT_MS` | Timeout of requests to the EDC and to data planes | `30000` |
| `CX_EDC_EDR_POLLING_ATTEMPTS` | Attempts to get the EDR after a contract negotiation | `30` |
| `CX_EDC_EDR_POLLING_INTERVAL_MS` | Delay between these attempts | `2000` |
| `CX_EDC_PROXY_CONFIG_JSON`, `CX_EDC_PROXY_CONFIG_FILE` | Several EDC proxies as JSON or as path to a JSON file, see [Multiple EDC proxies](#multiple-edc-proxies) | - |
| `NODE_USE_ENV_PROXY` | `1` routes outgoing requests through `HTTP_PROXY`/`HTTPS_PROXY` (respecting `NO_PROXY`) | disabled |

```{note}
Empty variables are ignored, e.g. those set by `${VAR:-}` in Docker Compose. They don't override a value from `CX_EDC_PROXY_CONFIG_*`.
```

### Multiple EDC Proxies

The `CX_EDC_DEFAULT_*` variables configure the proxy `default`. For several EDCs, or to give users read-only and read-write access to the same EDC, configure proxies with `CX_EDC_PROXY_CONFIG_JSON` or `CX_EDC_PROXY_CONFIG_FILE`:

```json
{
  "proxies": {
    "default": {
      "managementUrl": "https://consumer-edc.example.com/management",
      "apiKey": "<EDC_MANAGEMENT_API_KEY>",
      "allowedCounterPartyAddresses": ["https://provider-edc.example.com/api/v1/dsp"],
      "allowedDataPlaneAddresses": ["https://provider-dataplane.example.com/api/public"],
      "allowManagementWrites": true
    },
    "read-only": {
      "managementUrl": "https://consumer-edc.example.com/management",
      "apiKey": "<EDC_MANAGEMENT_API_KEY>",
      "participantId": "BPNL000000000000"
    }
  }
}
```

Each proxy accepts `managementUrl`, `apiKey`, `apiKeyHeader`, `participantId`, `dspEndpoint`, `dataPlaneProxyUrl`, `allowedCounterPartyAddresses`, `allowedDataPlaneAddresses`, `allowInsecureCounterPartyAddresses`, `allowManagementWrites`, `requestTimeoutMs`, `edrPollingAttempts` and `edrPollingIntervalMs`.

- The allowlists of a proxy are **added** to the global allowlists `CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES` and `CX_EDC_ALLOWED_DATA_PLANE_ADDRESSES`.
- The `CX_EDC_DEFAULT_*` variables that are set override only the matching fields of the `default` entry. Without a `default` entry, they create one only together with `CX_EDC_DEFAULT_MANAGEMENT_URL` or `CX_EDC_DEFAULT_API_KEY`.
- An infrastructure selects a proxy with `catenaX.edc.proxyId`.

---

## Security

### Authentication

| `CX_EDC_BFF_AUTH_MODE` | Behavior |
| --- | --- |
| `none` | The BFF accepts every request. Protect the Web UI by network or ingress. |
| `jwt` (default) | The BFF requires a bearer token, checks its signature against `CX_EDC_BFF_AUTH_JWKS_URL` and, if set, its issuer, audience and roles. The Web UI sends the token of the selected infrastructure, so configure the infrastructure with `security.type: oauth2`. |

Roles are read from `roles`, `realm_access.roles`, `resource_access.*.roles` and `scope` of the token. Never put OAuth2 client credentials in the browser configuration.

### Allowlists

The BFF only contacts partner endpoints that start with an allowed prefix:

- **`CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES`** covers the DSP endpoints of partners, used for catalog requests and contract negotiations. Other addresses are refused.
- **`CX_EDC_ALLOWED_DATA_PLANE_ADDRESSES`** covers the data planes of partners. A partner names its data plane in the EDR, usually on another host or path than its DSP endpoint, so this allowlist is separate and **does not inherit** from the DSP allowlist. It has no default: without it, the BFF reaches no data plane, so neither the CatenaXplorer nor the module can load DTR descriptors, Submodels or data. Refused data planes fail with `403 DATA_PLANE_ADDRESS_NOT_ALLOWED`, naming the refused origin.

Every data plane call uses `requestTimeoutMs` and doesn't follow redirects (`502 DATA_PLANE_REDIRECT_REFUSED`).

Only `https:` addresses are allowed. `CX_EDC_ALLOW_INSECURE_COUNTER_PARTY_ADDRESSES=true` additionally allows `http:`, for DSP and data plane addresses; other schemes are always refused. The wildcard `*` and `http:` are meant for local testing, not for shared or production environments.

### Management Writes

Reading works with every proxy. **Creating, updating and deleting** assets, policies and contracts is disabled by default, in every auth mode including `none`, because the BFF sends these requests with its own Management API key.

- Enable it per proxy with `allowManagementWrites: true`, or with `CX_EDC_DEFAULT_ALLOW_MANAGEMENT_WRITES=true` for the `default` proxy.
- Without it, write requests fail with `403 EDC_MANAGEMENT_WRITES_DISABLED`, and the Eclipse Dataspace Connector module hides its create, edit and delete actions (it reads `managementWritesAllowed` from the [status](#status)).
- With `CX_EDC_BFF_AUTH_MODE=jwt`, every user with a valid token (and one of the `CX_EDC_BFF_REQUIRED_ROLES`, if set) can write. To keep some users read-only, give their infrastructure a separate proxy without the flag.

A CatenaXplorer-only deployment doesn't need management writes.

Resource IDs containing `/` are refused with `400 EDC_ID_NOT_ADDRESSABLE`, also on create: the EDC refuses an encoded `/` (`%2F`) in the request path, so such a resource could not be updated or deleted later. An update whose `@id` differs from the ID in the path is refused with `400 EDC_ID_MISMATCH`.

### Secrets in Assets

Asset queries never return secrets to the browser. The BFF replaces them with `<redacted>`:

- in the data address: `authCode`, `oauth2:clientSecret`, the values of all `header:*` properties and other secret-like keys,
- in the private properties: secret-like values such as `apiKey`, `password` or `token`, also nested ones.

Names of secrets in the EDC vault, such as `secretName` or `oauth2:clientSecretKey`, and URLs stay visible.

When an asset is updated with `<redacted>` still in place, the BFF takes the stored secret from the EDC:

- **Data address**: only while the rest of the data address is unchanged. A new `baseUrl`, any other changed property or a renamed, added or removed secret needs the secret to be entered again, so a stored secret never goes to a new target.
- **Private properties**: from the same path, as the EDC sends them nowhere.

A placeholder the BFF can't resolve, also in a new asset, is refused with `400 EDC_REDACTED_SECRET`.

---

## Dataspace Protocol and Supported EDC Versions

### Dataspace Protocol 2025-1

The BFF uses the Dataspace Protocol (DSP) **`dataspace-protocol-http:2025-1`** for all catalog, DTR and contract requests. It decides the DSP version alone: a `protocol` in a request from the browser is ignored.

The BFF adds the version path `/2025-1` to the DSP address of a partner, unless the address already has one; a query stays at the end. For example, `https://partner.example.com/api/v1/dsp?tenant=a` becomes `https://partner.example.com/api/v1/dsp/2025-1?tenant=a`.

```{important}
**Partner connectors must support DSP 2025-1**, i.e. Tractus-X EDC 0.11 or later (0.12.3 or later is recommended, as it fixes a security issue). Partners that only speak DSP 0.8 can't be reached, neither from the CatenaXplorer nor from the Eclipse Dataspace Connector module.
```

### Supported Tractus-X EDC Versions

Your own EDC, the one the BFF talks to, has to be **Tractus-X EDC 0.12.x or 0.13.x**. The BFF uses these Management API endpoints:

| Endpoint | Available in |
| --- | --- |
| `/v3/assets`, `/v3/policydefinitions`, `/v3/contractdefinitions` | 0.8.0–0.13.0, deprecated in 0.13.0 |
| `/v3/catalog/request` | 0.8.0–0.13.0, deprecated in 0.13.0 |
| `/v3/edrs`, `/v3/edrs/request`, `/v3/edrs/{id}/dataaddress` | 0.8.0–0.13.0 |
| `/v4alpha/connectordiscovery/dspversionparams` | from 0.11.0, deprecated in 0.13.0 |
| `/v4alpha/connectordiscovery/connectors` | from 0.12.0, deprecated in 0.13.0 |

Older versions miss parts of the connector discovery, and versions before 0.11 support neither DSP 2025-1 nor the Catena-X 2025/9 policy context that the policy templates of the module use. The request bodies are the same in 0.12.x and 0.13.0. 0.13.0 also serves the connector discovery under `/v3/connectordiscovery`; `/v4alpha` still works there, so the BFF keeps using it. The BFF has no setting for the EDC version.

---

## API Reference

All routes are below `/api/catena-x/edc/<proxyId>/`. Request and response bodies are JSON.

| Route | Method | Purpose | Management writes |
| --- | --- | --- | --- |
| `status` | GET | Configuration status of the proxy, without secrets | |
| `connectors/discover` | POST | Discovers the connectors of a partner | |
| `catalog/request` | POST | Catalog of a partner; with `assetId` only the dataset of this asset | |
| `assets/request`, `policydefinitions/request`, `contractdefinitions/request` | POST | Queries the resources of your EDC (`/v3/<resource>/request`); asset secrets are redacted | |
| `assets`, `policydefinitions`, `contractdefinitions` | POST | Creates a resource | required |
| `assets/<id>`, `policydefinitions/<id>`, `contractdefinitions/<id>` | PUT | Updates a resource | required |
| `assets/<id>`, `policydefinitions/<id>`, `contractdefinitions/<id>` | DELETE | Deletes a resource | required |
| `dtr/shell-descriptors`, `dtr/shell-descriptors/by-id` | POST | Shell descriptors from the DTR of a partner (CatenaXplorer) | |
| `submodels/fetch` | POST | Submodel from the data plane of a partner (CatenaXplorer) | |
| `data/fetch` | POST | Negotiates an asset of a partner and gets its data from the data plane | |
| `data/push` | POST | Negotiates a push asset of a partner and posts data to its data plane (body at most 16 MB) | |

`/health` (outside the API path) returns `{"status": "ok"}` for container health checks.

### Status

`GET /api/catena-x/edc/<proxyId>/status` shows whether a proxy is configured, without revealing secrets, e.g.:

```json
{
  "id": "default",
  "configured": true,
  "managementUrlConfigured": true,
  "apiKeyConfigured": true,
  "participantId": "BPNL000000000000",
  "dspEndpointConfigured": false,
  "dataPlaneProxyUrlConfigured": false,
  "allowedCounterPartyAddressCount": 1,
  "allowedDataPlaneAddressCount": 1,
  "allowInsecureCounterPartyAddresses": false,
  "managementWritesAllowed": true
}
```

An unknown proxy ID returns `404`.

### Error Codes

Errors are JSON with `status`, `error`, `code` and, where helpful, `details` telling how to fix the request. Errors of the EDC Management API are passed on with their messages.

| Status | Code | Cause |
| --- | --- | --- |
| 400 | `INVALID_JSON` | The request body is no valid JSON |
| 400 | `INVALID_PATH_ENCODING` | Invalid percent-encoding in the request path |
| 400 | `EDC_ID_MISSING` | The route needs a resource ID |
| 400 | `EDC_ID_NOT_ADDRESSABLE` | The resource ID contains a `/` |
| 400 | `EDC_ID_MISMATCH` | The `@id` of an update differs from the ID in the path |
| 400 | `EDC_REDACTED_SECRET` | `<redacted>` can't be replaced by a stored secret |
| 401 / 403 | - | Missing, invalid or expired token, or wrong issuer, audience or role (`jwt` mode) |
| 403 | `EDC_MANAGEMENT_WRITES_DISABLED` | Management writes are not allowed for the proxy |
| 403 | `COUNTERPARTYADDRESS_IS_NOT_ALLOWED_BY_THE_EDC_PROXY_ALLOWLIST` | The DSP address of the partner is not in `CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES` |
| 403 | `DATA_PLANE_ADDRESS_NOT_ALLOWED` | The data plane is not in `CX_EDC_ALLOWED_DATA_PLANE_ADDRESSES` |
| 502 | `DATA_PLANE_REDIRECT_REFUSED` | The data plane answered with a redirect |
| 504 | `EDC_REQUEST_TIMEOUT` | The EDC or data plane didn't answer within `CX_EDC_REQUEST_TIMEOUT_MS` |

---

## Upgrading

When upgrading from a Web UI version without the Eclipse Dataspace Connector module:

1. **Set `CX_EDC_ALLOWED_DATA_PLANE_ADDRESSES`.** It is required now: without it, the CatenaXplorer can no longer load DTR descriptors and Submodels. Add the data plane origins of your partners; a refused request names the origin to add.
2. **Check the DSP version of your partners.** Partners need DSP 2025-1 (Tractus-X EDC 0.11 or later).
3. **Check `CX_EDC_ALLOW_INSECURE_COUNTER_PARTY_ADDRESSES`.** It now allows `http:` only; other schemes are refused.
4. **Check combined configurations.** If you use `CX_EDC_PROXY_CONFIG_*` together with `CX_EDC_DEFAULT_*` variables, the variables now override only their own fields of the `default` entry. Before, setting `CX_EDC_DEFAULT_MANAGEMENT_URL` or `CX_EDC_DEFAULT_API_KEY` cleared its other fields.
5. **Enable management writes** (`CX_EDC_DEFAULT_ALLOW_MANAGEMENT_WRITES=true` or `allowManagementWrites`) only where the Eclipse Dataspace Connector module should create, update and delete resources.

If you run the BFF behind your own reverse proxy, allow request bodies of 16 MB for `/api/catena-x/edc/`, as the bundled nginx does, so AAS and Submodels can be sent.

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `404` from `/api/catena-x/edc/...` for every request | The BFF doesn't know the proxy ID: check `catenaX.edc.proxyId` and the configured proxies. If nginx itself answers, check `CX_EDC_BFF_ENABLED` or `CX_EDC_BFF_UPSTREAM_URL`. |
| `401` from `/api/catena-x/edc/...` | Only in `jwt` mode: the token is missing, expired or not accepted. Check the `oauth2` security of the infrastructure and `CX_EDC_BFF_AUTH_*`. |
| The DSP address of a partner is refused | Add its prefix to `CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES`. |
| `403 DATA_PLANE_ADDRESS_NOT_ALLOWED` | Add the origin named in the error to `CX_EDC_ALLOWED_DATA_PLANE_ADDRESSES`. |
| Contract negotiation or catalog request of a partner fails with `400` | The partner probably doesn't support DSP 2025-1. |
| EDR polling timeout | The negotiation didn't produce an EDR in time. Check whether your EDC fulfills the policy of the partner and look at the EDC logs; raise `CX_EDC_EDR_POLLING_ATTEMPTS` if negotiations are slow. |
| The module offers no create, edit or delete actions | Management writes are not allowed for the proxy, see [Management writes](#management-writes). |
| Port `3001` is already in use | Stop the other process or set another `CX_EDC_BFF_PORT`. |
