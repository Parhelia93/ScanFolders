import os
from datetime import datetime

INI_FILE_NAME = 'ini_analyzeFile.txt'

def convert_date(timestamp):
    d = datetime.fromtimestamp (timestamp)
    formated_date = d.strftime('%d %b %Y, %H:%M:%S')
    return formated_date


def read_folder_files(folderPath, fileExtension):
    result = dict()
    extension = fileExtension.split(', ')
    try:
        with os.scandir(folderPath) as dir_contents:
            for entry in dir_contents:
                info = entry.stat()
                if entry.is_file():
                    for ex in extension:
                        if entry.name.endswith(ex):
                            result[entry.name] = (info.st_size,info.st_mtime)
        return result
    except FileNotFoundError:
        print('The system cannot find the path specified:', folderPath)
    except:
        print('General Problem with workin directory')          

       
def compare_tuple(tuple1, tuple2):
    same, d1_newer, d2_newer = 1, 2, 3
    result = [0,0] #Empty list
    for i in range(len(tuple1)):
        if tuple1[i]==tuple2[i]:
            result[i]=same
        elif tuple1[i]>tuple2[i]:
            result[i]=d1_newer
        else:
            result[i]=d2_newer
    return result

def compare_dict(d1,d2):
    #result {FileName: [exist, size, time]}
    exist, exist_path_one, exist_path_two = 1, 2, 3
    result_dict = dict()
    for key_d1,value_d1 in d1.items():
        result = [0,0,0] #Empty list
        if key_d1 in d2.keys():
            result[0]=exist
            res = compare_tuple(value_d1,d2.get(key_d1))
            result[1:]=res
            result_dict[key_d1]=result
        else:
            result_dict[key_d1] = [exist_path_one,0,0]
            
    for key_d2 in d2.keys():
        if key_d2 not in d1.keys():
            result_dict[key_d2] = [exist_path_two,0,0]           
    return result_dict


def read_ini_file(iniName):
    try:
        with open(iniName, encoding='utf-8') as file:
            s = file.readlines()
            result = dict()
            for i in s:
                key, value = i.split('=')
                result[key]=value.replace("\n","")
            return result
    except:
        print('Some problem with open ini file')

def parse_exist(value):
    exist, exist_path_one, exist_path_two = 1, 2, 3
    if value == exist:
        return 'exist in both folder'
    elif value == exist_path_one:
        return 'exist only in first folder'
    elif value == exist_path_two:
        return 'exist only in second folder'
    else:
        return ''

def parse_date(timestamp):
    same, d1_newer, d2_newer = 1, 2, 3
    if timestamp == same:
        return 'and timestamp equal'
    elif timestamp == d1_newer:
        return 'and timestamp from folder one has newer version'
    elif timestamp == d2_newer:
        'and timestamp from folder two has newer version'
    else:
        return ''


def write_result(result):
    date = datetime.now().strftime('%d %m %Y, %H:%M:%S')
    for key, value in result.items():
        exist, size, timestamp  = value
        res = f'{date} - {key} {parse_exist(exist)} {parse_date(timestamp)}\n'
        
        try:
            with open('result.txt','a') as file:
                file.write(res)
        except:
                print('Error work with file')

    try:
        with open('result.txt','a') as file:
            file.write('-------------------------------------\n')
    except:
                print('Error work with file')

if __name__ == '__main__':                
    ini_date = read_ini_file(INI_FILE_NAME)
    dict_one = read_folder_files(ini_date.get('folder_path_one'), ini_date.get('file_extension'))
    dict_two = read_folder_files(ini_date.get('folder_path_two'), ini_date.get('file_extension'))

    result = compare_dict(dict_one, dict_two)
    write_result(result)
