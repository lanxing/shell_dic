#! /usr/bin/env python3.5

import hashlib
import random
import requests
import re
from peewee import *

db = MySQLDatabase('mydb', user='root')
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')


# 基础类
class BaseModel(Model):
    class Meta:
        database = db


# 自定义词典
class MyDic(BaseModel):
    key = CharField(max_length=256)
    value = CharField(max_length=2048)
    times = BigIntegerField(default=1)


def getMd5(src):
    md5 = hashlib.md5()
    md5.update(src.encode(encoding='utf8'))
    return md5.hexdigest()


def containChinese(contents):
    match = zhPattern.search(contents)
    if match:
        return True
    return False


def createTable(table):
    db.connect()
    db.create_table(table)


def showInfo(json):
    basic = json.get('basic')
    if basic is not None:
        print('**************************基本词意*******************')
        if basic.get('phonetic') is not None:
            print('读音:' + basic.get('phonetic') + '\n')
        if basic.get('explains') is not None:
            for info in basic.get('explains'):
                print(info)

    translation = json.get('translation')
    if translation is not None:
        print('**************************翻译结果*******************')
        for info in translation:
            print(info)

    web = json.get('web')
    if web is not None:
        print('**************************网络释意*******************')
        for info in web:
            print(info.get('key'))
            print(info.get('value'))
            print('-------------')


def executeDic():
    appKey = '3785101610c308d5'
    salt = random.randint(32768, 65536)
    key = 'bPn9FXAVZLqvmlz1kAXFCUwK2yW7Tw1m'

    params = {
        'q': None,
        'from': 'auto',
        'to': 'auto',
        'appKey': appKey,
        'salt': salt,
        'sign': None
    }
    remindStr = '请输入需要查询的单词或语句(q for quit):'
    word = input(remindStr)
    db.connect()

    # 如果是中文的话则只缓存字符串长度小于5的翻译结果
    wordLenLimit = 5
    while word is not None and word != 'q':
        try:
            value = MyDic.get(MyDic.key == word).value
            q = MyDic.update(times = MyDic.times + 1).where(MyDic.key == word)
            q.execute()
            showInfo(eval(value))
        except DoesNotExist:
            params['q'] = word
            md5Src = appKey + word + str(salt) + key
            params['sign'] = getMd5(md5Src)
            r = requests.get('http://openapi.youdao.com/api', params=params)
            value = r.json()
            if value.get('errorCode') == '0':

                if containChinese(word) is False or len(word) < wordLenLimit:
                    MyDic.create(key=word, value=value)
                showInfo(value)
            else:
                print(value)
        word = input(remindStr)


def main():
    executeDic()

if __name__ == '__main__':
    main()
