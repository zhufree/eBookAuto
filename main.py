# coding: utf-8

from bs4 import BeautifulSoup
from PIL import Image

import os
import re
import sys
import HTMLParser

reload(sys)
sys.setdefaultencoding('utf8')
# read html template text files
with open('base.txt', 'r+') as f:
    text = f.read()

html_parser = HTMLParser.HTMLParser()

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


def insert_img(img_id, temp, count):
    """
    :param img_keyword:word for search in text to show here should be a image file, such as 'img', 'pic'
    :param para:one paragraphs in a chapter.
    :param temp: template of html
    :param count: count for img at left or right side
    :return new_div: create a tag of the picture, to insert into html.
    """
    # search pic id in current para, like 'pic1','img1'
    pic_id = 'pic' + img_id
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


def insert_sound(keyword, sound_id, para, temp):
    """    
    :param play_logoword:word for search in text to show here should be a sound file, such as 'sound', 'music', '音乐'
    :param para:one paragraphs in a chapter.
    :param temp: template of html
    :return new_div: create a tag of the sound, to insert into html.
    """
    # search sound id in current para, like 'sound1','img1'
    sound_id = 'sound' + sound_id
    print '==========insert sound ' + sound_id + '=========='
    # get path of the sound, like './sounds/sound1'
    sound_url = [
        url for url in os.listdir('./sounds') if url.startswith(sound_id)][0]
    play_logo = temp.new_tag('img', src='static/img/play.png')
    play_logo['onclick'] = 'play_sound("' + './sounds/' + sound_url + '")'
    play_logo['class'] = 'play_logo'    
    return play_logo


def insert_video(video_id, para, temp):
    """
    :param video_keyword:word for search in text to show here should be a video file, such as 'video'
    :param para:one paragraphs in a chapter.
    :param temp: template of html
    :return new_div: create a tag of the video, to insert into html.
    """
    # search video id in current para, like 'video1','img1'
    video_id = 'video' + video_id
    # get path of the video, like './videos/video1'
    video_url = [
        url for url in os.listdir('./videos') if url.startswith(video_id)][0]
    new_video_div = temp.new_tag(
    	'video', 
    	src='./videos/' + video_url, 
    	controls="controls", 
    	width="600", 
    	height="450"
    	)
    new_video_div['class'] = 'video_in_text'
    new_video_div['style'] = 'clear: both;display: block;margin: auto;'
    with open(video_url + '.html', 'w+') as f:
        f.write(new_video_div.prettify("utf-8"))
        print '==========finish create video page ' + video_url + '==========' 
    return video_url


def handle_text(filename, img_keyword, sound_keyword, video_keyword):
    """
    :param paras:file name of a charpter, such like 'Charpter1.txt', without directory path.
    :result: a html file
    """
    # open file and read paragraphs
    with open(os.path.join('./text/', filename), 'r+') as f:
        paras = [p.strip() for p in f.readlines() if len(p) > 4]
    # read html template
    with open(r'base.txt', 'r+') as f:
        template_text = f.read()
        temp = BeautifulSoup(template_text, "lxml")

    # replace cover img
    # cover = temp.find('img', {'id': 'cover'})
    # cover['src'] = './pics/cover.jpg'

    # handle title
    title = temp.find('h3')
    title.string = paras[0]
    temp.title = paras[0]

    # handle paras
    text_box = temp.find('div', {'id': 'text'})
    js_box = temp.find('script', {'id': 'main'})
    count = [0,0]
    img_pat = re.compile(r'\((\W+?)\)\['+img_keyword+r'(\S+?)\]')
    sound_pat = re.compile(r'\((\W+?)\)\['+sound_keyword+r'(\S+?)\]')
    video_pat = re.compile(r'\((\W+?)\)\['+video_keyword+r'(\S+?)\]')
    for i in range(1, len(paras)):
        new_p = temp.new_tag('p')
        new_br = temp.new_tag('br')
        # handle img in text
        if img_pat.findall(paras[i]):
            imgs = img_pat.findall(paras[i])# a list of tuple(text, img_id)
            for img in imgs:
                img_result = insert_img(img[1], temp, count)
                new_img_div, count = img_result[0], img_result[1]
                text_box.append(new_img_div)
            new_p.string = re.sub(img_pat, r'\1', paras[i])# delete () and []
            # text_box.append(new_p)
            # text_box.append(new_br)
        if sound_pat.findall(paras[i]):
            sounds = sound_pat.findall(paras[i])
            new_p.string = re.sub(sound_pat, r'\1', paras[i])
            for sound in sounds:
                new_play_logo = insert_sound(sound[0], sound[1], paras[i], temp)
                new_p.append(new_play_logo)
            # text_box.append(new_p)
            # text_box.append(new_br)
        if video_pat.findall(paras[i]):
            videos = video_pat.findall(paras[i])
            for video in videos:
                new_video_link = temp.new_string("<a target='_blank' href='"+insert_video(video[1], paras[i], temp) + ".html'>"+video[0]+"</a>")
                new_p.string = re.sub(video_pat, new_video_link, new_p.string)
                new_p = BeautifulSoup(html_parser.unescape(str(new_p)), 'lxml')
        if not (img_pat.findall(paras[i]) or sound_pat.findall(paras[i]) or video_pat.findall(paras[i])):
            new_p.string = paras[i]
        text_box.append(new_p)
        text_box.append(new_br)

    with open('audio.txt', 'r+') as f:
        text = f.read()
        audio_tag = BeautifulSoup(text, 'lxml').div
        text_box.append(audio_tag)

    # add js about sound to html script
    # with open('static/js/audio.js', 'r+') as f:
    #     audio_js = f.read()
    #     js_box.append(audio_js)     

    with open(filename[:-4] + '.html', 'w+') as f:
        f.write(temp.prettify("utf-8"))
        print '==========finish ' + filename + '==========' 


if __name__ == '__main__':
    # find files that exsit in 'text' directory
    files = [f for f in os.listdir('./text') if f.endswith('.txt')]
    for filename in files:
        print '==========handle ' + filename + '=========='
        handle_text(filename, 'pic', 'sound', 'video')
