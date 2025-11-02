import random, json
from copy import deepcopy
import csv

# load cleaned CSV
rooms_data = []
with open("RoomsAndObjects_clean.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        for key in ["Has","MutualExclusive","Inexclusive","Exclusive","WallAdjacent","Corner","CenterAxis","Creatures"]:
            if row.get(key):
                try:
                    row[key] = json.loads(row[key])
                except json.JSONDecodeError:
                    row[key] = []
            else:
                row[key] = []
        if row.get("Dimensions (px)"):
            try:
                row["Dimensions (px)"] = json.loads(row["Dimensions (px)"])
            except json.JSONDecodeError:
                row["Dimensions (px)"] = []
        rooms_data.append(row)

# helpers
def room_bounds(bsp_room):
    # bsp_room = [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
    x1, y1 = bsp_room[0]
    x2, y2 = bsp_room[2]
    return x1, y1, x2, y2

def random_position_in_room(bounds, constraints=[], max_attempts=1000):
    x1, y1, x2, y2 = bounds
    
    for _ in range(max_attempts):
        x = random.randint(x1, x2 - 1)
        y = random.randint(y1, y2 - 1)
        
        # Check all constraints - position must satisfy ALL of them
        valid = True
        
        if "Corner" in constraints:
            corners = [(x1, y1), (x1, y2 - 1), (x2 - 1, y1), (x2 - 1, y2 - 1)]
            if (x, y) not in corners:
                valid = False
        
        if valid and "WallAdjacent" in constraints:
            wall_tiles = [(i, j) for i in range(x1, x2) for j in [y1, y2 - 1]] + \
                         [(i, j) for i in [x1, x2 - 1] for j in range(y1, y2)]
            if (x, y) not in wall_tiles:
                valid = False
        
        if valid and "CenterAxis" in constraints:
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            if (x != cx and y != cy):
                valid = False
        
        # If all constraints passed, return this position
        if valid:
            return (x, y)
    
    # Fallback if no valid position found after max_attempts
    return (random.randint(x1, x2 - 1), random.randint(y1, y2 - 1))

# GA operators
def make_individual(bsp_rooms):
    individual = {}
    for i, bsp_room in enumerate(bsp_rooms):
        x1, y1, x2, y2 = room_bounds(bsp_room)
        room_row = rooms_data[i] if i < len(rooms_data) else {
            "Room": f"Room{i}",
            "Has": [],
            "Creatures": [],
            "WallAdjacent": [],
            "Corner": [],
            "CenterAxis": [],
            "MutualExclusive": [],
            "Dimensions (px)": [x2 - x1, y2 - y1]
        }
        room_name = room_row.get("Room") or room_row.get("Rooms", f"Room{i}")
        individual[room_name] = {}

        # place objects
        for obj in room_row.get("Has", []):
            # force WallAdjacent for windows and paintings
            constraints = room_row.get("Corner", []) + \
                          room_row.get("WallAdjacent", []) + \
                          room_row.get("CenterAxis", [])
            # enforce wall-only placements
            if obj.lower() in ["window", "painting"]:
                constraints.append("WallAdjacent")

            pos = random_position_in_room((x1, y1, x2, y2), constraints)
            individual[room_name][obj] = pos

        # place creatures
        for creature in room_row.get("Creatures", []):
            if creature:
                pos = random_position_in_room((x1, y1, x2, y2),
                       constraints=room_row.get("Corner", []) +
                                   room_row.get("WallAdjacent", []) +
                                   room_row.get("CenterAxis", []))
                individual[room_name][creature] = pos
    return individual

def fitness(individual, bsp_rooms):
    score = 0
    # penalty for overlaps
    for room_name, items in individual.items():
        positions = list(items.values())
        if len(positions) != len(set(positions)):
            score -= 1
    
    # penalty for constraint violations
    for i, bsp_room in enumerate(bsp_rooms):
        x1, y1, x2, y2 = room_bounds(bsp_room)
        room_row = rooms_data[i] if i < len(rooms_data) else {"Room": f"Room{i}"}
        room_name = room_row.get("Room", room_row.get("Rooms", f"Room{i}"))
        
        placed = individual.get(room_name, {})
        
        # Check wall-adjacent objects
        wall_tiles = set(
            [(i, j) for i in range(x1, x2) for j in [y1, y2 - 1]] + 
            [(i, j) for i in [x1, x2 - 1] for j in range(y1, y2)]
        )
        
        for obj, pos in placed.items():
            # Check Corner constraints
            if obj in room_row.get("Corner", []):
                corners = {(x1, y1), (x1, y2 - 1), (x2 - 1, y1), (x2 - 1, y2 - 1)}
                if pos not in corners:
                    score -= 0.5
            
            # Check WallAdjacent constraints
            if obj in room_row.get("WallAdjacent", []):
                if pos not in wall_tiles:
                    score -= 2
            
            # Check CenterAxis constraints
            if obj in room_row.get("CenterAxis", []):
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                if pos[0] != cx and pos[1] != cy:
                    score -= 0.5
    # penalize mutual exclusive violations
    for i, room_row in enumerate(rooms_data):
        room_name = room_row.get("Room", room_row.get("Rooms", f"Room{i}"))
        placed = individual.get(room_name, {})
        for me_obj in room_row.get("MutualExclusive", []):
            if me_obj in placed:
                for other in room_row.get("Exclusive", []):
                    if other in placed:
                        score -= 0.5
    # reward full placement coverage
    total_items = sum(len(r.get("Has", [])) + len(r.get("Creatures", [])) for r in rooms_data)
    placed_items = sum(len(items) for items in individual.values())
    score += placed_items / max(total_items, 1)
    return score

def mutate(individual, bsp_rooms, mutation_rate=0.2):
    ind = deepcopy(individual)
    for i, bsp_room in enumerate(bsp_rooms):
        x1, y1, x2, y2 = room_bounds(bsp_room)
        room_row = rooms_data[i] if i < len(rooms_data) else {
            "Room": f"Room{i}",
            "Has": [],
            "Creatures": [],
            "WallAdjacent": [],
            "Corner": [],
            "CenterAxis": []
        }
        room_name = room_row.get("Room", room_row.get("Rooms", f"Room{i}"))
        for key in ind.get(room_name, {}):
            if random.random() < mutation_rate:
                constraints = room_row.get("Corner", []) + \
                              room_row.get("WallAdjacent", []) + \
                              room_row.get("CenterAxis", [])
                if key.lower() in ["window", "painting"]:
                    constraints.append("WallAdjacent")
                ind[room_name][key] = random_position_in_room((x1, y1, x2, y2), constraints)
    return ind

def crossover(parent1, parent2):
    child = {}
    for room_name in parent1:
        child[room_name] = {}
        for key in parent1[room_name]:
            child[room_name][key] = (
                parent1[room_name][key]
                if random.random() < 0.5
                else parent2.get(room_name, {}).get(key, parent1[room_name][key])
            )
    return child

# GA loop
def run_ga(bsp_rooms, POPULATION=150, GENERATIONS=200, ELITISM=0.15):
    population = [make_individual(bsp_rooms) for _ in range(POPULATION)]
    for gen in range(GENERATIONS):
        population = sorted(population, key=lambda ind: fitness(ind, bsp_rooms), reverse=True)
        next_pop = population[:max(1, int(POPULATION * ELITISM))]
        while len(next_pop) < POPULATION:
            p1, p2 = random.choices(population[:POPULATION // 2], k=2)
            child = crossover(p1, p2)
            child = mutate(child, bsp_rooms)
            next_pop.append(child)
        population = next_pop
    return max(population, key=lambda ind: fitness(ind, bsp_rooms))

# example usage
if __name__ == "__main__":
    from BSPDungeonGeneration import generate_bsp_dungeon
    MAP_W, MAP_H, ROOMS = 30, 30, 6
    rooms, corridors, root = generate_bsp_dungeon(MAP_W, MAP_H, ROOMS, rng_seed=42)
    best_layout = run_ga(rooms)
    print(json.dumps(best_layout, indent=2))

