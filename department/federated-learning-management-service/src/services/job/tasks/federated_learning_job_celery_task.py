import time

from clients.celery import celery

@celery.task
def start_federated_learning_celery_task():
    time.sleep(30)
    print("Start federated learning from service")
    return "done"