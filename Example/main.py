# ！ /usr/bin/env python3
# -*- coding:utf-8 -*-

from datetime import datetime
import json


def isvaild(idnumber):
    if len(idnumber) != 18:
        return False
    alpha = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    cert = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    beta = []
    for a in range(17):
        beta.append(alpha[a] * int(idnumber[a]))
        theta = sum(beta) % 11
    return idnumber[-1] == cert[theta]


def getinfo(idnumber):
    try:
        birth = datetime.strptime(idnumber[6:14], '%Y%m%d')
        if (datetime.now() -
                birth.replace(year=datetime.now().year)).days >= 0:
            age = datetime.now().year - birth.year
        else:
            age = datetime.now().year - birth.year - 1

        if int(idnumber[-2]) % 2 == 0:
            sex = 'Female'
        else:
            sex = 'Male'

    except:
        age = 'Error'
        birth = 'Error'
        
    info = {
        'birth': birth.strftime('%Y/%m/%d'),
        'sex': sex,
        'age': age,
        'address': search_city(idnumber[:6])
    }
    return info


def search_city(code, path='./city_code.json'):
    try:
        f = open(path, encoding='utf-8')
    except FileNotFoundError:
        return 'Data not exist'
    city_code = json.loads(f.read())
    try:
        city = city_code[code]
    except KeyError:
        try:
            city = city_code[code[:4] + '00']
        except KeyError:
            try:
                city = city_code[code[:2] + '0000']
            except KeyError:
                city = 'Unknown'
    return city


if __name__ == '__main__':
    id = 1
    while id != 'n' and id != 'N':
        print('\n' * 100)
        print('Please input an id number:')
        id = str(input())
        if isvaild(id):
            info = getinfo(id)
            print('信息\n性别：%s\n出生日期：%s\n年龄：%i\n所属城市：%s' %
                  (info['sex'], info['birth'], info['age'], info['address']))
        else:
            print('您输入的身份证号码有误！')
        id = input('是否继续查询？[Y]/N ')
