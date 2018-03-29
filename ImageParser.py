
import os
import sys
import random
import math
import numpy as np
import scipy.misc
import matplotlib
import matplotlib.pyplot as plt
import argparse



import coco
import utils
import model as modellib
import visualize
from tensorflow.python.ops.metrics_impl import sensitivity_at_specificity


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))

class readable_file(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_file=values
        if not os.path.isfile(prospective_file):
            raise argparse.ArgumentTypeError("readable_file:{0} is not a valid path".format(prospective_file))
        if os.access(prospective_file, os.R_OK):
            setattr(namespace,self.dest,prospective_file)
        else:
            raise argparse.ArgumentTypeError("readable_file:{0} is not a readable dir".format(prospective_file))

    
class defaultDirectory(object):
    
    def __init__(self,inputDir, outputDir):
        self.inputDir= inputDir
        self.outputDir= outputDir
        
        
    def get_outputDir(self):
        return self.outputDir
    
    def get_inputDir(self):
        return self.inputDir


def main(): 
    
    parser = argparse.ArgumentParser(description='tool for processing a folder of image with MaskRCNN')
    parser.add_argument('-i', '--inputDir', action=readable_dir, help='input directory to process')
    parser.add_argument('-o', '--outputDir', action=readable_dir, help='output directory to process')
    parser.add_argument('-l', '--inputFileList',  action=readable_file, help='input file with a list of images')
    
    args = parser.parse_args()
    dirs= defaultDirectory(args.inputDir, args.outputDir)
    IMAGETest_DIR =dirs.get_inputDir()
    IMAGETestResult_DIR=dirs.get_outputDir()
    
    fileOfInputImages=""
    if args.inputFileList != None:
        fileOfInputImages=args.inputFileList
    
    # Root directory of the project
    ROOT_DIR = os.getcwd()  

    # Directory to save logs and trained model
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")
    
    # Path to trained weights file
    # Download this file and place in the root of your 
    # project (See README file for details)
    COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
    
    # Directory of images to run detection on
    IMAGE_DIR = os.path.join(ROOT_DIR, "imagetest")
    
    
    
    
    
    
    
    
    
    
    
    
    config = InferenceConfig()
    config.print()
    # Create model object in inference mode.
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
    
    # Load weights trained on MS-COCO
    model.load_weights(COCO_MODEL_PATH, by_name=True)
    
    # COCO Class names
    # Index of the class in the list is its ID. For example, to get ID of
    # class, use: class_names.index('teddy bear')
    class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
                   'bus', 'train', 'truck', 'boat', 'traffic light',
                   'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
                   'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
                   'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                   'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                   'kite', 'baseball bat', 'baseball glove', 'skateboard',
                   'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                   'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                   'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                   'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                   'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                   'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
                   'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                   'teddy bear', 'hair drier', 'toothbrush']
    
    
    
    
    if fileOfInputImages!="":
        with open(fileOfInputImages) as file:
            for index, line in enumerate(file):
                ImagePath = line.strip() 
                
                baseDir, file_name  = os.path.split(ImagePath)
                
                #debug test 10
                #if index == 10:  
                #    break
                
                if os.path.isfile(ImagePath):
                    #print(ImagePath)
                    image = scipy.misc.imread(ImagePath)
                    
                    # Run detection
                    results = model.detect([image], verbose=1)
                    # Visualize results
                    r = results[0]
                    print("Counter",index )
                    
                    saveImageDir=os.path.join(IMAGETestResult_DIR, file_name)
                    
                    saveJSONDir=os.path.join(IMAGETestResult_DIR,file_name.replace('.png','.json'))
                    visualize.save_instances(saveImageDir ,saveJSONDir ,file_name, image, r['rois'], r['masks'], r['class_ids'],class_names, r['scores'])
                    
                else:
                    print("Error finding", ImagePath)
    
    else:
        print("Error")


if __name__ == '__main__':
    main()
