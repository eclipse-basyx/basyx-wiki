# BaSyx Virtual Machine Setup
The virtual machine images for [these](../../basyx_components/v2/index.md) components and for the [databridge](../../../basyx_components/databridge/index.md) component can be found [here](https://oc.iese.de/index.php/s/9JyJAuOlhh9vMUu?path=%2F). In the following, it is explained how the images can be used with Oracle VirtualBox and VMware Workstation Player.

## Oracle VirtualBox
### Import the Virtual Machine
Import the virtual machine image under *File -> Import Appliance*. 

### Change the Shared Folder Location
Create a folder called *SharedFolder* on the host system and change the shared folder path under *Settings -> Shared Folders* to the new folder. Depending on the BaSyx component, create one of the following folders in *SharedFolder*:

- aasdiscoveryservice
- aasenvironment
- aasregistry_service_release_log_mem
- aasrepository
- conceptdescriptionrepository
- submodelregistry_service_release_log_mem
- submodelrepository
- databridge

For the virtual machine containing all components except the databridge, create all of those. Place the *application.properties* files in the respective folders. <br>
Place the databridge configuration files in the respective folder.

### Enable Port Forwarding
This step is only required when *NAT* or *NAT Network* is selected as networking mode under *Settings -> Network -> Attached to*. *NAT* does not facilitate inter-communication between virtual machines. If inter-communication is required, *Bridged Adapter* or *NAT Network* can be used instead. <br>
Create for every component a new entry in the port forwarding list (*Settings -> Network -> Adapter 1 -> Advanced -> Port Forwarding*) with the following properties:
- Host IP: 127.0.0.1
- Host Port: \<port>
- Guest IP: 10.0.2.15
- Guest Port: \<port>

For aasdiscoveryservice, aasenvironment, aasrepository, conceptdescriptionrepository and submodelrepository, the port can be specified in the respective *application.properties*. For aasregistry_service_release_log_mem and submodelregistry_service_release_log_mem, the port can be specified in the virtual machine in */home/basyx_aasregistry_service_release_log_mem/basyx_aasregistry_service_release_log_mem_startup.sh* (Default: 8086) and */home/basyx_submodelregistry_service_release_log_mem/basyx_submodelregistry_service_release_log_mem_startup.sh* (Default: 8087), respectively.

### Make the Virtual Machine Load the Shared Folder
Execute in the virtual machine

    crontab -e

and remove the # in front of the first *reboot* and comment out the subsequent line instead by placing a # in front of it.


## VMware Workstation Player
### Import the Virtual Machine
Import the machine (*Player -> File -> Open*). If the import fails, select *retry*.

### Add a Shared Folder
Create a folder called *SharedFolder* on the host system and add it under *Edit virtual machine settings -> Options -> Shared Folders -> Add*. Tick *always enabled*. Depending on the Basyx component, create one of the following folders in *SharedFolder*:

- aasdiscoveryservice
- aasenvironment
- aasregistry_service_release_log_mem
- aasrepository
- conceptdescriptionrepository
- submodelregistry_service_release_log_mem
- submodelrepository
- databridge

For the virtual machine containing all components except the databridge, create all of those. Place the *application.properties* files in the respective folders. <br>
Place the databridge configuration files in the respective folder.

### Make the Virtual Machine Load the Shared Folder
This step is only necessary if changes have been made to this file before. <br>
Execute in the virtual machine

    crontab -e

and remove the # in front of the second *reboot* and comment out the preceding line instead by placing a # in front of it. 

### IP Address and Port Number
The IP address of the virtual machine can be found out by executing *ifconfig* in the guest system, for instance. <br>
For aasdiscoveryservice, aasenvironment, aasrepository, conceptdescriptionrepository and submodelrepository, the port can be specified in the respective *application.properties*. For aasregistry_service_release_log_mem and submodelregistry_service_release_log_mem, the port can be specified in the virtual machine in */home/basyx_aasregistry_service_release_log_mem/basyx_aasregistry_service_release_log_mem_startup.sh* (Default: 8086) and */home/basyx_submodelregistry_service_release_log_mem/basyx_submodelregistry_service_release_log_mem_startup.sh* (Default: 8087), respectively.
