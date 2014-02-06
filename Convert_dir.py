# coding: utf-8
__author__ = 'Batuhan BUYUKGUZEL'

import os


path = os.getcwd()+"/"

for f in os.listdir(path):
    os.rename(os.path.join(path, f), os.path.join(path, f.replace(' ', '_')))

for f in os.listdir(path):
    if os.path.isdir(path+f):
        os.rename(os.path.join(path, f), os.path.join(path, f.upper()))
    elif os.path.isfile(path+f):
        os.rename(os.path.join(path, f), os.path.join(path, f[0].upper()+f[1::].lower()))