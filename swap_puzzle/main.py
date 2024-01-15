from grid import Grid

g = Grid(2, 3)
print(g)

data_path = "../input/"
file_name = data_path + "grid0.in"

print(file_name)
print("bonjour")
g = Grid.grid_from_file(file_name)
print(g)