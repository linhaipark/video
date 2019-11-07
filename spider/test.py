# @author:林海
# @date:2019-11-01
# -*- coding: utf-8 -*-


from urllib.parse import urlparse

import requests

url = 'https://www.douyu.com/gapi/rkc/directory/0_0/1'
html = requests.get(url).text
print(html)