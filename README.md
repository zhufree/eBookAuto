# 电子书自动排版说明文档

标签（空格分隔）： 作业 出版

---

##功能
>自动读取文件夹中的文字，图片，（视频音频还未实现），生成html页面。

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
 - **videos**-视频文件（暂不支持）
 - **sounds**-音频文件
 - **base.txt**-html-模板文件
如下：
```
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
│   └── pic5.jpg
├── requirement.txt
├── text
    ├── Charpter1.txt
    └── Charpter2.txt
```

- 图片需要在文本内容中标注出来，并尽量和图片的文件名保持格式一致，如"pic1""pic2",或"img1","img2"，代码中可以修改文件名关键词。
