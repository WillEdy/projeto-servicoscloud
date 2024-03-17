import io
from conexoes import connect_minio

def upload_to_minio(stream: io.StringIO, file_name, length: int):
    minio_conn = connect_minio()
    bucket_name = "fraudes-b"
    if minio_conn.bucket_exists(bucket_name):
        print(f"Bucket {bucket_name} já existe!")
    else:
        minio_conn.make_bucket(bucket_name)
        print("Bucket Criado")

    binaryIO = io.BytesIO(stream.getvalue().encode('utf-8'))
    minio_conn.put_object(bucket_name=bucket_name, object_name=file_name, data=binaryIO, length=length, content_type="text/plain")
    print(f"Arquivo {file_name} upado com sucesso")

    get_url = minio_conn.get_presigned_url(
        method='GET',
        bucket_name=bucket_name,
        object_name=file_name)
    print(f"Download URL: [GET]{get_url}")

def cria_relatorio_fraude(ac_number, t_anteriores, transaction):
    print("Relatorio de Fraude")
    file_stream = io.StringIO()
    file_stream.write("Numero da Conta: {}\n".format(ac_number))
    file_stream.write("Transacoes Anteriores: {}\n".format(t_anteriores))
    file_stream.write("Transacao Passivel de Fraude: {}\n".format(transaction))
    length = file_stream.write("Transacao Passivel de Fraude: {}\n".format(transaction))
    file_stream.seek(0)
    file_name = f"relatorio_fraude-{ac_number}.txt"
    upload_to_minio(file_stream, file_name, length)
    file_stream.close()