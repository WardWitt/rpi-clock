Python3 Clock
==============

## Use Raspberry Pi Imager to install Raspian.
Raspberry Pi OS (other) > Raspberry Pi OS Lite (Legacy, 64-bit)
Debian Bullseye, as of this writing Bookworm is causing problems with pygame.
Attach a keyboard before first boot, select “Other” when presented with the keyboard configuration and choose the US layout. Enter user and password (admin is suggested).

## Fixed IP address
    sudo nano /etc/dhcpcd.conf
Edit and uncomment the “Example static IP configuration” to suit your environment.

## Upgrade to latest OS
    sudo apt-get update
    sudo apt-get upgrade

## Enable SSH & I2C
    sudo rasp-config > 3 > I2 Enable SSH & I5 Enable I2C

## Set timezone
    sudo raspi-config > 5 > L2 Timezone

## Install pygame
    sudo apt-get install python3-pygame

## Install chrony
    sudo apt-get install chrony

## Copy the app to the RaspberryPi
From your PC
    scp ~/Desktop/rpi-clock.zip admin@172.18.18.237:~ 
    unzip rpi-clock.zip

## Configure Axia Livewire
Edit /home/admin/rpi-clock/RPiclock.ini to suit your environment.

## Configure systemd
    sudo cp /home/admin/rpi-clock/RPiclock.service /lib/systemd/system
    sudo systemctl enable RPiclock.service
    sudo systemctl start RPiclock.service
    
