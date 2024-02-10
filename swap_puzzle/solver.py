from grid import Grid

class Solver(Grid): 
    """
    A solver class, to be implemented.
    """
    def __init__(self, m, n, initial_state = []):
        super().__init__(m, n, initial_state = [])
    
    def get_solution(self):
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
        print(self.state)
        return list_swap
    
                        
                            



