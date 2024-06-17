import json
from helpers import formates_in_folders, find_folder
from settings import Settings
import re
import telebot


def main():
    client = Settings.client
    bucket_name = Settings.bucket_name
    objects = list(client.list_objects(bucket_name, recursive=True))  # Преобразуем в список сразу
    list_error = []
    list_path_only_folders = []  # список одних путей в бакете (без названий файлов)
    list_full_path_name = []  # список полныйх путей файлов в бакете (с названиями файлов)
    dict_structure_bucket = {}  # словарь со структурой бакета
    list_names_file = []
    pattern = [j for i, j in Settings.ftp.items()][0]['files_template']  # r'^\d{4}-\d{2}-\d{2}$'

    print('Все файлы, найденные в бакете:\n')

    # взяли все файлы, отобрали только те что проходят регулярку (уникальные файлы)
    for i in objects:
        name_file = i.object_name
        list_full_path_name.append(name_file)
        splitting_list_name_file = name_file.split('/')  # deals/Калужская область/Калуга/2024-06-10.csv
        if re.search(pattern, splitting_list_name_file[-1].split('.')[-2]) is not None:
            list_names_file.append(splitting_list_name_file[-1])
        else:
            list_error.append(f"{name_file} - не валидный")
    set_names_file = list(set(list_names_file))

    # проход по всем файлам
    for obj in objects:
        name_file = obj.object_name
        date = client.stat_object(bucket_name, name_file).last_modified
        splitting_list_name_file = name_file.split('/')  # deals/Калужская область/Калуга/2024-06-10.csv
        yyyy_mm_dd = splitting_list_name_file[-1].split('.')[-2]  # 2020-05-01

        print(name_file)

        # проверка на соответсвие расширений в папках
        if f'{splitting_list_name_file[0]} {splitting_list_name_file[-1].split(".")[-1]}' not in formates_in_folders():
            list_error.append(
                f'неверный формат файла {splitting_list_name_file[-1]} в - {splitting_list_name_file[0]} - {splitting_list_name_file[1]} - {splitting_list_name_file[2]}')

        # вывод  имен файлов и дата их последнего изменения
        print(f'date_modification: {date}\n')

        # проверка на нахождение файла xlsx по папкам:
        # берем только файлы проходящие проверку по паттерну из шаблона:
        if re.match(pattern, yyyy_mm_dd) is not None:
            find_file_xlsx = yyyy_mm_dd + '.xlsx'
            if find_file_xlsx in name_file and 'prices' not in name_file:
                foler = splitting_list_name_file[0]
                list_error.append(f'{find_file_xlsx} - в папке: {foler} - не верно')

        # проверка файлов по шаблону во всех папках; берем только csv файлы соответсвующие паттерну из шаблона
        elif re.match(pattern, yyyy_mm_dd) is not None:
            find_file_csv = yyyy_mm_dd + '.csv'
            if find_file_csv not in name_file:
                list_error.append(
                    f"Файл - {splitting_list_name_file[-1]} - не валидный в папке - {splitting_list_name_file[0]} - {splitting_list_name_file[1]} - {splitting_list_name_file[2]}")
        else:
            list_error.append(f'{splitting_list_name_file[-1]} - не соответсвует паттерну из шаблона')

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

    # проверка сущестования папок из шаблона в бакете
    for i in find_folder():
        if i not in list_path_only_folders:
            list_error.append(f'Иерархия {i} - нарушена в бакете')

    # проверка csv и xlsx файлов по папкам на сущесвтование
    for name in set_names_file:
        if name.endswith('.csv') or name.endswith('.xlsx'):
            for one, two in dict_structure_bucket.items():
                # проверка для xlsx файлов на нахождение только в 'prices'
                if name.endswith('.xlsx') and one != 'prices':
                    continue
                for three, four in two.items():
                    for i, j in four.items():
                        if name not in j:
                            list_error.append(f'{name} - нету в {one} - {three} - {i}')

    # преобразование списка во сножество и сортировка для корректного вывода
    set_error = set(list_error)
    sotred_set_errors = sorted(set_error)
    print('\nОшибки:\n')
    for i in sotred_set_errors:
        print(i)

    return sotred_set_errors


def send_errors(chat_id):
    # Формирование сообщения
    errors_message = '\nОшибки:\n'
    for error in list_error:
        errors_message += f"{error}\n"
    chat_id = Settings.telegram_chat_id_list
    bot = telebot.TeleBot(Settings.telegram_token)
    for i in chat_id:
        bot.send_message(i, errors_message)


if __name__ == "__main__":
    list_error = main()
    for id in Settings.telegram_chat_id_list:
        send_errors(id)
