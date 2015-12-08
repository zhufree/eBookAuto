# coding: utf-8

from bs4 import BeautifulSoup
from PIL import Image

import os
import re

# read html template text files
with open('base.txt', 'r+') as f:
    text = f.read()


def change_img_size(img, new_pic_url):
    print '==========change img size=========='
    row_width, row_height = img.size[0], img.size[1]
    print 'row_size' + str(img.size)
    radio = float(row_width)/300
    to_width = 300
    to_height = int(row_height/radio)
    print 'change to ' + str((to_width, to_height))
    img.thumbnail((to_width, to_height))
    img.save(os.path.join('./pics', new_pic_url))
    return img


def insert_img(img_keyword, para, temp, count):
    """
    :param img_keyword:word for search in text to show here should be a picture, such as 'img', 'pic', '图片'
    :param para:one paragraphs in a chapter.
    :param temp: template of html
    :param count: count for img at left or right side
    :return new_div: create a tag of the picture, to insert into html.
    """
    if img_keyword in para:
        # search pic id in current para, like 'pic1','img1'
        pic_id = re.search(img_keyword + r'(\d+)', para).group()
        print '==========insert img ' + pic_id + '=========='
        # get path of the pic, like './pics/pic1'
        pic_url = [
            url for url in os.listdir('./pics') if url.startswith(pic_id)][0]
        # use pillow lib to open the pic
        im = Image.open(os.path.join('./pics', pic_url))
        # decide where to locate the pic
        # rules: 1. if picture's width > 1/3 of the browser width
        # and picture's width > height: locate it center
        # 2. if picture's width > 1/3 of the browser width
        # and picture's width < height:zoom the pic and locate it at side
        # 3. if picture's width <1/3 of the browser width : locate it at side
        # 4. when locate pictures at side ,put it at left first, then right.
        if im.size[0] > 400 and im.size[0] > im.size[1]:
            # create a div to put the img
            new_div = temp.new_tag('div')
            # create a img tag
            new_pic = temp.new_tag('img', src='./pics/' + pic_url)
            # add class to div
            new_div['class'] = 'pic_in_text_center'
            # add img to div
            new_div.append(new_pic)
        elif im.size[0] > 400 and im.size[0] < im.size[1]:
            new_pic_url = 'small_' + pic_url
            im = change_img_size(im, new_pic_url)
            im.save(os.path.join('./pics', new_pic_url))
            if count[0] > count[1]:
                new_div = temp.new_tag('img', src='./pics/' + new_pic_url)
                new_div['class'] = 'pic_in_text_right'
                count[1] += 1
            else:
                new_div = temp.new_tag('img', src='./pics/' + new_pic_url)
                new_div['class'] = 'pic_in_text_left'
                count[0] += 1
        else:
            if count[0] > count[1]:
                new_div = temp.new_tag('img', src='./pics/' + pic_url)
                new_div['class'] = 'pic_in_text_right'
                count[1] += 1
            else:
                new_div = temp.new_tag('img', src='./pics/' + pic_url)
                new_div['class'] = 'pic_in_text_left'
                count[0] += 1
        return new_div, count
    else:
        return None, count


def insert_sound(sound_keyword, para, temp):
    """
    :param sound_keyword:word for search in text to show here should be a sound file, such as 'sound', 'music', '音乐'
    :param para:one paragraphs in a chapter.
    :param temp: template of html
    :return new_div: create a tag of the picture, to insert into html.
    """
    if sound_keyword in para:
        # search sound id in current para, like 'sound1','img1'
        sound_id = re.search(sound_keyword + r'(\d+)', para).group()
        print '==========insert sound ' + sound_id + '=========='
        # get path of the sound, like './sounds/sound1'
        sound_url = [
            url for url in os.listdir('./sounds') if url.startswith(sound_id)][0]
        new_div = temp.new_tag('audio', src='./sounds/' + sound_url, controls="controls")
        new_div['class'] = 'sound_in_text'
        return new_div
    else:
        return None


def insert_video(video_keyword, para, temp):
    """
    :param video_keyword:word for search in text to show here should be a video file, such as 'video', 'music', '音乐'
    :param para:one paragraphs in a chapter.
    :param temp: template of html
    :return new_div: create a tag of the picture, to insert into html.
    """
    if video_keyword in para:
        # search video id in current para, like 'video1','img1'
        video_id = re.search(video_keyword + r'(\d+)', para).group()
        print '==========insert video ' + video_id + '=========='
        # get path of the video, like './videos/video1'
        video_url = [
            url for url in os.listdir('./videos') if url.startswith(video_id)][0]
        new_div = temp.new_tag(
        	'video', 
        	src='./videos/' + video_url, 
        	controls="controls", 
        	width="600", 
        	height="450"
        	)
        new_div['class'] = 'video_in_text'
        return new_div
    else:
        return None

def handle_text(filename):
    """
    :param paras:file name of a charpter, such like 'Charpter1.txt', without directory path.
    :result: a html file
    """
    # open file and read paragraphs
    with open(os.path.join('./text/', filename), 'r+') as f:
        paras = [p.strip() for p in f.readlines() if len(p) > 3]
    # read html template
    temp = BeautifulSoup(text, "lxml")

    # replace cover img
    cover = temp.find('img', {'id': 'cover'})
    cover['src'] = './pics/cover.jpg'

    # handle title
    title = temp.find('h3')
    title.string = paras[0]

    # handle paras
    textbox = temp.find('div', {'id': 'text'})
    count = [0,0]
    for i in range(1, len(paras)):
        new_p = temp.new_tag('p')
        new_br = temp.new_tag('br')
        new_p.string = paras[i]
        # handle img in text
        img_result = insert_img('pic', paras[i], temp, count)
        new_img_div, count = img_result[0], img_result[1]
        if new_img_div:
            textbox.append(new_img_div)
        new_sound_div = insert_sound('sound', paras[i], temp)
        if new_sound_div:
            textbox.append(new_sound_div)
        new_video_div = insert_video('video', paras[i], temp)
        if new_video_div:
            textbox.append(new_video_div)
        textbox.append(new_p)
        textbox.append(new_br)

    with open(filename[:-4] + '.html', 'w+') as f:
        f.write(temp.prettify("utf-8"))
        print '==========finish ' + filename + '==========' 


if __name__ == '__main__':
    # find files that exsit in 'text' directory
    files = [f for f in os.listdir('./text') if f.endswith('.txt')]
    for filename in files:
        print '==========handle ' + filename + '=========='
        handle_text(filename)
