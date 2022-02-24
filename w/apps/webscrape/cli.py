#!/usr/bin/env python3
import twiv_picks
import hacker_news_sort
import dictionary_look_up
import tkinter as tk

root = tk.Tk()
root.title("Web scrapping / Web APIs")
root.configure(background='white')
root.geometry("450x350")

i=1
x0 = 50
dy=50

label = tk.Label(root)
label.place(x = x0, y = 4*dy +dy//2, width=350, height=30)
def f1():
   dictionary_look_up.run(label)

b = tk.Button(root, bg='#b1ffa3', command=dictionary_look_up.main,
                   text="Dictionary word-list look-up (API)")
b.place(x = x0, y = i*dy, width=350, height=30)

i+=1
b = tk.Button(root, bg='#b1ffa3', command=hacker_news_sort.main,
                   text="Hacker news; sort last week's links")
b.place(x = x0, y = i*dy, width=350, height=30)

i+=1
b = tk.Button(root, bg='#b1ffa3', command=twiv_picks.main,
                   text="TWIV picks; create different list types")
b.place(x = x0, y = i*dy, width=350, height=30)

i+=1
label = tk.Label(root, text = 'Check Terminal window after clicking a button')
label.place(x = x0, y = i*dy+20, width=350, height=15)

root.mainloop()

