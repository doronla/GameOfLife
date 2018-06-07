# PSEUDO CODE
import numpy as np


np.random.seed(42)


#class Backend:
#
#    def __init__(self, size_x, size_y):
#        self.size_x = size_x
#        self.size_y = size_y
#        self.initial_matrix = []
#
#
#    def initial_state(self):
#        np.random.seed(42)
#        self.initial_matrix = np.full((self.size_x, self.size_y), -1, dtype=int)
#        mask = np.product(self.initial_matrix.shape)
#        self.initial_matrix.ravel()[np.random.randint(1, mask, size=10)] = np.random.rand(10)
#        #        np.place(initial_matrix, initial_matrix == 0, 1)
#        return self.initial_matrix
#
#    def random_start(self):
#        self.initial_state()
#        for x in np.nditer(self.initial_matrix):
#            if np.random.randint(2) == 1:
#                x += 1
#        print(test.initial_matrix)


def random_start():
    global matrix
    matrix = [[(np.random.choice((-1, 0))) for i in range(10)] for j in range(10)]
    print(matrix)
#    for i in range(10):
#        for j in range(10):
#            if matrix[i][j] == 0:
#                fe.self.field[i][j]['bg'] = ["black"]


def custom_start():
    matrix = [[-1 for i in range(10)] for j in range(10)]

def rules(current, count):
    new = np.zeros_like(matrix)
    for i in range(int(x.get())):
        for j in range(int(y.get())):
            if matrix[i][j] == -1 and count == 3:
                new[i][j] == 0
            elif matrix[i][j] >= 0 and count < 2 or count > 3:
                new[i][j] = -1
            else:
                new[i][j] = current[i][j]

    illness()
    spreading_illness()

    new = current


def neighbour_count():
    count = 0
    x,y = current(i, j)
    for i in (x - 1, x, x + 1):
        for j in (y - 1, y, y + 1):
            if i == x and j == y:
                continue
            if i == -1 or j == -1:
                continue
            try:
                if current[i][j] >= 0:
                    count += 1
            except IndexError:
                pass


def spreading_illness(current, new):
    x, y = current(i, j)
    for i in (x - 1, x, x + 1):
        for j in (y - 1, y, y + 1):
            if np.random.uniform(0, 1) < float(fe.prob) and current[x][y] == 1:
                new[i][j] = 1


def illness(current, new):
    for i in range(int(x.get())):
        for j in range(int(y.get())):
            if 1 <= matrix[i][j] < 5:
                new[i][j] = current[i][j] + 1
            elif matrix[i][j] == 5:
                new[i][j] = np.random.choice((-1, 0))

def simulate():
    periods = 0

    if rnd.get() == 0:
        custom_start()
    else:
        random_start()

    global current
    current = matrix.copy

    rules()

    render()

    periods += 1


def render():
    for i in range(int(x.get())):
        for j in range(int(y.get())):
            if new[i][j] == 0:
                fe.field[i][j]['bg'] = ["black"]
            elif new[i][j] > 0:
                fe.field[i][j]['bg'] = ["red"]
            else:
                fe.field[i][j]['bg'] = ["white"]


