import hashlib
import random
import requests
from peewee import *

db = MySQLDatabase('mydb', user='root')


# 基础类
class BaseModel(Model):
    class Meta:
        database = db


# 自定义词典
class MyDic(BaseModel):
    key = CharField()
    value = CharField()


def getMd5(src):
    md5 = hashlib.md5()
    md5.update(src.encode(encoding='utf8'))
    return md5.hexdigest()


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


appKey = '3785101610c308d5'
q = '支票'
salt = random.randint(32768, 65536)
key = 'bPn9FXAVZLqvmlz1kAXFCUwK2yW7Tw1m'

params = {
    'q': q,
    'from': 'auto',
    'to': 'auto',
    'appKey': appKey,
    'salt': salt,
    'sign': None
}
remindStr = '请输入需要查询的单词或语句(q for quit):'
word = input(remindStr)
db.connect()
while word is not None and word != 'q':
    try:
        value = MyDic.get(MyDic.key == word).value
        showInfo(eval(value))
    except DoesNotExist:
        params['q'] = word
        md5Src = appKey + word + str(salt) + key
        params['sign'] = getMd5(md5Src)
        r = requests.get('http://openapi.youdao.com/api', params=params)
        value = r.json()
        if value.get('errorCode') == '0':
            MyDic.create(key=word, value=value)
            showInfo(value)
        else:
            print(value)
    word = input(remindStr)
