#Must be ini file, where we can add path main folder and path slave folder(s). We can add list of file extension
#Script make folder for result, and make txt file with name current date

import os
from datetime import datetime


def convert_date(timestamp):
    d = datetime.fromtimestamp (timestamp)
    formated_date = d.strftime('%d %b %Y, %H:%M:%S')
    return formated_date

dict_one = {}
dict_two = {}

with os.scandir('folder_one') as dir_contents:
    for entry in dir_contents:
        info = entry.stat()
        if entry.is_file():
            dict_one[entry.name] = (info.st_size,info.st_mtime)
            
        
with os.scandir('folder_two') as dir_contents:
    for entry in dir_contents:
        info = entry.stat()
        if entry.is_file():
            dict_two[entry.name] = (info.st_size,info.st_mtime)
            

def compareTuple(d1, d2):
    result = [0,0]
    #result = {FileName:[size result , time result]}
    for i in range(len(d1)):
        if d1[i]==d2[i]:
            result[i]=1#Same
        elif d1[i]>d2[i]:
            result[i]=2#d1 newer version
        else:
            result[i]=3#d2 newer version

    return tuple(result)

def compareDict(d1,d2):
    #result {FileName: [exist, size, time]}
    result = [0,0,0]
    outD = {}
    for k,v in d1.items():
        if k in d2.keys():
            result[0]=1
            res = compareTuple(v,d2.get(k))
            result[1:]=res
            outD[k]=result
            result = [0,0,0]
        else:
            outD[k] = [2,0,0]
            
    for k,v in d2.items():
        if k not in d1.keys():
            outD[k] = [3,0,0]
                
    return outD

def printResult(resultDict):
    for k,v in resultDict.items():
        if v[0] == 2:
            print(k, 'exist only path 1')
            continue
        elif v[0] == 3:
            print(k, 'exist only path 2')
            continue
        elif v[0]==1 and v[2]==2:
            print(k, 'exist in both folder but path 1 has newer timeStamp')
            continue
        elif v[0]==1 and v[2]==3:
            print(k, 'exist in both folder but path 2 has newer timeStamp')
            continue
        elif v[0]==1 and v[2]==1:
            print(k, 'exist in both folder and equal')
            continue
        
