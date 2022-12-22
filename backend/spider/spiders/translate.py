__name__ = '翻译'

import time
from spider.models import Mission
from findphd.models import Position
from hashlib import md5
import requests
from django.db.models import Q
from googletrans import Translator
import random

trans = Translator(service_urls=['translate.google.cn',])

def encrypt_md5(s):
    new_md5 = md5()
    new_md5.update(s.encode(encoding='utf-8'))
    return new_md5.hexdigest()

def cut(detail):
    slice = detail.strip().split("\n")
    result = []
    for item in slice:
        item = item.strip()
        if len(item)>2:
            num = int(len(item)/1999)+1
            if num == 1:
                result += [item]
            elif num > 1:
                result += [item[i:i+1999] for i in range(0,num)]
    return result

def wait():
    random_time = int(random.random()*10)+3
    print(random_time)
    time.sleep(random_time)

def main():
    # unitems = Position.objects.filter(Q(title_zh=None)|Q(detail_zh=None)|Q(title_zh='')|Q(detail_zh='')).exclude(Q(detail='')|Q(detail=None))
    unitems = Position.objects.filter(Q(title_zh=None)|Q(detail_zh=None)|Q(title_zh='')|Q(detail_zh=''))
    for item in unitems:
        title = item.title
        detail = item.detail
        if item.title_zh ==None or item.title_zh == '':
            item.title_zh = trans.translate(str(title), dest="zh-cn").text
            wait()

        if detail !=None and detail != '':
            slice_detail = cut(detail)
            detail_zh = ''
            for slice in slice_detail:
                detail_zh += trans.translate(str(slice), dest="zh-cn").text
                wait()
            item.detail_zh = detail_zh
        
        print(item.title_zh)
        item.save()
        

def run(missionDb):
    try:
        missionDb.status = Mission.Status.R
        missionDb.save()
        main()
        missionDb.status = Mission.Status.NR
        missionDb.save()
    except Exception as e:
        print(e)
        missionDb.status = Mission.Status.ER
        missionDb.save()
    