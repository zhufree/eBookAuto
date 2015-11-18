# coding: utf-8

from bs4 import BeautifulSoup, Tag
from PIL import Image

import os
import re
# read files

# find files that exsit in 'text' directory
files = os.listdir('./text')

with open(os.path.join('./text/', files[0]), 'r+') as f:
    paras = [p.strip() for p in f.readlines() if len(p) > 3]
    # print paras

# operate html
with open('base.txt', 'r+') as f:
    text = f.read()

with open(files[0][:-4] + '.html', 'w+') as f:
    temp = BeautifulSoup(text, "lxml")
    # replace cover img
    cover = temp.find('img', {'id': 'cover'})
    cover['src'] = './pics/cover.jpg'

    # for title
    title = temp.find('h4')
    title.string = paras[0]

    # for paras
    textbox = temp.find('div', {'id': 'text'})
    new_br = temp.new_tag('br')
    for i in range(1,len(paras)):
        # print paras[i]
        new_p = temp.new_tag('p')
        new_br = temp.new_tag('br')
        new_p.string = paras[i]
        # if img in text
        if 'pic' in paras[i]:
            pic_id = re.search(r'pic(\d+)', paras[i]).group()
            pic_url = [url for url in os.listdir('./pics') if url.startswith(pic_id)][0]
            # print pic_url
            im = Image.open(os.path.join('./pics', pic_url))
            print im.size# (wedth,height)
            if im.size[0] > 400:
                new_div = temp.new_tag('div')
                new_pic = temp.new_tag('img', src='./pics/' + pic_url)
                new_div['class'] = 'pic_in_text_center'
                new_div.append(new_pic)
            else:
                if int(pic_id[-1])%2 == 0:
                    new_div = temp.new_tag('img', src='./pics/' + pic_url)
                    new_div['class'] = 'pic_in_text_right'
                else:
                    new_div = temp.new_tag('img', src='./pics/' + pic_url)
                    new_div['class'] = 'pic_in_text_left'
           
            textbox.append(new_div)
            textbox.append(new_p)
            textbox.append(new_br)
        else:
            textbox.append(new_p)
            textbox.append(new_br)
    f.write(temp.prettify("utf-8"))
