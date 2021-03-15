import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import NullFormatter  # useful for `logit` scale


def neighbors(i, j, n):
    return np.array(
        [
            (i, (j + n - 1) % n),
            (i, (j + 1) % n),
            ((i + n - 1) % n, j),
            ((i + 1) % n, j)
        ]
    )


def count_neighbors(i, j, grid):
    idx = neighbors(i, j, grid.shape[0])
    return np.sum(grid[idx[:, 0], idx[:, 1]])


p = 0.1
q = 0.1

#### MAKE THE GRID ####
# Define the grid size
grid_size = 20

# Create a square grid of empty sites
grid = np.full((grid_size, grid_size), False)

plt.ion()

# Begin experiment
bodies_to_add = 100
total_grid_positions = grid_size * grid_size
while True:
    # add new particle first

    # make a possibility
    possibility = np.random.rand()

    willMove = 0
    hasAdd = 1
    hasMoved = 0

    if possibility <= p and bodies_to_add:
        #### Choose empty spot ####
        empty_sites_idx = np.argwhere(grid == False)  # Find all empty site

        try:
            # Select randomly an empty site
            new_empty_site = empty_sites_idx[np.random.randint(empty_sites_idx.shape[0])]
        except ValueError:
            break
        # Convert indices to tuple
        new_empty_site = tuple(new_empty_site)

        # Place a new particle
        grid[new_empty_site] = True

        bodies_to_add -= 1
    else:
        willMove = 1
        hasAdd = 0

    if willMove == 1:
        # Find the indices of all particles that can move
        idx = np.argwhere(grid == True)
        can_move = idx[[count_neighbors(x[0], x[1], grid) == 0 for x in idx]]

        if can_move.size == 0 and bodies_to_add == 0:
            break

        for i_j in can_move:
            if np.random.rand() > q:
                continue

            i, j = tuple(i_j)

            # Select a random movement
            _r = np.random.rand()
            if _r < 0.25:
                grid[i, (j + grid_size - 1) % grid_size] = True
            elif _r < 0.5:
                grid[i, (j + 1) % grid_size] = True
            elif _r < 0.75:
                grid[(i + grid_size - 1) % grid_size, j] = True
            else:
                grid[(i + 1) % grid_size, j] = True

            grid[i, j] = False
            hasMoved = 1

    #### MAKE VISUAL RESULTS ####
    aux = np.argwhere(grid == True)
    x, y = aux.T
    plt.scatter(x, y)
    plt.pause(1e-9)
    plt.clf()

    # if hasMoved == 0 and hasAdd == 0 :
    #    break

#### CALCULATE SIZE OF BODIES ####
repetitions = 1000
min_box_size = 3
max_box_size = 15

counts = dict(zip(range(min_box_size, max_box_size + 1), [0] * (max_box_size - min_box_size + 1)))
squares = dict(zip(range(min_box_size, max_box_size + 1), [0] * (max_box_size - min_box_size + 1)))

for _ in range(repetitions):
    # Select a random box size
    box_size = np.random.randint(min_box_size, max_box_size + 1)

    # Select a random position
    i = np.random.randint(grid_size - box_size)
    j = np.random.randint(grid_size - box_size)

    particles = np.sum(grid[i: i + box_size, j: j + box_size])
    counts[box_size] += particles
    squares[box_size] += 1

# Calculate mean values
x = []
y = []

for i in range(3, 15):
	m = counts[i] / squares[i]
	print(m)
	x.append(i)
	y.append(m)
print(x)
print(y)

plt.plot(x, y)
plt.yscale('log')
plt.xscale('log')
plt.title('log')
plt.grid(True)
plt.gca().yaxis.set_minor_formatter(NullFormatter())
# Adjust the subplot layout, because the logit one may take more space
# than usual, due to y-tick labels like "1 - 10^{-3}"
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
plt.show()

input("Save image and press enter : ")
