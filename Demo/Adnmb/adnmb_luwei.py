import bs4
import requests
import codecs
import datetime
import sys
import re

# encoding=utf-8
reload(sys)
sys.setdefaultencoding('utf-8')
nowTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

def get_html(page):
    print 'Running Adnmb'
    
    url = 'https://adnmb2.com/t/49607?page='+str(page)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def get_element(html,nowtime):
    soup = bs4.BeautifulSoup(html,'lxml')
    list = soup.find_all(class_='h-threads-item-reply')
    for item in list:
        title = item.find(class_='h-threads-info-title').string
        email = item.find(class_='h-threads-info-email').string
        creatlist = item.find(class_='h-threads-info-createdat').string
        uid = item.find(class_='h-threads-info-uid').string
        thread_id = item.find(class_='h-threads-info-id').string
        contend= item.find(class_='h-threads-content').string

        print creatlist

        save_txt(nowtime,'Title:{}\nEmail:{}\nCreatList:{}\nUid:{}\nThread_id:{}\nContend:{}\n'.format(title,email,creatlist,uid,thread_id,contend))

def save_txt(nowtime,*args):
    for i in args:
        with codecs.open(('Adnmb'+str(nowtime)),'a',encoding='utf-8') as f:
            f.write(i)
       



if __name__ == "__main__":
    print 'Running Adnmb'
    for i in range(1,263):
        html = get_html(i)
        get_element(html,nowTime)

