# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from  grid import Grid #????

class Test_Swap(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input//grid0.in") #vérifier si fonctionne avec un seul slash
        grid.swap((0,0),(0,1))
        self.assertEqual(grid.state, [[4, 2], [3, 1]])
        grid.swap((1,0),(1,1))
        self.assertEqual(grid.state, [[4, 2], [1, 3]]) #garde modif en mémoire?
        grid.swap((0,0),(1,0))
        self.assertEqual(grid.state, [[1, 2], [4, 3]])
        grid.swap((0,1),(1,1))
        self.assertEqual(grid.state, [[1, 3], [4, 2]])
        grid.swap((0,0),(1,1))
        self.assertRaises("The swap is invalid")
        grid.swap((0,1),(1,0))
        self.assertRaises("The swap is invalid")

    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid1.in") #deux slashs?
        grid.swap((3,0), (3,1))
        self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]]) #rajouter les interdits quand compris exception
    
    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid2.in") #deux slashs?
        #Rows
        grid.swap((0,1), (0,2))
        self.assertEqual(grid.state, [[5,7,3], [1,8,6], [4,2,9]])
        grid.swap((0,0), (0,1))
        self.assertEqual(grid.state, [[5,3,7], [1,8,6], [4,2,9]])
        grid.swap((1,0), (1,1))
        self.assertEqual(grid.state, [[5,3,7], [8,1,6], [4,2,9]])
        grid.swap((1,1), (1,2))
        self.assertEqual(grid.state, [[5,3,7], [8,6,1], [4,2,9]])
        grid.swap((2,0), (2,1))
        self.assertEqual(grid.state, [[5,3,7], [8,6,1], [2,4,9]])
        grid.swap((2,1), (2,2))
        self.assertEqual(grid.state, [[5,3,7], [8,6,1], [2,9,4]])
        #Columns
        grid.swap((0,0), (1,0))
        self.assertEqual(grid.state, [[8,3,7], [5,6,1], [2,9,4]])
        grid.swap((1,0), (2,0))
        self.assertEqual(grid.state, [[8,3,7], [2,6,1], [5,9,4]])
        grid.swap((0,1), (1,1))
        self.assertEqual(grid.state, [[8,6,7], [2,3,1], [5,9,4]])
        grid.swap((1,1), (2,1))
        self.assertEqual(grid.state, [[8,6,7], [2,9,1], [5,3,4]])
        grid.swap((0,2), (1,2))
        self.assertEqual(grid.state, [[8,6,1], [2,9,7], [5,3,4]])
        grid.swap((1,2), (2,2))
        self.assertEqual(grid.state, [[8,6,1], [2,9,4], [5,3,7]])

    def test_grid0_seq(self):
        grid = Grid.grid_from_file("input/grid0.in")
        grid.swap_seq([((0,0), (0,1)), ((0,1), (1,1)),((1,0), (0,0)) ])        
        self.assertEqual(grid.state, [[3,1], [4,2]])

    def test_grid1_seq(self):
        grid = Grid.grid_from_file("input/grid1.in")
        grid.swap_seq([((3,0), (3,1)), ((3,0), (3,1))])        
        self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [8, 7]])


if __name__ == '__main__':
    unittest.main()
