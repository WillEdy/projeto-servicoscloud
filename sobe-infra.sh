#!/bin/bash

# Inicia RabbitMQ em segundo plano
docker run -d --rm -p 15672:15672 -p 5672:5672 rabbitmq:3-management
# Inicia Redis em segundo plano
docker run -d --rm --name redis -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
# Inicia MinIO em segundo plano
docker run -d  --rm --name minio --rm -p 9000:9000 -p 9001:9001 quay.io/minio/minio server /data --console-address ":9001"

# Instala dependencias

pip install pika

pip install redis

pip install minio

