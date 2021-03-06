#!/usr/bin/env python
# coding: utf-8


import cv2
import matplotlib.pyplot as plt
import numpy as np
from yolov3.yolo_opencv import get_objects_demo
from plates.plates_roi import get_license_plates_demo
from plates.ocr import extract_plate_text
import os

def get_frame_objects(video_filename, sample_rate=1):
    frames = get_objects_video(video_filename, sample_rate)

    clean_frames = []
    
    for frame in frames:
        video_objects = []
        for i, obj in enumerate(frame):
            if obj[1].shape[0] > 0 and obj[1].shape[1] > 0 and obj[1].shape[2] > 0:
                video_objects.append(obj)
        if len(video_objects) > 0:
            clean_frames.append(video_objects)
    return clean_frames

def get_frame_objects_demo(video_filename, sample_rate=1):
    cam = cv2.VideoCapture(video_filename)

    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
    out2 = cv2.VideoWriter('plates.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 5, (500,300), 0)
    
    plates = []

    ret = True
    while ret: 
        frame = None
        # reading from frame 
        if sample_rate > 1:
            for _ in range(sample_rate):
                ret,frame = cam.read()
        else:
            ret,frame = cam.read()
        
        if ret:
            new_frame, obj_img = get_objects_demo(frame)

            new_car = None
            if obj_img is not None and len(obj_img) > 0:
                try:
                    car_plates = get_license_plates_demo(obj_img)
                    if len(car_plates) > 0:
                        new_car = cv2.resize(car_plates[0],(500,300))
                        txt, plate_img = extract_plate_text(new_car)
                        if len(txt) > 0:
                            print(txt)
                            plate_img = cv2.resize(plate_img,(500,300))
                            out2.write(plate_img)
                except cv2.error as e:
                    print("cv2 error")
            out.write(new_frame)
    
    cam.release()
    out.release()
    out2.release()

import sys

if len(sys.argv) > 1:
    get_frame_objects_demo(sys.argv[1])