import json

def read_data(namefield=None):
    with open('data.json', 'r+', encoding='utf-8') as f:
        if namefield != None:
            return json.load(f)[namefield]
        else:
            return json.load(f)

def update_data(namefield, namecolumn, value, newdata):
    
    if len(namecolumn) == 1:
        data = []
        for i in range(len(read_data(namefield))):
            if read_data(namefield)[i][namecolumn[0]] == value[0]:
                data.append(newdata)
            else:
                data.append(read_data(namefield)[i])
    else:
        data = []
        for i in range(len(read_data(namefield))):
            if read_data(namefield)[i][namecolumn[0]] == value[0] and read_data(namefield)[i][namecolumn[1]] == value[1]:
                data.append(newdata)
            else:
                data.append(read_data(namefield)[i])

    with open('data.json', 'r+', encoding='utf-8') as f:
        file = json.load(f)
        del file[namefield]
        file[namefield] = data
        json.dump(file, f.truncate(0).seek(0), ensure_ascii=False, indent=4)


def delete_data(namefield, namecolumn, value):

    if len(namecolumn) == 1:
        data = list(filter(lambda x: x[namecolumn[0]] != value[0], read_data(namefield)))
    else:
        data = []
        for i in range(len(read_data(namefield))):
            if read_data(namefield)[i][namecolumn[0]] == value[0] and read_data(namefield)[i][namecolumn[1]] == value[1]:
                pass
            else:
                data.append(read_data(namefield)[i])

    with open('data.json', 'r+', encoding='utf-8') as f:
        file = json.load(f)
        del file[namefield]
        file[namefield] = data
        json.dump(file, f.truncate(0).seek(0), indent=4)

def check_id(namefield, namecolumn, id):

    id_found = False
    for data in read_data(namefield):
        if data[namecolumn] == id:
            return True
    return id_found