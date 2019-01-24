from redis_queue.rq_conn import get, put
import time

put('move_fwd')
put('move_bwd')
put('move_right')
put('move_left')

time.sleep(2)

print(get())
print(get())
print(get())
print(get())
