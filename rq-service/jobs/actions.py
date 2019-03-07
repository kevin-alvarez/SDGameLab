from random import randint


def move(x, y, dir, game_map):
    map_data = eval(game_map)
    layout = map_data['layout']
    x = int(x)
    y = int(y)
    dir = int(dir)
    player_id = int(layout[x][y])

    # Borde superior del mapa
    if (x == 0):

        # Borde izquierdo del mapa
        if (y == 0) and (dir in [3, 1]):
            return str(map_data)

        # Borde derecho del mapa
        elif (y == 19) and (dir in [3, 2]):
            return str(map_data)

    # Borde inferior del mapa
    if (x == 19):
        # Borde izquierdo del mapa
        if (y == 0) and (dir in [4, 1]):
            return str(map_data)

        # Borde derecho del mapa
        elif (y == 19) and (dir in [4, 2]):
            return str(map_data)

    # if (x - 1 < 0) or (y - 1 < 0) or (x + 1 > 19) or (y + 1 > 19):
    #     return str(map_data)

    if dir == 1:
        layout[x][y] = 0  # Character moved
        layout[x][y-1] = player_id  # Character new position
    elif dir == 2:
        layout[x][y] = 0
        layout[x][y+1] = player_id
    elif dir == 3:
        layout[x][y] = 0
        layout[x-1][y] = player_id
    elif dir == 4:
        layout[x][y] = 0
        layout[x+1][y] = player_id
    map_data['layout'] = layout
    return str(map_data)


def insert_player(player_id, game_map):
    map_data = eval(game_map)
    layout = map_data['layout']
    while True:
        x = randint(0, 19)
        y = randint(0, 19)
        safe = True
        for i in range(-1, 1):
            if not safe:
                break
            for j in range(-1, 1):
                if (x + i < 0) or (y + j < 0) or (x + i > 19) or (y + j > 19):
                    safe = False
                    break

        layout[x][y] = player_id
        break
    map_data['layout'] = layout
    return str(map_data), x, y


def attack(game_map):
    return f'the character attacked! - map = {game_map}'
