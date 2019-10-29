# -*- coding: utf-8 -*-


import requests
import bs4
import codecs
import sys
import re
import jsonpath
import json
from functools import partial
import time



reload(sys)
sys.setdefaultencoding('utf-8')
avnum = None

def search_ID(nickname):
    print unicode('finding:{}'.format(nickname))
    url = 'https://search.bilibili.com/upuser?keyword='+nickname
    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            print 'got search search page'
            uid = get_space_url(reponse.text,nickname)
            return uid
    except requests.RequestException:
        print 'error occurs'
        return None

def get_space_url(html,nickname):
    soup = bs4.BeautifulSoup(html,'lxml')
    url_target = soup.find('a',attrs={'target':'_blank','class':'title'}).get('href')
    print url_target
    uid  = re.search('\d+',url_target,re.S).group()
    print uid
    return uid


def get_userpage_json(uid):
    l = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    for i in range(1,11):
        url_json = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid='+str(uid)+'&page='+str(i)

        html = requests.get(url_json,headers=headers).content
        obj = json.loads(html)
        videolist = jsonpath.jsonpath(obj,'$..vlist')
        print 'running........'
        l.append(videolist)
    return l

def find_info_from_json(l):
    av_list = []
    video_info={}
    global avnum

    for videolist in l:
        for i in videolist:
            for j in i:
                for m in j:
                    if str(m) == 'aid':
                        avnum = str(j[m])
                        av_list.append(avnum)
                    elif str(m) == 'description':
                        description = str(j[m])
                    elif str(m) == 'title':
                        title = str(j[m])
                    elif str(m) == 'play':
                        play = str(j[m])
                    elif str(m) == 'length':
                        length = str(j[m])
                    elif str(m) == 'author':
                        author = str(j[m])
                    elif str(m) == 'comment':
                        comment = str(j[m])
                    elif str(m) == 'video_review':
                        video_review = str(j[m])
                    elif str(m) == 'pic':
                        pic = str(j[m])

                other_info = []
                other_info.append(description)
                other_info.append(title)
                other_info.append(pic)
                other_info.append(comment)
                other_info.append(length)
                other_info.append(author)
                video_info[avnum] = other_info
#               with codecs.open('result-{}.txt'.format(author),'a',encoding='utf-16') as f:
#                    f.write('Vedio imformation:\nav:{}\ntitle:{}\nauthor:{}\nplay:{}\nfavorites:{}\ndecription:{}\ncomment:{}\npic_URl:https:{}\n\n\n\n\n\n'
#                    .format(avnum,title,author,play,favorites,description,comment,pic))
    
    return av_list,video_info

def get_all_comments(avlist,video_info):
    for i in avlist:
        get_one_video_comments(i,video_info)

def get_one_video_comments(av,video_info):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    url_detail_info = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='+str(av)
    html = requests.get(url_detail_info,headers=headers).content
    obj = json.loads(html)
    video_detail_info = jsonpath.jsonpath(obj,'$..data')
    for i in video_detail_info:
        for j in i:
            if str(j) == 'like':
                like = str(i[j])
            elif str(j) == 'share':
                share = str(i[j])
            elif str(j) == 'favorite':
                fav = str(i[j])
            elif str(j) == 'danmaku':
                danmaku = str(i[j])
            elif str(j) == 'reply':
                reply = str(i[j])
            elif str(j) == 'coin':
                coin = str(i[j])
            elif str(j) == 'his_rank':
                his_rank = str(i[j])
            elif  str(j) == 'view':
                view = str(i[j])
            elif str(j) == 'aid':
                aid = str(i[j])
        descripion,title,pic,comment,length,author=matching(video_info,aid)
        author = unicode(author)
        
        print 'writing av{}'.format(aid)
        with codecs.open(unicode(r'Demo\search_biliusr\search_result-{}.txt').format(author),'a',encoding='utf-16') as f:
            f.write('VIDEO INFORMATION:\nAV:{}\nTITLE:{}\nAUTHOR:{}\nDESCRIPTION:{}\nPICTURE_URL:https:{}\nLENGTH:{}\nLIKE:{}\nSHARE:{}\nFAVORITE:{}\nDANMUKU:{}\nREPLY:{}\nCOIN:{}\nRANK:{}\nVIEW:{}\n\n\n\n'
            .format(aid,title,author,descripion,pic,length,like,share,fav,danmaku,reply,coin,his_rank,view))

def matching(avdict,av):
    for i in avdict:
        if i == av:
            av_detail = avdict[i]
    descripion = av_detail[0]
    title = av_detail[1]
    pic = av_detail[2]
    comment = av_detail[3]
    length = av_detail[4]
    author = av_detail[5]
    return descripion,title,pic,comment,length,author

if __name__ == "__main__":
    start = time.clock()
    #upname_to_define = raw_input('input the up name:')
    #upname_to_define = unicode(upname_to_define)
    u = unicode(('lex').decode('utf-8'))
    uid = search_ID(u)
    l = get_userpage_json(uid)
    avlist,video_info = find_info_from_json(l)
    get_all_comments(avlist,video_info)

    elapsed = (time.clock() - start)
    print '\n\nTime used:{}'.format(elapsed)

