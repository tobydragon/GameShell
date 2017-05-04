import urllib.request
import pygame, json
import io
import os
import hashlib
import urlImage
import time
import pickle
starttime=time.clock()

def timestamp():
    global starttime
    print(time.clock()-starttime)
    starttime=time.clock()


print("fetching image")
timestamp()
img=urlImage.fetchLocationImage("France")
timestamp()
with open("temp",'wb') as f:
    pickle.dump(img,f)
timestamp()
with open("temp",'rb') as f:
    img=pickle.load(f)
timestamp()
