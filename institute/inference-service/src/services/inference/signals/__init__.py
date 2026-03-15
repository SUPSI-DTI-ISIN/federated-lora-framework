from .inference_celery_signals import inference_celery_task_success_signal, inference_celery_task_failure_signal

__all__ = [
    'inference_celery_task_success_signal',
    'inference_celery_task_failure_signal'
]

__version__ = "1.0.0"