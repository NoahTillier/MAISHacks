# example usage to get vertices of rooms (important for genetic algorithm input and final rendering)
# rooms = generate_bsp_dungeon(30, 30, approx_rooms=10, rng_seed=42)[0] ## note we're taking [0] to get rooms only
# rooms is a list of rooms as lists of 4 vertices each
# e.g. [[(x1,y1),(x2,y1),(x2,y2),(x1,y2)], ...]
# so rooms[0] is the first room, rooms[0][0] is the first vertex of the first room

import random
from dataclasses import dataclass

@dataclass
class Leaf:
    x: int
    y: int
    w: int
    h: int
    left = None # leaf
    right = None # leaf
    room = None  # (x1,y1,x2,y2) the vertices of the room

    def is_leaf(self):
        return self.left is None and self.right is None

    def rect(self):
        return (self.x, self.y, self.w, self.h)

def split_leaf(leaf: Leaf, min_leaf_size: int, rng: random.Random) -> bool:
    if not leaf.is_leaf():
        return False
    w, h = leaf.w, leaf.h
    # cant split if too small
    if w < 2*min_leaf_size and h < 2*min_leaf_size:
        return False

    # choose split orientation based on shape (prefer split the longer axis)
    split_horizontally = False
    if w / h >= 1.25:
        split_horizontally = False
    elif h / w >= 1.25:
        split_horizontally = True
    else:
        split_horizontally = rng.choice([True, False])

    if split_horizontally:
        # horizontal split creates top and bottom pieces (split on y)
        max_split = h - min_leaf_size
        min_split = min_leaf_size
        if max_split <= min_split:
            return False
        split = rng.randint(min_split, max_split)
        leaf.left = Leaf(leaf.x, leaf.y, w, split)
        leaf.right = Leaf(leaf.x, leaf.y + split, w, h - split)
    else:
        # vertical split left and right pieces (split on x)
        max_split = w - min_leaf_size
        min_split = min_leaf_size
        if max_split <= min_split:
            return False
        split = rng.randint(min_split, max_split)
        leaf.left = Leaf(leaf.x, leaf.y, split, h)
        leaf.right = Leaf(leaf.x + split, leaf.y, w - split, h)
    return True

def gather_leaves(root: Leaf):
    leaves = []
    stack = [root]
    while stack:
        n = stack.pop()
        if n.is_leaf():
            leaves.append(n)
        else:
            if n.right: stack.append(n.right)
            if n.left: stack.append(n.left)
    return leaves

def create_room_in_leaf(leaf: Leaf, min_room_size:int, margin:int, rng: random.Random):
    x, y, w, h = leaf.rect()
    # space available after margins
    avail_w = max(0, w - 2*margin)
    avail_h = max(0, h - 2*margin)
    if avail_w < min_room_size or avail_h < min_room_size:
        # fall back to tiny room equal to leaf's inner area
        room_w = max(min_room_size, avail_w)
        room_h = max(min_room_size, avail_h)
        room_x = x + margin
        room_y = y + margin
        room_x2 = room_x + max(1,room_w)
        room_y2 = room_y + max(1,room_h)
    else:
        # pick random room size within this leaf's inner area
        room_w = rng.randint(max(min_room_size, avail_w//2), avail_w)
        room_h = rng.randint(max(min_room_size, avail_h//2), avail_h)
        room_x = rng.randint(x + margin, x + w - margin - room_w)
        room_y = rng.randint(y + margin, y + h - margin - room_h)
        room_x2 = room_x + room_w
        room_y2 = room_y + room_h
    leaf.room = (room_x, room_y, room_x2, room_y2)

def room_center(room):
    x1,y1,x2,y2 = room
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    return (cx, cy)

def find_room_in_subtree(node):
    if node is None:
        return None
    if node.room:
        return node.room
    left_room = None
    right_room = None
    if node.left:
        left_room = find_room_in_subtree(node.left)
    if left_room:
        return left_room
    if node.right:
        right_room = find_room_in_subtree(node.right)
    return right_room

def connect_subtrees_with_corridors(node, corridors):
    if node is None or node.is_leaf():
        return
    # ensure children processed first (so their rooms exist)
    connect_subtrees_with_corridors(node.left, corridors)
    connect_subtrees_with_corridors(node.right, corridors)
    room_a = find_room_in_subtree(node.left)
    room_b = find_room_in_subtree(node.right)
    if room_a and room_b:
        ax,ay = room_center(room_a)
        bx,by = room_center(room_b)
        # create L-shaped corridor: horizontal then vertical (both are axis-aligned 1xn segments)
        # Decide order randomly? We'll use horizontal then vertical for determinism.
        if ay == by:
            # single horizontal segment
            corridors.append((ax,ay,bx,by))
        elif ax == bx:
            # single vertical segment
            corridors.append((ax,ay,bx,by))
        else:
            # two segments: (ax,ay)->(bx,ay) then (bx,ay)->(bx,by)
            corridors.append((ax,ay,bx,ay))
            corridors.append((bx,ay,bx,by))

def generate_bsp_dungeon(map_w: int, map_h: int, approx_rooms: int,
                         min_leaf_size: int = 6, min_room_size:int = 3, margin:int = 1,
                         rng_seed = None):
    rng = random.Random(rng_seed)
    root = Leaf(0,0,map_w,map_h)
    # split leaves until we reach approx_rooms or can't split
    leaves = gather_leaves(root)
    # Ensure we have somewhere to split
    attempts = 0
    while len(leaves) < approx_rooms:
        # pick a leaf to split, prefer largest leaf (by area)
        leaves = gather_leaves(root)
        leaf = max(leaves, key=lambda L: L.w * L.h)
        did = split_leaf(leaf, min_leaf_size, rng)
        attempts += 1
        if not did:
            # no leaf could be split further so stop
            break
        if attempts > approx_rooms * 10 + 1000:
            # safety
            break

    # create rooms for each leaf!
    for leaf in gather_leaves(root):
        create_room_in_leaf(leaf, min_room_size, margin, rng)

    # collect rooms as vertex lists
    rooms = []
    for leaf in gather_leaves(root):
        if leaf.room:
            x1,y1,x2,y2 = leaf.room
            # vertices in CCW order
            verts = [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
            rooms.append(verts)

    corridors = []
    connect_subtrees_with_corridors(root, corridors)

    return rooms, corridors, root

rooms = generate_bsp_dungeon(30, 30, approx_rooms=7, rng_seed=300)[0]
corridors = generate_bsp_dungeon(30, 30, approx_rooms=7, rng_seed=300)[1]
print(rooms)
print("")
print(corridors)
