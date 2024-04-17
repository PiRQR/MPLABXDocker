import xmltodict

project_path = 'CAN_Board.X/nbproject/configurations.xml'
project_path = input("enter path to your MPLABX project:")

with open(project_path) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())

mplab_version = "6.00"
mplab_version = input("enter your mplabx version:")
target_device = data_dict['configurationDescriptor']['confs']['conf']['toolsSet']['targetDevice']
language_toolchain = data_dict['configurationDescriptor']['confs']['conf']['toolsSet']['languageToolchain'].lower()
language_toolchain_version = data_dict['configurationDescriptor']['confs']['conf']['toolsSet']['languageToolchainVersion']

pack_name = data_dict['configurationDescriptor']['confs']['conf']['packs']['pack']['@name']
pack_version = data_dict['configurationDescriptor']['confs']['conf']['packs']['pack']['@version']

print(f"--Project config loaded--\n- target device: {target_device}\n- toolchain: {language_toolchain} {language_toolchain_version}\n- pack: {pack_name} {pack_version}")
    
df_text = f'''
# This file was generated by python CI/CD Wizard

FROM debian:buster-slim

ENV DEBIAN_FRONTEND noninteractive

USER root
RUN dpkg --add-architecture i386 \
 && apt-get update -yq \
 && apt-get install -yq --no-install-recommends \
    ca-certificates \
    curl \
    make \
    unzip \
    procps \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# Download and install MPLAB X IDE version 6.00
ENV MPLABX_VERSION {mplab_version}

RUN curl -fSL -A "Mozilla/4.0" -o /tmp/mplabx-installer.tar \
         "https://ww1.microchip.com/downloads/en/DeviceDoc/MPLABX-v{mplab_version}-linux-installer.tar" \
 && tar xf /tmp/mplabx-installer.tar -C /tmp/ && rm /tmp/mplabx-installer.tar  \
 && USER=root ./tmp/MPLABX-v{mplab_version}-linux-installer.sh --nox11 \
    -- --unattendedmodeui none --mode unattended \
 && rm ./tmp/MPLABX-v{mplab_version}-linux-installer.sh \
 && rm -rf /opt/microchip/mplabx/v{mplab_version}/packs/Microchip/*_DFP \
 && rm -rf /opt/microchip/mplabx/v{mplab_version}/mplab_platform/browser-lib
ENV PATH /opt/microchip/mplabx/v{mplab_version}/mplab_platform/bin:$PATH
ENV PATH /opt/microchip/mplabx/v{mplab_version}/mplab_platform/mplab_ipe:$PATH
ENV XCLM_PATH /opt/microchip/mplabx/v{mplab_version}/mplab_platform/bin/xclm

ENV TOOLCHAIN {language_toolchain}
ENV TOOLCHAIN_VERSION {language_toolchain_version}

# Download and install toolchain
RUN curl -fSL -A "Mozilla/4.0" -o /tmp/{language_toolchain}.run \
    "https://ww1.microchip.com/downloads/en/DeviceDoc/{language_toolchain}-v{language_toolchain_version}-full-install-linux64-installer.run" \
 && chmod a+x /tmp/{language_toolchain}.run \
 && /tmp/{language_toolchain}.run --mode unattended --unattendedmodeui none \
    --netservername localhost --LicenseType NetworkMode \
 && rm /tmp/{language_toolchain}.run
ENV PATH /opt/microchip/{language_toolchain}/v{language_toolchain_version}/bin:$PATH

# DFPs needed for default configuration

# Download and install Microchip.dsPIC33E-GM-GP-MC-GU-MU_DFP.1.3.85
RUN curl -fSL -A "Mozilla/4.0" -o /tmp/tmp-pack.atpack \
         "https://packs.download.microchip.com/Microchip.dsPIC33E-GM-GP-MC-GU-MU_DFP.1.3.85.atpack" \
 && mkdir -p /opt/microchip/mplabx/v{mplab_version}/packs/dsPIC33E-GM-GP-MC-GU-MU_DFP/1.3.85 \
 && unzip -o /tmp/tmp-pack.atpack -d /opt/microchip/mplabx/v{mplab_version}/packs/dsPIC33E-GM-GP-MC-GU-MU_DFP/1.3.85 \
 && rm /tmp/tmp-pack.atpack
ENV BUILD_CONFIGURATION default
'''

with open('Dockerfile.generated', 'w') as df:
    df.write(df_text)
