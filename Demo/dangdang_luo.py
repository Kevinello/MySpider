import bs4
import requests
import re
import sys
import codecs
import datetime
# encoding=utf-8
reload(sys)
sys.setdefaultencoding('utf-8')
nowTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')


def get_html(page):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def parse_html(html, nowtime):
    output = {'Title:{title}  Stars:{stars}  {publish_info}  Price:{price}\n'}
    soup = bs4.BeautifulSoup(html, 'html.parser')
    soup_list = soup.find('ul', attrs={'class': 'bang_list clearfix bang_list_mode'})
    for li in soup_list.find_all('li'):
        title = str(li.find('div', attrs={'class': 'name'}))
        title = re.sub(r'<.*?>', '', title)
        comments = str(li.find('div', attrs={'class': 'star'}))
        comments = re.sub(r'<.*?>', '', comments)
        publish_info = str(li.find('div', attrs={'class': 'publisher_info'}))
        publish_info = re.sub(r'<.*?>', '', publish_info)
        price = str(li.find('div', attrs={'class': 'price'}).find('p'))
        price = re.sub(r'<.*?>', '', price)
        save_txt(nowtime, 'Title:{}\nComments:{}\n{}\nPrice:{}\n'.format(title, comments, publish_info, price))


def save_txt(nowtime, *args):
    with codecs.open(('dangdang'+str(nowtime)), 'a', encoding='utf-16') as f:
        f.write(i)


if __name__ == '__main__':
    for i in range(1,26):
        html = get_html(i)
        parse_html(html, nowTime)