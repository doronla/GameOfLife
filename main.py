import tkinter as tk
import time


DEFAULT_X_SIZE = 10
DEFAULT_Y_SIZE = 10
DEFAULT_PROB = 0.2


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.create_ui(master)

    def create_ui(self, master):
        master.title("Game of Life")
        self.grid(row=10, column=10)

        tk.Label(master, text="Size x-Axis").grid(row=0)
        self.x = tk.Entry(master)
        self.x.insert(10, str(DEFAULT_X_SIZE))
        self.x.grid(row=0, column=1)

        tk.Label(master, text="Size y-Axis").grid(row=1)
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

        self.start_button = tk.Button(master, text="Start", command=self.start)
        self.start_button.grid(row=5, column=0)

        self.end_button = tk.Button(master, text="Stop", command=self.stop)
        self.end_button.grid(row=5, column=1)
        self.end_button.configure(state=tk.DISABLED)

        self.field = []
        for i in range(int(self.x.get())):
            self.field.append([])

            for j in range(int(self.y.get())):
                self.field[-1].append(tk.Button(master, bg="white", width=2, height=1))
                self.field[-1][-1].grid(row=5 + i, column=3 + j)

    def regenerate_grid(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    game = Application(root)
    root.mainloop()
