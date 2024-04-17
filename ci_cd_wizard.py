import xmltodict
import logging
from string import Template
from xml.parsers.expat import ExpatError

REQ_XML_VERSION = 65

class CICDWizard:
    
    def __init__(self, project_path: str, mplab_version: str):
        self.logger = logging.getLogger(__name__)    
        logging.basicConfig(level=logging.INFO)        
        self.logger.info(f"XML config version min requirement version: {REQ_XML_VERSION}")
        self.project_path = project_path + '/nbproject/configurations.xml'
        self.mplab_version = mplab_version
        try:
            with open(self.project_path) as xml_file:
                data_dict = xmltodict.parse(xml_file.read())
        except FileNotFoundError as efnf:
            self.logger.error(f"Config file {self.project_path} not found: {efnf}")
            exit()
        except ExpatError as eee:
            self.logger.error(f"Error with file {self.project_path} check your file: {eee}")
            exit()

        self.xml_version = data_dict["configurationDescriptor"]['@version']
        if int(self.xml_version) < REQ_XML_VERSION:
            self.logger.error(f"XML version {self.xml_version} is too old, must be newer than version {REQ_XML_VERSION}")
            exit()
        
        # load Dockerfile template to fill
        try:
            with open("template.txt") as template_file:
                self.template = Template(template_file.read())
        except FileNotFoundError as efnf:
            self.logger.error(f"Template file {self.project_path} not found: {efnf}")
            exit()
        
        try:
            # read mplab project configuration
            self.target_device = data_dict['configurationDescriptor']['confs']['conf']['toolsSet']['targetDevice']
            self.language_toolchain = data_dict['configurationDescriptor']['confs']['conf']['toolsSet']['languageToolchain'].lower()
            self.language_toolchain_version = data_dict['configurationDescriptor']['confs']['conf']['toolsSet']['languageToolchainVersion']
            self.pack_name = data_dict['configurationDescriptor']['confs']['conf']['packs']['pack']['@name']
            self.pack_version = data_dict['configurationDescriptor']['confs']['conf']['packs']['pack']['@version']
            self.logger.info(f"--- Project config loaded ---\n- target device: {self.target_device}\n- toolchain: {self.language_toolchain} {self.language_toolchain_version}\n- pack: {self.pack_name} {self.pack_version}")
        except KeyError as eke:
            self.logger.error(f"Error with file {self.project_path} key {eke} not found, check config version")
            exit()
        
    
    def generate_dockerfile(self, df_name):
        try:
            t = self.template.substitute(target_device=self.target_device,
                                        language_toolchain=self.language_toolchain,
                                        language_toolchain_version=self.language_toolchain_version,
                                        pack_name=self.pack_name,
                                        pack_version=self.pack_version,
                                        mplab_version=self.mplab_version)
        except KeyError as eke:
            self.logger.error(f"Error with a key in template file: {eke} not found")
            exit()
        try:
            with open(df_name, 'w') as df:
                df.write(t)
        except FileNotFoundError as efnf:
            self.logger.error(f"Template file {df_name} not found: {efnf}")
            exit()
        self.logger.info(f"Dockerfile generated with name : {df_name}")
    


import logging
from pyCLN import CLNModbusLoader
from pyCLN.__version__ import version_str

def main():
    import argparse
    parser = argparse.ArgumentParser(
                    description = 'CICD Wizard for generating dockerfile from mplab project')    
    parser.add_argument('-d', '--debug', help='enable debug prints', action='store_true')
    parser.add_argument('-p', '--project', help='Path of MPLAB project', default='')
    parser.add_argument('-mv', '--mplab_version', help='Wanted version of mplabx for your image', default='6.00')
    args = parser.parse_args()
    
    if args.project=='':
        project_path = input("enter path to your MPLABX project:")
    else:
        project_path = args.project
    wizard = CICDWizard(project_path=project_path, mplab_version=args.mplab_version)
    wizard.generate_dockerfile('Dockerfile.generated')
    
if __name__ == '__main__':
    main()