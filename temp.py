# coding: utf-8

from bs4 import BeautifulSoup
from PIL import Image

import os
import re
img_keyword = 'pic'
img_pat = re.compile(r'\((\S+)\)\['+img_keyword+r'(\S+)\]')
# read html template text files
with open('text/Charpter1.txt', 'r+') as f:
    text = f.read()
    print text
    print img_pat.pattern
    print img_pat.findall(text)
    print re.sub(img_pat, r'\1', text)
