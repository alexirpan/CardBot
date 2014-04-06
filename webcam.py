from SimpleCV import *
import time
from cardReader import output_cards

cam = Camera()
disp = Display()

while disp.isNotDone():
    img = Image("http://10.24.24.147:8080/shot.jpg")
    cards = output_cards(img, disp)
    if disp.mouseLeft:
        break
    