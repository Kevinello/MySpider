import re

content = 'Xiaoshuaib has 100 bananas'
content = re.sub('\d+','29',content)
print(content)

res = re.compile('^.*?(\d+)\s.*?Z$')
