import tkinter as tk
import backend as b
import time

import tkinter.messagebox


DEFAULT_X_SIZE = 10
DEFAULT_Y_SIZE = 10
DEFAULT_PROB = 0
DEFAULT_CYCLE = 100


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.create_ui(master)
        self.state = None
        self.iteration = 0

    # TODO(aelphy): add max_epochs parameter
    # TODO(aelphy): add parameter illness duration
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

        tk.Label(master, text="Number of Periods").grid(row=3)
        self.cycle = tk.Entry(master)
        self.cycle.insert(10, str(DEFAULT_CYCLE))
        self.cycle.grid(row=3, column=1)

        self.rnd = tk.IntVar()
        tk.Checkbutton(master, text="Random initial position", variable=self.rnd).grid(row=4)

        self.regenerate_grid_button = tk.Button(master, text="Regenerate Grid", command=self.regenerate_grid)
        self.regenerate_grid_button.grid(row=5, column=0)

        self.quit_button = tk.Button(master, text="Quit", command=quit)
        self.quit_button.grid(row=5, column=1)

        self.start_button = tk.Button(master, text="Start", command=self.start)
        self.start_button.grid(row=6, column=0)

        self.end_button = tk.Button(master, text="Stop", command=self.stop)
        self.end_button.grid(row=6, column=1)
        self.end_button.configure(state=tk.DISABLED)

        self.field = []
        for i in range(int(self.x.get())):
           self.field.append([])

           for j in range(int(self.y.get())):
               self.field[-1].append(tk.Button(self.master, bg="white", width=2, height=1))
               self.field[-1][-1].grid(row=i, column=3 + j)
               self.field[-1][-1]['command'] = self.gen_cell_click_func(self.field[-1][-1])

    def gen_cell_click_func(self, cell):
        def f():
            self.cell_toggle(cell)

        return f

    def cell_toggle(self, cell):
        if cell['bg'] == "white":
            cell['bg'] = "red"
        else:
            cell['bg'] = "white"

    def regenerate_grid(self):
        try:
            for i in range(len(self.field)):
                for j in range(len(self.field[i])):
                    self.field[i][j].destroy()

            self.field = []

            for i in range(int(self.x.get())):
               self.field.append([])

               for j in range(int(self.y.get())):
                   self.field[-1].append(tk.Button(self.master, bg="white", width=2, height=1))
                   self.field[-1][-1].grid(row=i, column=3 + j)
                   self.field[-1][-1]['command'] = self.gen_cell_click_func(self.field[-1][-1])
        except ValueError:
            tk.messagebox.showinfo("Game of Life", "Axis must be an integer")

    def draw_state(self, state):
        assert(state.shape[0] == len(self.field))
        assert(state.shape[1] == len(self.field[0]))

        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if state[i, j] == 0:
                    self.field[i][j]['bg'] = 'white'
                elif self.field[i][j] == -1:
                    self.field[i][j]['bg'] = 'black'
                elif 1 <= state[i, j] <= 4:  # 4 here is the duration of illness
                    self.field[i][j]['bg'] = 'red'
                else:
                    tk.messagebox.showinfo("Game of Life", "smth went wrong, check the code, wrong value of the cell")

    # TODO(aelphy): add the possibility to add dead cells in the initial configuration
    # TODO(aelphy): add parameters of random initialization as a parameter
    # TODO(aelphy): add maximal game duration as a parameter: DONE
    # TODO(aelphy): think about immunity
    def start(self):
        if not (0 <= int(self.rnd.get()) <= 1):
            tk.messagebox.showinfo("Game of Life", "Entry must be between 0 and 1")
            return

        self.end_button.configure(state=tk.NORMAL)
        self.start_button.configure(state=tk.DISABLED)
        self.regenerate_grid_button.configure(state=tk.DISABLED)

        self.state = b.gen_initial_state(int(self.x.get()), int(self.y.get()), 4, int(self.rnd.get()) == 1)  # 4 here is the duration of illness

        if int(self.rnd.get()) == 1:
            self.draw_state(self.state)
        else:
            for i in range(len(self.field)):
                for j in range(len(self.field[i])):
                    if self.field[i][j]['bg'] == 'white':
                        self.state[i, j] = 0
                    elif self.field[i][j]['bg'] == 'red':
                        self.state[i, j] = 1
                    else:
                        tk.messagebox.showinfo("Game of Life", "smth went wrong, check the code, wrong value of the cell")

        while True:
            period = 0
            # if the state is stable stop the game
            if b.is_stable(self.state) or period == int(self.cycle.get()):
                 self.stop()
                 return

            self.state = b.next_state(self.state, float(self.prob.get()))
            self.draw_state(self.state)
            period += 1

    def stop(self):
        self.end_button.configure(state=tk.DISABLED)
        self.start_button.configure(state=tk.NORMAL)

if __name__ == '__main__':
    root = tk.Tk()
    game = Application(root)
    root.mainloop()
