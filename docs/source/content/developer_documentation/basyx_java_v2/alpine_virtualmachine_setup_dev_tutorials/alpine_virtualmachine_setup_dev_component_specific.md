# Single Component
This tutorial explains how a virtual machine for one of [these](../../../basyx_components/v2/index.md) components is created based on the base image described [here](./alpine_virtualmachine_setup_dev_base_image.md).


## VirtualBox
### Import the base image
Import the virtual machine image under *File -> Import Appliance*. Do **not** tick *Import hard drives as VDI*.


### Create a Component Specific Folder in the Shared Folder
Create a folder called *SharedFolder* on the host system and change the shared folder path under *Settings -> Shared Folders* to the new folder. In this new folder, create a component specific folder with one of the following names depending on the desired component:
- aasdiscoveryservice
- aasenvironment
- aasregistry_service_release_log_mem
- aasrepository
- conceptdescriptionrepository
- submodelregistry_service_release_log_mem
- submodelrepository


### Enable Port Forwarding (for VirtualBox)
This step is only required when *NAT* or *NAT Network* is selected as networking mode under *Settings -> Network -> Attached to*. *NAT* does not facilitate inter-communication between virtual machines. If inter-communication is required, *Bridged Adapter* or *NAT Network* can be used instead. <br>
Create a new entry in the port forwarding list (*Settings -> Network -> Adapter 1 -> Advanced -> Port Forwarding*) with the following properties:
- Host IP: 127.0.0.1
- Host Port: \<port>
- Guest IP: 10.0.2.15
- Guest Port: \<port>


## Alpine Linux
The scripts used in the following can be found [here](https://oc.iese.de/index.php/s/9JyJAuOlhh9vMUu?path=%2Fdevelopment%2FComponentSpecificVM%2FScripts).


### Create a Component Folder on the Virtual Machine
Execute:

    mkdir /home/basyx_<component>


### Place the Setup and Startup Scripts on the Virtual Machine
Place *basyx_\<component>\_setup.sh* and *basyx_\<component>_startup.sh* in the shared folder on the host system and execute:

    mv /mnt/shared/basyx_<component>_setup.sh /home/basyx_<component>
    mv /mnt/shared/basyx_<component>_startup.sh /home/basyx_<component>

Registry components have only a startup script.


### Activate Automatic Execution of the Setup and Startup Scripts
Add the following lines to *crontab -e* to the already existing line from the base image setup:

    @reboot <base image command> && /bin/sh /home/basyx_<component>/basyx_<component>_setup.sh ; /bin/sh /home/basyx_<component>/basyx_<component>_startup.sh > /dev/tty1

Registry components have only a startup script.


### Place the Executable on the Virtual Machine
Place the *.jar* file of the respective component in the shared folder on the host system and execute:

    mv /mnt/shared/<component>.jar /home/basyx_<component>


### Export the Virtual Machine
Export the machine as an *ova* file (*File -> Export Appliance*) with the following properties:
- Format: Open Virtualization Format 1.0
- MAC Address Policy: Include only NAT network adapter MAC addresses.
- Appliance Settings: Tick only the network adapter checkbox.
