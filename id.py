from PIL import Image 
import subprocess 
import cv2
from ultralytics import YOLO
import os, sys
import torch


image_path=sys.argv[1]
if(sys.argv.__len__()>2): #second arg is confidence (optional)
    confidence_needed=float(sys.argv[2])
else:
    confidence_needed=.8#80% arbitrarily
frame = cv2.imread(image_path)#ngl this is some random pic rn but cv2 works with camera imports
model = YOLO("./YOLOv8-crack-seg/yolov8n/weights/best.pt") #general crack detection
#yolov8n is also being used because its the more "lightweight" version and can hopefully run
#without any internet stuff
labels=["crack"] #its fortunately only crack and not detecting a crack
results = model.predict(frame,verbose=False,conf=confidence_needed) #verbose means it talks, verbose=False means it shuts up
crack_count=0
for result in results:
    for box in result.boxes:
        print(f"{labels[int(box.cls)]}:{float(box.conf[0])*100}%")
        if float(box.conf[0])>confidence_needed:
            crack_count+=1
oldmodel=model #debug thing, ignore this line

model = YOLO("./YOLOv8-three-level-crack-classification/last.pt")  #classifying cracks
labels=["Hairline","Structural Cracks","Spalling Cracks"] #ngl I just found these off the site docs


confidence_needed_sub=confidence_needed
outputs=[]
confvals=[]
while outputs.__len__()!=crack_count:
    outputs=[]
    confvals=[]
    results = model.predict(frame,verbose=False,conf=confidence_needed_sub)
    for result in results:
        for box in result.boxes:
            outputs.append([labels[int(box.cls)],float(box.conf[0])])
            confvals.append(float(box.conf[0]))
    confvals.sort(reverse=True)#descending order
    if outputs.__len__()>crack_count: #tl;dr if too many cracks, increase standards so there arent
        confidence_needed_sub=(confvals[crack_count]+confvals[crack_count-1])/2
    if outputs.__len__()<crack_count: #tl;dr, if not enough cracks, lower standards so there are more
        confidence_needed_sub=.3#idk .3 looks low enough, definitely an asspull of a number
for thing in outputs:
    print(f"{thing[0]}:{thing[1]*100}%")
model.predict(frame,verbose=False,save=True,conf=confidence_needed_sub)

