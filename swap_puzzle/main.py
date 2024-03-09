#Imports
from graph import Graph
from grid import Grid
from solver import Solver
from interface import Interface 

#Graphic representation
grid=Grid.grid_from_file("input\\grid0.in")
grid.graphic_representation()

grid=Grid.grid_from_file("input\\grid1.in")
grid.graphic_representation()

grid=Grid.grid_from_file("input\\grid2.in")
grid.graphic_representation()



#Comparisons of solutions between bfs and simple solution
grid=Grid.grid_from_file("input\\grid0.in")
print("Grid 0")
print("Short bfs solution",Solver.short_bfs_solution(grid))
print("Simple solution",Solver.simple_solution(grid))


grid=Grid.grid_from_file("input\\grid1.in")
print("Grid 1")
print("Short bfs solution",Solver.short_bfs_solution(grid))
print("Simple solution",Solver.simple_solution(grid))


grid=Grid.grid_from_file("input\\grid0.in")
print("Grid 2")
print("Short bfs solution",Solver.short_bfs_solution(grid))
print("Simple solution",Solver.simple_solution(grid))

#Game
Interface.start(Interface.grid_from_file_bis("input\\grid2.in"))









                                                                                                                               


