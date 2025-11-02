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

def corridorCleaner(listOfCorridors, listOfRooms):
  #needs logic to remove corridors from inside rooms
  for room in listOfRooms:
    #nomenclature will be bottom y, left is left x, top is top y, right is right x
    bottom = room[0][1]
    top = room[2][1]
    left = room[0][0]
    right = room[1][0]
    i = 0
    while i < len(listOfCorridors):
      if listOfCorridors[i][0] != listOfCorridors[i][2]:
        #case where the corridor end is to the left of the room wall
        if listOfCorridors[i][0] <= right and listOfCorridors[i][0] >= left:
          if listOfCorridors[i][1] <= top and listOfCorridors[i][1] >= bottom:
            listOfCorridors[i] = (right, listOfCorridors[i][1], listOfCorridors[i][2], listOfCorridors[i][3])
        #case where the corridor end is to the right of the room wall
        if listOfCorridors[i][2] <= right and listOfCorridors[i][2] >= left:
          if listOfCorridors[i][3] <= top and listOfCorridors[i][3] >= bottom:
            listOfCorridors[i] = (listOfCorridors[i][0],listOfCorridors[i][1],left, listOfCorridors[i][3])
      if listOfCorridors[i][1] != listOfCorridors[i][3]:
       #case where the corridor end is under the room wall
       if listOfCorridors[i][0] <= right and listOfCorridors[i][0] >= left:
         if listOfCorridors[i][1] <= top and listOfCorridors[i][1] >= bottom:
           listOfCorridors[i] = (listOfCorridors[i][0],top,listOfCorridors[i][2],listOfCorridors[i][3])
       #case where the corridor end is above the room wall
       if listOfCorridors[i][2] <= right and listOfCorridors[i][2] >= left:
          if listOfCorridors[i][3] <= top and listOfCorridors[i][3] >= bottom:
            listOfCorridors[i] = (listOfCorridors[i][0],listOfCorridors[i][1],listOfCorridors[i][2],bottom)
      i+=1

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

def addFloors(bg: PILImage.Image, listOfRooms):
    url= "https://raw.githubusercontent.com/GawainsGreenGirdle/MAISHacks/main/Tokens/FloorTile.png"
    floorTile = PILImage.open(urlopen(url))

    for room in listOfRooms:
      length = abs(room[1][0]-room[0][0])
      height = abs(room[2][1]-room[1][1])
      for i in range(length):
        for j in range(height):
          addInexclusive(bg, floorTile, (room[0][0]+i),(room[0][1]+j))
