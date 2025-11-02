import genetic_dungeon
from BSPDungeonGeneration import generate_bsp_dungeon
import matplotlib.pyplot as plt

MAP_W, MAP_H, ROOMS = 30, 30, 6

## IMPORTANT:
## for now, this is just an example of running the genetic algorithm on the BSP dungeon and visualizing the result

if __name__ == "__main__":
    rooms, corridors, root = generate_bsp_dungeon(MAP_W, MAP_H, ROOMS, rng_seed=42)
    best_layout = genetic_dungeon.run_ga(rooms)
    
    plt.figure(figsize=(8, 8))
    for room, objs in best_layout.items():
        for obj, (x, y) in objs.items():
            plt.scatter(x, y, label=obj)
            plt.text(x + 0.3, y, obj, fontsize=8)
        

    for room in rooms:
        x1, y1 = room[0]
        x2, y2 = room[2]
        plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], color='black')
    
    for corridor in corridors:
        x1, y1, x2, y2 = corridor
        plt.plot([x1, x2, ], [y1, y2], color='gray', linestyle='--')

    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Dungeon Room Object Positions")
    plt.show()

    
