import os 
import json
import glob
import util.annotation
import numpy as np
import cv2
import math


def pointList2contour(c):
    return np.array(c).reshape((-1,1,2)).astype(np.int32)

def extract_bboxes(ImgAnnotation):
    """Compute bounding boxes from ImageAnnotation.
    ImgAnnotation: instance of the ImageAnnotation class.
    Returns: bbox array [num_instances, (y1, x1, y2, x2)].
    """
    boxes = np.zeros([len(ImgAnnotation.annotation), 4], dtype=np.int32)
    classes = []
    confidences=[]
    for i in range(len(ImgAnnotation.annotation)):
        c = pointList2contour(ImgAnnotation.annotation[i].segmentation)
        # Bounding box
        x1,y1,w,h = cv2.boundingRect(c)
        x2=x1+w
        y2=y1+h
        boxes[i] = np.array([y1, x1, y2, x2])
        classes.append(ImgAnnotation.annotation[i].tags[0])
        confidences.append(1.0) ##TODO
    classes = np.expand_dims(np.array(classes), axis=1)
    confidences = np.expand_dims(np.array(confidences), axis=1)
    return boxes.astype(np.int32), classes, confidences
    
def extract_bboxes(ImgAnnotation, classFilter, classDict, size_thresh=0):
    """Compute bounding boxes from ImageAnnotation.
    ImgAnnotation: instance of the ImageAnnotation class.
    Returns: bbox array [num_instances, (y1, x1, y2, x2)].
    """
    boxes = np.zeros([len(ImgAnnotation.annotation), 4], dtype=np.int32)
    classes = []
    confidences=[]
    n=0
    for i in range(len(ImgAnnotation.annotation)):
        if ImgAnnotation.annotation[i].tags[0] not in classDict.keys():
            continue        
        if classDict[ImgAnnotation.annotation[i].tags[0]] not in classFilter:
            continue
        c = pointList2contour(ImgAnnotation.annotation[i].segmentation)
        # Bounding box
        x1,y1,w,h = cv2.boundingRect(c)
        if h < size_thresh:
            continue
        x2=x1+w
        y2=y1+h
        boxes[n] = np.array([y1, x1, y2, x2])
        classes.append(classDict[ImgAnnotation.annotation[i].tags[0]])
        confidences.append(1.0 ) ##TODO
        n=n+1
    boxes = boxes[0:n]
    classes = np.expand_dims(np.array(classes), axis=1)
    confidences = np.expand_dims(np.array(confidences), axis=1)
    return boxes.astype(np.int32), classes, confidences

def extract_bboxes_pred(ImgAnnotation, classFilter, size_thresh=0):
    """Compute bounding boxes from ImageAnnotation.
    ImgAnnotation: instance of the ImageAnnotation class.
    Returns: bbox array [num_instances, (y1, x1, y2, x2)].
    """
    boxes = np.zeros([len(ImgAnnotation.annotation), 4], dtype=np.int32)
    classes = []
    confidences=[]
    n=0
    for i in range(len(ImgAnnotation.annotation)):
        if ImgAnnotation.annotation[i].tags not in classFilter:
            continue
        c = pointList2contour(ImgAnnotation.annotation[i].segmentation)
        # Bounding box
        x1,y1,w,h = cv2.boundingRect(c)
        if h < size_thresh:
            continue
        x2=x1+w
        y2=y1+h
        boxes[n] = np.array([y1, x1, y2, x2])
        classes.append(ImgAnnotation.annotation[i].tags)
        confidences.append(ImgAnnotation.annotation[i].confidence ) ##TODO
        n=n+1
    boxes = boxes[0:n]
    classes = np.expand_dims(np.array(classes), axis=1)
    confidences = np.expand_dims(np.array(confidences), axis=1)
    return boxes.astype(np.int32), classes, confidences
    
def compute_iou(box, boxes):
    """Calculates IoU of the given box with the array of the given boxes.
    box: 1D vector [y1, x1, y2, x2]
    boxes: [boxes_count, (y1, x1, y2, x2)]
    box_area: float. the area of 'box'
    boxes_area: array of length boxes_count.
    Note: the areas are passed in rather than calculated here for
          efficency. Calculate once in the caller to avoid duplicate work.
    """
    # Calculate intersection areas
    box_area = (box[2]-box[0]) * (box[3]-box[1])
    boxes_area = np.multiply(boxes[:,2]-boxes[:,0], boxes[:,3]-boxes[:,1])
    y1 = np.maximum(box[0], boxes[:, 0])
    y2 = np.minimum(box[2], boxes[:, 2])
    x1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[3], boxes[:, 3])
    
    intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
    union = box_area + boxes_area[:] - intersection[:]
    iou = intersection / union
    return iou    

def compute_overlaps(boxes1, boxes2):
    """Computes IoU overlaps between two sets of boxes.
    boxes1, boxes2: [N, (y1, x1, y2, x2)].
    For better performance, pass the largest set first and the smaller second.
    """
    # Areas of anchors and GT boxes
    area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    area2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])

    # Compute overlaps to generate matrix [boxes1 count, boxes2 count]
    # Each cell contains the IoU value.
    overlaps = np.zeros((boxes1.shape[0], boxes2.shape[0]))
    for i in range(overlaps.shape[1]):
        box2 = boxes2[i]
        overlaps[:, i] = compute_iou(box2, boxes1)
    return overlaps

def trim_zeros(x):
    """It's common to have tensors larger than the available data and
    pad with zeros. This function removes rows that are all zeros.
    x: [rows, columns].
    """
    assert len(x.shape) == 2
    return x[~np.all(x == 0, axis=1)]

