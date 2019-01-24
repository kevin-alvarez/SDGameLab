from redis import Redis
from rq import Queue
from collections import deque
from .worker_jobs import process_action

redis_conn = Redis('localhost', '6379', 0)
q = Queue('actions', connection=redis_conn)
jobs = deque([])

def get():
  current_job = jobs.popleft()
  if current_job:
    return current_job.result
  else:
    jobs.append(current_job)

def put(action):
  jobs.append(q.enqueue(process_action, action))
