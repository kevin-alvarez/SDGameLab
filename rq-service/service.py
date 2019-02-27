import os

from flask import Flask
from redis import Redis
from rq import Queue
from actions import move, attack
from time import sleep

app = Flask(__name__)

"""
En caso de querer realizar pruebas sin necesidad de Docker, reemplazar las
siguientes variables por su correspondiente valor. Antes de iniciar la app,
asegurese de haber iniciado el servidor de Redis ($ redis-server).
"""
# REDIS_HOST = localhost | REDIS_PORT = 6379
redis = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])

# BIND_PORT = 5000
bind_port = int(os.environ['BIND_PORT'])

"""
Las colas siguen el siguiente formato para ser instanciadas:

Queue(
  'nombre_de_la_cola'               ## (podria usarse para identificar mapas 1...n)
  connection = <conexion_de_redis>  ## (variable asociada, en este caso)
)

- ejemplo -
-----------
q1 = Queue(connection=redis)          # Al NO indicar un nombre, se asume como 'default'
q2 = Queue('map1', connection=redis)
"""
q = Queue('actions', connection=redis)


"""
La linea 48 podría producir inanicion, en el caso de que se trabaje con un unico worker
para una cola y la tarea que se este realizando, no haya finalizado aun.

Una "solucion" para evitar un caso posible, es simplemente asignar mas de 1 worker
a las colas que se posean. Otra alternativa la dejo comentada mas abajo.
"""
@app.route('/move')
def moveQ():
  job = q.enqueue(move)
  while job.result == None: pass  # Espera hasta obtener un resultado
  return job.result

@app.route('/attack')
def attackQ():
  job = q.enqueue(attack)
  while job.result == None: pass
  return job.result

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True, port=bind_port)


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