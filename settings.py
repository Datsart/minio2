import json
import re
from minio import Minio
import telebot


def return_ftp():
    """здесь указываем шаблон"""
    ftp = {
        'Калужская область': {
            'regions': ['Калуга', 'Калужская область'],
            'source': ['full_objects', 'prices', 'deals'],
            'files_template': r'^\d{4}-\d{2}-\d{2}$',  # сюда пишем регулярку
        },
    }
    return ftp


def formates_in_folders():
    '''указываем форматы файлов в паках'''
    extension_template = {
        'full_objects': ['csv'],
        'prices': ['csv'],
        'deals': ['csv'],
    }
    list_formates = []
    for i, j in extension_template.items():
        for k in j:
            list_formates.append(f'{i} {k}')
    return list_formates  # ['full_objects csv', 'prices csv', 'deals csv']


def client_connection():
    '''словарь с настройками бакета'''
    dict_info = {}
    # Создаем клиента для подключения к MinIO серверу с указанными ключами доступа
    client = Minio("play.min.io",
                   access_key="Q3AM3UQ867SPQQA43P2F",
                   secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
                   )
    bucket_name = "python-test-bucket"
    dict_info['client'] = client
    dict_info['bucket_name'] = bucket_name
    return dict_info


def telegram_settings():
    '''настройки телеграмм бота'''
    settings_dict = {}
    settings_dict['bot'] = telebot.TeleBot('6985148923:AAHwmhG0KogYrTRho9A6gWCtHTT30AsXGag')  # свой токен
    settings_dict['chat_id'] = ['1141944164']  # свой chat_id
    return settings_dict


def find_folder(ftp):
    '''возвращает список иерархии папок из шаблона'''
    main_area = list(ftp.keys())[0]
    list_regions = ftp[main_area]['regions']
    list_source = ftp[main_area]['source']
    list_folder_path = []
    for source in list_source:
        for region in list_regions:
            find_path_folder = f'{source}/{main_area}/{region}'
            list_folder_path.append(find_path_folder)
    return list_folder_path

# # для вывода струтктуры шаблона в консоли
# file_path_list = []  # список с путями файлов
# dict_structure_ftp = {}  # словарь со структурой шаблона
# for main_area, second_param in return_ftp().items():
#     for folder in second_param['source']:
#         for town in second_param['regions']:
#             file_path = f'{folder}/{main_area}/{town}/{second_param['files_template'].string}'
#             if file_path.endswith('.xlsx') is True and file_path.startswith('prices') is True:
#                 file_path_list.append(file_path)
#             elif file_path.endswith('.csv') is True and file_path.startswith('prices') is False:
#                 file_path_list.append(file_path)
#             splitting_list_name_file = file_path.split('/')
#             source = splitting_list_name_file[0]
#             region = splitting_list_name_file[1]
#             subregion = splitting_list_name_file[2]
#             file_name = splitting_list_name_file[3]
#
#             if source not in dict_structure_ftp:
#                 dict_structure_ftp[source] = {}
#
#             if region not in dict_structure_ftp[source]:
#                 dict_structure_ftp[source][region] = {}
#
#             if subregion not in dict_structure_ftp[source][region]:
#                 dict_structure_ftp[source][region][subregion] = []
#
#             dict_structure_ftp[source][region][subregion].append(file_name)
# a = json.dumps(dict_structure_ftp, indent=2, ensure_ascii=False)


# print(a)
def find_file_func():
    '''возвращает строку искомого файла гггг-мм-дд'''
    FIND_FILE = ''
    for area, name_list in return_ftp().items():
        FIND_FILE += name_list['files_template'].string
    print(FIND_FILE)
    return FIND_FILE