def compute_ap(gt_boxes, gt_class_ids,
               pred_boxes, pred_class_ids, pred_scores,
               iou_threshold=0.5):
    """Compute Average Precision at a set IoU threshold (default 0.5).
    Returns:
    mAP: Mean Average Precision
    precisions: List of precisions at different class score thresholds.
    recalls: List of recall values at different class score thresholds.
    overlaps: [pred_boxes, gt_boxes] IoU overlaps.
    """
    # Trim zero padding and sort predictions by score from high to low
    # TODO: cleaner to do zero unpadding upstream
    gt_boxes = trim_zeros(gt_boxes)
    pred_boxes = trim_zeros(pred_boxes)
    pred_scores = pred_scores[:pred_boxes.shape[0]]
    indices = np.argsort(pred_scores, axis=0)#[::-1]
    pred_boxes = pred_boxes[indices]
    pred_class_ids = pred_class_ids[indices]
    pred_scores = pred_scores[indices]
    #print(pred_boxes.shape, pred_boxes[:,0,:].shape, gt_boxes.shape)
    # Compute IoU overlaps [pred_boxes, gt_boxes]
    overlaps = compute_overlaps(pred_boxes[:,0,:], gt_boxes)

    # Loop through ground truth boxes and find matching predictions
    match_count = 0
    pred_match = np.zeros([pred_boxes.shape[0]])
    gt_match = np.zeros([gt_boxes.shape[0]])
    for i in range(len(pred_boxes)):
        # Find best matching ground truth box
        sorted_ixs = np.argsort(overlaps[i])[::-1]
        for j in sorted_ixs:
            # If ground truth box is already matched, go to next one
            if gt_match[j] == 1:
                continue
            # If we reach IoU smaller than the threshold, end the loop
            iou = overlaps[i, j]
            if iou < iou_threshold:
                break
            # Do we have a match?
            if pred_class_ids[i] == gt_class_ids[j]:
                match_count += 1
                gt_match[j] = 1
                pred_match[i] = 1
                break

    # Compute precision and recall at each prediction box step
    precisions = np.cumsum(pred_match) / (np.arange(len(pred_match))+1)
    recalls = np.cumsum(pred_match).astype(np.float32) / len(gt_match)
    #----------------------------------------------------------
    if len(pred_match) != 0:
        precision = np.sum(pred_match) / len(pred_match)
    else:
        precision = 1.0
    if len(gt_match) != 0:
        recall = np.sum(gt_match) / len(gt_match)
    else:
        recall = 1.0
    # Pad with start and end values to simplify the math
    precisions = np.concatenate([[0], precisions, [0]])
    recalls = np.concatenate([[0], recalls, [1]])

    # Ensure precision values decrease but don't increase. This way, the
    # precision value at each recall threshold is the maximum it can be
    # for all following recall thresholds, as specified by the VOC paper.
    for i in range(len(precisions)-2, -1, -1):
        precisions[i] = np.maximum(precisions[i], precisions[i+1])

    # Compute mean AP over recall range
    indices = np.where(recalls[:-1] != recalls[1:])[0] + 1
    mAP = np.sum((recalls[indices] - recalls[indices - 1]) * precisions[indices])

    return mAP, precisions, recalls, precision, recall, overlaps
 
 
    
if __name__ == "__main__":
    
    MIN_SIZES = [0, 25, 40, 50, 80]
    fileloc = "/mnt/ssd/home/rosalia/data/mtyai_semantic/jsons/" #1207.143950_FV_450.json"
    predloc = "/mnt/ssd/nfs/datasets/mightyAI_MaskRCNN/testResults/" #1207.143950_FV_450.json"
    classFilters = [["car"], ["person"], ["car", "bus", "truck", "bicycle", "motorcycle", "person"]]
    #classFilter = ["car", "van", "bus", "truck", "trailer", "bicycle", "motorcycle", "group_vehicles", "pedestrian", "rider"]
    classDict = {"car": "car", "van": "car", "bus" : "bus", "truck" : "truck", "trailer": "truck", "bicycle" : "bicycle", "motorcycle": "motorcycle", "group_vehicles": "car", "pedestrian" : "person", "rider" : "person"}
    for classFilter in classFilters:
        for MIN_SIZE in MIN_SIZES:            
            avg_mAP = 0.0
            avg_precision = 0.0
            avg_recall = 0.0
            cont = 0
            for file in glob.glob(fileloc+"*.json"):
                filename = os.path.basename(file)
                gt = util.annotation.ImageDBAnnotation()
                gt.load(file) 
                gtbbox, gtclasses, gtconfs = extract_bboxes(gt.imageAnnotation, classFilter, classDict, MIN_SIZE)
                predfile = predloc+filename
                preds = util.annotation.ImageDBAnnotation()
                preds.load(predfile) 
                predbbox, predclasses, predconfs = extract_bboxes_pred(preds.imageAnnotation, classFilter, MIN_SIZE)
                if len(gtclasses) == 0:
                    continue
                mAP, precisions, recalls, precision, recall, overlaps= compute_ap(gtbbox, gtclasses,
                   predbbox, predclasses, predconfs,
                   iou_threshold=0.5)
                if math.isnan(mAP):
                    continue
                avg_mAP = mAP + avg_mAP
                avg_precision = avg_precision + precision
                avg_recall = avg_recall + recall
                cont = cont + 1
            
            print("kpis for classes: " + str(classFilter) )
            print("min object size: " + str(MIN_SIZE) + " px" )
            print("files: " + str(cont))
            if cont==0:
                exit()
            print("mAP: " + str(avg_mAP/cont) )
            print("precision: " + str(avg_precision/cont) )
            print("recall: " + str(avg_recall/cont) )
            print("**----------------------------------------------**")
        