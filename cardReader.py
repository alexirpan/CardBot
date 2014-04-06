from SimpleCV import *
import os
import glob
import time

cards_path = "sampleCards/"
extension = "*.jpg"

directory = os.path.join(cards_path, extension)
files = glob.glob(directory)

for file in files:
    img = Image(file).scale(0.1)
    img.show()
    time.sleep(0.5)
    img.edges().show()
    time.sleep(0.5)
    img.binarize().show()
    time.sleep(0.5)
