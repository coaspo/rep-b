#!/usr/bin/env python3
from tkinter import LEFT

import twiv_picks
import hacker_news
import dictionary_look_up
import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Web scrapping / Web APIs")
    root.configure(background='white')
    root.geometry("450x350")
    add_widgets(root)
    root.mainloop()


def add_widgets(root):
    x0, dy = 50, 50

    i = 1
    b = tk.Button(root, bg='#b1ffa3', command=dictionary_look_up.main,
                  text="Dictionary word-list look-up (API)")
    b.place(x=x0, y=i * dy, width=350, height=30)

    i += 1
    b = tk.Button(root, bg='#b1ffa3', command=hacker_news_sort.main,
                  text="Hacker news; sort last week's links")
    b.place(x=x0, y=i * dy, width=350, height=30)

    i += 1
    b = tk.Button(root, bg='#b1ffa3', command=twiv_picks.main,
                  text="TWIV picks; create different list types")
    b.place(x=x0, y=i * dy, width=350, height=30)

    i += 1
    label = tk.Label(root, text=' Click a button and\n interact/check Terminal window.',
                     anchor="w", justify=LEFT)
    label.place(x=x0, y=i * dy + 20, width=350, height=45)


main()
