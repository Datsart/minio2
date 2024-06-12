import json
import re

file_path_list = []
dict_structure_ftp = {}  # словарь со структурой шаблона
ftp = {
    'Калужская область': {
        'regions': ['Калуга', 'Калужская область'],
        'source': ['full_objects', 'prices', 'deals'],
        'files_template': '2024-06-10'  # сюда пишем дату
    },
}
for main_area, second_param in ftp.items():
    for folder in second_param['source']:
        for town in second_param['regions']:
            for name_file in second_param['files_template']:
                file_path = f'{folder}/{main_area}/{town}/{name_file}'
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

FIND_FILE = ''
for area, name_list in ftp.items():
    if re.search(r'^\d{4}-\d{2}-\d{2}$', name_list['files_template']) is not None:
        FIND_FILE += name_list['files_template']
    else:
        print('Формат не соотвествует')
print(FIND_FILE)
