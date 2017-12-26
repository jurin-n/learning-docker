# -*- coding: utf-8 -*-
import requests

res = requests.get('https://api.github.com/users/jurin-n')
json_content=res.content
with open('workfile','wb') as f:
    f.write(json_content)
