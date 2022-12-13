import numpy as np
from random import randint

cols = 75
rows = 75

dx = 0.1
dy = 0.1
alpha = 1.0
dt = (dx*dx)/(4*alpha)


gamma = 0.1*(alpha*dt)/(dx*dx)
Tr = 300

Th = 300
Tc = 286

sparse = False
max_steps = 3500

grid = np.zeros((max_steps+1, rows, cols))

if sparse:
    centerx = [randint(0, cols) for _ in range(20)]
    centery = [randint(0, rows) for _ in range(20)]

    for i in range(rows):
        for j in range(cols):
            inflag = False
            for xc, yc in zip(centerx, centery):
                if (i <= yc+2 and i >= yc-2) and (j <= xc+2 and j >= xc-2):
                    inflag = True

            if inflag:
                grid[0][i][j] = Tc
            else:
                grid[0][i][j] = Th

else:

    len_side = 30
    lowx = (cols-len_side)/2
    highx = (cols+len_side)/2
    lowy = (rows-len_side)/2
    highy = (cols+len_side)/2

    for i in range(rows):
        for j in range(cols):
            if (j <= highx and j >= lowx) and (i <= highy and i>=lowy):
                grid[0][i][j] = Tc
            else:
                grid[0][i][j] = Th


#now for the actual computation
k = 0

while k<max_steps:


    for i in range(rows):
        for j in range(cols):

            if i==0:
                if j==0:
                    #top left
                    uimj = Tr
                    uijm = Tr
                    uipj = grid[k][i+1][j]
                    uijp = grid[k][i][j+1]
                elif j==cols-1:
                    #top right
                    uimj = Tr
                    uijp = Tr
                    uipj = grid[k][i+1][j]
                    uijm = grid[k][i][j-1]
                else:
                    #top edge
                    uimj = Tr
                    uipj = grid[k][i+1][j]
                    uijp = grid[k][i][j+1]
                    uijm = grid[k][i][j-1]
            elif i==rows-1:
                if j==0:
                    #bottom left
                    uipj = Tr
                    uijm = Tr
                    uimj = grid[k][i-1][j]
                    uijp = grid[k][i][j+1]
                elif j==cols-1:
                    #bottom right
                    uipj = Tr
                    uijp = Tr
                    uimj = grid[k][i-1][j]
                    uijm = grid[k][i][j-1]
                else:
                    #bottom edge
                    uipj = Tr
                    uimj = grid[k][i-1][j]
                    uijp = grid[k][i][j+1]
                    uijm = grid[k][i][j-1]
            else:
                if j==0:
                    #left edge
                    uijm = Tr
                    uipj = grid[k][i+1][j]
                    uimj = grid[k][i-1][j]
                    uijp = grid[k][i][j+1]
                elif j==cols-1:
                    #right edge
                    uijp = Tr
                    uipj = grid[k][i+1][j]
                    uimj = grid[k][i-1][j]
                    uijm = grid[k][i][j-1]
                else:
                    #all other points
                    uipj = grid[k][i+1][j]
                    uimj = grid[k][i-1][j]
                    uijp = grid[k][i][j+1]
                    uijm = grid[k][i][j-1]


            grid[k+1][i][j] = grid[k][i][j] + gamma*(uipj+uimj+uijp+uijm - 4*grid[k][i][j])



    #difference analysis here

    k+=1


reshaped_grid = grid.reshape(grid.shape[0], -1)  #gives rows only at different times with each row concatenated

filename = "sparse_data.txt" if sparse else "park_data.txt"

np.savetxt(filename, reshaped_grid)
print("Saved to %s"%filename)



