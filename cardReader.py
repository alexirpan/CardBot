from SimpleCV import *
import os
import glob
import time

cards_path = "sampleCards/"
extension = "*.jpg"

directory = os.path.join(cards_path, extension)
files = glob.glob(directory)

size_threshold = 6000 # max pixels in box
ratio = 1.35 # taken from a picture
ratio_threshold = 0.2

for file in files:
    print "New image"
    img = Image(file).scale(0.2)
    img.show()
    time.sleep(0.5)
    modified = img
    modified.show()
    time.sleep(0.5)
    edges = modified.edges()
    blobs = edges.findBlobs()
    edges.show()
    time.sleep(0.5)
    boxlayer = DrawingLayer((img.width, img.height))
    to_crop_to = []
    for blob in blobs:
        x, y, w, h = blob.boundingBox()
        imgratio = max(w,h) / float(min(w,h))
        print w*h
        if w*h >= size_threshold:
            boxlayer.rectangle((x, y), (w,h), width=2, color=Color.GREEN)
            to_crop_to.append((x,y,w,h))
            print max(w,h) / float(min(w,h))
    img.addDrawingLayer(boxlayer)
    img.applyLayers()
    img.show()
    time.sleep(0.5)
    
    for c in to_crop_to:
        img.crop(*c).show()
        time.sleep(0.5)
    
        
    
