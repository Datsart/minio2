from minio import Minio
import telebot
import json
from app2 import FIND_FILE


def main():
    # Создаем клиента для подключения к MinIO серверу с указанными ключами доступа
    client = Minio("play.min.io",
                   access_key="Q3AM3UQ867SPQQA43P2F",
                   secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
                   )

    # Название бакета
    bucket_name = "python-test-bucket"

    # Список всех объектов в бакете
    objects = client.list_objects(bucket_name, recursive=True)
    list_error = []

    print('Все файлы, найденные в бакете:\n')
    dict_structure_bucket = {}  # словарь со структурой бакета

    find_file_xlsx = FIND_FILE + '.xlsx'
    for obj in objects:
        name_file = obj.object_name
        date = client.stat_object(bucket_name, name_file).last_modified
        print(name_file)
        print(f'date_modification: {date}\n')
        if find_file_xlsx in name_file and 'prices' not in name_file:  # проверка на нахождение файла xlsx по папкам:
            list_split_name = name_file.split('/')
            foler = list_split_name[0]
            list_error.append(f'{find_file_xlsx} - в папке: {foler} - не верно')
        elif FIND_FILE not in name_file:  # проверка файлов по шаблону во всех папках
            list_split_name = name_file.split('/')
            list_error.append(
                f"Файл - {list_split_name[-1]} - не валидный в папке - {list_split_name[0]} - {list_split_name[1]} - {list_split_name[2]}")
        # создание словаря со структурой папок и файлов ИЗ БАКЕТА
        splitting_list_name_file = name_file.split('/')
        source = splitting_list_name_file[0]
        region = splitting_list_name_file[1]
        subregion = splitting_list_name_file[2]
        file_name = splitting_list_name_file[3]

        if source not in dict_structure_bucket:
            dict_structure_bucket[source] = {}

        if region not in dict_structure_bucket[source]:
            dict_structure_bucket[source][region] = {}

        if subregion not in dict_structure_bucket[source][region]:
            dict_structure_bucket[source][region][subregion] = []

        dict_structure_bucket[source][region][subregion].append(file_name)

    # print(dict_structure_bucket)
    a = json.dumps(dict_structure_bucket, indent=2, ensure_ascii=False)
    # print(a)
    find_file_csv = FIND_FILE + '.csv'
    if find_file_csv.endswith('.csv') is True:  # берем только csv файлы; проверка на нахождение csv в папках
        for one, two in dict_structure_bucket.items():
            for three, four in two.items():
                for i, j in four.items():
                    if find_file_csv not in j:
                        list_error.append(f'{find_file_csv} - нету в {one} - {three} - {i}')
    print('\nОшибки:\n')
    for i in list_error:
        print(i)

    return list_error


bot = telebot.TeleBot('6985148923:AAHwmhG0KogYrTRho9A6gWCtHTT30AsXGag')

chat_id = '1141944164'


def send_errors(chat_id, list_error):
    # Формирование сообщения
    errors_message = '\nОшибки:\n'
    for error in list_error:
        errors_message += f"{error}\n"
    bot.send_message(chat_id, errors_message)


if __name__ == "__main__":
    list_error = main()
    send_errors(chat_id, list_error)
