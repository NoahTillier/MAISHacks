from typing import List
from PIL import Image as PILImage
from urllib.request import urlopen
from IPython.display import Image, display
import numpy as np

def placeItem(bg: PILImage.Image, dictionary):
  urls={"Armor": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Armor.png", "Bed": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Bed.png", "Candle": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Candle.png","Chandelier": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Chandelier.png","Oven": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Oven.png","Painting": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Painting.png","Pillar": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Pillar.png","Pot": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Pot.png","Table": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Table.png","Throne": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Throne.png","Toilet": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Toilet.png","Window": "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/Window.png"}
  for key, innerDictionary in dictionary.items():
    for keyTwo, (x,y) in innerDictionary.items():
      for item, url in urls.items():
        if(item.lower() in keyTwo.lower()):
          img = PILImage.open(urlopen(url)).convert("RGBA")
          datas = img.getdata()
          new_data = []
          for item in datas:
            r, g, b, a = item
            if r >= 240 and g >= 240 and b >= 240:
              # Replace white-ish pixel with transparent
              new_data.append((255, 255, 255, 0))
            else:
              new_data.append((r, g, b, a))

          img.putdata(new_data)

          addInexclusive(bg, img, x, y)
          break
