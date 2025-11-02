from typing import List
from PIL import Image as PILImage
from urllib.request import urlopen
from IPython.display import Image, display
import numpy as np
from addFunction import addInexclusive

def addFloors(bg: PILImage.Image, listOfRooms):
    url= "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/FloorTile.png"
    floorTile = PILImage.open(urlopen(url))

    for room in listOfRooms:
      length = abs(room[1][0]-room[0][0])
      height = abs(room[2][1]-room[1][1])
      for i in range(length):
        for j in range(height):
          addInexclusive(bg, floorTile, (room[0][0]+i),(room[0][1]+j))
