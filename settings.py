from minio import Minio


class Settings:
    ftp = {
        'Калужская область': {
            'regions': ['Калуга', 'Калужская область'],
            'source': ['full_objects', 'prices', 'deals'],
            'files_template': r'^\d{4}-\d{2}-\d{2}$',  # сюда пишем регулярку
        },
    }
    extension_template = {
        'full_objects': ['csv'],
        'prices': ['csv'],
        'deals': ['csv'],
    }
    client = Minio("play.min.io",
                   access_key="Q3AM3UQ867SPQQA43P2F",
                   secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
                   )
    bucket_name = "python-test-bucket"
    telegram_token = '6985148923:AAHwmhG0KogYrTRho9A6gWCtHTT30AsXGag'  # свой токен
    telegram_chat_id_list = ['1141944164']  # свой chat_id
