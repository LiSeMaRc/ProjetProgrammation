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
            coordonnees_i = (np.(floor((i-1)/(self.n))), (i-1)%(self.n)) #définit les coordonnées où i devrait se trouver 
       
        #On fait une double boucle pour déplacer les chiffres 
        for m_i in range(0,self.m): 
            for n_i in range(0,self.n):
                i = self.state(m_i, n_i)
                if (m_i,n_i) == (np.floor((i-1)/self.n), (i-1)%(self.n)):
                    i = i
                elif (i-1)%3 - n_i < 0 :
                    for j in range (1, n_i+1) : 
                        self.swap(self, 
                

