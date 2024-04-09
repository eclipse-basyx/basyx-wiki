# Corporate Design
>As AAS Web UI user
>I want to change the look of the AAS Web UI according to my company's corporate design.

The AAS Web UI provides a feature to use your Logos and set the primary application colour.

## Feature Overview
The corporate design can be applied through Docker.

When using **Docker run**, you can add the logos by mounting a local folder containing the main logo (Logo.png/jpg/svg) and the favicon (browser tab icon) named favicon.ico. The primary colour can be configured by using the *VITE_PRIMARY_COLOR* environment variable. It expects a colour value in hex format.

`docker run -p 3000:3000 -v <local_path_to_logo>:/app/src/assets/Logo -e VITE_PRIMARY_COLOR=<primary_color> eclipsebasyx/aas-gui`
The same feature can also be adapted for **Docker compose**:
```
aas-web-gui:
   image: eclipsebasyx/aas-gui
   container_name: aas-web-gui
   ports:
       - "3000:3000"
   environment:
       VITE_PRIMARY_COLOR: "<primary_color>"
   volumes:
       - <local_path_to_logo>:/app/src/assets/Logo
```