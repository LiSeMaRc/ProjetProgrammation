#Imports
from graph import Graph
from grid import Grid
from solver import Solver

#TESTS

#Question 2: is_sorted et swaps
print("Question 2, sorted, grid1",Grid.is_sorted(Grid.grid_from_file("input\\grid1.in")))
print("Question 2, sorted, grid2",Grid.is_sorted(Grid.grid_from_file("input\\grid2.in")))
print("Question 2, sorted, grid5",Grid.is_sorted(Grid.grid_from_file("input\\grid5.in")))

print("Question 2, swap, grid0",Grid.swap(Grid.grid_from_file("input\\grid0.in"),(0,0),(0,1)))
#print("Question 2, swap, grid0 imp",Grid.swap(Grid.grid_from_file("input\\grid0.in"),(0,0),(1,1)))
print("Question 2, swap, grid1",Grid.swap(Grid.grid_from_file("input\\grid1.in"),(0,0),(0,1)))
#print("Question 2, swap, grid1 imp",Grid.swap(Grid.grid_from_file("input\\grid1.in"),(0,0),(1,1)))

#Grid.swap_seq(Grid.grid_from_file("C:\\Users\\lisem\\OneDrive\\Documents\\ENSAE\\1A\\ensae-prog24\\input\\grid0.in"),[((0,0),(0,1)),((1,0),(1,1))])
#Grid.swap_seq(Grid.grid_from_file("C:\\Users\\lisem\\OneDrive\\Documents\\ENSAE\\1A\\ensae-prog24\\input\\grid0.in"),[((0,0),(1,1)),((1,0),(1,1))])

#Question 3
print("Question 3, grid0",Solver.get_solution(Grid.grid_from_file("input\\grid0.in")))


#Question 5: bfs first version
for i in range(1,20):
    for j in range(i+1,21):
        print("Question 5",i,j,len(Graph.bfs(Graph.graph_from_file("input\\graph1.in"),i,j)),Graph.bfs(Graph.graph_from_file("input\\graph1.in"),i,j))
for i in range(1,20):
    for j in range(i+1,21):
        print("Question 5",i,j,Graph.bfs(Graph.graph_from_file("input\\graph2.in"),i,j))

#Question 7: bfs for grid
print("Question 7, grid0",Grid.resolution(Grid.grid_from_file("input\\grid0.in")))
print("Question 7, grid1",Grid.resolution(Grid.grid_from_file("input\\grid1.in")))

#Question 8: short bfs for grid
print("Question 8, grid0",Grid.resolution_short(Grid.grid_from_file("input\\grid0.in")))
print("Question 8, grid1",Grid.resolution_short(Grid.grid_from_file("input\\grid0.in")))

