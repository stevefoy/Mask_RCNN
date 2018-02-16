import sys
import os
import yaml

import argparse

parser = argparse.ArgumentParser(description='Install ImageSelection environment')
parser.add_argument('--name', dest='name', action='store', default="imageselection", required=False, help="Name of the conda environment")
parser.add_argument('--envpath', dest='envpath', action='store', required=True,  help="Path to conda environments. Usually: /home/user1/miniconda2/envs/")

args = parser.parse_args()

env_name = args.name
env_path = args.envpath

out_yml_name = env_name+".yml"

first_line = "name: " + env_name + "\n"
last_line = "prefix: " + env_path + env_name + "\n"

with open("env.yml", 'r') as stream:
    data_loaded = stream.read()
    full_yml = first_line + data_loaded + last_line
    out_file = open(out_yml_name, "w")
    out_file.write(full_yml)
    out_file.close()

os.system("source deactivate")    
os.system("conda env create -f " + out_yml_name)
os.system("source activate "+env_name)
os.system("git clone https://github.com/cocodataset/cocoapi.git")
os.system("cd cocoapi/PythonAPI/")
os.system("make")
os.system("python setup.py install")
os.system("cd ..")
os.system("cd ..")
os.system("rm -rf cocoapi/")
os.system("wget https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5")





    






