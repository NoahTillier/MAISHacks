from typing import List
from PIL import Image as PILImage
from urllib.request import urlopen
from IPython.display import Image, display
import numpy as np
from addFunction import add
from addFunction import addInexclusive

def corridors(im1: PILImage.Image, matrix: np.array, listOfCorridors):
  url = "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Wall.png"
  url2= "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/FloorTile.png"
  wallTile = PILImage.open(urlopen(url))
  wallTileT = wallTile.transpose(PILImage.Transpose.ROTATE_90)
  floorTile = PILImage.open(urlopen(url2))
  for corridor in listOfCorridors:
    length = corridor[2]-corridor[0]
    #dx = 1 if corridor[2] >= corridor[0] else -1
    height = corridor[3]-corridor[1]
    #dy = 1 if corridor[3] >= corridor[1] else -1
    for j in range(length):
      addInexclusive(im1, floorTile, corridor[0]+j, float(corridor[1]))
      add(im1, wallTile, matrix, corridor[0]+j,float(corridor[1]+1)-12/80)
      add(im1, wallTile, matrix, corridor[0]+j,float(corridor[1])-12/80)
    for j in range(height):
      addInexclusive(im1, floorTile, corridor[0], float(corridor[1])+j)
      add(im1, wallTileT, matrix, float(corridor[0]+1)-12/80,corridor[1]+j)
      add(im1, wallTileT, matrix, float(corridor[2])-12/80,corridor[1]+j)
