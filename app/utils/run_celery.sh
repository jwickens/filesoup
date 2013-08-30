#!bin/sh
#Make sure RabbitMQ is also running

celery -A app.tasks worker --loglevel=info
