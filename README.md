# MPLABX Docker image

Docker image based on python image (debian bookworm) with MPLABX and XC16 environement

## prerequisite

Because Microchip website has now security for downloads, please make sure to download and put requirements in root folder:
- Download xc16 for linux : http://www.microchip.com/mplabxc16linux
- Download MPLAB linux installer : https://www.microchip.com/mplabx-ide-linux-installer

## usage

- build image : `docker build . -t mplabx-6.20-xc16`
- run container with not exit: `docker run -dit --name mplabx -d pierre2bia/mplabx-xc16:6.20`
