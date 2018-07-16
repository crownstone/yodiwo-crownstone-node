from CrownstoneYodiwo import CrownstoneNode

from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--configFile', default='nodeConfig.json', help='configuration file')
args = parser.parse_args()
configFile = args.configFile

cFile = Path(configFile)
if cFile.is_file():
        node = CrownstoneNode()
        node.loadConfig(configFile)
        node.start()
else:
        print("Error: File " + configFile + " does not exist")
~                                                                                                                       
~                                                                     
