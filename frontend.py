# import the tkinter and numpy modules and load the backend file
import tkinter as tk
import tkinter.messagebox
import numpy as np
import backend as b

# set the default values
DEFAULT_X_SIZE = 10
DEFAULT_Y_SIZE = 10
DEFAULT_PROB = 0.5
DEFAULT_DURATION = 5
DEFAULT_IMMUNITY = 5
DEFAULT_CYCLE = 100


# The frontend only works on the UI and the visual implementation of the game
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.create_ui(master)
        self.state = None
        self.running = False
        self.after(500, self.manage)

    def create_ui(self, master):
        # This function creates the UI with all entries and buttons and builds a first grid.
        master.title("Game of Life")
        self.grid(row=10, column=10)

        # Entry for x-Axis
        tk.Label(master, text="Size x-Axis").grid(row=0)
        self.x = tk.Entry(master)
        self.x.insert(10, str(DEFAULT_X_SIZE))
        self.x.grid(row=0, column=1)

        # Entry for y-Axis
        tk.Label(master, text="Size y-Axis").grid(row=1)
        self.y = tk.Entry(master)
        self.y.insert(10, str(DEFAULT_X_SIZE))
        self.y.grid(row=1, column=1)

        # Entry for Probability of spreading the illness
        tk.Label(master, text="Probability of Spreading").grid(row=2)
        self.prob = tk.Entry(master)
        self.prob.insert(10, str(DEFAULT_PROB))
        self.prob.grid(row=2, column=1)

        # Entry for duration of illness
        tk.Label(master, text="Duration of Illness").grid(row=3)
        self.duration = tk.Entry(master)
        self.duration.insert(10, str(DEFAULT_DURATION))
        self.duration.grid(row=3, column=1)

        # Entry for duration of immunity
        tk.Label(master, text="Duration of Immunity").grid(row=4)
        self.immunity = tk.Entry(master)
        self.immunity.insert(10, str(DEFAULT_IMMUNITY))
        self.immunity.grid(row=4, column=1)

        # Entry for cycle limit
        tk.Label(master, text="cycle limit").grid(row=5)
        self.cycle = tk.Entry(master)
        self.cycle.insert(10, str(DEFAULT_CYCLE))
        self.cycle.grid(row=5, column=1)

        # Checkbutton for random selection start
        self.rnd = tk.IntVar()
        tk.Checkbutton(master, text="Random initial position", variable=self.rnd).grid(row=6)

        # Button for regenerating the grid
        self.regenerate_grid_button = tk.Button(master, text="Regenerate Grid", command=self.regenerate_grid)
        self.regenerate_grid_button.grid(row=7, column=0)

        # Button to quit the whole application
        self.quit_button = tk.Button(master, text="Quit", command=quit)
        self.quit_button.grid(row=7, column=1)

        # Button to start the game
        self.start_button = tk.Button(master, text="Start", command=self.validate)
        self.start_button.grid(row=8, column=0)

        # Button to stop the game during the process
        self.end_button = tk.Button(master, text="Stop", command=self.stop)
        self.end_button.grid(row=8, column=1)
        self.end_button.configure(state=tk.DISABLED)

        # building a grid from a 2D-Array containing buttons to toggle
        self.field = []
        for i in range(int(self.x.get())):
            self.field.append([])

            for j in range(int(self.y.get())):
                self.field[-1].append(tk.Button(self.master, bg="white", width=2, height=1))
                self.field[-1][-1].grid(row=i, column=3 + j)
                self.field[-1][-1]['command'] = self.gen_cell_click_func(self.field[-1][-1])

    def gen_cell_click_func(self, cell):
        # This functions allows to switch the color of a button when it is clicked
        def f():
            # In order to execute the function properly and display the colors, it has to be nested
            self.cell_toggle(cell)

        return f

    def cell_toggle(self, cell):
        # Actually changes the button's color
        # If clicked while white, turn red
        if cell['bg'] == "white":
            cell['bg'] = "red"
        # If clicked while red, turn black
        elif cell['bg'] == "red":
            cell['bg'] = "black"
        # If anything else (black), turn white
        else:
            cell['bg'] = "white"

    def regenerate_grid(self):
        # If one wants a different grid size, he can click the 'Regenerate Grid'-button
        # to either create a grid with a new scale or a new blank grid
        try:
            # prevents negative numbers
            if int(self.x.get()) < 1 or int(self.y.get()) < 1 or int(self.cycle.get()) < 1:
                tk.messagebox.showinfo("Game of Life", "Invalid Entry. Must be integer greater than 0.")
            # generates a new grid
            else:
                # destroys the old grid
                for i in range(len(self.field)):
                    for j in range(len(self.field[i])):
                        self.field[i][j].destroy()

                # empties the old array
                self.field = []

                # generates the new grid
                for i in range(int(self.x.get())):
                    self.field.append([])

                    for j in range(int(self.y.get())):
                        self.field[-1].append(tk.Button(self.master, bg="white", width=2, height=1))
                        self.field[-1][-1].grid(row=i, column=3 + j)
                        self.field[-1][-1]['command'] = self.gen_cell_click_func(self.field[-1][-1])
        # In case of a wrong value (i.e. string), an error message is shown
        except ValueError:
            tk.messagebox.showinfo("Game of Life", "Axis must be an integer")

    def validate(self):
        # To prevent invalid entries, all parameters must be first validated
        try:
            # x-Axis, y-Axis, duration of illness, and Cycles all must be greater than or equal one
            if int(self.x.get()) < 1 or int(self.y.get()) < 1 or int(self.duration.get()) < 0 or int(self.cycle.get()) < 1:
                tk.messagebox.showinfo("Game of Life", "Invalid Entry. Must be integer greater than or equal 1.")
            # Immunity must be a positive integer
            elif int(self.immunity.get()) < 0:
                tk.messagebox.showinfo("Game of Life", "Invalid Entry. Must be integer greater than or equal 0.")
            # The probability of spreading the illness has to be a float between 0 and 1
            elif not 0 <= float(self.prob.get()) <= 1:
                tk.messagebox.showinfo("Game of Life", "Invalid Entry. Must be float between 0 and 1.")
            # If all conditions are met, the game can start
            else:
                self.start()
        # In case of a wrong value (i.e. string), an error message is shown
        except ValueError:
            tk.messagebox.showinfo("Game of Life", "Invalid entry")

    def start(self):
        # After validation, the proocess will be started
        # To prevent any crashes, all entry fields are disabled while the game runs
        self.x.configure(state=tk.DISABLED)
        self.y.configure(state=tk.DISABLED)
        self.prob.configure(state=tk.DISABLED)
        self.duration.configure(state=tk.DISABLED)
        self.immunity.configure(state=tk.DISABLED)
        self.cycle.configure(state=tk.DISABLED)

        self.start_button.configure(state=tk.DISABLED)
        self.regenerate_grid_button.configure(state=tk.DISABLED)

        # The "Stop"-button is now enabled
        self.end_button.configure(state=tk.NORMAL)

        # A counter keeps track of how many iterations ocurred
        self.period = 0

        # while True, the iteration is looping infinitely
        self.running = True

        # A matrix is created from the backend and is called state
        self.state = b.gen_initial_state(int(self.x.get()), int(self.y.get()), int(self.rnd.get()) == 1)

        if int(self.rnd.get()) == 1:
            # If the cells are selected randomly, the grid has to be drawn according to the matrix
            self.draw_state(self.state)
        else:
            # Vice versa in custom build. The matrix has to be changed according to the grid.
            for i in range(len(self.field)):
                for j in range(len(self.field[i])):
                    # If the field is alive, change the matrix element to 0.
                    if self.field[i][j]['bg'] == 'white':
                        self.state[i, j] = 0
                    # If the field is ill, change the matrix element to 1.
                    elif self.field[i][j]['bg'] == 'red':
                        self.state[i, j] = 1
                    # If the field is dead, change the matrix element to negative infinity.
                    elif self.field[i][j]['bg'] == 'black':
                        self.state[i, j] = -np.inf
                    else:
                        tk.messagebox.showinfo("Game of Life",
                                               "something went wrong, check the code, wrong value of the cell")

    def draw_state(self, state):
        # visualization of the matrix
        assert (state.shape[0] == len(self.field))
        assert (state.shape[1] == len(self.field[0]))

        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                # The field is alive if the element is between the immunity parameter and 0
                if -int(self.immunity.get()) <= state[i, j] <= 0:
                    self.field[i][j]['bg'] = 'white'
                # The field is dead if the element is negative infinity
                elif state[i, j] == -np.inf:
                    self.field[i][j]['bg'] = 'black'
                # The field is ill if the element is between 1 and the duration parameter
                elif 1 <= state[i, j] <= int(self.duration.get()):
                    self.field[i][j]['bg'] = 'red'
                else:
                    tk.messagebox.showinfo("Game of Life",
                                           "something went wrong, check the code, wrong value of the cell")

    def manage(self):
        # this function is called in the __init__ function and manages the infinite loop
        if self.running:
            # while True, the iteration keeps going
            self.next_iter()
        # In order to run fluently, the function waits half a second before calling itself
        self.after(500, self.manage)

    def next_iter(self):

        # if the state is stable or the iteration reaches the limit stop the game
        if b.is_stable(self.state) or self.period == int(self.cycle.get()):
            self.stop()
            # Different messages appear, depending on stop condition
            if b.is_stable(self.state):
                tk.messagebox.showinfo("Game of Life", "Stable state after {} periods".format(self.period))
            else:
                tk.messagebox.showinfo("Game of Life", "Cycle limit reached!")
            return

        # A function is called from the backend to refresh the matrix
        self.state = b.next_state(self.state, float(self.prob.get()), int(self.duration.get()),
                                  int(self.immunity.get()))
        # The visualisation is changed according to the new matrix
        self.draw_state(self.state)
        self.period += 1

    def stop(self):
        # This function stops the game during the process
        # All the disabled fields arenabled again
        self.x.configure(state=tk.NORMAL)
        self.y.configure(state=tk.NORMAL)
        self.prob.configure(state=tk.NORMAL)
        self.duration.configure(state=tk.NORMAL)
        self.immunity.configure(state=tk.NORMAL)
        self.cycle.configure(state=tk.NORMAL)

        self.end_button.configure(state=tk.DISABLED)
        self.start_button.configure(state=tk.NORMAL)
        self.regenerate_grid_button.configure(state=tk.NORMAL)

        # The boolean value is set to False to break the iteration
        self.running = False


if __name__ == '__main__':
    # The application is created
    root = tk.Tk()
    game = Application(root)
    root.mainloop()
