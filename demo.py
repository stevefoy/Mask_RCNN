
import os
import sys
import random
import math
import numpy as np
import scipy.misc
import matplotlib
import matplotlib.pyplot as plt

import coco
import utils
import model as modellib
import visualize


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


def main(): 
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
    # the teddy bear class, use: class_names.index('teddy bear')
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
    
    
    
    
    
    
    IMAGETest_DIR = "/home/stephen/Videos/France_TestVideo/seq1"
    IMAGETestResult_DIR = "/home/stephen/Videos/France_TestVideo/seq1Result"
    # Load a random image from the images folder
    file_names = next(os.walk(IMAGETest_DIR))[2]
    
    
    
    
    
    for index, file_name in enumerate(file_names) :
        
        print(index)
        if index == 10:  # There's gotta be a better way.
            break
            
        image = scipy.misc.imread(os.path.join(IMAGETest_DIR, file_name))
        # Run detection
        results = model.detect([image], verbose=1)
    
        # Visualize results
        r = results[0]
        visualize.save_instances(os.path.join(IMAGETestResult_DIR, file_name), image, r['rois'], r['masks'], r['class_ids'],
                                class_names, r['scores'])


if __name__ == '__main__':
    main()
