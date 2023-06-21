import os
import cv2
import torch
import numpy as np
from ultralytics import YOLO

from utils.hyper import *


CACHE_DIR = '.cache'

map_label = {0: 'address', 
             1: 'date_of_birth', 
             2: 'gender', 
             3: 'email', 
             4: 'tel', 
             5: 'full_name', 
             6: 'text', 
             7: 'avatar',
             8: 'position'}

def get_otb(boxes, labels, percents, i): # get one the best of box with label not text
    max_percent = 0
    box, label = None, None
    for j in range(len(labels)):
        if labels[j] == i and percents[j] > max_percent:
            max_percent = percents[j]
            box = boxes[j]
            label = labels[j]
    return box, label, max_percent

class YOLO_Det:
    def __init__(self, weight_path=None, model_name=None):
        self.model_name = model_name
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = YOLO(weight_path)
        self.model.to(self.device)        
    
    def __call__(
            self, 
            image, 
            yolo_confidence=0.5,
            yolo_iou=0.5,
            return_result=False,
            output_path=None):
        """
        Input: path to image
        Output: boxes (coordinates of 4 points)
        """

        # Detect and OCR for final result
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = np.repeat(gray[:, :, np.newaxis], 3, axis=2)

        result = self.model(image, conf=yolo_confidence, iou=yolo_iou, agnostic_nms=True, verbose=False, device=self.device)
        
        if result[0].boxes.data.shape[0] == 0:
            return [], []
        
        boxes = result[0].boxes.data[:, :4].cpu().numpy().tolist()
        labels = result[0].boxes.data[:, 5].cpu().numpy().tolist()
        percents = result[0].boxes.data[:, 4].cpu().numpy().tolist()     

        boxes_list, labels_idx, percents_list = [], [], []
        for i in range(len(map_label)):
            if map_label[i] == 'text':
                for j in range(len(labels)):
                    if labels[j] == i:
                        boxes_list.append(boxes[j])
                        labels_idx.append(labels[j])
                        percents_list.append(percents[j])
            else:
                box, label, max_percent = get_otb(boxes, labels, percents, i)
                if box is not None:
                    boxes_list.append(box)
                    labels_idx.append(label)
                    percents_list.append(max_percent)
        
        labels_list = [map_label[int(i)] for i in labels_idx]

        if return_result and len(boxes_list) > 0:
            detect_image = image[:, :, ::-1].copy()
            for i in range(len(boxes_list)):
                box = boxes_list[i]
                label = labels_list[i]
                percent = percents_list[i]
                cv2.rectangle(detect_image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)
                cv2.putText(detect_image, label + ', ' + str(round(percent, 2)), (int(box[0]), int(box[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            cv2.imwrite(os.path.join(output_path, 'detect_image.png'), detect_image)

        return boxes_list, labels_list