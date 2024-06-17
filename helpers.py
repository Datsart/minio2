from minio import Minio
import telebot
from settings import Settings


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


def find_folder():
    '''возвращает список иерархии папок из шаблона'''
    ftp = Settings.ftp
    main_area = list(ftp.keys())[0]
    list_regions = ftp[main_area]['regions']
    list_source = ftp[main_area]['source']
    list_folder_path = []
    for source in list_source:
        for region in list_regions:
            find_path_folder = f'{source}/{main_area}/{region}'
            list_folder_path.append(find_path_folder)
    return list_folder_path
