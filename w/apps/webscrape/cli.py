#!/usr/bin/env python3
import twiv_picks
import hacker_news_sort
import tkinter as tk

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

button = tk.Button(frame,
                   text="TWIV picks, easily scanned list",
                   fg="red",
                   command=twiv_picks.main)
button.pack(side=tk.TOP)
slogan = tk.Button(frame,
                   text="Hacker news, sorted by points",
                   command=hacker_news_sort.main)
slogan.pack(side=tk.TOP)

root.mainloop()
