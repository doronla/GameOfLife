import tkinter as tk
from tkinter import *
from tkinter import messagebox
import time
from backend import *

DEFAULT_X_SIZE = 10
DEFAULT_Y_SIZE = 10
DEFAULT_PROB = 0


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.create_ui(master)
        self.field = []


    def create_ui(self, master):
        master.title("Game of Life")
        self.grid(row=10, column=10)

        tk.Label(master, text="Size x-Axis").grid(row=0)
        global x
        self.x = tk.Entry(master)
        self.x.insert(10, str(DEFAULT_X_SIZE))
        self.x.grid(row=0, column=1)

        tk.Label(master, text="Size y-Axis").grid(row=1)
        global y
        self.y = tk.Entry(master)
        self.y.insert(10, str(DEFAULT_X_SIZE))
        self.y.grid(row=1, column=1)

        tk.Label(master, text="Probability of Sickness").grid(row=2)
        self.prob = tk.Entry(master)
        self.prob.insert(10, str(DEFAULT_PROB))
        self.prob.grid(row=2, column=1)

        self.rnd = tk.IntVar()
        tk.Checkbutton(master, text="Random initial position", variable=self.rnd).grid(row=3)

        self.regenerate_grid_button = tk.Button(master, text="Regenerate Grid", command=self.regenerate_grid)
        self.regenerate_grid_button.grid(row=4, column=0)

        self.quit_button = tk.Button(master, text="Quit", command=quit)
        self.quit_button.grid(row=4, column=1)

        self.start_button = tk.Button(master, text="Start", command=random_start)
        self.start_button.grid(row=5, column=0)

        self.end_button = tk.Button(master, text="Stop", command=self.stop)
        self.end_button.grid(row=5, column=1)
        self.end_button.configure(state=tk.DISABLED)

#        self.field = []
#        for i in range(int(self.x.get())):
#            self.field.append([])
#
#            for j in range(int(self.y.get())):
#                self.field[-1].append(tk.Button(self.master, bg="white", width=2, height=1))
#                self.field[-1][-1].grid(row=0 + i, column=3 + j)

        self.field = [[Button(self.master, bg="white", width=2, height=1) for i in range(int(self.x.get()) + 2)]
                             for j in range(int(self.y.get()) + 2)]

        for i in range(0, int(self.x.get()) + 1):
            for j in range(0, int(self.y.get()) + 1):
                self.field[-i][j].grid(row=0 + i, column=3 + j)
                # in a custom game, the user turns the cells dead or alive on their own
                self.field[i][j]['command'] = lambda i=i, j=j: self.cell_toggle(self.field[i][j])


    def cell_toggle(self, cell):
        if cell['bg'] == "white":
            cell['bg'] = "black"
        else:
            cell['bg'] = "white"

    def regenerate_grid(self):

        try:
            for i in range(int(self.x.get())):
                self.field.append([])

                for j in range(int(self.y.get())):
                    self.field[-1].append(tk.Button(self.master, bg="white", width=2, height=1))
                    self.field[-1][-1].grid(row=0 + i, column=3 + j)
        except ValueError:
            tk.messagebox.showinfo("Game of Life", "Axis must be an integer")

    def start(self, matrix, loop):
        if 0 <= int(self.rnd.get()) <= 1:
            pass
        else:
            tk.messagebox.showinfo("Game of Life", "Entry must be between 0 and 1")
            stop()
            return

        self.end_button.configure(state=tk.NORMAL)
        random_start()

        for i in range(int(self.x.get())):
            for j in range(int(self.y.get())):
                if matrix[i][j] == 0:
                    self.field[i][j]['bg'] = ["black"]

    #        global loop
    #        while loop == True:
    #
    #            simulate()
    #
    #            if len(current[(current == -1) | (current == 0)] == np.prod(current.shape):
    #               print(It took {} periods to eliminate the disease).format(periods)
    #                break
    #
    #            time.sleep(1)

    def stop(self):
        loop = False
        self.regenerate_grid()
        pass


if __name__ == '__main__':
    root = tk.Tk()
    game = Application(root)
    root.mainloop()
