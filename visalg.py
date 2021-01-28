#!/usr/local/bin/python3

from tkinter import Tk, Canvas, Frame, BOTH, Button, YES, NO, LEFT, RIGHT, BOTTOM, TOP
from tkinter import CENTER
from random import randrange
from chart import Chart
from timer import Timer

WIDTH = 600
HEIGHT = 400

def main():
    root = Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.resizable(False, False)

    frame = Frame(root,
            highlightbackground="blue",
            highlightcolor="blue",
            highlightthickness=0,
            bd=0)
    frame.master.title("Visual Sort Algorithms")
    frame.pack(expand=YES, fill=BOTH)

    canvas = Canvas(frame,
            highlightbackground="green",
            highlightcolor="green",
            highlightthickness=0,
            bd=0)
    canvas.pack(expand=YES, fill=BOTH)

    chart = Chart(canvas, root, 50)

    btn = Button(root, text='reset', command=chart.reset)
    btn2 = Button(root, text='insertion', command=chart.insertionsort)
    btn3 = Button(root, text='bubble', command=chart.bubblesort)
    btn4 = Button(root, text='selection', command=chart.selectionsort)
    btn5 = Button(root, text='merge', command=chart.mergesort)
    btn6 = Button(root, text='quick', command=chart.quicksort)
    btn7 = Button(root, text='shell', command=chart.shellsort)
    btn.pack(side=LEFT)
    btn2.pack(side=RIGHT)
    btn3.pack(side=RIGHT)
    btn4.pack(side=RIGHT)
    btn5.pack(side=RIGHT)
    btn6.pack(side=RIGHT)
    btn7.pack(side=RIGHT)

    chart.update()
    chart.reset()
    root.mainloop()

if __name__ == '__main__':
    main()
