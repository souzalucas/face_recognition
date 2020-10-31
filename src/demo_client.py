import os
import lib
from tkinter import Tk
# from tkinter.filedialog import askopenfilename
# from threading import Thread
import tkinter.filedialog
import string
#import re
from tkinter import *

if __name__ == '__main__':
    client = lib.FileClient('localhost:8888')

    # var = []
    # var.append('../1.jpg')
    # var.append('../arduino.jpeg')
    # var.append('../woddy.jpg')


    # demo for file uploading
    in_file_name = '/tmp/large_file_in'

    root = tkinter.Tk()
    files = tkinter.filedialog.askopenfilenames(parent=root,title='Choose a file')
    files = root.tk.splitlist(files)

    print ("list of filez =",files)

    # for path in var:
    client.upload(files) # in_file_name

    # demo for file downloading:
    # out_file_name = '/tmp/large_file_out'
    # if os.path.exists(out_file_name):
    #     os.remove(out_file_name)
    # client.download('whatever_name', out_file_name)
    # os.system(f'sha1sum {in_file_name}')
    # os.system(f'sha1sum {out_file_name}')
