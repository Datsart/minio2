from settings import Settings


def formates_in_folders():
    '''указываем форматы файлов в паках'''
    list_formates = []
    for i, j in Settings.extension_template.items():
        for k in j:
            list_formates.append(f'{i} {k}')
    return list_formates  # ['full_objects csv', 'prices csv', 'deals csv']


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
