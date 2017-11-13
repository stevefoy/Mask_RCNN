'''
Created on 13 Nov 2017

@author: stephen
'''


class Annotation(object):
    
    def __init__(self, annotation):
        self.__annotation = annotation
        self.__zOrder = None
        self.__segmentation = []
        self.__tags = []
        self.__imageId = None
        self.__id = None
      
        self.__setFields()
        
    def __setFields(self):
        self.__zOrder = self.__annotation['z_order']
        self.__segmentation = self.__annotation['segmentation']
        self.__tags = self.__annotation['tags']
        assert(len(self.__tags) == 1)
        self.__imageId = self.__annotation['image_id']
        self.__id = self.__annotation['id']
        
    def getZOrder(self):
        return self.__zOrder
    
    def getSegmentation(self):
        return self.__segmentation
    
    def getTags(self):
        return self.__tags
    
    def getImageId(self):
        return self.__imageId
    
    def getId(self):
        return self.__id
    
    def appendSegmentation(self, imageAnnotation):
        self.__segmentation.append(imageAnnotation)
    