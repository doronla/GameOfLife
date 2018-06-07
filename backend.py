import numpy as np


def generate_random_position(x, y):
    return np.random.randint(0, 2, size=x * y).reshape(x, y)
    

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
