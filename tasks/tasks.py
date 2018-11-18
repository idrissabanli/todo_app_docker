from celery.task.schedules import crontab
from celery.decorators import periodic_task


@periodic_task(run_every=(crontab(minute='*/15')), name="some_task", ignore_result=True)
def some_task():
    print('salam')


some_task()


import redis

r = redis.Redis('redis')

def add(id, time):
	r.zadd('idtime', id, time)
    # r.lpush('users', id)
	return r.zrange('idtime', 0, -1)