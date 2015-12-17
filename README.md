# 电子书自动排版说明文档

---

##功能
>自动读取文件夹中的文字,图片,视频,音频,生成html页面。

##配置
运行环境要求：python2.7+

第三方库依赖：
>beautifulsoup4==4.4.0
Pillow==2.3.0

安装了pip之后可以直接运行

    sudo pip install -r requirement.txt


##文件系统要求
- 内容文件放在特定文件夹中
 - **text**-文本文件
 - **pics**-图片文件
 - **videos**-视频文件
 - **sounds**-音频文件
 - **base.txt**-html-模板文件
如下：
```
.
├── base.txt
├── Charpter1.html
├── Charpter2.html
├── main.py
├── pics
│   ├── cover.jpg
│   ├── pic1.jpg
│   ├── pic2.jpg
│   ├── pic3.jpg
│   ├── pic4.jpg
│   ├── pic5.jpg
│   ├── pic6.jpg
│   └── small_pic6.jpg
├── README.md
├── requirement.txt
├── sounds
│   └── sound1.mp3
├── text
│   ├── Charpter1.txt
│   └── Charpter2.txt
├── videos
│   └── video1.mp4

```

- 图片需要在文本内容中单行标注出来（标注文字不会插入正文中，并和图片的文件名保持格式一致，如"pic1""pic2",或"img1","img2"，代码中可以修改文件名关键词。
- 最近更新：改写音频播放器样式，依赖jqueryui，css和js文件与html分离，保存在static文件夹中。视频播放提供链接，以单独页面显示。
