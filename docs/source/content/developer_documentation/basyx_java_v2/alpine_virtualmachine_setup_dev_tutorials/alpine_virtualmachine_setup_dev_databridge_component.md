# DataBridge Component
This tutorial explains how a virtual machine for the [DataBridge](../../../basyx_components/databridge/index.md) component is created based on the base image described [here](./alpine_virtualmachine_setup_dev_base_image.md).


## VirtualBox
### Import the base image
Import the virtual machine image under *File -> Import Appliance*. Do **not** tick *Import hard drives as VDI*.


### Add a Shared Folder
Create a folder called *SharedFolder* on the host system and change the shared folder path under *Settings -> Shared Folders* to the new folder. In this new folder, create a folder called *databridge*.


## Alpine Linux
The scripts used in the following can be found [here](https://oc.iese.de/index.php/s/9JyJAuOlhh9vMUu?path=%2Fdevelopment%2FComponentSpecificVM%2FScripts).


### Create a Component Folder on the Virtual Machine
Execute:

    mkdir /home/basyx_databridge


### Create a DataBridge Configuration Files Folder on the Virtual Machine
Execute:

    mkdir /usr/share/config


### Place the Setup and Startup Scripts on the Virtual Machine
Place *basyx_databridge_setup.sh* and *basyx_databridge_startup.sh* in the shared folder on the host system and execute:

    mv /mnt/shared/basyx_databridge_setup.sh /home/basyx_databridge
    mv /mnt/shared/basyx_databridge_startup.sh /home/basyx_databridge


### Activate Automatic Execution of the Setup and Startup Scripts
Add the following lines to *crontab -e* to the already existing line from the base image setup:

    @reboot <base image command> && /bin/sh /home/basyx_databridge/basyx_databridge_setup.sh ; /bin/sh /home/basyx_databridge/basyx_databridge_startup.sh &> /dev/tty1


### Place the Executable on the Virtual Machine
Place the *.jar* file in the shared folder on the host system and execute:

    mv /mnt/shared/databridge.component-1.0.0-SNAPSHOT-jar-with-dependencies.jar /home/basyx_databridge


### Export the Virtual Machine
Export the machine as an *ova* file (*File -> Export Appliance*) with the following properties:
- Format: Open Virtualization Format 1.0
- MAC Address Policy: Include only NAT network adapter MAC addresses.
- Appliance Settings: Tick only the network adapter checkbox.
