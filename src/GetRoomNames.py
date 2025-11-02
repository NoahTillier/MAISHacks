# get the room names for the final matplotlib rendering based on the objects placed in each room
# this can be done without "guessing", but longer to implement and running out of time!

import csv
import json

def load_room_definitions():
    room_defs = {}
    with open("RoomsAndObjects_clean.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            room_name = row.get("Room", "").strip()
            if room_name:  # onl process rows with actual room names
                has_objects = row.get("Has", "[]")
                try:
                    objects = set(json.loads(has_objects))
                    room_defs[room_name] = objects
                except json.JSONDecodeError:
                    room_defs[room_name] = set()
    return room_defs

def identify_room_type(placed_objects, room_definitions):
    placed_set = set(placed_objects)
    best_match = ""
    best_score = 0
    
    for room_type, required_objects in room_definitions.items():
        if not required_objects:
            continue
        
        # calculate score
        matches = len(placed_set & required_objects)
        total_required = len(required_objects)
        
        score = matches / total_required if total_required > 0 else 0
        
        if score > best_score:
            best_score = score
            best_match = room_type
    
    # return room
    return f"{best_match}"