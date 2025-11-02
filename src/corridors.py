from typing import List
from PIL import Image as PILImage
from urllib.request import urlopen
from IPython.display import Image, display

def corridors(im1: PILImage.Image, listOfCorridors):
  url = "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Wall.png"
  wallTile = PILImage.open(urlopen(url))
  wallTileT = wallTile.transpose(PILImage.Transpose.ROTATE_90)
  for corridor in listOfCorridors:
    length = corridor[2]-corridor[0]
    #dx = 1 if corridor[2] >= corridor[0] else -1
    height = corridor[3]-corridor[1]
    #dy = 1 if corridor[3] >= corridor[1] else -1
    for j in range(length):
      add(im1, wallTile, corridor[0]+j,corridor[1]+1)
      add(im1, wallTile, corridor[0]+j,corridor[1])
    for j in range(height):
      add(im1, wallTileT, corridor[0]+1,corridor[1]+j)
      add(im1, wallTileT, corridor[2],corridor[1]+j)
