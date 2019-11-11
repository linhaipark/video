# @author:林海
# @date:2019-11-01
# -*- coding: utf-8 -*-


from urllib.parse import urlparse

import requests

# name = '\u82f1\u96c4\u8054\u76df'
# print(name.encode('utf-8').decode('utf-8'))

s = "http:\/\/live-cover.msstatic.com\/huyalive\/96262147-96262147-413442773207744512-3407890260-10057-A-0-1\/20191111153143.jpg"
print(eval(repr(s).replace('\\', '')))
