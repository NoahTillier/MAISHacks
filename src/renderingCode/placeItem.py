from typing import List
from PIL import Image as PILImage
from urllib.request import urlopen
from IPython.display import Image, display
import numpy as np
from addFunction import addInexclusive

def placeItem(bg: PILImage.Image, matrix, dictionary):
  urls={"Armor": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Armor.png", "Bed": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Bed.png", "Candle": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Candle.png","Chandelier": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Chandelier.png","Oven": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Oven.png","Painting": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Painting.png","Pillar": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Pillar.png","Pot": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Pot.png","Table": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Table.png","Throne": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Throne.png","Toilet": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Toilet.png","Window": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Window.png"}
  for key, innerDictionary in dictionary.items():
    for keyTwo, (x,y) in innerDictionary.items():
      for item, url in urls.items():
        if(item.lower() in keyTwo.lower()):
          img = PILImage.open(urlopen(url))
          img = img.convert("RGBA")

          #rotates the item according to the nearest wall
          valid_items = {"throne", "armor", "bed", "oven", "painting", "window", "toilet"}
          if item.lower() in valid_items:
            for i in range(32):
              wallRight = (x+i)%32
              wallLeft = (x-i)%32
              wallUp = (y-i)%32
              wallDown = (y+i)%32
              if matrix[x][wallUp] == 1:
                break
              if matrix[wallRight][y] == 1:
                img = img.transpose(PILImage.ROTATE_90)
                break
              if matrix[x][wallDown] == 1:
                img = img.transpose(PILImage.ROTATE_180)
                break
              if matrix[wallLeft][x] == 1:
                img = img.transpose(PILImage.ROTATE_270)
                break

          #adds the item
          addInexclusive(bg, img, x, y)
          break
