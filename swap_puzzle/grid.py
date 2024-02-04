"""
This is the grid module. It contains the Grid class and its associated methods.
"""

import random

import itertools #pour permutations

from graph import Graph #résolution par bfs

import copy



def grid_from_tuple(t,n,m): #juste fonction pas méthode

    if len(t)!=n*m:
        print("Ce tuple ne peut pas représenter une grille")
        return None 
    else:
        grid=[list(t[i:i+m] for i in range (0,len(t),m))]
        return grid



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
        Checks is the current state of the grid is sorte and returns the answer as a boolean.
        """
        sorted=True
        for i in range(0,self.m):
            for j in range (0,self.n-1):
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
        print(sorted)


    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        if (cell1[0]==cell2[0] and (cell1[1]==cell2[1]+1 or cell1[1]==cell2[1]-1)) or (cell1[1]==cell2[1] and (cell1[0]==cell2[0]+1 or cell1[0]==cell2[0]-1)):
            """
            a=cell1
            b=cell2
            cell1=b
            cell2=a
            print("La cellule 1 est",cell1,"et la cellule 2 est",cell2)
            return (cell1,cell2)
            """
            
            a=self.state[cell1[0]][cell1[1]]
            b=self.state[cell2[0]][cell2[1]]
            self.state[cell1[0]][cell1[1]]=b
            self.state[cell2[0]][cell2[1]]=a
            return self.state
                
        else:
            return None
        


    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        new_list=[]
        for k in cell_pair_list:
            new_list.append(Grid.swap(self,k[0],k[1]))
        print (new_list)
        return(new_list)
    
    def node(self): 
        """
        Représentation d'une grille comme d'un noeud
        tuple n'est pas mutable (noeud doit être hashable) mais il est ordonné donc on pourra représenter la grille de manière similaire à la représentation par la double liste state
        tuple de tuple: chaque élément du grand tuple est une ligne
        """
        
        node_list=[]
        for i in range (0,self.m):
            for j in range(0,self.n):
                node_list.append(self.state[i][j])
        node_tuple=tuple(node_list)
        return node_tuple
        """autres essais au cas où on chercherait à faire des tuples de tuples
        node=(tuple(tuple(self.state)[0]),tuple(tuple(self.state[1]))) pb est qu'il faudrait le faire m fois
        nodebis=tuple(self.state) pour le moment, version la plus convaincante
        """


    
    def permutations(self):
        """Les différents états d'une grille peuvent s'obtenir 
        en cherchant de combien de façons on peut ranger n*m éléments distincts.
        On rappelle qu'on peut maintenant représenter grille comme un tuple"""
        permutations=list(itertools.permutations(Grid.node(self)))
        return permutations

    def adj_state(self):
        """Construction d'un dictionnaire qui à chaque coef associe les coef avec lesquels on peut faire de swaps """
        adj={self.state[0][0]:[(0,1),(1,0)],
               self.state[0][self.n-1]:[(1,self.n-1),(0,self.n-2)],
               self.state[self.m-1][self.n-1]:[(self.m-2,self.n-1),(self.m-1,self.n-2)],
               self.state[self.m-1][0]:[(self.m-1,1),(self.m-2,0)]} #traitement des coins de la grille
        if self.n>2 or self.m>2:
            for i in range(0,self.m-1):#on enlève la dernière ligne
                for j in range(1,self.n-1): #on enlève la première et la dernière colonne
                    adj[self.state[i][j]]=[(i+1,j),(i,j-1),(i,j+1)]

            #colonne 1, n-1 et ligne m-1 or sommets
            
            for i in range(1,self.m-2): #traitement de la première colonne
                adj[self.state[i][0]]=[(i-1,0),(i+1,0),(i,1)]

            for i in range(1,self.m-2): #traitement de la dernière colonne
                adj[self.state[i][self.n-1]]=[(i-1,self.n-1),(i+1,self.n-1),(i,self.n-2)]
            
            for j in range(1,self.n-2):
                adj[self.state[self.m-1][j]]=[(self.m-1,j-1),(self.m-1,j+1),(self.m-2,j)]
            
        return adj
    """adj={self.state[0][0]:[self.state[0][1],self.state[1][0]],
               self.state[0][self.n-1]:[self.state[1][self.n-1],self.state[0][self.n-2]],
               self.state[self.m-1][self.n-1]:[self.state[self.m-2][self.n-1],self.state[self.m-1][self.n-2]],
               self.state[self.m-1][0]:[self.state[self.m-1][1],self.state[self.m-2][0]]} #traitement des coins de la grille
        if self.n>2 or self.m>2:
            for i in range(0,self.m-1):#on enlève la dernière ligne
                for j in range(1,self.n-1): #on enlève la première et la dernière colonne
                    adj[self.state[i][j]]=[self.state[i+1][j],self.state[i][j-1],self.state[i][j+1]]

            #colonne 1, n-1 et ligne m-1 or sommets
            
            for i in range(1,self.m-2): #traitement de la première colonne
                adj[self.state[i][0]]=[self.state[i-1][0],self.state[i+1][0],self.state[i][1]]

            for i in range(1,self.m-2): #traitement de la dernière colonne
                adj[self.state[i][self.n-1]]=[self.state[i-1][self.n-1],self.state[i+1][self.n-1],self.state[i][self.n-2]]
            
            for j in range(1,self.n-2):
                adj[self.state[self.m-1][j]]=[self.state[self.m-1][j-1],self.state[self.m-1][j+1],self.state[self.m-2][j]]
            
        return adj"""
    #dico corrigé pour prendre en compte le format des arguments de la méthode swap
    
    def adj_grids(self):
        """Associe à une grille la liste des grilles pouvant être obtenues par un swap"""
        """
        adj=[]
        for i in list(Grid.adj_state(self).keys()): #on parcourt les clés du dictionnaire
            for j in Grid.adj_state(self)[i]: #on parcourt les éléments des listes de cases adjaçantes
               adj.append(Grid.swap(self,i,j))
               Grid.swap(self,i,j) #On réinitialise la grille pour le suivant
        return adj
        """
        adj=[]
        for i in range(0,self.m-1):
            for j in range(0,self.n-1): #vérifier cette histoire d'index out of range
                for k in Grid.adj_state(self)[self.state[i][j]]:
                    gridbis=copy.deepcopy(self)
                    adj.append(Grid.swap(gridbis,(i,j),k)) 
        return adj

    
    def resolution(self):
        """
        Construction d'un graph de tous les états possibles de la grille pour appliquer l'algorithme bfs à la résolution du problème
        """
        #Création d'une instance de la classe Graph avec la liste de noeuds composée des tuples représentant les différents états de la grille
        g=Graph(Grid.permutations(self))

        #Ajout arêtes entre grilles adjaçantes, i.e. entre lesquelles on peut passer par un swap
        for i in g.nodes: #tuples
            grid=Grid(self.m,self.n,grid_from_tuple(i,self.m,self.n))
            list_grid=Grid.adj_grids(grid)
            for j in list_grid: #adj_grids est méthode qui s'applique à une grille. Or ne semble par reconnaître k comme grille
                g.add_edge(i,self.node(j)) #la méthode adj_grids retourne une liste de grilles (de states)
        
        #Application de l'algorithme bfs
        return g.bfs(Grid.node(self),tuple(range(1,self.n*self.m+1)))

