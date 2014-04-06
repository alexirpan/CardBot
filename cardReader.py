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

def output_cards(img):
    modified = img
    edges = modified.edges()
    blobs = edges.findBlobs()
    #boxlayer = DrawingLayer((img.width, img.height))
    to_crop_to = []
    edges.findBlobs().show()
    time.sleep(1)
    for blob in blobs:
        x, y, w, h = blob.boundingBox()
        imgratio = max(w,h) / float(min(w,h))
      #  print w*h
        if w*h >= size_threshold:
     #       boxlayer.rectangle((x, y), (w,h), width=2, color=Color.GREEN)
       #     print imgratio
            if abs(imgratio - ratio) <= 0.5:
                to_crop_to.append((x,y,w,h))
    # some post processing
    # face cards have blobs in the center, which we don't want
    # check if a box contains another, remove inner box
    boxes = list(to_crop_to)
    print boxes
    for x,y,w,h in to_crop_to:
        remove = False
        for x2,y2,w2,h2 in to_crop_to:
            if x > x2 and y > y2 and w < w2 and h < h2:
                remove = True
                break
        if remove:
            boxes.remove((x,y,w,h))
    #img.addDrawingLayer(boxlayer)
    #img.applyLayers()
    #img.show()
    cropped = [img.crop(*c) for c in boxes]
    return cropped

suits_path = "suits/"
extension = "*.png"
suit_imgs = glob.glob(os.path.join(suits_path, extension))
    
def check_suit(card_img):
    t = 5

    methods = ["SQR_DIFF","SQR_DIFF_NORM","CCOEFF","CCOEFF_NORM","CCORR","CCORR_NORM"] # the various types of template matching available
    for m in methods:
        copy = card_img.scale(1)
        print "current method:", m # print the method being used
        dl = DrawingLayer((copy.width, copy.height))
        colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
        curr = 0
        for suit in suit_imgs:
            fs = copy.findTemplate(Image(suit), threshold=t, method=m)
            for match in fs:
                dl.rectangle((match.x,match.y),(match.width(),match.height()),color=colors[curr])
            curr += 1
        copy.addDrawingLayer(dl)
        copy.applyLayers()
        copy.show()
        time.sleep(1.5)
    
def read_card(card_img):
    # normalize card
    if card_img.width > card_img.height:
        card_img = card_img.rotate(90, fixed=False)
    normalized_size_width = 186.0# random value
    card_img = card_img.scale(card_img.width / normalized_side_width)
    # at normalized size,
    suit_width = 18
    suit_height = 22 # +/- a bit
    
    card_img.show()
    time.sleep(1.5)
    card_img.edges().show()
    time.sleep(1.5)
    check_suit(card_img)
    blobs = card_img.edges().findBlobs()
    count = 0
    boxlayer = DrawingLayer((card_img.width, card_img.height))
    boxes = [blob.boundingBox() for blob in blobs]
    for box in boxes:
        x,y,w,h = box
        boxlayer.rectangle((x, y), (w,h), width=2, color=Color.GREEN)
        count += 1
    # find the top left and bottom right boxes
    # this only does leftmost + rightmost but works on cards
    boxes.sort(key=lambda b: b[0])
    boxlayer.rectangle(boxes[0][:2], boxes[0][2:], width=2, color=Color.RED)
    boxlayer.rectangle(boxes[1][:2], boxes[1][2:], width=2, color=Color.RED)
    boxes.sort(key=lambda b: -b[0])
    boxlayer.rectangle(boxes[0][:2], boxes[0][2:], width=2, color=Color.BLUE)
    boxlayer.rectangle(boxes[1][:2], boxes[1][2:], width=2, color=Color.BLUE)
    
    card_img.addDrawingLayer(boxlayer)
    card_img.applyLayers()
    card_img.show()
    print "guess of %d" % count
    time.sleep(1.5)
    
import random
for file in files:
    print "New image"
    img = Image(file).scale(0.2)
    cards = output_cards(img)
    for card in cards:
        read_card(card)