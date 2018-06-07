import numpy as np


def gen_initial_state(x, y, is_random):
    # Creating the initial state
    # If the game has randomly started, create a 2D-Array with elements containing randomly selected 0 or 1
    if is_random:
        return np.random.randint(0, 2, size=x * y).reshape(x, y).astype("float")
    # In a custom build, create a 2D-Array containing only 0 for later use
    else:
        return np.zeros((x, y))


def next_state(prev_state, prob, d, im):
    # To play the game correctly, we need every time a new array to store the new elements. Otherwise the neighbours are
    # not counted properly.
    new_state = np.zeros_like(prev_state)

    # With the following rules, the new array is set
    for i in range(prev_state.shape[0]):
        for j in range(prev_state.shape[1]):
            # If the element in the previous array was dead, it stays dead
            if prev_state[i, j] == -np.inf:
                new_state[i, j] = -np.inf
            else:
                # If the element in the previous array was ill, it is one step closer to the moment of decision.
                if 1 <= prev_state[i, j] <= d - 1:
                    new_state[i, j] = prev_state[i, j] + 1
                # If the element in the previous array was ill and reaches the moment of decision,
                # it will either die or be healthy again and obtain immunity
                elif prev_state[i, j] == d:
                    new_state[i, j] = np.random.choice([-np.inf, -im])
                # If the element in the previous array was immune, it is one step closer to losing immunity
                elif -im <= prev_state[i, j] < 0:
                    new_state[i, j] = prev_state[i, j] + 1
                # If the element in the previous array was healthy, there are two possibilities
                elif prev_state[i, j] == 0:
                    for cell in give_neighbours(prev_state, i, j, d):
                        if cell > 0:
                            # If the cell has at least one ill neighbour, it can get with a certain probability also ill
                            if np.random.random() <= prob:
                                new_state[i, j] = 1
                            else:
                                new_state[i, j] = np.max(new_state[i, j], 0)
    return new_state


def give_neighbours(state, x, y, d):
    # This function counts all ill neighbours. However, a cell on the edge might noght have all 8 neighbours.
    # In that case, the condition is passed
    result = []

    try:
        if 1 <= state[x, y - 1] <= d:
            result.append(state[x, y - 1])
    except:
        pass

    try:
        if 1 <= state[x, y + 1] <= d:
            result.append(state[x, y + 1])
    except:
        pass

    try:
        if 1 <= state[x - 1, y] <= d:
            result.append(state[x - 1, y])
    except:
        pass

    try:
        if 1 <= state[x + 1, y] <= d:
            result.append(state[x + 1, y])
    except:
        pass

    try:
        if 1 <= state[x + 1, y + 1] <= d:
            result.append(state[x + 1, y + 1])
    except:
        pass

    try:
        if 1 <= state[x + 1, y - 1] <= d:
            result.append(state[x + 1, y - 1])
    except:
        pass

    try:
        if 1 <= state[x - 1, y + 1] <= d:
            result.append(state[x - 1, y + 1])
    except:
        pass

    try:
        if 1 <= state[x - 1, y - 1] <= d:
            result.append(state[x - 1, y - 1])
    except:
        pass

    return result


def is_stable(state):
    # when the grid does not contain any ill cell, a stable state is reached
    return len(state[(state == -np.inf) | (state == -4) | (state == -3) | (state == -2) | (state == -1) | (state == 0)]) == np.prod(state.shape)
