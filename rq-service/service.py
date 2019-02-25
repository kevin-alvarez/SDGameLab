import os

from flask import Flask
from redis import Redis
from rq import Queue
from actions import move, attack
from time import sleep

app = Flask(__name__)
redis = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])
bind_port = int(os.environ['BIND_PORT'])
q = Queue('actions', connection=redis)

@app.route('/move')
def moveQ():
  job = q.enqueue(move)
  while job.result == None: pass
  return job.result

@app.route('/attack')
def attackQ():
  job = q.enqueue(attack)
  while job.result == None: pass
  return job.result
  
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True, port=bind_port)
