import numpy as np


a = np.array([[1, 2, 3],
             [4, 5, 6],
             [7, 0, 8]])

print(a)

location = np.argwhere(a == 0)
print(location)

x = location[0][0] # 2
y = location[0][1] # 1

a[x][y] = a[x-1][y]
a[x-1][y] = 0

print(a)
