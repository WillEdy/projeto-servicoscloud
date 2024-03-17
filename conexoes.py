import pika
import redis
from minio import Minio

def connect_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host="localhost",
        port=5672,
        virtual_host="/"))
    channel = connection.channel()
    return channel

def connect_redis():
    return redis.Redis(host='localhost', port=6379, db=0)

def connect_minio():
    return Minio(
        endpoint="localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False)