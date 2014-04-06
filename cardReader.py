from SimpleCV import *
import os
import glob
import time

debugCard = False
last_time = [time.time()]
text = [[]]

def output_cards(img, disp):
    size_threshold = 5000
    ratio = 1.4 # taken from a picture

    modified = img
    edges = modified.edges()
    blobs = edges.findBlobs()
    boxlayer = DrawingLayer((img.width, img.height))
    to_crop_to = []
    if not blobs:
        return
    for blob in blobs:
        x, y, w, h = blob.boundingBox()
        imgratio = max(w,h) / float(min(w,h))
        #print w*h
        if w*h >= size_threshold:
            boxlayer.rectangle((x, y), (w,h), width=2, color=Color.GREEN)
            #print imgratio
            if abs(imgratio - ratio) <= 0.5:
                to_crop_to.append((x,y,w,h))
    img.addDrawingLayer(boxlayer)
    img.applyLayers()
    # some post processing
    # face cards have blobs in the center, which we don't want
    # check if a box contains another, remove inner box
    boxes = list(to_crop_to)
    for x,y,w,h in to_crop_to:
        remove = False
        for x2,y2,w2,h2 in to_crop_to:
            if x > x2 and y > y2 and x+w < x2+w2 and y+h < y2+h2:
                remove = True
                break
        if remove:
            boxes.remove((x,y,w,h))
    #img.addDrawingLayer(boxlayer)
    #img.applyLayers()
    #img.show()
    cropped = [img.crop(*c) for c in boxes]
    if not cropped:
        return
    # Text updates every second
    ranks = [read_card(card) for card in cropped]
    if time.time() - last_time[0] > 1:
        last_time[0] = time.time()
        # write text
        text[0] = []
        for rank, c in zip(ranks, boxes):
            if rank:
                text[0].append((word(rank), c[0], c[1]))
    for s, x, y in text[0]:
        img.drawText(s, x=x, y=y, color=Color.BLACK, fontsize=56)
    img.save(disp)

def word(val):
    l = ['zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
    return l[val]
    
    
def find_color(card_img):
    # Takes normalized card
    # Get the top left corner (roughly)
    rank_and_suit = card_img.crop(8,8,24,64)
    rank_and_suit.show()
    # count red pixels and black pixels
    # red: RGB value has R as largest value, R is above 100
    # black: Each value below threshold
    black_threshold = 50
    red_pix = 0
    black_pix = 0
    
    flat = rank_and_suit.getNumpy()
    for i in range(len(flat)):
        for j in range(len(flat[0])):
            b, g, r = flat[i, j]
            if r > 100 and r == max(b,g,r):
                red_pix += 1
            elif max(r,g,b) < black_threshold:
                black_pix += 1
    print "Red ", red_pix, "Black ", black_pix
    if black_pix > 100:
        print "Guessing a black card"
    else:
        print "Guessing a red card"
    
suits_path = "suits/"
extension = "*.png"
suit_imgs = glob.glob(os.path.join(suits_path, extension))
    
def find_suit(card_img, boxes):
    return "I have no clue"
    find_color(card_img)
    return
    boxes.sort(key=lambda b: b[0])
    boxlayer.rectangle(boxes[0][:2], boxes[0][2:], width=2, color=Color.RED)
    boxlayer.rectangle(boxes[1][:2], boxes[1][2:], width=2, color=Color.RED)
    boxes.sort(key=lambda b: -b[0])
    boxlayer.rectangle(boxes[0][:2], boxes[0][2:], width=2, color=Color.BLUE)
    boxlayer.rectangle(boxes[1][:2], boxes[1][2:], width=2, color=Color.BLUE)
    
    methods = ["SQR_DIFF","SQR_DIFF_NORM","CCOEFF","CCOEFF_NORM","CCORR","CCORR_NORM"] # the various types of template matching available
    for m in methods:
        copy = card_img.scale(1)
        print "current method:", m # print the method being used
        dl = DrawingLayer((copy.width, copy.height))
        colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
        curr = 0
        for name, suit in zip(('club', 'diamond', 'heart', 'spade'), suit_imgs):
            fs = copy.findTemplate(Image(suit), method=m)
            if fs:
                print "%s found" % name
            for match in fs:
                dl.rectangle((match.x,match.y),(match.width(),match.height()),color=colors[curr])
            curr += 1
        copy.addDrawingLayer(dl)
        copy.applyLayers()
        copy.show()
    
def read_card(card_img):
    # normalize card
    normalized_side_width = 200.0 # random value
    if card_img.width > card_img.height:
        card_img = card_img.rotate(90, fixed=False)
    card_img = card_img.scale(normalized_side_width / card_img.width)
    # at normalized size,
    suit_width = 18
    suit_height = 22 # +/- a bit
    
    #card_img.save(disp)
    # check_suit(card_img)
    blobs = card_img.edges().findBlobs()
    if not blobs:
        return
    count = 0
    boxes = [blob.boundingBox() for blob in blobs]
    rank = find_rank(card_img, boxes)
    return rank
    suit = find_suit(card_img, boxes)
    # display this guess

def find_rank(card_img, boxes):
    # Debug drawing
    boxlayer = DrawingLayer((card_img.width, card_img.height))
    cellSize = 30*30
    cellRatio = 1.15 # +/- at least 0.15
    for box in boxes:
        x,y,w,h = box
        boxlayer.rectangle((x, y), (w,h), width=2, color=Color.GREEN)
        ratio = max(w,h) / float(min(w,h))
        if w*h > cellSize and w*h < 4*cellSize and abs(ratio - cellRatio) < 0.5:
            boxlayer.rectangle((x, y), (w,h), width=2, color=Color.RED)
    card_img.addDrawingLayer(boxlayer)
    card_img.applyLayers()
    #card_img.save(disp)
    # check for face card
    largest = [w*h for x,y,w,h in boxes]
    boxes = zip(boxes, largest)
    boxes.sort(key=lambda x: -x[1])
    while boxes and 200*280 - boxes[0][1] < 10000:
        boxes = boxes[1:]
    if not boxes:
        return
    # check largest remaining for facecard
    if boxes[0][1] > 90*75:
        # is face card
        print "face card"
        return 10
    numCells = len(filter(lambda x: x > cellSize and x < 4*cellSize, largest))
    if numCells > 10:
        print "Something went wrong"
        print "Guessing 10"
        return 10
    if numCells == 0:
        print "Couldn't find cell"
        print "Guess A"
        return 1
    return numCells
    
if debugCard:
    cards_path = "sampleCards/"
    extension = "*.jpg"

    directory = os.path.join(cards_path, extension)
    files = glob.glob(directory)
    suits_path = "suits/"
    extension = "*.png"
    suit_imgs = glob.glob(os.path.join(suits_path, extension))
    
    for file in files:
        print "New image"
        img = Image(file, colorSpace=ColorSpace.BGR).scale(0.2)
        cards = output_cards(img)
        for card in cards:
            read_card(card)