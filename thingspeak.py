import os

from dotenv import load_dotenv

#import RPi.GPIO as GPIO
from time import sleep
from PIL import Image
import sys
import requests
load_dotenv("/home/qsqcqs/py/.env")
index=0
TOKEN = os.getenv('THINGSPEAK_WRITE_TOKEN')
thingSpeakURL = f'http://api.thingspeak.com/update?api_key={TOKEN}&field1={index}'
#channel is 3020720
image_path="/home/qsqcqs/Videos/Untitled.jpg"
imData = Image.open(image_path)
with open(image_path, 'rb') as f:
    img_byte_arr = f.read()
    

print(thingSpeakURL)
print(img_byte_arr)
print({'Content-Type': f'image/{imData.format.lower()}',
    'thingspeak-image-channel-api-key': TOKEN,
    'Content-Length' : str(sys.getsizeof(img_byte_arr))})

x = requests.post(url = thingSpeakURL, data = img_byte_arr,
    headers = {'Content-Type': f'image/{imData.format.lower()}',
    'thingspeak-image-channel-api-key': TOKEN,
    'Content-Length' : str(sys.getsizeof(img_byte_arr))})
print(x)
# Sleep so we do not get locked out of ThingSpeak for posting too fast
#sleep(30)