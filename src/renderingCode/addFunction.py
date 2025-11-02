from typing import List
from PIL import Image as PILImage
from urllib.request import urlopen
from IPython.display import Image, display
import numpy as np

def addInexclusive(img: PILImage.Image, im2: PILImage.Image, x, y):
  #note that im1 should be the background or other image such that
  #each cell is 80*80.
  i = int(x * 80)
  j = int(y * 80)
  xSize, ySize = img.size
  if xSize-80 < i or ySize-80 < j:
    raise Exception("Invalid coordinate for input image size");
  else:
    im2 = im2.convert("RGBA")
    mask = im2.split()[3]
    img.paste(im2, (i,j), mask)

def add(im1: PILImage.Image, im2: PILImage.Image, matrix: np.array, x, y):
  #note that im1 should be the background or other image such that
  #each cell is 80*80.
  i = int(x * 80)
  j = int(y * 80)
  xSize, ySize = im1.size
  if xSize-80 < i or ySize-80 < j:
    raise Exception("Invalid coordinate for input image size");
  else:
    im1.paste(im2, (i,j))
    matrix[int(y), int(x)] = 1
