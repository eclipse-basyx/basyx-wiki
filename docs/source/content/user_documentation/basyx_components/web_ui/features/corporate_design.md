# Corporate Design

>As AAS Web UI user
>I want to change the look of the AAS Web UI according to my company's corporate design.

The AAS Web UI provides a feature to use your Logos and set the primary application colour.

## Feature Overview

The corporate design can be applied through Docker.

When using **Docker run**, you can add the logos by mounting a local folder containing the main logo (Logo.png/jpg/svg) and the favicon (browser tab icon) named favicon.ico. The primary color can be configured by using the *PRIMARY_COLOR* environment variable. It expects a color value in hex format.

Please note, that the logo and primary color for the light and dark theme can be configured separately (starting with eclipsebasyx/aas-gui:v2-241114) using *PRIMARY_LIGHT_COLOR*, *PRIMARY_DARK_COLOR* respectivly *LOGO_LIGHT_PATH* and *LOGO_DARK_PATH*.

`docker run -p 3000:3000 -v <local_path_to_logo>:/usr/src/app/dist/Logo -e LOGO_PATH=Logo/<your-logo.png> -e VITE_PRIMARY_COLOR=<primary_color> eclipsebasyx/aas-gui`
The same feature can also be adapted for **Docker compose**:

```yaml
aas-web-gui:
   image: eclipsebasyx/aas-gui
   container_name: aas-web-gui
   ports:
       - "3000:3000"
   environment:
       LOGO_PATH: "Logo/<your-logo.png>"
       PRIMARY_COLOR: "<primary_color>"
   volumes:
       - <local_path_to_logo>:/usr/src/app/dist/Logo
```
