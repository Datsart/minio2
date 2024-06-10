from minio import Minio

# Инициализация клиента Minio
client = Minio(
    "play.min.io",
    access_key="Q3AM3UQ867SPQQA43P2F",
    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
)

# Название бакета
bucket_name = "python-test-bucket"

# Получение списка всех объектов в бакете
objects = client.list_objects(bucket_name, recursive=True)

# Удаление каждого объекта
for obj in objects:
    client.remove_object(bucket_name, obj.object_name)
    print(f"Удален объект: {obj.object_name}")

print(f"Бакет {bucket_name} очищен.")
