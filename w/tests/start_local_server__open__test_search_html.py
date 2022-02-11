#!/usr/bin/env python3

import os
import time
import traceback
import webbrowser
from multiprocessing import Process
from tkinter import messagebox


def f():
    # start local server:
    os.system('python3 -m http.server 8080')


def start_local_server():
    os.chdir('..')
    os.chdir('..')
    global msg
    msg += 'start_local_server()\n  1. cwd= ' + os.getcwd()
    # stop any local server:
    os.system('fuser -k 8080/tcp')
    msg += '\n  2. process using 8080 stopped'

    p = Process(target=f)
    p.start()
    time.sleep(2)
    msg += '\n  3. local server started'


def do_it():
    global msg
    msg = ''
    try:
        start_local_server()
        webbrowser.open('http://localhost:8080/w/tests/test_search.html')
        msg += '\n 4/4. Ran javascript tests'
        print(msg)
    except Exception as e:
        print(traceback.format_exc())
        messagebox.showinfo(__file__, os.path.basename(__file__) + ' FAILED; \n\n' + str(e))



if __name__ == '__main__':
    do_it()