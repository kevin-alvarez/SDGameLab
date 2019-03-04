def move(x, y, dir, game_map):
  map_data = eval(game_map)
  layout = map_data['layout']
  x = int(x)
  y = int(y)
  if dir == '1':
    layout[x][y] = 0 # Character moved
    layout[x-1][y] = 1 # Character new position
  elif dir == '2':
    layout[x][y] = 0 
    layout[x+1][y] = 1 
  elif dir == '3':
    layout[x][y] = 0 
    layout[x][y+1] = 1 
  elif dir == '4':
    layout[x][y] = 0 
    layout[x][y-1] = 1
  map_data['layout'] = layout
  return str(map_data)

def attack(game_map):
  return f'the character attacked! - map = {game_map}'
