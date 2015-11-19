# coding: utf-8

from bs4 import BeautifulSoup, Tag
from PIL import Image

import os
import re

# read html text files
with open('base.txt', 'r+') as f:
    text = f.read()


def insert_img(keyword, para, temp):
    """
    :param keyword:word for search in text to show here should be a picture, such as 'img', 'pic', '图片'
    :param para:one paragraphs in a charpter.
    :return new_div: create a tag of the picture, to insert into html.
    """
    if keyword in para:
        pic_id = re.search(keyword + r'(\d+)', para).group()
        pic_url = [
            url for url in os.listdir('./pics') if url.startswith(pic_id)][0]
        print pic_url
        im = Image.open(os.path.join('./pics', pic_url))
        print im.size  # (wedth,height)
        if im.size[0] > 400:
            new_div = temp.new_tag('div')
            new_pic = temp.new_tag('img', src='./pics/' + pic_url)
            new_div['class'] = 'pic_in_text_center'
            new_div.append(new_pic)
        else:
            if int(pic_id[-1]) % 2 == 0:
                new_div = temp.new_tag('img', src='./pics/' + pic_url)
                new_div['class'] = 'pic_in_text_right'
            else:
                new_div = temp.new_tag('img', src='./pics/' + pic_url)
                new_div['class'] = 'pic_in_text_left'
        return new_div
    else:
        return None


def handle_text(filename):
    """
    :param paras:file name of a charpter, such like 'Charpter1.txt',without directory path.
    :result: a html file
    """
    with open(os.path.join('./text/', filename), 'r+') as f:
        paras = [p.strip() for p in f.readlines() if len(p) > 3]
        # print paras

    temp = BeautifulSoup(text, "lxml")

    # replace cover img
    cover = temp.find('img', {'id': 'cover'})
    cover['src'] = './pics/cover.jpg'

    # handle title
    title = temp.find('h4')
    title.string = paras[0]

    # handle paras
    textbox = temp.find('div', {'id': 'text'})
    for i in range(1, len(paras)):
        new_p = temp.new_tag('p')
        new_br = temp.new_tag('br')
        new_p.string = paras[i]
        # handle img in text
        new_div = insert_img('pic', paras[i], temp)
        if new_div:
            textbox.append(new_div)
        textbox.append(new_p)
        textbox.append(new_br)

    with open(filename[:-4] + '.html', 'w+') as f:
        f.write(temp.prettify("utf-8"))


if __name__ == '__main__':
    # find files that exsit in 'text' directory
    files = os.listdir('./text')
    for filename in files:
        handle_text(filename)
