from tkinter import IntVar

class Timer:
    def __init__(self, root):
        self.var = IntVar()
        self.root = root

    def wait(self, ms):
        self.var.set(0)
        self.root.after(ms, lambda:self.var.set(1))
        self.root.wait_variable(self.var)
        self.var.set(0)

