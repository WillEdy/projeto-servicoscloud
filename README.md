O sistema verifica se alguma transação seguida foi realizada em alguma outra unidade federativa(estado) a partir da última unidade utilizada.

Use o comando bash no arquivo sobe-infra.sh para subir os containers e instalar dependencias. "bash sobe-infra.sh"

Após isso o usar o comando python para ativar o consumer "python consumer-validador.py"

Usar o comando python para ativar o producer "python t-producer.py"

As transções do producer estão no arquivo transaction.json. 

O arquivo/link com número da conta passível de fraude vai estar disponível para download no minio e no console.
