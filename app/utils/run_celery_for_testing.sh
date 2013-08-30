#!bin/sh
#Make sure RabbitMQ is also running
celery -A app.utils.celery_tests worker --loglevel=info
