def get_quils_data(get_new_data: bool, create_quils_data_file: bool):
    import csv
    import os
    import requests
    
    quils_data_exists = os.path.exists("quil's-data.csv")
    
    if get_new_data:
        response = requests.get('https://docs.google.com/spreadsheets/d/1ndHX9YF8Q8NgwQ_vhwcuoJpU9lrZ6MXm2pbNc6jpPAU/export?format=csv&gid=1553811417')
        response.raise_for_status()
        quils_data_csv_string = response.text.replace('\r','')
        
        with open("quil's-data.csv", 'w+') as file:
            file.write(quils_data_csv_string)
    
        with open("quil's-data.csv") as file:
            quils_data = list(csv.reader(file))
        
        # Fix incorrect name
        name_correction = {
            'LoveyDovey': 'Loveydovey',
            'PrickleFluff': 'Pricklefluff',
        }
        name_idx = quils_data[0].index('Dragon')
        for idx, row in enumerate(quils_data):
            name = row[name_idx]
            if name in name_correction.keys(): quils_data[idx][name_idx] = name_correction[name]
    else:
        with open("quil's-data.csv") as file:
            quils_data = list(csv.reader(file))
        
    if (not quils_data_exists) and (not create_quils_data_file):
        os.remove("quil's-data.csv")
        
    return quils_data

def get_quils_earning_data(quils_data, create_quils_earning_data_file: bool):
    import json
        
    name_idx = quils_data[0].index('Dragon')
    elder_idx = quils_data[0].index('Is Elder')
    earn_gold_idx = quils_data[0].index('Earn Gold')
    earn_etherium_idx = quils_data[0].index('Earn Etherium')
    earn_gems_idx = quils_data[0].index('Earn Gems')
    
    quils_earning_data = {}
    
    for row in quils_data[1:]:
        earning_dict = {}
        for title, earn_idx in [('Earn Gold', earn_gold_idx), ('Earn Etherium', earn_etherium_idx), ('Earn Gems', earn_gems_idx)]:
            if row[earn_idx] != '':
                earning_dict[title] = int(row[earn_idx])
        if earning_dict != {}:
            earning_dict['Is Elder'] = row[elder_idx] == '1'
            quils_earning_data[row[name_idx]] = earning_dict
    
    if create_quils_earning_data_file:
        # CONSIDER STORING THIS AS CSV TO SAVE ON FILE SIZE. IF SO, NEED TO CONVERT BACK TO NORMAL DATA STRUCTURES AFTER READING IT FROM LOCAL STORAGE
        with open("quil's-earning-data.json", 'w+') as file:
            json.dump(quils_earning_data, file, indent=4, separators=(',', ': '), sort_keys=True)

    return quils_earning_data