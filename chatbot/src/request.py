

import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}


url='https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=json&exintro=&redirects=&titles=袋鼠'
r  = requests.get(url, headers=headers)
print(r)

