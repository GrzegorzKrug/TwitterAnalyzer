from celery import Celery
from celery.concurrency.prefork import TaskPool
from celery.worker.autoscale import Autoscaler
import time
import os

user = os.getenv('LOGIN', 'admin')
password = os.getenv('PASSWORD', 'mypass')
hostname = os.getenv('HOSTNAME', 'localhost')

broker_url = f'amqp://{user}:{password}@{hostname}:5672/'
app = Celery('tasks', broker=broker_url)


# app.conf.worker_pool = TaskPool
# app.control.p
# app.control.worker_max_tasks_per_child = 10
# app.conf.worker_autoscaler = Autoscaler(None, min_concurrency=3, max_concurrency=10)


@app.task
def show():
    print("Hello celery 15")
    for x in range(15):
        print(15 - x)
        time.sleep(1)
    print("Bye celery")


if __name__ == "__main__":
    # app.control.autoscale(10, 4)
    # app.conf.autoscale(40)
    app.worker_main()
