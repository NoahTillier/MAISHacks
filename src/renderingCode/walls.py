from typing import List
from PIL import Image as PILImage
from urllib.request import urlopen
from IPython.display import Image, display
import numpy as np

def walls(im1: PILImage.Image, matrix: np.array, listOfRooms: List[int]):
  url = "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Wall.png"
  wallTile = PILImage.open(urlopen(url))
  wallTileT = wallTile.transpose(PILImage.Transpose.ROTATE_90)
  for room in listOfRooms:
    #assumes that the vertices are listed counterclockwise
    length = room[1][0]-room[0][0]
    height = room[2][1]-room[1][1]
    for j in range(length):
      add(im1, wallTile, matrix, room[0][0] + j, float(room[0][1])-12/80)
      add(im1, wallTile, matrix, room[0][0] + j, float(room[2][1])-12/80)
    for j in range(height):
      add(im1, wallTileT, matrix, float(room[0][0])-12/80, room[0][1] + j)
      add(im1, wallTileT, matrix, float(room[1][0])-12/80, room[0][1] + j)
