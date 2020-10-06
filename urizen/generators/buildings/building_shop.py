#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C, T, A

from urizen.generators.rooms.room_default import room_default

def building_shop(w=11,h=9, shop_type=None, has_exterior=False, wall_material=None, floor_material=None):
    """
    Construct shops with storage, living part and trading part.

    Constraints:

        - Map width and map height must be >= 9 and <=13.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    """
    
    # Initial checks. Don't accept too small/big shop
    if w < 9 or h < 9:
        raise ValueError('Building is too small: w or h < 9')
    elif w > 30 or h > 30:
        raise ValueError('Building is too big: w or h > 30')

    shop_h = h-1 if has_exterior else h
    shop_left = random.choice([True, False])

    # Choose materials
    if not wall_material:
        wall_material = random.choice([C.wall_block, C.wall_plank, C.wall_brick])
    elif wall_material not in (['block', 'plank', 'brick']):
        raise ValueError('Wall material should be "block", "plank" or "brick"')
    if wall_material == 'block':
        wall_material = C.wall_block
    elif wall_material == 'plank':
        wall_material = C.wall_plank
    elif wall_material == 'brick':
        wall_material = C.wall_brick

    if not floor_material:
        floor_material = random.choice([C.floor_dirt, C.floor_parquet, C.floor_cobblestone])
    elif floor_material not in (['dirt', 'parquet', 'cobblestone']):
        raise ValueError('Floor material should be "dirt", "parquet" or "cobblestone"')
    if floor_material == 'dirt':
        floor_material = C.floor_dirt
    elif floor_material == 'parquet':
        floor_material = C.floor_parquet
    elif floor_material == 'cobblestone':
        floor_material = C.floor_cobblestone

    if not shop_type:
        shop_type = random.choice(['food', 'jewelry', 'clothe', 'weapon', 'armor', 'potion', 'tool', 'magic'])
    elif shop_type not in (['food', 'jewelry', 'clothe', 'weapon', 'armor', 'potion', 'tool', 'magic']):
        raise ValueError(
        'Shop type should be "food", "jewelry", "clothe", "weapon", "armor", "potion", "tool" or "magic"'
        )

    M = room_default(w, h, wall_type=C.void, floor_type=C.void)
    shop = room_default(w, shop_h, wall_type=wall_material, floor_type=floor_material)
    M.meld(shop, 0, 0)

    shop_part_w = w // 3 * 2
    living_part_w = w - shop_part_w

    shop_part = room_shop(shop_part_w+1, shop_h, shop_type, wall_material, floor_material)
    living_part = room_storage(living_part_w, shop_h, shop_type, wall_material, floor_material, shop_left)

    M.meld(shop_part, 0, 0)
    M.meld(living_part, shop_part_w, 0)

    all_coord = [((shop_part_w+1)//2, h-1),((shop_part_w+1)//2-1, h-1), ((shop_part_w+1)//2+2, h-1)]
    if has_exterior:
        for item_class in (
            C.flora_tree_willow,
            C.flora_grass,
            C.flora_grass,
            C.flora_cane
            ):
            while True:
                x = random.randint(0, w-1)
                y = h-1
                if (x, y) not in all_coord:
                    M[x, y] = item_class()
                    all_coord.append((x, y))
                    break
        M[(shop_part_w+1)//2-1, h-1].put(T.sign())
        M[(shop_part_w+1)//2+2, h-1].put(T.furniture_stool())
    
    if not shop_left:
        M.hmirror()

    return M

def room_shop(w, h, shop_type, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    M[w//2, h-1] = C.door_closed()
    M[1, h-2].put(T.light_lantern_oil())

    shop_counter_h = h // 2 - 1

    for x in range(w-3):
        cell_x = 2 + x
        M[cell_x, shop_counter_h].put(T.furniture_longtable_showcase())
    M[w-2, shop_counter_h-1].put(T.money_pile())

    type_items = {
        'food': [T.food_meat, T.food_carrot, T.food_apple],
        'jewelry': [T.necklace, T.necklace_star, T.ring],
        'clothe': [T.clothes_coat, T.clothes_hat, T.clothes_belt],
        'weapon':[T.weapon_sword_rapier, T.weapon_naginata, T.weapon_crossbow],
        'armor': [T.helmet, T.armor_mail, T.clothes_belt],
        'potion': [T.potion_health, T.potion_mana_empty, T.potion_magic],
        'tool': [T.tool_tongs, T.tool_pickaxe, T.tool_broom],
        'magic': [T.magic_orb, T.weapon_stave, T.potion_stamina]
    }
    all_coord = []
    for item_class in type_items[shop_type]:
        while True:
            x = random.randint(1, w//2)
            y = 1
            if (x, y) not in all_coord:
                M[x, y].put(item_class())
                all_coord.append((x, y))
                break

    type_items = {
        'food': [T.furniture_box_filled, T.furniture_box_filled, T.bag, T.food_milk],
        'jewelry': [T.mineral_crystal, T.bag, T.necklace, T.ring],
        'clothe': [T.clothes_boots_right, T.clothes_shirt, T.clothes_shirt_inverted, T.clothes_sweater],
        'weapon':[T.weapon_sword, T.weapon_sword_saber, T.weapon_spear, T.weapon_dagger],
        'armor': [T.helmet, T.armor_mail, T.furniture_mannequin, T.shield_buckler],
        'potion': [T.potion_magic_empty, T.potion_stamina, T.dining_bottle, T.potion_health_empty],
        'tool': [T.tool_nails, T.tool_scissors, T.tool_fishingrod, T.tool_pitchfork],
        'magic': [T.weapon_stave, T.book_magic, T.scroll_magic, T.scroll_curled]
    }
    all_coord = []
    for item_class in type_items[shop_type]:
        while True:
            x = random.randint(w//2+1, w-2)
            y = random.randint(shop_counter_h+1, h-2)
            if (x, y) not in all_coord:
                M[x, y].put(item_class())
                all_coord.append((x, y))
                break
    cat_place_x = random.randint(1, 2)
    cat_place_y = random.randint(shop_counter_h+1, h-3)
    M[cat_place_x, cat_place_y].put(A.animal_cat())     

    return M

def room_storage(w, h, shop_type, wall_material, floor_material, shop_left):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    storage_part_h = h // 2
    for x in range(w):
        M[x, storage_part_h] = wall_material()
    M[w//2, storage_part_h] = C.door_closed_window()
    M[0, 1] = C.door_open_empty()
    
    all_coord = [(w//2, storage_part_h+1)]
    for item_class in (
            T.furniture_bed_single, 
            T.furniture_torch,
            T.furniture_chest_profile
            ):
        while True:
            x = random.randint(1, w-2)
            y = random.randint(storage_part_h+1, h-2)
            if (x, y) not in all_coord:
                M[x, y].put(item_class())
                all_coord.append((x, y))
                break

    type_items = {
        'food': [T.furniture_barrel, T.furniture_barrel, T.food_cheese, T.food_egg, T.food_pumpkin],
        'jewelry': [T.necklace, T.mineral_diamond, T.necklace_cross, T.material_ingot, T.ring],
        'clothe': [T.clothes_gloves_left, T.clothes_downjacket, T.clothes_hat, T.clothes_belt, T.clothes_overalls],
        'weapon': [T.weapon_sword, T.weapon_halberd, T.weapon_maul, T.weapon_sling, T.weapon_club],
        'armor': [T.clothes_shirt, T.armor_mail, T.helmet, T.shield, T.shield_tower],
        'potion': [T.dining_bottle, T.potion_health, T.potion_mana, T.potion_stamina, T.furniture_flowers_pot],
        'tool': [T.tool_wateringcan, T.tool_rake, T.tool_hoe, T.tool_saw, T.tool_fishingrod],
        'magic': [T.book_magic, T.weapon_stave, T.scroll_curled, T.scroll_magic, T.magic_orb]
    }
    all_coord = [(w//2, storage_part_h-1), (1,1)]
    for item_class in type_items[shop_type]:
        while True:
            x = random.randint(1, w-2)
            y = random.randint(1, storage_part_h-1)
            if (x, y) not in all_coord:
                M[x, y].put(item_class())
                all_coord.append((x, y))
                break
    return M
