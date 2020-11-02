import os
import lib
from tkinter import Tk
import tkinter.filedialog
import string
from tkinter import *

if __name__ == '__main__':
    client = lib.FileClient('localhost:8000')

    root = tkinter.Tk()
    files = tkinter.filedialog.askopenfilenames(parent=root,title='Choose a file')
    in_file_name = root.tk.splitlist(files)

    print(in_file_name[0])
    client.upload(in_file_name[0])

    out_file_name = '/tmp/large_file_out'
    if os.path.exists(out_file_name):
        os.remove(out_file_name)
    client.download('whatever_name', out_file_name)
    os.system(f'sha1sum {in_file_name}')
    os.system(f'sha1sum {out_file_name}')
