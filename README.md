# MPLABX Docker image

Docker image based on python image (debian bookworm) with MPLABX and XC16 environement

## prerequisite

Because Microchip website has now security for downloads, please make sure to download and put requirements in root folder:
Download xc16 for linux : http://www.microchip.com/mplabxc16linux
Donwload MPLAB linux installer : https://www.microchip.com/mplabx-ide-linux-installer

## usage

- build image : `docker build . -t mplabx-6.20-xc16`
- run container : docker run -d mplabx-6.20-xc16 --name mplabx
