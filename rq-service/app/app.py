import os

from flask import Flask
from redis import Redis
from rq import Queue
from works import sumNums
from time import sleep

app = Flask(__name__)
redis = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])
bind_port = int(os.environ['BIND_PORT'])
q = Queue('low', connection=redis)

@app.route('/')
def go2Queue():
  job = q.enqueue(sumNums, 5)
  sleep(5)
  return str(job.result)
  
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True, port=bind_port)
