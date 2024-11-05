# Alpine Linux Virtual Machine Setup -  Base Image
Based on this base image, the virtual machine images for [these](/docs/source/content/user_documentation/basyx_components/v2/index.md) components can be created as described [here](./alpine_virtualmachine_setup_dev_component_specific.md) for the component specific images and [here](./alpine_virtualmachine_setup_dev_all_in_one.md) for an image containing all components.

## VirtualBox
### Creation of the VM in VirtualBox
Download the .iso file from https://alpinelinux.org/downloads/. Choose *x86_64* as architecture and *virtual* as image type.
Configuration steps in VirtualBox:
1. Create a new machine.
2. Choose the downloaded .iso file.
3. Choose as type *Linux* and as version *Other Linux (64-bit)*.
4. Choose 1024 MB of RAM and one core.
5. Choose *Do not add a hard disk*.
6. Finish the setup.
7. Create a virtual hard disk of type .vmdk of size 4 GB and attach it to the machine (*Settings -> Storage -> Controller: SATA*). Do **not** pre-allocate the the storage space.
8. Start the machine.


### Create a Shared Folder
Create a shared folder called *SharedFolder* on the host system and add this folder as a shared folder under *Settings -> Shared Folders*.


## Alpine Linux
### Alpine Linux Setup
When the system is started for the first time, different properties have to be set to finish system setup.
This can be done by executing `setup-alpine`.
- keymap: de
- hostname: localhost
- interface: eth0
- ip address: dhcp
- manual network configuration: no
- root password: none
- timezone: Europe/Berlin
- proxy: none
- network time protocol: chrony
- mirror: fastest
- user: no
- ssh server: none
- disks: choose earlier created disk
- disk usage: sys
- erase disk: yes

Then, shutdown the machine and deselect all options from the boot order except for the hard disk (*Settings -> System*). Now, restart the machine.


### Activate Community Repositories
To be able to install the VirtualBox Guest Additions and Eclipse Temurin, the community repositories have to be activated in */etc/apk/repositories*. Therefore, remove the *#* in front of them.


### Install Eclipse Temurin
Execute

    wget -O /etc/apk/keys/adoptium.rsa.pub https://packages.adoptium.net/artifactory/api/security/keypair/public/repositories/apk

    echo 'https://packages.adoptium.net/artifactory/apk/alpine/main' >> /etc/apk/repositories

    apk update && apk upgrade
    apk add temurin-17-jdk

Source: https://adoptium.net/installation/linux/


### Add a Shared Folder (VirtualBox)
Execute:

    mkdir -p /mnt/shared
    apk add virtualbox-guest-additions linux-virt
    modprobe -a vboxsf
    mount -t vboxsf SharedFolder /mnt/shared

Add to *crontab -e*:

    @reboot mount -t vboxsf SharedFolder /mnt/shared


### Add a Shared Folder (VMware player)
Execute:

    mkdir -p /mnt/shared
    apk add open-vm-tools-hgfs
    rc-service open-vm-tools start
    rc-update add open-vm-tools boot

Add to *crontab -e*:

    @reboot modprobe fuse && /usr/bin/vmhgfs-fuse .host:/SharedFolder /mnt/shared -o subtype=vmhgfs-fuse,allow_other


### Deactivate Login Request After Booting
Make the following changes to */etc/inittab*:
- Comment out 
    
        tty1::respawn:/sbin/getty 38400 tty1

- Add

        tty1::respawn:/bin/sh


### Export the Virtual Machine
Export the machine as an ova file (*File -> Export Appliance*) with the following properties:
- Format: Open Virtualization Format 1.0
- MAC Address Policy: Include only NAT network adapter MAC addresses
- Appliance Settings: Tick only the network adapter checkbox
