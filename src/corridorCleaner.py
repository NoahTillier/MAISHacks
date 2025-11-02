from typing import List
from PIL import Image as PILImage
from urllib.request import urlopen
from IPython.display import Image, display

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
