# MPLABX Docker image

Wizard to generate Docker image based on python image (debian bookworm) with MPLABX and XC16 environement

## prerequisite (not mandatory)

If your docker container not able to download requirements by itself, please find links below:
- Download xc16 for linux : http://www.microchip.com/mplabxc16linux
- Download MPLAB linux installer : https://www.microchip.com/mplabx-ide-linux-installer

## Template

You can modify Dockerfile template with file template.txt
You can change docker base image with another one (ex: python:slim-bookworm to debian:buster) depending of your needs

## usage
- see help: `python ci_cd_wizard.py -h`
- generate Dockerfile : `python ci_cd_wizard.py -p{path_of_your_project} -mv{MPLABX.version}`
- build image : `docker build -t mplabx-6.20-xc16 -f Dockerfile.generated .`
- run container with not exit: `docker run -dit --name mplabx -d pierre2bia/mplabx-xc16:6.20`
