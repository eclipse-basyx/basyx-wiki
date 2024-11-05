# All Components
This tutorial explains how the virtual machine containing all of [these](../../../basyx_components/v2/index.md) components is created based on the base image described [here](./alpine_virtualmachine_setup_dev_base_image.md).

## Virtual Box
### Import the Base Image
Import the machine (*File -> Import Appliance*) with the following settings: 
- Tick only the network adapter checkbox
- MAC Address Policy: Include only NAT network adapter MAC addresses


### Create a Shared Folder
Create a shared folder called *SharedFolder* on the host system that has the following subfolders:
- aasdiscoveryservice
- aasenvironment
- aasregistry_service_release_log_mem
- aasrepository
- conceptdescriptionrepository
- submodelregistry_service_release_log_mem
- submodelrepository

Add this folder as a shared folder under *Settings -> Shared Folders*.


### Enable Port Forwarding
Create for every component a new entry in the port forwarding list (*Settings -> Network -> Adapter 1 -> Advanced -> Port Forwarding*) with the following properties:
- Host IP: 127.0.0.1
- Host Port: \<port>
- Guest IP: 10.0.2.15
- Guest Port: \<port>

For the registry components, the port number can be seen in the respective startup script. For the other components, the port number is set in the respective *application.properties* file.


## Alpine Linux
The scripts used in the following can be found [here](https://oc.iese.de/index.php/s/9JyJAuOlhh9vMUu?path=%2Fdevelopment%2FAllComponentsInOneVM%2FScripts).


### Place the General Shell Scripts on the Virtual Machine
Place *basyx_components_setup.sh* and *basyx_components_startup.sh* in the shared folder on the host system and execute:

    mv /mnt/shared/basyx_components_setup.sh /home/basyx_components_setup.sh
    mv /mnt/shared/basyx_components_startup.sh /home/basyx_components_startup.sh 


### Activate Automatic Execution of the General Scripts
Add the following lines to *crontab -e* to the already existing line from the base image setup:

    @reboot <base image command> && /bin/sh /home/basyx_components_setup.sh ; /bin/sh /home/basyx_components_startup.sh


### Create for Each Component a Folder on the Virtual Machine
Execute:

    mkdir /home/basyx_aasdiscoveryservice
    mkdir /home/basyx_aasenvironment
    mkdir /home/basyx_aasregistry_service_release_log_mem
    mkdir /home/basyx_aasrepository
    mkdir /home/basyx_conceptdescriptionrepository
    mkdir /home/basyx_submodelregistry_service_release_log_mem
    mkdir /home/basyx_submodelrepository


### Place the Component Specific Shell Scripts on the Virtual Machine
Place *\<component>_startup.sh* for each component in the shared folder on the host system and execute:

    mv /mnt/shared/basyx_aasdiscoveryservice_startup.sh /home/basyx_aasdiscoveryservice
    mv /mnt/shared/basyx_aasenvironment_startup.sh /home/basyx_aasenvironment
    mv /mnt/shared/basyx_aasregistry_service_release_log_mem_startup.sh /home/basyx_aasregistry_service_release_log_mem
    mv /mnt/shared/basyx_aasrepository_startup.sh /home/basyx_aasrepository
    mv /mnt/shared/basyx_conceptdescriptionrepository_startup.sh /home/basyx_conceptdescriptionrepository
    mv /mnt/shared/basyx_submodelregistry_service_release_log_mem_startup.sh /home/basyx_submodelregistry_service_release_log_mem
    mv /mnt/shared/basyx_submodelrepository_startup.sh /home/basyx_submodelrepository


### Place the Executables on the Virtual Machine
Place the *.jar* file of each component in the shared folder on the host system and execute:

    mv /mnt/shared/basyx.aasdiscoveryservice.component-2.0.0-SNAPSHOT-exec.jar /home/basyx_aasdiscoveryservice
    mv /mnt/shared/basyx.aasenvironment.component-2.0.0-SNAPSHOT-exec /home/basyx_aasenvironment
    mv /mnt/shared/basyx.aasregistry-service-release-log-mem-2.0.0-SNAPSHOT-exec /home/basyx_aasregistry_service_release_log_mem
    mv /mnt/shared/basyx.aasrepository.component-2.0.0-SNAPSHOT-exec /home/basyx_aasrepository
    mv /mnt/shared/basyx.conceptdescriptionrepository.component-2.0.0-SNAPSHOT-exec /home/basyx_conceptdescriptionrepository
    mv /mnt/shared/basyx.submodelregistry-service-release-log-mem-2.0.0-SNAPSHOT-exec /home/basyx_submodelregistry_service_release_log_mem
    mv /mnt/shared/basyx.submodelrepository.component-2.0.0-SNAPSHOT-exec /home/basyx_submodelrepository


### Place the Scripts for Printing Logs and Errors on the Virtual Machine (optional)
Place *show_errors.sh* and *show_logs.sh* in the shared folder on the host and execute:

    mv /mnt/shared/show_errors.sh /home/show_errors.sh
    mv /mnt/shared/show_logs.sh /home/show_logs.sh


### Export the Virtual Machine
Export the machine as an ova file (*File -> Export Appliance*) with the following properties:
- Format: Open Virtualization Format 1.0
- MAC Address Policy: Include only NAT network adapter MAC addresses
- Appliance Settings: Tick only the network adapter checkbox
