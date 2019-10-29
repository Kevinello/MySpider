# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import codecs



def request_douban(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def save_to_excel(soup):
    list = soup.find(class_='grid_view').find_all('li')

    for item in list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        if(item.find(class_='inq')!=None):
            item_intr = item.find(class_='inq').string

        print('Running:')
        with codecs.open('Douban Top250.txt','a',encoding='utf-8') as f:
            f.write(item_author+item_name+item_index+item_score+item_intr)
        


def main(page):
    url = 'https://movie.douban.com/top250?start='+ str(page*25)+'&filter='
    html = request_douban(url)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


if __name__ == '__main__':

    for i in range(0, 10):
        main(i)

