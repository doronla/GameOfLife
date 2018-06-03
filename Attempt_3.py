from tkinter import *
import random
import time


class Start(Frame):

    def __init__(self, start):
        Frame.__init__(self, start)
        self.start = start
        self.grid(row=0, column=0)

        self.start_window()

    # creates Start UI to insert all parameters
    def start_window(self):
        self.start.title("Game of Life")

        Label(root, text="Size x-Axis").grid(row=0)
        self.get_x = Entry(root)
        self.get_x.insert(10, "20")
        self.get_x.grid(row=0, column=1)

        Label(root, text="Size y-Axis").grid(row=1)
        self.get_y = Entry(root)
        self.get_y.insert(10, "20")
        self.get_y.grid(row=1, column=1)

        Label(root, text="Probability of Sickness").grid(row=2)
        self.probs = Entry(root)
        self.probs.insert(10, "0.2")
        self.probs.grid(row=2, column=1)

        self.rdm = IntVar()
        Checkbutton(root, text="Random Game", variable=self.rdm).grid(row=3)

        self.generate = Button(root, text="Generate Grid", command=self.generate_grid)
        self.generate.grid(row=4, column=0)
        self.quit_button = Button(root, text="Quit Game", command=quit)
        self.quit_button.grid(row=4, column=1)

    # creates new window and starts the actual game class
    def generate_grid(self):
        window = Tk()
        self.game = GameOfLife(window)


class GameOfLife(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.parent = parent
        self.grid(row=0, column=0)

        self.size_x = int(game.get_x.get())
        self.size_y = int(game.get_y.get())
        self.cell_buttons = []
        self.simulation_cycle = 0
        self.generate_next = True

        self.initialUI()

    # creates a raw UI for the game
    def initialUI(self):
        self.parent.title("Game of Life")

        self.title_frame = Frame(self.parent)
        self.title_frame.grid(row=0, column=0, columnspan=4)

        title = Label(self.title_frame, text="Conway's Game of Life")
        title.pack(side=TOP)

        prompt = Label(self.title_frame,
                       text="Click the cells to create the starting configuration, then press Start Game:")
        prompt.pack(side=BOTTOM)

        self.build_grid()

        # depending whether you play a random generation or custom build, different commands apply
        if game.rdm.get() == 0:
            self.start_button = Button(self.parent, text="Start Game", command=self.simulate_game)
        elif game.rdm.get() == 1:
            self.start_button = Button(self.parent, text="Start New", command=self.build_grid)
        self.start_button.grid(row=1, column=1, sticky=E)

        self.reset_button = Button(self.parent, text="Reset Game", command=self.reset_game)
        self.reset_button.grid(row=1, column=2, sticky=W)

    # builds the grid with cells
    def build_grid(self):
        self.game_frame = Frame(
            self.parent, width=self.size_x, height=self.size_y + 2, borderwidth=1, relief=SUNKEN)
        self.game_frame.grid(row=2, column=0, columnspan=4)

        self.cell_buttons = [[Button(self.game_frame, bg="white", width=2, height=1) for i in range(self.size_x + 2)]
                             for j in range(self.size_y + 2)]

        for i in range(1, self.size_y + 1):
            for j in range(1, self.size_x + 1):
                self.cell_buttons[i][j].grid(row=i, column=j, sticky=W + E)
                # in a custom game, the user turns the cells dead or alive on their own
                if game.rdm.get() == 0:
                    self.cell_buttons[i][j]['command'] = lambda i=i, j=j: self.cell_toggle(self.cell_buttons[i][j])
                # in a random game, the cells will be selected randomly whether alive or dead
                elif game.rdm.get() == 1:
                    self.cell_buttons[i][j]['command'] = self.random_select(self.cell_buttons[i][j])

        # in a random game, the game starts automatically
        if game.rdm.get() == 1:
            self.simulate_game()

    # randomly selects a cell dead or alive
    def random_select(self, cell):
        color = ["white", "black"]
        cell['bg'] = random.choice(color)

    # main function for the fame simulation
    def simulate_game(self):

        # a sick cell will either die or become healthy
        for i in range(1, self.size_y + 1):
            for j in range(1, self.size_x + 1):
                if self.cell_buttons[i][j]['bg'] == "red":
                    color = ["black", "white"]
                    self.cell_buttons[i][j]['bg'] = random.choice(color)

        # applies the rules of over- or underpopulation to each cell
        buttons_to_toggle = []
        for i in range(1, self.size_y + 1):
            for j in range(1, self.size_x + 1):
                coord = (i, j)
                if self.cell_buttons[i][j]['bg'] == "white" and self.neighbour_count(i, j) == 3:
                    buttons_to_toggle.append(coord)
                elif self.cell_buttons[i][j]['bg'] != "white" and self.neighbour_count(i, j) != 3 and \
                        self.neighbour_count(i, j) != 2:
                    buttons_to_toggle.append(coord)

        # a live cell can become sick with a given probability
        for i in range(1, self.size_y + 1):
            for j in range(1, self.size_x + 1):
                if random.uniform(0, 1) < float(game.probs.get()) and self.cell_buttons[i][j]['bg'] == "black":
                    self.cell_buttons[i][j]['bg'] = "red"

        # each cell that changes will transform
        for coord in buttons_to_toggle:
            self.cell_toggle(self.cell_buttons[coord[0]][coord[1]])

        # the simulation cycle continues
        if self.generate_next:
            self.after(100, self.simulate_game)
        else:
            self.enable_buttons()

        self.simulation_cycle += 1

#    def disable_buttons(self):
#
#        if self.cell_buttons[1][1] != DISABLED:
#            for i in range(0, self.size_y + 2):
#                for j in range(0, self.size_x + 2):
#                    self.cell_buttons[i][j].configure(state=DISABLED)
#
#            #           self.reset_button.configure(state = NORMAL)
#            self.start_button.configure(state=DISABLED)
#
    def enable_buttons(self):

        for i in range(0, self.size_y + 2):
            for j in range(0, self.size_x + 2):
                self.cell_buttons[i][j]['bg'] = "white"
                self.cell_buttons[i][j].configure(state=NORMAL)

        #        self.reset_button.configure(state = DISABLED)
        self.start_button.configure(state=NORMAL)
        self.generate_next = TRUE

    # each neighbour to a cell will be counted in order to aplly the rules
    def neighbour_count(self, x_coord, y_coord):
        count = 0
        for i in range(x_coord - 1, x_coord + 2):
            for j in range(y_coord - 1, y_coord + 2):
                if (i != x_coord or j != y_coord) and self.cell_buttons[i][j]['bg'] == "black":
                    count += 1

        return count

    # changes the color if the cell transforms
    def cell_toggle(self, cell):
        if cell['bg'] == "white":
            cell['bg'] = "black"
        else:
            cell['bg'] = "white"

    # resets the game
    def reset_game(self):
        self.generate_next = False


if __name__ == '__main__':
    root = Tk()
    game = Start(root)
    root.mainloop()
