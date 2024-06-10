import os
from minio import Minio


def upload_files(client, bucket_name, source_folder):
    '''для загрузки файлов в бакет'''
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)  # Полный путь к файлу
            object_name = os.path.relpath(file_path, source_folder)  # Относительный путь для объекта в бакете
            client.fput_object(bucket_name, object_name, file_path)  # Загрузка файла в бакет
            print(f"Загружен {file_path} как {object_name} в бакет {bucket_name}")


if __name__ == "__main__":
    # Создаем клиента для подключения к MinIO серверу с указанными ключами доступа
    client = Minio("play.min.io",
                   access_key="Q3AM3UQ867SPQQA43P2F",
                   secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
                   secure=True)

    # Папка для загрузки
    source_folder = "./test_dir"

    # Название бакета
    bucket_name = "python-test-bucket"

    # Проверяем, существует ли бакет, если нет, то создаем
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print(f"Бакет {bucket_name} создан")
    else:
        print(f"Бакет {bucket_name} уже существует")

    # Загружаем файлы в бакет
    upload_files(client, bucket_name, source_folder)
