##Question 7:
from grid import Grid

g = Grid(2, 3)
print(g.swap((0,0),(0,1)))
g.swap(((1,2),(1,0)))
print(g.resolution)

"""
data_path = "../input/"
file_name = data_path + "grid0.in"

print(file_name)
g = Grid.grid_from_file(file_name)
print(g)
"""