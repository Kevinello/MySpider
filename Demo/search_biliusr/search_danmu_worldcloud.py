# -*- coding: utf-8 -*-
import login_test2
import requests
import bs4
import re
import os
import time
import json
import jsonpath
import codecs
import lxml.etree
import multiprocessing
from functools import partial
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy
from PIL import Image
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.'}
    data = requests.get(url, headers=headers)
    return data.content


def getaidlist(b_up):
    print 'spiding aids...'
    space_search_url = 'https://search.bilibili.com/upuser?keyword={}'.format(b_up)
    search_result = download_page(space_search_url)
    search_result = bs4.BeautifulSoup(search_result, 'html.parser')
    up_url = search_result.find('a', attrs={'class': 'title', 'target': '_blank'})
    b_up = up_url.get('title')
    up_url = str(up_url.get('href'))
    up_url = re.search(r'\d+', up_url).group()
    avnumbers = download_page('https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}'.format(up_url))
    avnumbers = json.loads(avnumbers)
    aidlist = jsonpath.jsonpath(avnumbers, '$..aid')
    return b_up, aidlist


def getcidlist(aidlist):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    print 'spiding cids...'
    cidlist = pool.map(getcid, aidlist)
    pool.close()
    pool.join()
    return cidlist


def getcid(aid):
    time.sleep(0.1)
    cid_ = download_page('https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp'.format(aid))
    cid_ = json.loads(cid_)
    cid = jsonpath.jsonpath(cid_, '$..cid')[0]
    return cid


def getbarrage(oidlist, name):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    print 'spiding barrages...'
    pool.map(partial(getb, name=name), oidlist)
    pool.close()
    pool.join()
    pool.terminate()
    reorganize_barrage(name)


def getb(oid, name):
    barrage = download_page('https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(oid))
    time.sleep(0.1)
    if not os.path.exists(unicode('barrage/{}'.format(name))):
        os.makedirs(unicode('barrage/{}'.format(name)))
    with codecs.open(unicode('barrage/{}/av{}.xml'.format(name, oid)), 'wb', encoding='utf-16') as f:
        f.write(barrage)


def reorganize_barrage(name):
    results = {}
    for filename in os.listdir(unicode('barrage/{}'.format(name))):
        html = lxml.etree.parse(unicode('barrage/{}/{}'.format(name, filename)), lxml.etree.HTMLParser())
        barrages = html.xpath('//d//text()')
        for barrage in barrages:
            barrage = barrage.replace('\r', '')
            if barrage in results:
                results[barrage] += 1
            else:
                results[barrage] = 1
    if not os.path.exists('statistical result'):
        os.makedirs('statistical result')
    with codecs.open(unicode('statistical result/{}.txt'.format(name)), 'w', encoding='utf-16') as f:
        for key, value in results.items():
            f.write('{}\n'.format(key.rstrip('\r')))


def enwordcloud(name):
    with codecs.open(unicode('statistical result/{}.txt'.format(name)), 'r', encoding='utf-16') as f:
        f = f.read()
    #background_image = numpy.array(Image.open('Marshmello.jpg'))
    jieba_txt = ' '.join(jieba.cut(f))
    word_cloud = WordCloud(font_path='ziti.ttf',
                           background_color='white', width=1920, height=1080)#, #mask=background_image)
    word_cloud_ = word_cloud.generate(jieba_txt)
    plt.imshow(word_cloud_)
    plt.axis('off')
    plt.show()
    if not os.path.exists('wordcloud'):
        os.makedirs('wordcloud')
    word_cloud.to_file(unicode('wordcloud/{}_wordcloud.jpg'.format(name)))


if __name__ == '__main__':
#    browser = login_test2.main()
#    browser.close()
    b_up = unicode(raw_input('Input Up_id:').decode('utf-8'))
    b_up, aidlist = getaidlist(b_up)
    cidlist = getcidlist(aidlist)
    getbarrage(cidlist, b_up)
    enwordcloud(b_up)
