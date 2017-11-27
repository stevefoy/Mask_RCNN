'''
Created on 13 Nov 2017

@author: stephen
'''

import json
from pprint import pprint
from Cython.Shadow import NULL


#    JSON                    Python
#    ==================================
#    object                  dict
#    array                   list
#    string                  unicode
#    number (int)            int, long
#    number (real)           float
#    true                    True
#    false                   False
#    null                    None

def xstr(s):
    if s is None:
        return 'None'
    
    #ans=str(s).encode("ascii","replace")
    
    s.replace("u\'","")
    
    return s

class Segmentation_Polygon:
       
    def __init__(self):
        s = []
        self.number_points = 0
        self.coordinates_x = []
        self.coordinates_y = []
        self.number_points =0

    def addpoly(self, coord_list=[]):
        if len(coord_list) // 2 < 3:
            raise Exception("Side count must be 3 or more.")
        s = []
        self.number_points = 0
        self.coordinates_x = coord_list[::2]
        self.coordinates_y = coord_list[1::2]
        self.s = s.append([self.coordinate_x, self.coordinate_y])
        self.number_points += len(coord_list // 2)
        
class AnswerSummary:
    def __init__(self, ans=True):
        self.no=ans
     
    def loadJSON(self,s=None):
        if s != None:
            self.no=s['answer_summary']
        
    def json_string(self):
        #for key in self.no:
        #JsonStr+=str("\"answer_summary\":{"+str("\"")+str(key)+str("\"")+str(": ")+str(self.no[key])+"},")
        JsonStr=""
        JsonStr+=str("\"answer_summary\": "+json.dumps(self.no)+", ")                
        return JsonStr
    
class AnnotationSegment: 
    def __init__(self,s=None):
        if s != None:        
            self.z_order=None if 'z_order' not in s else s['z_order']
            self.segmentation = None if 'segmentation' not in s else s['segmentation']
            self.tags=None if 'tags' not in s else s['tags']
            self.image_id=None if 'image_id' not in s else s['image_id']
            self.id=None if 'id' not in s else s['id']
            self.confidence=None if 'confidence' not in s else s['confidence']
        else:         
            self.z_order=0
            self.segmentation = []
            self.tags=[]
            self.confidence=[]
            self.image_id="XX"
            #example format EE5B8F2A-0CF6-E2A7-77F5-CC3B5B04934A 
            self.id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
            self.confidence=0
            
    def addPoint(self, x, y):
        self.segmentation.append([x,y])
             
    def addOpencvContour(self, contour):
        for pt in contour:
            self.segmentation.append([float(pt[0][0]),float(pt[0][1])])
    
    def addConfidence(self, confidence):    
            self.confidence=float(confidence)
        
    def add_tag(self, tag):
        self.tags=tag     
            
    def json_string(self):
        JsonStr="{"
        JsonStr+=str("\"z_order\": "+json.dumps(self.z_order)+", ")
        JsonStr+=str("\"segmentation\":"+json.dumps(self.segmentation)+",")
        JsonStr+=str("\"tags\":"+json.dumps(self.tags)+", ")
        JsonStr+=str("\"image_id\": " +json.dumps(self.image_id)+", ")
        JsonStr+=str("\"id\": " +json.dumps(self.id)+", ")
        JsonStr+=str("\"confidence\": " +json.dumps(self.confidence))
        JsonStr+=str("} ")
        return JsonStr
    
class ImageAnnotation:
    
    def __init__(self):
        self.job_id=0
        self.job_batch_id=0
        self.reference_id=0
        self.answer_summary=AnswerSummary() 
        self.status= ["status: finished"]
        self.annotation_annotator_type=0
        self.finished_at=0
        self.annotation_image_url=None
        self.annotation_tags=[]
        self.more_objects_Best_Response=None
        self.annotation_preview_url=None
        self.annotation =[]
        self.more_objects_media_url=None
        
            
    def loadJSON(self, s):
        
        self.job_id=None if 'job_id' not in s else s['job_id']
        self.job_batch_id=None if 'job_batch_id' not in s else s['job_batch_id']
        self.reference_id=None if 'reference_id' not in s else s['reference_id']
        if 'answer_summary' in s:
            self.answer_summary=AnswerSummary(s['answer_summary'])            
        self.status=None if 'status' not in s else s['status']
        self.annotation_annotator_type=None if 'annotation-annotator_type' not in s else s['annotation-annotator_type']
        self.finished_at=None if 'finished_at' not in s else s['finished_at']
        self.annotation_image_url=None if 'annotation-image-url' not in s else s['annotation-image-url']
        #class annotation tags
        self.annotation_tags=None if 'annotation-tags' not in s else s['annotation-tags']   
        self.more_objects_Best_Response=None if 'more-objects Best Response' not in s else s['more-objects Best Response'] 
        self.annotation_preview_url=None if 'annotation-preview-url' not in s else s['annotation-preview-url'] 
        
        #Complex Array of annotaiton objects
        if 'annotation' in s:
            for obj in s['annotation']:
                self.annotation.append(AnnotationSegment(obj))
          
        self.more_objects_media_url=None if 'more-objects media url' not in s else s['more-objects media url'] 
    
    #append annotaiton objet     
    def annoation_append(self, obj):
        self.annotation.append(obj)
        
    def annoation_clear(self, obj):
        del self.annotation[:]
        
    
    
                
    def json_string(self):
        JsonStr=""
        JsonStr+=str(" {")
        JsonStr+=str("\"job_id\": "+json.dumps(self.job_id)+",")
        JsonStr+=str("\"job_batch_id\": "+json.dumps(self.job_batch_id)+",")
        JsonStr+=str("\"reference_id\": "+json.dumps(self.reference_id)+",")
        #error "answer_summary": {"no": 1}     
        JsonStr+=self.answer_summary.json_string()
        JsonStr+=str("\"status\": "+json.dumps(self.status)+",")
        JsonStr+=str("\"annotation-annotator_type\": "+json.dumps(self.annotation_annotator_type)+", ")
        #JsonStr+=str("\"annotation-annotator_type\": "+str("null" if self.annotation_annotator_type==NULL else self.annotation_annotator_type)+", ")
        JsonStr+=str("\"finished_at\": "+json.dumps(self.finished_at)+",")
        JsonStr+=str("\"annotation-image-url\":  "+json.dumps(self.annotation_image_url)+",")
        #class annotation tags
        JsonStr+=str("\"annotation-tags\": "+json.dumps(self.annotation_tags)+",")
        JsonStr+=str("\"more-objects Best Response\": "+json.dumps(self.more_objects_Best_Response)+", ")
        JsonStr+=str("\"annotation-preview-url\": "+json.dumps(self.annotation_preview_url)+",")
        JsonStr+=str("\"annotation\": [")       
        for i, obj in enumerate(self.annotation):
            
            if i!=len(self.annotation)-1:
                JsonStr+=obj.json_string()
                JsonStr+=str(",")
                
            else:
                JsonStr+=obj.json_string()
                
        
           
        JsonStr+=str("]")
        JsonStr+=str(",") 
        JsonStr+=str("\"more-objects media url\": "+json.dumps(self.more_objects_media_url)+"")
        JsonStr+=str("}")
        return JsonStr
                        
class ImageDBAnnotation:
     
    def __init__(self, fileID=None):
        self.ImageID=fileID
        self.imageAnnotation=ImageAnnotation()
        
    def load(self, datafile):
        with open(datafile,'r') as f:
            data = json.load(f)
            if len(data.keys()) == 1:
                #ToDo class for ID 
                self.ImageID=data.keys()[0]
                self.imageAnnotation=ImageAnnotation()
                self.imageAnnotation.loadJSON(data[data.keys()[0]])

    def json_print(self):
        JsonStr=""
        JsonStr+=str("{\""+self.ImageID+"\":")
        JsonStr+=self.imageAnnotation.json_string()
        JsonStr+=str("}")
        print(JsonStr)
 
    def write_file(self, filename):
        file = open(filename,"w") 
        #format of json                             
        JsonStr=""
        JsonStr+=str("{\""+self.ImageID+"\":")
        JsonStr+=self.imageAnnotation.json_string()
        JsonStr+=str("}")
        file.write(JsonStr) 
        file.close() 
        
 
 
#======================================================================== 
         
if __name__ == "__main__":
    fileloc="/home/stephen/Videos/mightyAI/jsons/1003.145632_FV_450.json"
    
    
    imageID = ImageDBAnnotation()
    
    annot = AnnotationSegment()
    imageID.load(fileloc)
    imageID.json_print()
    result="/home/stephen/Videos/atest.txt"
    imageID.write_file(result)
    
    imageID2 = ImageDBAnnotation()
    imageID2.load(result)
    imageID.json_print()
    
    
    
    #load file
    
    
    
    