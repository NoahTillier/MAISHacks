import csv
import re
import json

input_file = "RoomsAndObjects.csv"
output_file = "RoomsAndObjects_clean.csv"

creatures = ["Wizard", "Dragon", "Minion", "King", "Knight", "Courtier"]

def normalize_cell(value):
    #bracketed lists to proper JSON lists
    value = value.strip()
    if not value:
        return "[]"
    if re.match(r"^\[.*\]$", value):
        inner = value[1:-1].strip()
        if not inner:
            return "[]"
        # split on commas and strip
        items = [x.strip() for x in inner.split(",")]
        return json.dumps(items)
    return value

with open(input_file, newline='') as f:
    reader = list(csv.reader(f))
    header = reader[0]
    rows = reader[1:]

# normalize cells
for r in rows:
    for i, val in enumerate(r):
        r[i] = normalize_cell(val)

# add creature column
header.append("Creatures")
for i, r in enumerate(rows):
    r.append(creatures[i] if i < len(creatures) else "")

# get cleaned CSV
with open(output_file, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Reformatted and added Creatures column")

