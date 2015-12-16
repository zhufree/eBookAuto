# coding: utf-8

from bs4 import BeautifulSoup
from PIL import Image

import os
import re

# read html template text files
with open('static/js/audio.js', 'r+') as f:
    text = f.read()
    print text