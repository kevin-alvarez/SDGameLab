import os

from flask import Flask, request
from redis import Redis
from rq import Queue
from cache_redis import Cache
from actions import move, attack, insert_player
from time import sleep
from flask_cors import CORS
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
cors = CORS(app)
socketio = SocketIO(app)

"""
En caso de querer realizar pruebas sin necesidad de Docker, reemplazar las
siguientes variables por su correspondiente valor. Antes de iniciar la app,
asegurese de haber iniciado el servidor de Redis ($ redis-server).
"""
# QUEUE_HOST = rq-server | QUEUE_PORT = 6379
# CACHE_HOST = map-cache-server | CACHE_PORT = 6379
queue_conn = Redis(host=os.environ['QUEUE_HOST'],
                   port=os.environ['QUEUE_PORT'])
cache_conn = Redis(host=os.environ['CACHE_HOST'],
                   port=os.environ['CACHE_PORT'])

# BIND_PORT = 5000
bind_port = int(os.environ['BIND_PORT'])

"""
Las colas siguen el siguiente formato para ser instanciadas:

Queue(
  ## (podria usarse para identificar mapas 1...n)
  'nombre_de_la_cola'
  connection = <conexion_de_redis>  ## (variable asociada, en este caso)
)

- ejemplo -
-----------
# Al NO indicar un nombre, se asume como 'default'
q1 = Queue(connection=redis)
q2 = Queue('map1', connection=redis)
"""
q = Queue('actions', connection=queue_conn)
cache = Cache(connection=cache_conn)

# Map first instance for cache (tal vez se deba consulta primero el mapa)
default_map = {
    'id': '1234',
    'layout': [[0]*20]*20
}

cache.set('map_1', str(default_map))
cache.set('players', '0')

"""
La linea 48 podría producir inanicion, en el caso de que se trabaje con un unico worker
para una cola y la tarea que se este realizando, no haya finalizado aun.

Una "solucion" para evitar un caso posible, es simplemente asignar mas de 1 worker
a las colas que se posean. Otra alternativa la dejo comentada mas abajo.
"""
@app.route('/load-test')
def test():
    x = request.json['f']
    y = request.json['c']
    dir = request.json['dir']
    game_map = cache.get('map_1')
    job = q.enqueue(move, x, y, dir, game_map)
    while job.result == None:
        pass

    # Se guarda el mapa resultante en cache (existe condición de carrera para el caché)
    cache.set('map_1', job.result)
    # Para evitar condición de carrera se puede guardar la cantidad de acciones realizadas y luego comparar número al momento de entregar la respuesta, en caso de falla reprocesar con mapa nuevo (rollback)
    # numero_nuevo <= numero_cache -> mapa desactualizado
    return job.result

@app.route('/attack')
def attackQ():
    game_map = cache.get('map_1')
    job = q.enqueue(attack, game_map)
    while job.result == None:
        pass
    return job.result


@socketio.on('connect')
def connect():
    cache.incr('players')
    player_id = cache.get('players')
    game_map = cache.get('map_1')
    job = q.enqueue(insert_player, int(player_id), game_map)
    while job.result == None:
        pass
    cache.set('map_1', job.result[0])
    socketio.emit('map', eval(job.result[0]))
    socketio.emit('player', {'x': job.result[1], 'y': job.result[2], 'id': player_id})
    socketio.emit('message', 'Ha ingresado el jugador ' + player_id)


@socketio.on('disconnect')
def disconnect(message):
    socketio.emit('message', 'Se ha desconectado el jugador '+ message)


@socketio.on('move')
def message(data):
    x = data['f']
    y = data['c']
    dir = data['d']
    game_map = cache.get('map_1')
    job = q.enqueue(move, x, y, dir, game_map)
    while job.result == None:
        pass

    # Se guarda el mapa resultante en cache (existe condición de carrera para el caché)
    cache.set('map_1', job.result)
    # Para evitar condición de carrera se puede guardar la cantidad de acciones realizadas y luego comparar número al momento de entregar la respuesta, en caso de falla reprocesar con mapa nuevo (rollback)
    # numero_nuevo <= numero_cache -> mapa desactualizado
    socketio.emit('map', eval(job.result))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")


"""
Para instanciar un worker mediante la bash, colocar el siguiente comando:

$ rq worker <nombre_queue>

<nombre_queue>: Representan los nombres de las colas a la cuales estara atento
                el worker que se instancie. Para nombrar multiples colas, se
                deben separar por un espacio. ($ rq worker cola1 cola2 ...)
"""

"""
---------------------------------------------------------
Solucion alternativa (asumiendo una entrada de tipo JSON)
---------------------------------------------------------

from rq.job import Job

@app.route('/perform_action')
def perform_action(data):

  job = None
  action = data['action']

  if action == 'move':
    job = q_move.enqueue(move, data['x'], data['y'], data['direction'])

  elif action == 'attack:
    job = q_attack.enqueue(attack, data['attack_choosed'])

  return job.key

@app.route('/confirm_action')
def confirm_action(job_key):

  job = Job().fetch(job_key, connection=redis)

  if job.is_finished:
    return True

  return False
"""
