import json
import re
from minio import Minio
import telebot

# шаблон
ftp = {
    'Калужская область': {
        'regions': ['Калуга', 'Калужская область'],
        'source': ['full_objects', 'prices', 'deals'],
        'files_template': re.search(r'^\d{4}-\d{2}-\d{2}$', '2024-06-10'),  # сюда пишем дату
    },
}
file_path_list = []  # список с путями файлов
dict_structure_ftp = {}  # словарь со структурой шаблона
for main_area, second_param in ftp.items():
    for folder in second_param['source']:
        for town in second_param['regions']:
            file_path = f'{folder}/{main_area}/{town}/{second_param['files_template'].string}'
            if file_path.endswith('.xlsx') is True and file_path.startswith('prices') is True:
                file_path_list.append(file_path)
            elif file_path.endswith('.csv') is True and file_path.startswith('prices') is False:
                file_path_list.append(file_path)
            splitting_list_name_file = file_path.split('/')
            source = splitting_list_name_file[0]
            region = splitting_list_name_file[1]
            subregion = splitting_list_name_file[2]
            file_name = splitting_list_name_file[3]

            if source not in dict_structure_ftp:
                dict_structure_ftp[source] = {}

            if region not in dict_structure_ftp[source]:
                dict_structure_ftp[source][region] = {}

            if subregion not in dict_structure_ftp[source][region]:
                dict_structure_ftp[source][region][subregion] = []

            dict_structure_ftp[source][region][subregion].append(file_name)
a = json.dumps(dict_structure_ftp, indent=2, ensure_ascii=False)


# print(a)
def find_file_func():
    '''возвращает строку искомого файла гггг-мм-дд'''
    FIND_FILE = ''
    for area, name_list in ftp.items():
        FIND_FILE += name_list['files_template'].string
    return FIND_FILE


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
    settings_dict = {}
    settings_dict['bot'] = telebot.TeleBot('6985148923:AAHwmhG0KogYrTRho9A6gWCtHTT30AsXGag')
    settings_dict['chat_id'] = '1141944164'
    return settings_dict
