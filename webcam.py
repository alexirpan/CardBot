from SimpleCV import *
import time
from cardReader import output_cards

cam = Camera()
disp = Display()

while disp.isNotDone():
    img = cam.getImage()
    cards = output_cards(img, disp)
    if disp.mouseLeft:
        break
    