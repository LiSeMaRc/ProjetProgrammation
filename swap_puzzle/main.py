#Imports
from graph import Graph
from grid import Grid
from solver import Solver



#Question 4: graphic representation of a grid : voir plutôt module partie Interface pygame

#print("Question 4,grid0",Grid.graphic_representation(Grid.grid_from_file("input\\grid0.in")))
#print("Question 4,grid1",Grid.graphic_representation(Grid.grid_from_file("input\\grid1.in")))

#Permutations
#print("Question 4,grid0",Grid.permutations(Grid.grid_from_file("input\\grid0.in")))






"""
#Question 5: bfs first version
for i in range(1,20):
    for j in range(i+1,21):
        print("Question 5, graph1",i,j,len(Graph.bfs(Graph.graph_from_file("input\\graph1.in"),i,j)),Graph.bfs(Graph.graph_from_file("input\\graph1.in"),i,j))
for i in range(1,20):
    for j in range(i+1,21):
        print("Question 5, graph2",i,j,Graph.bfs(Graph.graph_from_file("input\\graph2.in"),i,j))
"""

#Question 7: bfs for grid
#print("Question 7, grid0",Grid.resolution(Grid.grid_from_file("input\\grid0.in")))
#print("Question 7, grid1",Grid.resolution(Grid.grid_from_file("input\\grid1.in")))
print("Question 7, grid2",Grid.resolution(Grid.grid_from_file("input\\grid2.in")))

"""
#Question 8: short bfs for grid
print("Question 8, grid0",Grid.resolution_short(Grid.grid_from_file("input\\grid0.in")))
print("Question 8, grid1",Grid.resolution_short(Grid.grid_from_file("input\\grid1.in")))
print("Question 8, grid2",Grid.resolution_short(Grid.grid_from_file("input\\grid2.in")))
"""
#print("Question 8, grid2",Grid.resolution_short(Grid.grid_from_file("input\\grid2.in")))

#print("Question 9, grid0",Grid.heuristic(Grid.grid_from_file("input\\grid0.in"),(1,2,4,3)))

#Question 9: A star
#print("Question 9, grid0",Grid.a_star(Grid.grid_from_file("input\\grid0.in")))
#print("Question 9, grid1",Grid.a_star(Grid.grid_from_file("input\\grid1.in")))

#print("Question 8, grid2",Grid.resolution_short(Grid.grid_from_file("input\\grid2.in")))
#grid=Grid(6, 6, [[34, 20, 26, 1, 25, 13], [12, 35, 11, 31, 7, 27], [6, 2, 17, 36, 30, 21], [9, 29, 8, 3, 16, 18], [32, 15, 4, 22, 14, 19], [24, 33, 23,10,28,5]])
#print("Question 9, grid2",grid.a_star())

#for grid in Grid.adj_grids(Grid.grid_from_file("input\\grid2.in")):
    #print(grid.node())

#Grilles à niveau de difficulté contrôlé
#print(Grid.controlled_difficulty(3))

#Grilles 1*n
#print(Grid.bubble_sort(Grid.grid_from_file("input\\grid5.in")))
#print(Grid.bubble_sort(Grid.grid_from_file("input\\grid6.in")))
