import requests
import io

res = requests.get('https://movie.douban.com/top250')
with io.open('html_dd.txt','a',encoding='UTF-8') as f:
    f.write(res.text)
