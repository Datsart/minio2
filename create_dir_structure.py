import os

# Определяем структуру директорий и файлов
structure = {
    'deals': {
        'Калужская область': {
            'Калуга': ['2024-06-10.xlsx', 'file_n.csv'],
            'Калужская область': ['2024-06-10.xlsx', 'file_n.csv']
        },
        'Московская область': {
            'Москва': ['2024-06-10.xlsx', 'file_n.csv'],
            'Московская область': ['2024-06-10.xlsx', 'file_n.csv']
        }
    },
    'full_objects': {
        'Калужская область': {
            'Калуга': ['2024-06-10.xlsx', 'file_n.csv'],
            'Калужская область': ['2024-06-10.xlsx', 'file_n.csv']
        },
        'Московская область': {
            'Москва': ['2024-06-10.xlsx', 'file_n.csv'],
            'Московская область': ['2024-06-10.xlsx', 'file_n.csv']
        }
    },
    'analytics': {
        'Калужская область': {
            'Калуга': ['2024-06-10.xlsx', 'file_n.csv'],
            'Калужская область': ['2024-06-10.xlsx', 'file_n.csv']
        },
        'Московская область': {
            'Москва': ['2024-06-10.xlsx', 'file_n.csv'],
            'Московская область': ['2024-06-10.xlsx', 'file_n.csv']
        }
    },
    'prices': {
        'Калужская область': {
            'Калуга': ['2024-06-10.xlsx', 'file_n.csv'],
            'Калужская область': ['2024-06-10.xlsx', 'file_n.csv']
        },
        'Московская область': {
            'Москва': ['2024-06-10.xlsx', 'file_n.csv'],
            'Московская область': ['2024-06-10.xlsx', 'file_n.csv']
        }
    },
}


# Функция для создания структуры директорий и файлов
def create_structure(base_path, structure):
    for folder, subfolders in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        for subfolder, regions in subfolders.items():
            subfolder_path = os.path.join(folder_path, subfolder)
            os.makedirs(subfolder_path, exist_ok=True)

            for region, files in regions.items():
                region_path = os.path.join(subfolder_path, region)
                os.makedirs(region_path, exist_ok=True)

                for file in files:
                    file_path = os.path.join(region_path, file)
                    with open(file_path, 'w') as f:
                        pass  # Создаем пустой файл


if __name__ == "__main__":
    # Путь к базовой директории (например, рабочая директория проекта)
    base_path = "./test_dir"

    # Создаем структуру директорий и файлов
    create_structure(base_path, structure)
    print(f"Структура директорий и файлов создана в {base_path}")
