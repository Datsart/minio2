from minio import Minio
from minio.error import S3Error
import telebot


def main():
    # Создаем клиента для подключения к MinIO серверу с указанными ключами доступа
    client = Minio("play.min.io",
                   access_key="Q3AM3UQ867SPQQA43P2F",
                   secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
                   )

    # Название бакета
    bucket_name = "python-test-bucket"

    # Список всех объектов в бакете
    print('Все файлы:\n')
    print(f"Объекты в бакете '{bucket_name}':\n")
    objects = client.list_objects(bucket_name, recursive=True)
    LIST_ERROR = []
    find_time = '2024-06-10'  # дата по которой ищем загрузки
    # find_file = '2024-06-10.csv'  # файл который будем искать во всех папках, здесь можно строку закоментить

    counter = 0
    for obj in objects:
        name_file = obj.object_name
        date = client.stat_object(bucket_name, name_file).last_modified
        print(name_file)
        print(f'date_modification: {date}\n')
        cut_date_load_file = date.strftime('%Y-%m-%d')[:10]
        if name_file.endswith('.csv'):  # проверка на csv
            cut_date_from_name_file = name_file[-14:-4]
            if not name_file.endswith('file_n.csv'):  # не берем файлы file_n.csv
                if cut_date_load_file != cut_date_from_name_file:  # проверка на дату загрузки и дату в имени
                    LIST_ERROR.append(f'{name_file} - дата загрузки и дата имени не совпадают')
        else:
            LIST_ERROR.append(f'{name_file} - ошибка формата - не csv')
        if name_file.startswith('prices') and not name_file.endswith('.xlsx'):
            LIST_ERROR.append(f'{name_file} - в prices не xlsx')
        if find_time != cut_date_load_file and counter == 0:  # проверка на загрузку данных по указанной дате
            LIST_ERROR.append('Данных нет по указанной дате')
        counter += 1

        # 4ое задание пошло отсюда
        file_path_list = name_file.split('/')  # разбили на список имен папок и файлов
        file_path1 = '/'.join(file_path_list[:-1])  # склеили путь обратно без последнего искомого файла
        try:
            file_path = f'{file_path1}/{find_file}'  # полный путь до искомого файла
            try:
                client.stat_object(bucket_name, file_path)
            except S3Error as err:
                if err.code == "NoSuchKey" and f'{file_path} - не во всех папках' not in LIST_ERROR:  # чтобы запись оишбок не повторялась
                    LIST_ERROR.append(f'{file_path} - не во всех папках')
                else:
                    pass
        except BaseException:
            pass

    print('\nОшибки:\n')
    for i in LIST_ERROR:
        print(i)

    return LIST_ERROR


# Инициализация бота с вашим токеном
bot = telebot.TeleBot('6985148923:AAHwmhG0KogYrTRho9A6gWCtHTT30AsXGag')

# Замените 'YOUR_CHAT_ID' на реальный chat_id, полученный ранее
chat_id = '1141944164'


def send_errors(chat_id, list_error):
    # Формирование сообщения
    errors_message = '\nОшибки:\n'
    for error in list_error:
        errors_message += f"{error}\n"

    # Отправка сообщения
    bot.send_message(chat_id, errors_message)


if __name__ == "__main__":
    list_error = main()
    send_errors(chat_id, list_error)
