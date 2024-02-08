from grid import Grid
import numpy as np 

class Solver(): 
    """
    A solver class, to be implemented.
    """
    
    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        # NOTE: you can add other methods and subclasses as much as necessary. The only thing imposed is the format of the solution returned.
        raise NotImplementedError
        for i in range(1, (self.m)*(self.n) +1) : 
            coordinates_i = (np.(floor((i-1)/(self.n))), (i-1)%(self.n)) #Defines i's coordinates 
       
        #Creating a double loop to move i into the right column and then to the right row 
            T = [] #Empty list which will be filled with all the necessary swaps 
            for m_i in range(0,self.m + 1 ): 
                for n_i in range(0,self.n + 1):
                    i = self.state(m_i, n_i)
                    if (m_i,n_i) == (np.floor((i-1)/self.n), (i-1)%(self.n)):
                        i = i
                    elif (i-1)%(self.n) - n_i < 0 :
                        L = [] #Creates an empty list
                        for j in range (1,abs((i-1)%(self.n) - n_i)) : 
                            L.append(((m_i,n_i),(m_i,n_i-j))) #Adding the swaps needed to get i to the right column
                        Grid.swap_seq(L)
                    elif (i-1)%(self.n) - n_i > 0: 
                        c = n_i
                        for j in range(1,abs((i-1)%(self.n) - n_i)):
                            L.append(((m_i,c),(m_i,n_i+j)))
                            c = n_i + j 
                        Grid.swap_seq(L)
                if m_i = np.(floor((i-1)/(self.n)):
                    i = i
                else :
                    R = []
                    l = m_i
                    for k in range(1, abs(np.(floor((i-1)/(self.n)) - m_i)) :
                        R.append((l,(i-1)%(self.n)),(m_i + k,(i-1)%(self.n)))
                        l = m_i + k
                    Grid.swap_seq(R)
                T.append(L+R)
            return(T)
                
            
                
                
            
                    
                

