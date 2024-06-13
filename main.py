import json
from settings import find_file_func, client_connection, telegram_settings, find_folder, return_ftp, formates_in_folders


def main():
    client = client_connection()['client']
    bucket_name = client_connection()['bucket_name']
    objects = client.list_objects(bucket_name, recursive=True)
    list_error = []
    list_path_only_folders = []  # список одних путей в бакете (без названий файлов)
    dict_structure_bucket = {}  # словарь со структурой бакета

    print('Все файлы, найденные в бакете:\n')

    find_file_xlsx = find_file_func() + '.xlsx'
    for obj in objects:
        name_file = obj.object_name
        date = client.stat_object(bucket_name, name_file).last_modified
        splitting_list_name_file = name_file.split('/')

        print(name_file)

        # проверка на соответсвие расширений в папках
        if f'{splitting_list_name_file[0]} {splitting_list_name_file[-1].split('.')[-1]}' not in formates_in_folders():
            list_error.append(
                f'не верный формат файла в - {splitting_list_name_file[0]} - {splitting_list_name_file[1]} - {splitting_list_name_file[2]}')

        # вывод  имен файлов и дата их последнего изменения
        print(f'date_modification: {date}\n')

        # проверка на нахождение файла xlsx по папкам:
        if find_file_xlsx in name_file and 'prices' not in name_file:
            list_split_name = name_file.split('/')
            foler = list_split_name[0]
            list_error.append(f'{find_file_xlsx} - в папке: {foler} - не верно')

        # проверка файлов по шаблону во всех папках
        elif find_file_func() not in name_file:
            list_split_name = name_file.split('/')
            list_error.append(
                f"Файл - {list_split_name[-1]} - не валидный в папке - {list_split_name[0]} - {list_split_name[1]} - {list_split_name[2]}")

        # создание словаря со структурой папок и файлов ИЗ БАКЕТА

        list_path_only_folders.append(
            '/'.join(splitting_list_name_file[:-1]))  # добавление путей файлов в список (без самих файлов)

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

    # проверка сущестования папок из шаблона в бакете
    for i in find_folder(return_ftp()):
        if i not in list_path_only_folders:
            list_error.append(f'Иерархия {i} - нарушена в бакете')

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
    for id in settings['chat_id']:
        send_errors(id, list_error)
