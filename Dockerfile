FROM python:slim-bookworm
ENV DEBIAN_FRONTEND noninteractive

# Microchip Tools Require i386 Compatability as Dependency

RUN dpkg --add-architecture i386 \
    && apt-get update -yq \
    && apt-get upgrade -yq \
    && apt-get install -yq --no-install-recommends build-essential bzip2 cpio curl python3 unzip wget procps\
    libc6:i386 libx11-6:i386 libxext6:i386 libstdc++6:i386 libexpat1:i386 \
    libxext6 libxrender1 libxtst6 libgtk2.0-0 libxslt1.1 libncurses5-dev libusb-1.0-0-dev

# --- INSTALL XC16 ---
COPY xc16.run /tmp/xc16.run
RUN chmod a+x /tmp/xc16.run
RUN /tmp/xc16.run --mode unattended --unattendedmodeui none --netservername localhost --LicenseType FreeMode --prefix /opt/microchip/xc16
RUN rm /tmp/xc16.run

ENV PATH $PATH:/opt/microchip/xc16/bin

# --- INSTALL MPLABX ---
COPY MPLABX-v6.20-linux-installer.sh /tmp/MPLABX-v6.20-linux-installer.sh
RUN USER=root ./tmp/MPLABX-v6.20-linux-installer.sh --nox11 -- --unattendedmodeui none --mode unattended --installdir /opt/microchip/mplabx
RUN rm /tmp/MPLABX-v6.20-linux-installer.sh
ENV PATH $PATH:/opt/microchip/mplabx/mplab_platform/bin

VOLUME /tmp/.X11-unix

###### Container Developer User Ident
RUN useradd user && mkdir -p /home/user/MPLABXProjects && touch /home/user/MPLABXProjects/.directory && chown user:user /home/user/MPLABXProjects
VOLUME /home/user/MPLABXProjects

# --- TEST XC16 INSTALL BY ASKING VERSION ---
RUN [ -x /opt/microchip/xc16/bin/xc16-gcc ] && xc16-gcc --version
