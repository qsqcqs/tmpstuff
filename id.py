#@misc{
#cracks-3ii36_dataset,
#title = { cracks Dataset },
#type = { Open Source Dataset },
#author = { FYP },
#howpublished = { \url{ https://universe.roboflow.com/fyp-ny1jt/cracks-3ii36 } },
#url = { https://universe.roboflow.com/fyp-ny1jt/cracks-3ii36 },
#journal = { Roboflow Universe },
#publisher = { Roboflow },
#year = { 2024 },
#month = { may },
#note = { visited on 2025-07-30 },
#}
#key=TEl483hUremqGrXv6vqO

from PIL import Image 
import subprocess 
import cv2
from ultralytics import YOLO
import os, sys
import torch

frame = cv2.imread("/home/qsqcqs/Videos/Closeup-concrete-cracks.webp")#ngl this is some random pic rn but cv2 works with camera imports


model = YOLO("./YOLOv8-crack-seg/yolov8n/weights/best.pt") #general crack detection
#yolov8n is also being used because its the more "lightweight" version and can hopefully run
#without any internet stuff
labels=["crack"] #its fortunately only crack and not detecting a crack
results = model.predict(frame,verbose=False) #verbose means it talks, verbose=False means it shuts up
confidence_needed=.8#80% 

crack_count=0
for result in results:
    for box in result.boxes:
        print(f"{labels[int(box.cls)]}:{float(box.conf[0])*100}%")
        if float(box.conf[0])>confidence_needed:
            crack_count+=1

oldmodel=model #debug thing, ignore this line

model = YOLO("./YOLOv8-three-level-crack-classification/last.pt")  #classifying cracks
labels=["Hairline","Structural Cracks","Spalling Cracks"] #ngl I just found these off the site docs
results = model.predict(frame,verbose=False)

outputs=[]
for result in results:
    for box in result.boxes:
        outputs.append([labels[int(box.cls)],float(box.conf[0])])
if outputs.__len__()==crack_count: #if they agree on the number of cracks 
    for thing in outputs:
        print(f"{thing[0]}:{thing[1]*100}%")

#some shady stuff to handle the crack classifier being weird
elif outputs.__len__()>crack_count and crack_count==1:
    ono=False #ono is indeed very bad, we do not want the oh no
    x=1
    while x<outputs.__len__():
        if outputs[0][0]!=outputs[x][0]:#if some of the other detected cracks are different types
            ono=True #honestly idk what to do about it
            oldmodel.predict(frame,verbose=False,save=True)
            model.predict(frame,verbose=False,save=True)
            raise ValueError("classifier is weird lol")
            #merging them probably isnt the best practice but its still better than flat out erroring
        else:
            if outputs[0][1]>outputs[x][1]:
                outputs.pop(x)
            else:
                outputs.pop(0)
            x-=1
        x+=1
    if not ono:
        for thing in outputs:
            print(f"{thing[0]}:{thing[1]*100}%")
    else:
        for thing in outputs:
            print(f"{thing[0]}:{thing[1]*100}%")

elif outputs.__len__()>crack_count and crack_count>1:
    oldmodel.predict(frame,verbose=False,save=True)
    model.predict(frame,verbose=False,save=True)
    raise ValueError("classifier is weird lol")
    
            
        

#font = cv2.FONT_HERSHEY_SIMPLEX 
#bottom_left_corner_of_text = (2, 40)
#font_scale = 1
#font_color = (0, 0, 0)  
#line_type = 3 
#cv2.putText(annotated_frame, "mmmtext", bottom_left_corner_of_text, font, font_scale, font_color, line_type)
#final_save_frame = frame 
#cv2.putText(final_save_frame, "mmmtext", bottom_left_corner_of_text, font, font_scale, font_color, line_type)
#model.predict(final_save_frame, save=True) 

    

