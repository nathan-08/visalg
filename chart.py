from random import randrange
from timer import Timer
from tkinter import BooleanVar

def check_if_running(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args):
        if not args[0].running:
            args[0].running = True
            return_val = fn(*args)
            args[0].running = False
            return return_val
    return wrapper

class Chart:
    def __init__(self, canvas, root, animation_time):
        root.update()
        self.running = False
        self.__animation_time = animation_time
        self.canvas = canvas
        self.root = root
        self.width = canvas.winfo_width() 
        self.height = canvas.winfo_height()
        self.r_ids = []
        self.__time = Timer(root)
        root.protocol("WM_DELETE_WINDOW", self.__handle_close)

    def __handle_close(self):
        if self.running:
            self.__animation_time = 0
            self.__wait_and_quit()
        else:
            self.root.destroy()

    def __wait_and_quit(self):
        if self.running:
            self.root.after(100, self.__wait_and_quit)
        else:
            self.root.destroy()

    def __wait(self, ms=-1):
        self.__time.wait(ms if ms > 0 else self.__animation_time)

    def update(self):
        self.root.update()
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

    def setcolor(self, idx, color):
        self.canvas.itemconfig(self.r_ids[idx], fill=color)

    def swap(self, idx1, idx2):
        h1 = self.getheight(idx1)
        h2 = self.getheight(idx2)
        self.setheight(idx1, h2)
        self.setheight(idx2, h1)

    def getheight(self, idx):
        x0, y0, x1, y1 = self.canvas.coords(self.r_ids[idx])
        height = y1 - y0
        return height

    def setheight(self, idx, height):
        x0, y0, x1, y1 = self.canvas.coords(self.r_ids[idx])
        new_y0 = y1 - height
        self.canvas.coords(self.r_ids[idx],
                x0, new_y0, x1, y1)

    def __drawrects(self):
        for n in range(self.width // 20):
        # for n in range(20):
            r = self.canvas.create_rectangle(
                    n * 20,
                    self.height,
                    (n * 20) + 16,
                    randrange(0, self.height),
                    fill='#000',
                    activefill='red',
                    width=0 # border width
                    )

            self.r_ids.append(r)

    def __clearrects(self):
        for r in self.r_ids:
            self.canvas.delete(r)
        self.r_ids.clear()

    @check_if_running
    def reset(self):
        self.__clearrects()
        self.__drawrects()

    @check_if_running
    def bubblesort(self):
        for i in range(len(self.r_ids) - 1, 0, -1):
            for j in range(i):
                self.setcolor(j, 'red')
                self.setcolor(j+1, 'red')
                h1 = self.getheight(j)
                h2 = self.getheight(j+1)
                if h1 > h2:
                    self.swap(j, j+1)
                self.__wait()
                self.setcolor(j, '#000')
                self.setcolor(j+1, '#000')

    @check_if_running
    def selectionsort(self):
        for i in range(len(self.r_ids) - 1, 0, -1):
            greatest_idx = 0
            for j in range(i + 1):
                self.setcolor(i, 'blue')
                self.setcolor(j, 'red')
                self.setcolor(greatest_idx, 'green')

                if self.getheight(j) > self.getheight(greatest_idx):
                    self.setcolor(greatest_idx, '#000')
                    greatest_idx = j
                self.__wait()
                self.setcolor(j, '#000')
            if i != greatest_idx:
                self.setcolor(greatest_idx, '#000')
                self.swap(i, greatest_idx)
            self.setcolor(i, '#000')

    @check_if_running
    def insertionsort(self):
        for i in range(1, len(self.r_ids)):
            cur_val = self.getheight(i)
            cur_pos = i

            while cur_pos > 0 and cur_val < self.getheight(cur_pos - 1):
                self.setcolor(cur_pos, 'red')
                self.setheight(cur_pos, self.getheight(cur_pos - 1))
                cur_pos = cur_pos - 1
                self.setheight(cur_pos, 0)
                self.__wait()
                self.setcolor(cur_pos + 1, '#000')
            self.setheight(cur_pos, cur_val)

    @check_if_running
    def mergesort(self):
        vals = [self.getheight(i) for i in range(len(self.r_ids))]
        self.__mergesort_recurs(vals)

    def __mergesort_recurs(self, vals, offset=0):
        if len(vals) > 1:

            midpoint = len(vals) // 2
            left = vals[:midpoint]
            right = vals[midpoint:]

            self.__mergesort_recurs(left, offset + 0)
            self.__mergesort_recurs(right, offset + midpoint)

            i, j, k = 0, 0, 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    self.setheight(k + offset, left[i])
                    vals[k] = left[i]
                    i = i + 1
                else:
                    self.setheight(k + offset, right[j])
                    vals[k] = right[j]
                    j = j + 1
                self.setcolor(k + offset, 'blue')
                k = k + 1
                self.__wait()

            while i < len(left):
                self.setcolor(k + offset, 'blue')
                self.setheight(k + offset, left[i])
                vals[k] = left[i]
                i = i + 1
                k = k + 1
                self.__wait()

            while j < len(right):
                self.setcolor(k + offset, 'blue')
                self.setheight(k + offset, right[j])
                vals[k] = right[j]
                j = j + 1
                k = k + 1
                self.__wait()

            for i in range(offset, len(vals)):
                self.setcolor(i, '#000')

    @check_if_running
    def quicksort(self):
        self.__quicksort_helper(0, len(self.r_ids) - 1)

    def __quicksort_helper(self, first, last):
        if first < last:
            split = self.__quicksort_partition(first, last)
            self.__quicksort_helper(first, split - 1)
            self.__quicksort_helper(split + 1, last)

    def __quicksort_partition(self, first, last):
        pivot_val = self.getheight(first)
        left_mark = first + 1
        right_mark = last
        done = False
        
        while not done:
            while left_mark <= right_mark and self.getheight(left_mark) <= pivot_val:
                self.setcolor(left_mark, 'red')
                self.__wait()
                self.setcolor(left_mark, '#000')
                left_mark = left_mark + 1
            while left_mark <= right_mark and self.getheight(right_mark) >= pivot_val:
                self.setcolor(right_mark, 'red')
                self.__wait()
                self.setcolor(right_mark, '#000')
                right_mark = right_mark - 1
            if right_mark < left_mark:
                done = True
            else: 
                self.swap(left_mark, right_mark)
                self.__wait()

        self.swap(first, right_mark)
        self.__wait()
        return right_mark

    @check_if_running
    def shellsort(self):
        sublist_count = len(self.r_ids) // 2
        while sublist_count > 0:
            for pos_start in range(sublist_count):
                self.__shellsort_gap_insertion(pos_start, sublist_count)
            sublist_count = sublist_count // 2

    def __shellsort_gap_insertion(self, start, gap):
        for i in range(start + gap, len(self.r_ids), gap):
            cur_val = self.getheight(i)
            cur_pos = i
            while cur_pos >= gap and self.getheight(cur_pos - gap) > cur_val:
                self.setcolor(cur_pos, 'red')
                self.setheight(cur_pos, self.getheight(cur_pos - gap))
                cur_pos = cur_pos - gap
                self.setheight(cur_pos, 0)
                self.__wait()
                self.setcolor(cur_pos + gap, '#000')
            self.setheight(cur_pos, cur_val)
