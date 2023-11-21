RPiclock
==============

RPiclock is a Raspberry Pi Radio Studio Clock written in python using pygame with studio indicators for microphones, telephones etc... on widescreen (16:9) monitors, displays and TVs.

This was designed specifically for the Raspberry Pi. This version includes configurable indicators for microphones, telephones etc... for use in a radio studio.

Either Livewire GPI or GPO closures trigger the 5 available indicators

## Development Status

***

Code modified extensively by Tim Wright to allow for Livewire GPIO , JSON file config, and LOGO image.
RPiclock is currently stable and ready for use, but is  work in progress with many additions coming

## Installation for Raspberry Pi

***

It's recommended to use the latest build of Raspbian for this project and a 4GB or more SD Card.
It runs very well on a Pi3B, but should also run on a Pi Zero, if networking can be provided for the NTP input on port 161 and the LW input on port 93

Note 1: The Pi will have the most accuracy in time keeping when it has a constant connection to the internet.

Note 2: On older HDMI displays and composite video you may need to force 16:9 mode. This is done by adding this to the config.txt in the boot partition:

    sdtv_aspect=3
    
See [http://elinux.org/RPiconfig](http://elinux.org/RPiconfig) for more info.

Once you have copied the Raspbian Image to your SD Card and booted your Pi for the first time, a prompt will come up called:
    
    Raspberry Pi Software Configuration Tool (raspi-config)

You need to select:

    1 Expand Filesystem
Then

    <Ok>

Next we need to:

    3 Enable Boot to Desktop/Scratch

and select:

    Console Text console

**THIS PART IS IMPORTANT TO GET THE RIGHT TIMEZOME**

Select:

    4 Internationalisation Options

Then:

    I2 Change Time Zone

You will have a list of continents/geographical areas, select your one. Then select a region or city in your time zone.

When you are done select:

    <Finish>
    
Then Reboot.

Once you have rebooted and logged in lets make sure everything is up to date:

    sudo apt-get update
    
Then

    sudo apt-get upgrade

Copy the RPiClock files to a folder in your home directory and edit them to fit your specifics
    
## Running it

***

All we have to do is:

run autostart.sh in the startup script for the X session
    
To quit just press the'Q' key.

## Custom configuration

***

To set colors of the indicators, change the numerical values in ind1color - ind4color.

The values are standard RGB

The First value is RED, the second is GREEN and the third is BLUE. The max value is 255 and the min is 0

Example:

    ind1color = (255, 0, 0)
    
would make the first indicator red in this example.

To change the text in the indicators, change the word in the "quotes" in ind1txt - ind4txt

Example:

    ind1txt = indfont.render("HELLO",True,bgcolor)

This would change the text to HELLO on the first indicator in this example.

