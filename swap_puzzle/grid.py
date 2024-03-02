"""
This is the grid module. It contains the Grid class and its associated methods.
"""

#import

import random

import itertools 

import copy

from graph import Graph 

import matplotlib.pyplot as plt

import math

import heapq

import numpy as np






class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    
    def __init__(self, m, n, initial_state = []):
        """
        Initializes the grid.

        Parameters: 
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intiail state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

    def __str__(self): 
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):
        """
        Checks is the current state of the grid is sorted and returns the answer as a boolean.
        """
        sorted=True
        for i in range(self.m):
            for j in range (self.n-1):
                if self.state[i][j]<=self.state[i][j+1]:
                    sorted=True
                    continue
                else:
                    sorted=False
                    break
            if i!=self.m-1:
                if self.state[i][self.n-1]<self.state[i+1][0]:
                    sorted=True
                    continue
                else:
                    sorted=False
                    break
        return sorted


    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed. 
        Returns the state of the list if the swap is valid.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        i,j=cell1
        k,l=cell2
        if abs(i-k)+abs(j-l)==1:
            a=self.state[i][j]
            b=self.state[k][l]
            self.state[i][j]=b
            self.state[k][l]=a
            return self.state 
        else:
            raise Exception("The swap is invalid")
        

    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        for k in cell_pair_list:
            self.swap(k[0],k[1])
    
    def graphic_representation(self):
        """
        Gives a graphic representation of the grid.
        """
        grid=self.state
        fig, ax=plt.subplots()
        ax.set_axis_off()
        ax.table(cellText=grid,cellLoc ='center')
        plt.show()

    
    def node(self): 
        """
        Represents a grid as a node.
        The node is represented by a tuple, which is a hashable but also ranked object.
        """
        
        node_list=[]
        for i in range (self.m):
            for j in range(self.n):
                node_list.append(self.state[i][j])
        node_tuple=tuple(node_list)
        return node_tuple
    
    @staticmethod
    def grid_from_tuple(tuple,n,m): 
        """
        A function that transforms a tuple in the state of a grid.

        Parameters:
        - - - - - - - - - - - - - - - - - - -
        t: tuple
        n: number of rows of the expected grid
        m: number of columns of the expected grid
        """

        if len(tuple)==n*m:
            grid=[list(tuple[i:i+m]) for i in range (0,len(tuple),m)]
            return grid
        else:
            raise Exception("The tuple can't represent a grid")

  
    def permutations(self):
        """
        Represents the possible states of the grid, which are the different ways to organise n*m elements.
        It returns a liste of tuples, that is to say of grids as nodes. 
        """
        permutations=list(itertools.permutations(self.node()))
        return permutations 

    def adj_state(self):
        """
        Builds a dictionary which associates each cell with the cells with which swaps are valid.
        The cells are in the format (i,j)
        """
        adj={}
        for i in range(self.m):
            for j in range(self.n):
                adj[(i,j)]=[]
                if i!=0: #special case first row: no row above
                    adj[(i,j)].append((i-1,j))
                if j!=0: #special case first column: no column before
                    adj[(i,j)].append(((i,j-1)))
                if i!=self.m-1: #special case last row: no row below
                    adj[(i,j)].append((i+1,j))
                if j!=self.n-1: #special case last column: no column after
                    adj[(i,j)].append(((i,j+1)))
        return adj
    #Complexity: nm

    
    def adj_grids(self):
        """
        Associates with a grid the list of grids (as grids, not state, not tuple) that can be obtained by a swap
        """

        adj=[]
        dict=self.adj_state()
        for k in dict.keys():
            for l in dict[k]:
                self.swap(k,l)
                adj.append(Grid(self.m,self.n,copy.deepcopy(self.state)))
                self.swap(k,l)
        return adj
    #Complexity: nm
    
    def resolution(self):
        """
        Applies the bfs algorithm to a graph representing all the possible states of the Grid to find the shortest path.
        Returns a list of necessary swaps.
        """
        #Creation of an instance of the Graph class with the list of nodes made up of tuples representing the different states of the grid.
        g=Graph(Grid.permutations(self)) #Complexity: (nm)!

        #Addition of edges between adjoining grids, i.e. between grids separated by one swap only
        for i in g.nodes: 
            grid=Grid(self.m,self.n,Grid.grid_from_tuple(i,self.m,self.n))
            list_grid=Grid.adj_grids(grid)
            for j in list_grid:
                g.add_edge(i,j.node()) 
        

        #bfs algorith: list of the different grids of the paths
        list=g.bfs(Grid.node(self),tuple(range(1,self.n*self.m+1)))
        print(list)

        #list of the necessary swaps
        list_swap=[]
        
        for i in range (len(list)-1):
            (a,b)=(-1,-1)
            for k in range(0,self.m):
                for l in range(0,self.n):
                    if list[i][k*self.n+l]!=list[i+1][k*self.n+l]:
                        if(a,b)==(-1,-1):
                            (a,b)=(k,l)
                        else:
                            list_swap.append(((a,b),(k,l)))
        return list_swap
    #Complexity: (nm)!(nm)^2

    def resolution_short(self):
        """
        Returns the shortest path without creating and going through the entire graph
        """
        src=self.node()
        dst=tuple(range(1,self.n*self.m+1))
        file=[src] 
        visited=[src]
        previous_nodes={}
        path=[dst] 
        while len(file)>0: 
            n=file.pop(0) 
            if n==dst:
                p=n
                while p !=src:
                    path.insert(0,previous_nodes[p])
                    p=previous_nodes[p]
                print(path)

                list=path
                list_swap=[]
         
                for i in range (len(list)-1):
                    (a,b)=(-1,-1)
                    for k in range(0,self.m):
                        for l in range(0,self.n):
                            if list[i][k*self.n+l]!=list[i+1][k*self.n+l]:
                                if(a,b)==(-1,-1):
                                    (a,b)=(k,l)
                                else:
                                    list_swap.append(((a,b),(k,l)))
                return list_swap
             
            else:
                for i in Grid(self.m,self.n,Grid.grid_from_tuple(n,self.m,self.n)).adj_grids(): #adds adjoining nodes thanks to adj_grids
                    i=i.node()
                    if i not in visited:
                        file.append(i) 
                        visited.append(i)
                        previous_nodes[i]=n
        return None
    
    def heuristic(self,node): #en faire une méthode statique?
        """
        Parameters:
        ---
        node: node is a tuple
        
        """

        #Création de deux objets grilles pour accéder à l'attribut state
        grid1=Grid(self.m,self.n,Grid.grid_from_tuple(node,self.m,self.n))
        grid2=Grid(self.m,self.n,Grid.grid_from_tuple(tuple(range(1,self.n*self.m+1)),self.m,self.n))

        #Parcours de toutes les cellules des grilles par leur contenu
        for k in range (1,self.m*self.n+1):
            counter_swap=0

        #Parcours de toutes les cellules des grilles par leurs coordonnées 
            for i in range (self.m):
                for j in range (self.n):

        #Stockage des coordonnées de k dans grid1 sous m1 et n1
                    if grid1.state[i][j]==k:
                        m1=i
                        n1=j
        #Stockage des coordonnées de k dans grid2 sous m2 et n2            
                    if grid2.state[i][j]==k:
                        m2=i
                        n2=j
            counter_swap=counter_swap+abs(m2-m1)+abs(n2-n1)
        counter_swap=counter_swap/2
        return counter_swap
        
    
    def a_star(self):
        """
        
        """
        #noeud source et d'arrivée sous forme de tuple
        src=self.node()
        dst=tuple(range(1,self.n*self.m+1))

        #List composée de tuples (coût, noeud sous forme de tuple)
        open_list=[(self.heuristic(src),src)]

        #On modifie la liste pour trier par coût croissant
        heapq.heapify(open_list)

        #Liste des noeuds visités sous forme de tuple
        closed_list=[]

        #Dictionnaire qui à chaque noeud sous forme de tuple associe son coût
        cost={src:self.heuristic(src)}

        #Dictionnaire qui à chaque noeud associe le coût réel, i.e. le coût qui le sépare du noeud source
        src_cost={src:0}

        #Dictionnaire qui à chaque noeud associe noeud précédent
        previous_nodes={}

        #Liste des noeuds parcourus dans chemin optimal
        path=[dst]

        #Condition de sortie précoce: A EFFACER
        counter=0
        

        while len(open_list)>0:
            c,ext_node=heapq.heappop(open_list) #premier élément de la liste, c=coût, n=node sous forme de tuple
            if ext_node==dst: #tuples
                p=ext_node
                while p !=src:
                    path.insert(0,previous_nodes[p])
                    p=previous_nodes[p]
                print(path) 
                list=path
                list_swap=[]
         
                for i in range (len(list)-1):
                    (a,b)=(-1,-1)
                    for k in range(self.m):
                        for l in range(0,self.n):
                            if list[i][k*self.n+l]!=list[i+1][k*self.n+l]:
                                if(a,b)==(-1,-1):
                                    (a,b)=(k,l)
                                else:
                                    list_swap.append(((a,b),(k,l)))
                return list_swap
            else:
              for grid in Grid.adj_grids(Grid(self.m,self.n,Grid.grid_from_tuple(ext_node,self.m,self.n))): #adj_grids s'applique à une grille
                  node=grid.node() #on retransforme grille en tuple
                  
                #Traitement du noeud s'il n'a pas déjà été visité ou s'il a été visité avec un coût supérieur
                  if node not in closed_list or cost[node]>src_cost[ext_node]+1:
                      #Actualisation du dictionnaire src_cost:
                      src_cost[node]=src_cost[ext_node]+1
                      #Ajout du tuple (coût,noeud) à la file
                      node_cost=src_cost[node]+self.heuristic(node)
                      heapq.heappush(open_list,(node_cost,node)) 
                      #Ajout du noeud à la liste des noeuds visités
                      closed_list.append(node)
                      #Actualisation du dictionnaire avec coût du noeud
                      cost[node]=node_cost
                      #Actualisation du dico previous nodes
                      previous_nodes[node]=ext_node
                    
    @staticmethod
    def controlled_difficulty(level):
        """
        Generates a grid with a controlled level of difficulty.
        There are two components of the difficulty level: 
        - Size of the table (level+1)^2. The number of rows and colums are generated randomly.
        - Number of swaps: level*2. The swaps are also generated randomly. 
        
        Parameters:
        ------------------
        level from 1 to 10
        """
        #Difficulty: size of the grid
        size=(level+1)**2

        #Sorted_list with the determined size
        sorted_list=[]
        for i in range (1,size+1):
            sorted_list.append(i)

        #list of dividers of size 
        list_div=[]
        for i in range(1,size//2+1):
            if size%i==0:
                list_div.append(i)
        list_div.append(size)
        print("liste div",list_div)

        #random but adequate number of rows and columns
        m=random.choice(list_div)
        n=int(size/m)

        #création d'une grille
        grid=Grid(m,n,Grid.grid_from_tuple(tuple(sorted_list),m,n))

        #génération aléatoire d'un nombre plus ou moins complexe de swaps
        cell_pair_list=[]
        dict=grid.adj_state()
        counter=0
        while counter<=level*2:
            counter=counter+1
            t1=random.randint(0,m-1)
            t2=random.randint(0,n-1)
            tuple1=(t1,t2)
            tuple2=random.choice(dict[tuple1])
            cell_pair_list.append((tuple1,tuple2))
        print("cell list",cell_pair_list,"len",len(cell_pair_list))
        
        grid.swap_seq(cell_pair_list)

        return grid




                  
    def bubble_sort(self):
        if self.m==1:
            #transformation d'une double liste en simple liste
            list=self.state[0]
            list_swap=[]
            for i in range(self.n-2):
                for j in range (self.n-1-i):
                    if list[j]>list[j+1]:
                        self.swap((0,j),(0,j+1))
                        list_swap.append(((0,j),(0,j+1)))
                    
            print(self.state)
            return list_swap
        else:
            raise Exception("Grid not in the format 1*n")


                      








                    




    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next m lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid








