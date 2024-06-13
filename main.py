import json
from settings import find_file_func, client_connection, telegram_settings


def main():
    client = client_connection()['client']
    bucket_name = client_connection()['bucket_name']
    objects = client.list_objects(bucket_name, recursive=True)
    list_error = []
    # Список всех объектов в бакете
    print('Все файлы, найденные в бакете:\n')
    dict_structure_bucket = {}  # словарь со структурой бакета

    find_file_xlsx = find_file_func() + '.xlsx'
    for obj in objects:
        name_file = obj.object_name
        date = client.stat_object(bucket_name, name_file).last_modified

        # вывод  имен файлов и дата их последнего изменения
        print(name_file)
        print(f'date_modification: {date}\n')
        if find_file_xlsx in name_file and 'prices' not in name_file:  # проверка на нахождение файла xlsx по папкам:
            list_split_name = name_file.split('/')
            print(list_split_name)
            foler = list_split_name[0]
            list_error.append(f'{find_file_xlsx} - в папке: {foler} - не верно')
        elif find_file_func() not in name_file:  # проверка файлов по шаблону во всех папках
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

    a = json.dumps(dict_structure_bucket, indent=2, ensure_ascii=False)
    # print(a)

    find_file_csv = find_file_func() + '.csv'
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


def send_errors(chat_id, list_error):
    # Формирование сообщения
    errors_message = '\nОшибки:\n'
    for error in list_error:
        errors_message += f"{error}\n"
    chat_id = telegram_settings()['chat_id']
    telegram_settings()['bot'].send_message(chat_id, errors_message)


if __name__ == "__main__":
    list_error = main()
    settings = telegram_settings()
    send_errors(settings['chat_id'], list_error)
