import numpy as np


def gen_initial_state(x, y, n, is_random):
    if is_random:
        return np.random.randint(0, 2, size=x * y).reshape(x, y)
    else:
        return np.zeros((x, y))


def is_stable(state):
    return len(state[(state == -1) | (state == 0)]) == np.prod(state.shape)


def next_state(prev_state, prob):
    new_state = np.zeros_like(prev_state)

    for i in range(prev_state.shape[0]):
        for j in range(prev_state.shape[1]):

            if prev_state[i, j] == -1 and neighbour_count(prev_state, i, j) == 3:
                new_state[i, j] = 0
            else:
                if 0 < prev_state[i, j] <= 4:
                    new_state[i, j] += 1
                elif prev_state[i, j] == 5:
                    new_state[i, j] = np.random.randint(2)
                elif prev_state[i, j] >= 0 and neighbour_count(prev_state, i, j) < 2 or neighbour_count(prev_state, i, j) > 3:
                    new_state[i, j] = -1
                else:
                    new_state[i, j] = prev_state[i, j]

            if 0 < prev_state[i, j] <= 5:
                for k in range(i - 1, i + 2):
                    for m in range(j - 1, j + 2):
                        if (k != i or m != j) and prev_state[i, j] == 0:
                            new_state[i, j] = 1


def neighbour_count(prev_state, x, y):
    count = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i == x and j == y:
                continue
            if i == -1 or j == -1:
                continue
            try:
                if prev_state[i, j] >= 0:
                    count += 1
            except IndexError:
                pass

    return count


### PRIVATE INERNAL FUNCTIONS

#def ill_neighbours_present(prev_state, i, j):
#    for i in range(int(x.get())):
#        for j in range(int(y.get())):
#            if matrix[i][j] == -1 and count == 3:
#                new[i][j] == 0
#            elif matrix[i][j] >= 0 and count < 2 or count > 3:
#                new[i][j] = -1
#            else:
#                new[i][j] = current[i][j]
#
#    illness()
#    spreading_illness()
#
#    new = current
#
#
#def neighbour_count():
#    count = 0
#    x,y = current(i, j)
#    for i in (x - 1, x, x + 1):
#        for j in (y - 1, y, y + 1):
#            if i == x and j == y:
#                continue
#            if i == -1 or j == -1:
#                continue
#            try:
#                if current[i][j] >= 0:
#                    count += 1
#            except IndexError:
#                pass
#
#
#def spreading_illness(current, new):
#    x, y = current(i, j)
#    for i in (x - 1, x, x + 1):
#        for j in (y - 1, y, y + 1):
#            if np.random.uniform(0, 1) < float(fe.prob) and current[x][y] == 1:
#                new[i][j] = 1
#
#
#def illness(current, new):
#    for i in range(int(x.get())):
#        for j in range(int(y.get())):
#            if 1 <= matrix[i][j] < 5:
#                new[i][j] = current[i][j] + 1
#            elif matrix[i][j] == 5:
#                new[i][j] = np.random.choice((-1, 0))
#
#def simulate():
#    periods = 0
#
#    if rnd.get() == 0:
#        custom_start()
#    else:
#        random_start()
#
#    global current
#    current = matrix.copy
#
#    rules()
#
#    render()
#
#    periods += 1
#
#
