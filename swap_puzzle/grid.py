"""
This is the grid module. It contains the Grid class and its associated methods.
"""

#import

import random

import itertools 

import copy

from graph import Graph 

import pygame

import math








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
        self.node=self.calculate_node()

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


    def swap(self, cell1, cell2,calc_node=True):
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
            if calc_node==True:
                self.node=self.calculate_node()
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

        pygame.init()
        
        #colors
        black=(0,0,0)
        white=(255,255,255)

        #font
        font=pygame.font.Font(None,20)

        #Sizes:
        width=500
        height=500
        cell_size=(width-200)//max(self.m,self.n),(height-200)//max(self.m,self.n)

        #Creation of the window:
        window = pygame.display.set_mode((width, height))
        window.fill(black)

        #horizontal lines
        for i in range(self.m+1): 
            pygame.draw.line(window, white, (100, 100+i * cell_size[1]), (100+self.n * cell_size[0], 100+i * cell_size[1]))

        #vertical lines
        for j in range(self.n+1):
            pygame.draw.line(window, white, (100+j * cell_size[0], 100), (100+j *cell_size[0], 100+self.m * cell_size[1]))
    
        #numbers
        for i in range(self.m):
            for j in range(self.n):
                text=font.render(str(self.state[i][j]),True,white)
                window.blit(text, (100+j*cell_size[0] + cell_size[0]//2-1, 100+i*cell_size[1] + cell_size[1]//2-1))
    
        pygame.display.update() 
        pygame.time.delay(10000) 

    
    def calculate_node(self): 
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
        permutations=list(itertools.permutations(self.node))
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
        for k,v in dict.items():
            for l in v:
                g = Grid(self.m,self.n,copy.deepcopy(self.state))
                g.swap(k,l)
                adj.append(g)
        return adj
    #Complexity: nm
    

    
    def heuristic(self,node): 
        """
        Parameters:
        ---
        node: node is a tuple
        
        """
        
        #Creation of Grids to access the grid.state attribute
        grid1=Grid(self.m,self.n,Grid.grid_from_tuple(node,self.m,self.n))
        grid2=Grid(self.m,self.n,Grid.grid_from_tuple(tuple(range(1,self.n*self.m+1)),self.m,self.n))

        counter_swap=0

        for i in range (self.m):
            for j in range (self.n): 
                k=grid1.state[i][j]
                m2=(k-1)//self.n
                n2=(k-1)%self.n
                counter_swap=counter_swap+abs(m2-i)+abs(n2-j)
        counter_swap=counter_swap/2
        return counter_swap


        
 
                    
    @staticmethod
    def controlled_difficulty(level):
        """
        Generates a grid with a controlled level of difficulty.
        - Size of the table: (level+1)^2. The number of rows and colums are generated randomly.
        - Number of swaps: level*2. The swaps are also generated randomly. 
        
        Parameters:
        ------------------
        level from 1 to 3 (for the graphic interface)
        """
        #Size of the grid
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
        
        
        grid.swap_seq(cell_pair_list)

        return grid

                  

    



                      








                    




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








