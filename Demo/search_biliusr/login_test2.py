# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import random
from PIL import Image

web = 'http://literallycanvas.com/'


def init():
    global url, browser, username, password, wait
    url = 'https://passport.bilibili.com/login'
    browser = webdriver.Firefox()
    username = '15112514782'
    password = 'kevin,,4.2'
    wait = WebDriverWait(browser, 30)


def login():
    browser.get(url)
    browser.maximize_window()
    user = wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
    passwd = wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
    user.send_keys(username)
    passwd.send_keys(password)
    login_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-login')))
    time.sleep(random.random() * 3)
    login_btn.click()


def show_element(element):
    browser.execute_script("arguments[0].style=arguments[1]", element, "display: block;")


def hide_element(element):
    browser.execute_script("arguments[0].style=arguments[1]", element, "display: none;")


def save_pic(obj, name):
    try:
        pic_url = browser.save_screenshot('.\\bilibili.png')
        print("%s:截图成功!" % pic_url)
        left = 1107
        top = 320
        right = 1419
        bottom = 514
        im = Image.open('.\\bilibili.png')
        im = im.crop((left, top, right, bottom))
        file_name = 'bili_' + name + '.png'
        im.save(file_name)
    except BaseException as msg:
        print("%s:截图失败!" % msg)


def cut():
    c_background = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_bg.geetest_absolute')))
    c_slice = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_slice.geetest_absolute')))
    c_full_bg = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_fullbg.geetest_fade.geetest_absolute')))
    hide_element(c_slice)
    time.sleep(1)
    save_pic(c_background, 'back')
    show_element(c_slice)
    time.sleep(1)
    save_pic(c_slice, 'slice')
    show_element(c_full_bg)
    time.sleep(1)
    save_pic(c_full_bg, 'full')


def is_pixel_equal(bg_image, fullbg_image, x, y):
    bg_pixel = bg_image.load()[x, y]
    fullbg_pixel = fullbg_image.load()[x, y]
    threshold = 60
    if (abs(bg_pixel[0] - fullbg_pixel[0] < threshold) and abs(bg_pixel[1] - fullbg_pixel[1] < threshold) and abs(
            bg_pixel[2] - fullbg_pixel[2] < threshold)):
        return True
    else:
        return False


def get_distance(bg_image, fullbg_image):
    distance = 60
    for i in range(distance, fullbg_image.size[0]):
        for j in range(fullbg_image.size[1]):
            if not is_pixel_equal(fullbg_image, bg_image, i, j):
                return i * 0.8


def get_trace(distance):
    result = []
    current = 0
    mid = distance * 7 / 10
    t = 0.2
    v = 0
    while current < (distance):
        if current < mid:
            a = 21
        else:
            a = -49
        v0 = v
        v = v0 + a * t
        s = v0 * t + 0.5 * a * t * t
        current += s
        result.append(round(s))
    return result


def move_to_gap(trace):
    slider = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.geetest_slider_button')))
    ActionChains(browser).click_and_hold(slider).perform()
    for x in trace:
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
    ActionChains(browser).move_by_offset(xoffset=3, yoffset=0).perform()
    ActionChains(browser).move_by_offset(xoffset=-3, yoffset=0).perform()
    ActionChains(browser).move_by_offset(xoffset=-2, yoffset=0).perform()
    ActionChains(browser).move_by_offset(xoffset=2, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(browser).release().perform()


def slide():
    distance = get_distance(Image.open('.\\bili_back.png'), Image.open('.\\bili_full.png'))
    print('计算偏移量为：%s Px' % distance)
    trace = get_trace(distance - 7.5)
    move_to_gap(trace)
    time.sleep(3)


def main():
    init()
    while browser.current_url != 'https://www.bilibili.com/':
        login()
        cut()
        slide()
        time.sleep(2)
    return browser


if __name__ == '__main__':
    main()