def resolution_short(self):
    list_nodes=[Grid.node(self)] #noeuds à traiter sous forme de tuple
    initialisation=[Grid.node(self)] #liste des noeuds avec lesquels créer le graph
    while tuple(range(1,self.n*self.m+1)) not in list_nodes: #on s'arrêtera quand on aura trouvé la grille rangée (is_sorted?)
        while len(list_nodes)>0:
            for k in list_nodes: #sûrement pb 
                for j in Grid.adj_grids(k): #parmi les grilles adjaçantes au noeud à traiter
                    initialisation.append(Grid.node(j)) #on l'ajoute à la liste des noeuds utiles pour le graph sous forme de tuple
                    list_nodes.append(Grid.node(j)) #on l'ajoute à la liste des noeuds à traiter
             #plein de pbs
    
        #Création d'une instance de la classe Graph avec la liste de noeuds utiles
        g=Graph(initialisation)

        #Ajout arêtes entre grilles adjaçantes, i.e. entre lesquelles on peut passer par un swap
        for i in g.nodes: #tuples
            grid=Grid(self.m,self.n,grid_from_tuple(i,self.m,self.n))
            list_grid=Grid.adj_grids(grid)
            for j in list_grid: #adj_grids est méthode qui s'applique à une grille. Or ne semble par reconnaître k comme grille
                g.add_edge(i,self.node(j)) #la méthode adj_grids retourne une liste de grilles (de states)
        
        #Application de l'algorithme bfs
    return g.bfs(Grid.node(self),tuple(range(1,self.n*self.m+1)))

    
        
    

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

def resolution_short(self):



    Grid.swap(Grid.grid_from_file("C:\\Users\\lisem\\OneDrive\\Documents\\ENSAE\\1A\\ensae-prog24\\input\\grid0.in"),(0,0),(0,1))

print(Grid.adj_state(Grid.grid_from_file("C:\\Users\\lisem\\OneDrive\\Documents\\ENSAE\\1A\\ensae-prog24\\input\\grid0.in")))

print(Grid.adj_grids(Grid.grid_from_file("C:\\Users\\lisem\\OneDrive\\Documents\\ENSAE\\1A\\ensae-prog24\\input\\grid0.in")))

print(Grid.resolution(Grid.grid_from_file("C:\\Users\\lisem\\OneDrive\\Documents\\ENSAE\\1A\\ensae-prog24\\input\\grid0.in")))