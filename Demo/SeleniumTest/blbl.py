from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs   
import requests
import re

browser = webdriver.Chrome()
WAIT = WebDriverWait(browser, 30)
browser.set_window_size(1400,900)


def search():

    try:
        print('visiting pilipili....')
        browser.get("https://www.bilibili.com/")

        # covered by login 
        index = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#primary_menu > ul > li.home > a")))#reload
        index.click()

        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#banner_link > div > div > form > input")))
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="banner_link"]/div/div/form/button')))

        input.send_keys('caixukun lanqiu')
        submit.click()

        # jump to new window
        print('jump to new window')
        all_h = browser.window_handles
        for handle in all_h:
            if handle != browser.current_window_handle:
                browser.switch_to_window(handle)


        get_source()
        return browser.current_url
    except TimeoutException:
        return search()


def next_page(page_num,thisURL):
    url = thisURL+'&page='+str(page_num)
    print url
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'html.parser')
        save_to_txt(soup)
    except requests.RequestException:
        return None
    


def save_to_txt(soup):
    list = soup.find_all(class_='tags')

    for item in list:
        item_av = item.find('span',attrs={'class':'type avid'})
        #item_playnu = item.find('span', attrs={'class':'so-icon watch-num'})

        #item_danmu = item.find(class_='so-icon hide').string
        #item_time = item.find(class_='so-icon time').string
        #item_up = item.find(class_='so-icon').string

       # print('getting:' + item_av)

        save('\n:{}'.format(item_av))


def save(*args):
    for i in args:
        with codecs.open('bilibili.txt','a',encoding='utf-8',errors='ignore') as f:
            f.write(i)

def get_source():
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    save_to_txt(soup)

def main():

    try:
        thisURL = search()
        for i in range(2,48):
            next_page(i,thisURL)

    finally:
        browser.close()


if __name__ == '__main__':
    main()
