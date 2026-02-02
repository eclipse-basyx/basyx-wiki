# Corporate Design

>As AAS Web UI user
>I want to change the look of the AAS Web UI according to my company's corporate design.

The AAS Web UI provides a feature to use your Logos and set the primary application colour.

## Feature Overview

The corporate design can be applied through Docker, while your own logo can either be added as a file or using an URL (e.g. from your CDN).

When using **Docker run**, you can configure the following:
1. Adding your own logos:
   * by mounting a local folder containing the main logo (Logo.png/jpg/svg) and the favicon (browser tab icon) named favicon.ico.
   _or_
   * by using an URL for the LOGO_PATH environment variable.
2. Changing the primary color: This is configured by using the *PRIMARY_COLOR* environment variable. It expects a color value in hex format.

> [!NOTE]
> Please note, that the logo and primary color for the light and dark theme can be configured separately (starting with eclipsebasyx/aas-gui:v2-241114) using *PRIMARY_LIGHT_COLOR*, *PRIMARY_DARK_COLOR* respectivly *LOGO_LIGHT_PATH* and *LOGO_DARK_PATH*.

## Usage with Docker

To start the UI with docker run and your own logo, you can use the following commands either providing the logo as a file via a volume or directly as an URL:

`docker run -p 3000:3000 -v <local_path_to_logo>:/usr/src/app/dist/Logo -e LOGO_PATH=<your-logo.png> -e VITE_PRIMARY_COLOR=<primary_color> eclipsebasyx/aas-gui`

*or*

`docker run -p 3000:3000 -e LOGO_PATH=<your-logo-url-path> -e VITE_PRIMARY_COLOR=<primary_color> eclipsebasyx/aas-gui`

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
```
