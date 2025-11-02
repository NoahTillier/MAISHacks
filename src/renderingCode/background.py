from typing import List
from PIL import Image as PILImage
from urllib.request import urlopen
from IPython.display import Image, display
import numpy as np

def background() -> PILImage.Image:
  #sets width and height of new image to be 80*32 pixels
  w = 80 * 32
  h = 80 * 32
  im = PILImage.new("RGBA", (w,h))

  #uses url from github page to render blankTile.
  url = "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Blank.png"
  blankTile = PILImage.open(urlopen(url))

  #iterates from 0 to 32 (exclusive) to generate a 30X30 map with a border of 1
  for i in range(32):
    for j in range(32):
      im.paste(blankTile, (i*80,j*80))
  
  return im
