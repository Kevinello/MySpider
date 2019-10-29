# encoding=utf-8
import  requests
url = 'http://www.adnmb.com'
r = requests.get(url,timeout = 1)


with open('demo.txt', 'w') as f:
    f.write(r.text)
