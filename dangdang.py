# -*- coding: utf-8 -*-
import requests
import re
import json
import io
import codecs
import sys
import datetime



reload(sys)
sys.setdefaultencoding('utf-8')


def request_douban(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def parse_result(html):
    pattern = re.compile('<li>.*?<div class="info">.*?title">(.*?)</span>.*?v:average">(\d).(\d).*?</li>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield  {
            'name':item[0],
            'int':item[1],
            'float':item[2].decode('unicode_escape')
        }

def write_to_file(item):
    
    print 'writing data =====>'+str(item).decode('unicode_escape')
    a =a+1
    print(a)
    with codecs.open('book_Douban'+datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.txt','a',encoding = 'UTF-8') as f:
        f.write(json.dumps(dict(item),ensure_ascii=False)+'\n')
        f.close()

def main(page):
    url = 'https://movie.douban.com/top250?start=' + str(page)
    html = request_douban(url)
    items = parse_result(html)
    a = 0
    for item in items:
        write_to_file(item)

if __name__ == "__main__":
    for i in range(25,225,25):
        main(i)
        