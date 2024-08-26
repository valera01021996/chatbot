# import boto3
# from io import BytesIO
# from minio import Minio
# from minio.error import S3Error
#
# minio_endpoint = '10.10.0.210:9000'
# minio_access_key = 'ecwncAPfrmjJA2LkY08Z'
# minio_secret_key = '7BNs8tnBD9G8FmpXS9nbD0dcV1Wp2qELRGiOljtY'
# minio_bucket = 'diags'
#
# minio_client = boto3.client(
#     's3',
#     endpoint_url=f'http://{minio_endpoint}',
#     aws_access_key_id=minio_access_key,
#     aws_secret_access_key=minio_secret_key
# )
#
# with open("test", 'rb') as file:
#     file_data = file.read()
# # Отправка файла на Minio
# file_name = 'uploaded_file.txt'  # Имя файла на Minio
# minio_client.put_object(
#     Bucket=minio_bucket,
#     Key=file_name,
#     Body=BytesIO(file_data)
# )
#
# print(f"Файл {file_name} успешно загружен на Minio сервер в bucket '{minio_bucket}'.")
from minio import Minio
from minio.error import S3Error
from datetime import timedelta


expiration = timedelta(hours=1)
# Подключение к Minio
minio_client = Minio(
    "10.10.0.210:9000",
    access_key="ecwncAPfrmjJA2LkY08Z",
    secret_key="7BNs8tnBD9G8FmpXS9nbD0dcV1Wp2qELRGiOljtY",
    secure=False  # Установите True, если используете HTTPS
)

# Загрузка файла
bucket_name = "diags"
object_name = "my-file.txt"
file_path = "test"

try:
    minio_client.fput_object(bucket_name, object_name, file_path)
    print(f"'{file_path}' is successfully uploaded as '{object_name}' to bucket '{bucket_name}'.")

    # Генерация ссылки на скачивание (срок действия ссылки 1 час)
    url = minio_client.presigned_get_object(bucket_name, object_name, expires=expiration)
    print("Download link:", url)

except S3Error as exc:
    print("Error occurred:", exc)
