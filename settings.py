from minio import Minio


class Settings:
    # расширения
    extension_template = {
        # 'full_objects': ['csv'],
        'prices': ['csv', 'xlsx'],
        # 'deals': ['csv', 'xlsx'],
    }
    # шаблон
    ftp = {
        'Калужская область': {
            'regions': ['Калуга', 'Калужская область'],
            'source': extension_template,
            'files_template': r'^\d{4}-\d{2}-\d{2}$',  # сюда пишем регулярку
        },
    }

    # настройка клиента
    client = Minio("play.min.io",
                   access_key="Q3AM3UQ867SPQQA43P2F",
                   secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
                   )

    # имя бакета
    bucket_name = "python-test-bucket"

    # свой телеграмм
    telegram_token = '6985148923:AAHwmhG0KogYrTRho9A6gWCtHTT30AsXGag'

    # список чатов id
    telegram_chat_id_list = ['1141944164']
