# Corporate Design

>As AAS Web UI user
>I want to change the look of the AAS Web UI according to my company's corporate design.

The AAS Web UI supports custom logos, primary application colours, and optional company information in the application footer.

## Feature Overview

The corporate design can be applied through Docker, while your own logo can either be added as a file or using an URL (e.g. from your CDN).

When using **Docker run**, you can configure the following:
1. Adding your own logos:
   * by mounting a local folder containing the main logo (Logo.png/jpg/svg) and the favicon (browser tab icon) named favicon.ico.
   _or_
   * by using an URL for the LOGO_PATH environment variable.
2. Changing the primary color: This is configured by using the *PRIMARY_COLOR* environment variable. It expects a color value in hex format.
3. Adding company information to the footer:
   * `COPYRIGHT_NAME` adds the company name next to the current year in the center of the footer.
   * `LEGAL_NOTICE_URL` adds a **Legal notice** link ("Impressum").
   * `PRIVACY_POLICY_URL` adds a **Privacy policy** link ("Datenschutz").

All three values are optional. If a value is empty or not configured, its footer entry is not shown. The company copyright is displayed in the center with the legal links in a compact row below it. The BaSyx copyright remains unchanged, is displayed on the left side of the desktop footer, and is hidden on mobile devices.

```{note}
Please note, that the logo and primary color for the light and dark theme can be configured separately (starting with eclipsebasyx/aas-gui:v2-241114) using `PRIMARY_LIGHT_COLOR`, `PRIMARY_DARK_COLOR` respectively `LOGO_LIGHT_PATH` and `LOGO_DARK_PATH`.
```

## Usage with Docker

To start the UI with docker run and your own logo, you can use the following commands either providing the logo as a file via a volume or directly as an URL:

`docker run -p 3000:3000 -v <local_path_to_logo>:/usr/src/app/dist/Logo -e LOGO_PATH=<your-logo.png> -e PRIMARY_COLOR=<primary_color> -e COPYRIGHT_NAME="Example Corp" -e LEGAL_NOTICE_URL=https://example.com/legal-notice -e PRIVACY_POLICY_URL=https://example.com/privacy-policy eclipsebasyx/aas-gui`

*or*

`docker run -p 3000:3000 -e LOGO_PATH=<your-logo-url-path> -e PRIMARY_COLOR=<primary_color> -e COPYRIGHT_NAME="Example Corp" -e LEGAL_NOTICE_URL=https://example.com/legal-notice -e PRIVACY_POLICY_URL=https://example.com/privacy-policy eclipsebasyx/aas-gui`

The same feature can also be adapted for **Docker compose**:

```yaml
aas-web-gui:
   image: eclipsebasyx/aas-gui
   container_name: aas-web-gui
   ports:
       - "3000:3000"
   environment:
       LOGO_PATH: "<your-logo.png>"
       PRIMARY_COLOR: "<primary_color>"
       COPYRIGHT_NAME: "Example Corp"
       LEGAL_NOTICE_URL: "https://example.com/legal-notice"
       PRIVACY_POLICY_URL: "https://example.com/privacy-policy"
   volumes:
       - <local_path_to_logo>:/usr/src/app/dist/Logo
```
*or*
```yaml
aas-web-gui:
   image: eclipsebasyx/aas-gui
   container_name: aas-web-gui
   ports:
       - "3000:3000"
   environment:
       LOGO_PATH: "<your-logo-url-path>"
       PRIMARY_COLOR: "<primary_color>"
       COPYRIGHT_NAME: "Example Corp"
       LEGAL_NOTICE_URL: "https://example.com/legal-notice"
       PRIVACY_POLICY_URL: "https://example.com/privacy-policy"
```
