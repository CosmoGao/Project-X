# ！ /usr/bin/env python3
# -*- coding:utf-8 -*-


import pandas as pd
import main
from datetime import datetime

global filetype

def read_file(filename):
    filetype = filename.split('.')[-1]
    if filetype == 'xlsx':
        df = pd.read_excel(filename)
    elif filetype == 'csv':
        df = pd.read_csv(filename)
    else:
        print('不支持的文件类型!')
    return df


def get_sex(idnumber):
    if int(idnumber[-2]) % 2 == 0:
        sex = 'Female'
    else:
        sex = 'Male'
    return sex


def get_birth(idnumber):
    birth = idnumber[6:10] + '/' + idnumber[10:12] + '/' + idnumber[12:14]
    return birth


def get_age(idnumber):
    try:
        birth = datetime.strptime(idnumber[6:14], '%Y%m%d')
        if (datetime.now() - birth.replace(year=datetime.now().year)).days >= 0:
            age = datetime.now().year - birth.year
        else:
            age = datetime.now().year - birth.year - 1
    except:
        age = 'Wrong date!'
    return age


def trans(df):
    df['身份证号'] = df['身份证号'].apply(str)
    df['有效'] = df['身份证号'].apply(main.isvaild)
    df['性别'] = df['身份证号'].apply(lambda x:main.getinfo(x)['sex'])
    df['出生日期']= df['身份证号'].apply(lambda x:main.getinfo(x)['birth'])
    df['年龄']= df['身份证号'].apply(lambda x:main.getinfo(x)['age'])
    df['所属城市'] = df['身份证号'].apply(main.search_city)
    return df


def write_file(df, newfile):
    filetype = newfile.split('.')[-1]
    if filetype == 'xlsx':
        df.to_excel('./' + newfile, index = False)
    elif filetype == 'csv':
        df.to_csv('./' + newfile, index = False, encoding = 'gbk')
    else:
        print('不支持的文件类型!')
    return None

def run(filename):
    df =read_file(filename)
    trans(df)
    write_file(df, 'o_'+filename.split('/')[-1])
