ftp = {
    'Калужская область': {
        'regions': ['Калуга', 'Калужская область'],
        'source': ['full_objects', 'prices', 'deals'],
        'files_template': ['yyyy-mm-dd.csv', 'yyyy-mm-dd.xlsx']
    },
    'target_file': '2024-06-10.csv',
}

for i, j in ftp.items():
    print(f'i: {i}\n j:{j}')
