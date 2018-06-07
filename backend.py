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
            if prev_state[i, j] == -1:
                # if alive_neighbour_count(prev_state, i, j) != 3:
                new_state[i, j] = -1
            else:
                if 1 <= prev_state[i, j] <= 3:
                    new_state[i, j] = prev_state[i, j] + 1
                elif prev_state[i, j] == 4:
                    new_state[i, j] = np.random.choice([-1, 0])
                # elif alive_neighbour_count(prev_state, i, j) < 2 or alive_neighbour_count(prev_state, i, j) > 3:
                #     new_state[i, j] = -1
                elif prev_state[i, j] == 0:
                    for cell in give_neighbours(prev_state, i, j):
                        if cell > 0:
                            if np.random.random() <= prob:
                                new_state[i, j] = 1
                            else:
                                new_state[i, j] = np.max(new_state[i, j], 0)

    return new_state


def give_neighbours(state, x, y):
    result = []

    try:
        result.append(state[x, y - 1])
    except:
        pass

    try:
        result.append(state[x, y + 1])
    except:
        pass

    try:
        result.append(state[x - 1, y])
    except:
        pass

    try:
        result.append(state[x + 1, y])
    except:
        pass

    try:
        result.append(state[x + 1, y + 1])
    except:
        pass

    try:
        result.append(state[x + 1, y - 1])
    except:
        pass

    try:
        result.append(state[x - 1, y + 1])
    except:
        pass

    try:
        result.append(state[x - 1, y - 1])
    except:
        pass

    return result


def alive_neighbour_count(prev_state, x, y):
    count = 0

    for cell in give_neighbours(prev_state, x, y):
        if cell != -1:
            count += 1

    return count
