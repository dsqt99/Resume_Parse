import os
import json
import numpy as np
import uuid

from PIL import Image
import pytesseract
import cv2

import logging
import requests

from pdf2image import convert_from_path
from modules import YOLO_Det
from utils.extract_feature import resume_extract
from utils.hyper import *

def pdf2image(pdf_path):
    pages = convert_from_path(pdf_path)
    # merge all pages into one image
    image = np.vstack([np.asarray(page) for page in pages])
    return image

def docx2image(docx_path):
    pass

def download_from_path(path):
    if path.endswith(('.png', '.jpg', '.jpeg')):
        # download image
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif path.endswith('.pdf'):
        image = pdf2image(path)
    elif path.endswith(('.docx', '.doc', 'odt')):
        image = docx2image(path)
    else:
        raise Exception("Invalid input path")
    return image

def download_from_url(url):
    if url.endswith(('.png', '.jpg', '.jpeg')):
        # download image
        response = requests.get(url)
        image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif url.endswith('.pdf'):
        # download pdf
        response = requests.get(url)
        if not os.path.exists('./data_save'):
            os.mkdir('./data_save')
        pdf_path = './data_save/resume.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        
        image = pdf2image(pdf_path)
        # remove folder
        os.remove(pdf_path)
        os.rmdir('./data_save')
    elif url.endswith(('.docx', '.doc', 'odt')):
        # download docx
        response = requests.get(url)
        if not os.path.exists('./data_save'):
            os.mkdir('./data_save')
        docx_path = './data_save/resume.docx'
        with open(docx_path, 'wb') as f:
            f.write(response.content)
        image = docx2image(docx_path)
        # remove folder
        os.remove(docx_path)
        os.rmdir('./data_save')
    else:
        raise Exception("Invalid input path")
    return image
    
def ocr_image_tess(image):
    custom_config = r'--oem 3 --psm 6 -l vie+eng'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text
    
def get_feature(input_dir):
    # Load image
    if input_dir.startswith('http'):
        image = download_from_url(input_dir)
    else:
        image = download_from_path(input_dir)

    # Detect text
    det_model = YOLO_Det(weight_path=yolo_det_weight)
    boxes_list, label_list = det_model(image, yolo_confidence, yolo_iou, return_result=True, output_path=detbox_image_folder)

    # OCR and correct
    texts, labels = [], []
    avatar_status = False
    
    if len(boxes_list) == 0:
        raise Exception("No text detected")

    for i, box in enumerate(boxes_list):
        cropped_img = image[int(box[1]):int(box[3]), int(box[0]):int(box[2]), :]
        if label_list[i] == 'avatar':
            avatar = cropped_img.copy()
            avatar_status = True
        else:
            text = ocr_image_tess(cropped_img)
            text = text.split('\n')
            text = [t for t in text if t != '']
            text = '\n'.join(text)
            texts.append(text)
            labels.append(label_list[i])

    if not os.path.exists(avatar_folder):
        os.mkdir(avatar_folder)
    
    if avatar_status:
        avatar_path = os.path.join(avatar_folder, str(uuid.uuid4()) + '.png')
        cv2.imwrite(avatar_path, avatar[:,:,::-1])
        avatar_path = root_avatar_url + avatar_path.split('/')[-1]
    else:
        avatar_path = ''

    infos = resume_extract(texts, labels)

    data = {
        'avatar_path': avatar_path,
        'infos': infos
    }
   
    return data