import datetime
import json
import pika
import os
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host="localhost",
     port=5672,
     virtual_host="/"))

channel = connection.channel()

properties = pika.BasicProperties(
     app_id="t-producer.py",
     content_type="application/json",
    )

trasaction_file = open("transaction.json")

transactions = json.load(trasaction_file)

trasaction_file.close()

for transaction in transactions:
    transaction["data"] = str(datetime.datetime.now())

    channel.basic_publish(exchange="amq.fanout",
                        routing_key="",
                        body=json.dumps(transaction),
                        properties=properties,
                        )
    print(f"[x] Sent '{json.dumps(transaction)}'")

    time.sleep(5)

channel.close()