import pika
import json
import io
from conexoes import connect_rabbitmq, connect_redis
from gera_relatorio import cria_relatorio_fraude

queue_name = "fraud-validator_queue"
first_uf = None

channel = connect_rabbitmq()
redis_conn = connect_redis()
channel.queue_declare(queue=queue_name)
channel.queue_bind(exchange="amq.fanout", queue=queue_name)

def chamado_quando_uma_transacao_eh_consumida(channel, method_frame, header_frame, body):
    global first_uf
    transaction = json.loads(body.decode('utf-8') )
    print("Transacao: ", transaction)
    ac_number = transaction['ac_number']
    uf_trans = transaction['uf']
    t_anteriores_result = redis_conn.get(ac_number)

    if t_anteriores_result is None:
        transactions = [transaction]
        redis_conn.set(ac_number, json.dumps(transactions))
    else:
        t_anteriores = json.loads(t_anteriores_result)
        t_anteriores.append(transaction)
        redis_conn.set(ac_number, json.dumps(t_anteriores))

    if first_uf is None:
        first_uf = uf_trans
    else:
        if uf_trans != first_uf:
            print("Alerta! Possível Fraude detectada")
            cria_relatorio_fraude(ac_number, t_anteriores, transaction)

channel.basic_consume(queue=queue_name, 
                      on_message_callback=chamado_quando_uma_transacao_eh_consumida, auto_ack=True)

print("Esperando por mensagens. Para sair pressione CTRL+C")
channel.start_consuming()