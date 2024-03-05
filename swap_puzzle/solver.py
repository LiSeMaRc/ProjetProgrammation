from grid import Grid
from graph import Graph
import heapq

class Solver(Grid): 
    """
    A solver class, to be implemented.
    """
    def __init__(self, m, n, initial_state = []):
        super().__init__(m, n, initial_state = [])
    
    def simple_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        list_swap=[]
        for k in range(1,self.m*self.n+1):
            row=(k-1)//self.n
            column=(k-1)%self.n
            for i in range(self.m):
                for j in range(self.n):
                    if self.state[i][j]==k:
                        if i<row:
                            for l in range(i,row):
                                list_swap.append(((l,j),(l+1,j)))
                                self.swap((l,j),(l+1,j))
                        if i>row:
                            for l in range(i,row,-1):
                                list_swap.append(((l,j),(l-1,j)))
                                self.swap((l,j),(l-1,j))
                        if j<column:
                            for l in range(j,column):
                                list_swap.append(((i,l),(i,l+1)))
                                self.swap((i,l),(i,l+1))
                        if j>column:
                            for l in range(j,column,-1):
                                list_swap.append(((i,l),(i,l-1)))
                                self.swap((i,l),(i,l-1))
        return list_swap
    #Complexity: (m*n)^2(m+n)
    
    def bfs_solution(self):
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

    def short_bfs_solution(self):
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
        counter=0

        while len(open_list)>0:
            counter=counter+1
            
            
            c,ext_node=heapq.heappop(open_list)
            #print("\n========================")
            # print(open_list[:10])
            #print("Selected node:", c, ext_node)
            #print("open_list:", open_list)
            #input()
            #premier élément de la liste, c=coût, n=node sous forme de tuple
            # print(open_list)
            # print("ext_node",ext_node)
            # print("dst",dst)
            # print(ext_node==dst)
            if ext_node==dst: #tuples
                p=ext_node
                while p !=src:
                    path.insert(0,previous_nodes[p])
                    #print("p",p,"previous",previous_nodes[p])
                    p=previous_nodes[p]
                    #print("nouveau p",p)
                    
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
                  if node not in closed_list or src_cost[node]>src_cost[ext_node]+1:
                      
                    #   if node in closed_list:
                    #       print("Last src_cost", src_cost[node])
                      #Actualisation du dictionnaire src_cost:
                      src_cost[node]=src_cost[ext_node]+1

                    #   if node in closed_list:
                    #       print("New src_cost", src_cost[node])
                    #       print()

                      #Ajout du tuple (coût,noeud) à la file
                      node_cost=src_cost[node]+self.heuristic(node)

                    #   print("node",node)
                    #   print("node cost", src_cost[node], src_cost[ext_node]+1, node_cost)

                      heapq.heappush(open_list,(node_cost,node)) 
                      
                      #Ajout du noeud à la liste des noeuds visités
                      closed_list.append(node)
                      #Actualisation du dictionnaire avec coût du noeud
                      cost[node]=node_cost
                      #Actualisation du dico previous nodes
                      previous_nodes[node]=ext_node
                      #print("previous node fin",previous_nodes[node])
        return None              


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