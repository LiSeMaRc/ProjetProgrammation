from grid import Grid
from solver import Solver

import pygame 

import random

from math import sqrt

pygame.init()

class Interface(Grid): 
    """
    
    """
    def __init__(self, m, n, initial_state = [],width=500,height=500):
        super().__init__(m, n, initial_state = [])
        self.width=width
        self.height=height
        self.cell_size=(self.width-200)//max(self.m,self.n),(self.height-200)//max(self.m,self.n)
    
    def start(self):

        #Colours
        global window_color
        window_color=(175,211,227)
        global white
        white=(255,255,255)
        global black
        black=(0,0,0)
        rect_color=(47,106,133)

        #Fonts
        global title_font
        title_font=pygame.font.Font(None,50)
        global text_font
        text_font=pygame.font.Font(None,30)
        global font
        font=pygame.font.Font(None,20)

        #Sizes
        global rect_size
        rect_size=(self.width//10,self.height//10)

        #Creation of the window:
        global window
        window = pygame.display.set_mode((self.width, self.height))
        window.fill(window_color)

        #Title and instruction
        pygame.display.set_caption("Swap Puzzle") 

        title_text=title_font.render("Swap puzzle",True,black)
        window.blit(title_text,(25,25))

        text=text_font.render("Choose your level of difficulty",True,black)
        window.blit(text,(25,75))

        """
        Draw the buttons corresponding to each level.
        Deux questions: manière plus simple avec boucle? et je voulais le mettre dans une fonction mais pb de reconnaissance de l'objet rect1 même avec un return
        """
        #Creation of rectangles
        space=((self.width-200)-3*rect_size[0])//2
        global rect1
        rect1=pygame.Rect((100,self.height//2-rect_size[1]),rect_size)
        global rect2
        rect2=pygame.Rect((100+rect_size[0]+space,self.height//2-rect_size[1]),rect_size)
        global rect3
        rect3=pygame.Rect((100+2*(rect_size[0]+space),self.height//2-rect_size[1]),rect_size)
        

        #Drawing of rectangles
        pygame.draw.rect(window,rect_color,rect1)
        pygame.draw.rect(window,rect_color,rect2)
        pygame.draw.rect(window,rect_color,rect3)


        #Creation of the text    
        text1=font.render("Level1",True,white)
        text2=font.render("Level2",True,white)
        text3=font.render("Level3",True,white)


        #Writing of the text
        window.blit(text1,(rect1.x+rect_size[0]//10,rect1.y+rect_size[1]//2-5))
        window.blit(text2,(rect2.x+rect_size[0]//10,rect2.y+rect_size[1]//2-5))
        window.blit(text3,(rect3.x+rect_size[0]//10,rect3.y+rect_size[1]//2-5))


        pygame.display.update()
        Interface.choose_level(self)
        pygame.time.delay(10000)
    
    def draw_grid(self):

        window.fill(window_color)

        #Instructions:
        text=text_font.render("Solve this swap puzzle in a minimum time",True,white)
        rules=font.render("Don't swap diagonal cells and avoid obstacles or you will lose",True,white)
        window.blit(text,(50,30))
        window.blit(rules,(50,70))

        #horizontal lines
        for i in range(self.m+1): 
            pygame.draw.line(window, black, (100, 100+i * self.cell_size[1]), (100+self.n * self.cell_size[0], 100+i * self.cell_size[1]))

        #vertical lines
        for j in range(self.n+1):
            pygame.draw.line(window, black, (100+j * self.cell_size[0], 100), (100+j * self.cell_size[0], 100+self.m * self.cell_size[1]))
    
        #numbers
        for i in range(self.m):
            for j in range(self.n):
                text=font.render(str(self.state[i][j]),True,black)
                window.blit(text, (100+j*self.cell_size[0] + self.cell_size[0]//2-1, 100+i*self.cell_size[1] + self.cell_size[1]//2-1))
    
        pygame.display.update()
        
    
    def obstacle(self,number):
        """
        Returns a list of invalid swaps in the format [((i,j),(i+1),j)]

        Parameters
        -----------------------
        Number: between 1, 2, 3
        """
        red=(255, 87, 51)
        list_obstacles=[]
        if number==1:
            return list_obstacles
        elif number==2: 
            i=random.randint(0,self.m-2)
            j=random.randint(0,self.n-1) 
            list_obstacles.append(((i,j),(i+1,j)))
            pygame.draw.line(window, red, (100+j * self.cell_size[0],100+(i+1) * self.cell_size[1]), (100+(j+1) * self.cell_size[0],100+(i+1) * self.cell_size[1]))
            pygame.display.update()
            return list_obstacles
        elif number==3:
            i=random.randint(0,self.m-2)
            j=random.randint(0,self.n-1)
            k=random.randint(0,self.m-1)
            l=random.randint(0,self.n-2)
            list_obstacles.append(((i,j),(i+1,j)))
            list_obstacles.append(((k,l),(k,l+1)))
            pygame.draw.line(window, red, (100+j * self.cell_size[0],100+(i+1) * self.cell_size[1]), (100+(j+1) * self.cell_size[0],100+(i+1) * self.cell_size[1]))
            pygame.draw.line(window, red, (100+(l+1) * self.cell_size[0],100+k * self.cell_size[1]), (100+(l+1) * self.cell_size[0],100+(k+1) * self.cell_size[1]))
            pygame.display.update()
            return list_obstacles
        else:
            raise Exception("There can be only one or two obstacles.")
            
            

    
    def swap_cells(self,number):

        exit=False
        cell_to_swap=None
        list_swap=[]
        list_obstacles=self.obstacle(number)
        length=len(Solver.a_star(self))

        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #clic gauche
                        x,y=pygame.mouse.get_pos()
                        col=(x-100)//self.cell_size[0]
                        row=(y-100)//self.cell_size[1]
                        #Premier ou deuxième clic?
                        if cell_to_swap==None:
                            cell_to_swap=(row,col)
                        else: 
                            if (cell_to_swap,(row,col)) not in list_obstacles and ((row,col),cell_to_swap) not in list_obstacles :
                                
                                #Modification of state[i][j]
                                self.swap((row,col),cell_to_swap) #add error message if swap not allowed?
                                #Shortest way?  
                                list_swap.append(((row,col),cell_to_swap))
                                #Sorted grid?
                            
                                if self.node()==tuple(range(1,self.n*self.m+1)):
                                    if len(list_swap)==length:
                                        window.fill(window_color)
                                        text1=title_font.render("Congratulations!",True,black)
                                        text2=font.render("You solved the grid in the shortest way possible!",True,black)
                                        window.blit(text1,(50,150))
                                        window.blit(text2,(50,300))
                                        pygame.display.update()
                                        pygame.time.delay(10000)
                                    else:
                                        window.fill(window_color)
                                        text1=title_font.render("Congratulations!",True,black)
                                        text2=font.render("You solved the grid with "+str(len(list_swap))+" swaps.",True,black)
                                        text3=font.render("The optimal path contains "+str(length)+" swaps",True,black)
                                        window.blit(text1,(50,150))
                                        window.blit(text2,(50,250))
                                        window.blit(text3,(50,350))
                                        pygame.display.update()
                                else:
                                    self.draw_grid()
                                    list_obstacles=self.obstacle(number)
                                    pygame.display.update()
                            else:
                                raise Exception("The swap is not valid.")


                            #Reinitialisation for the next couple of swaps
                            cell_to_swap=None
    
    @staticmethod
    def controlled_difficulty_bis(level):
        """
        Generates a grid with a controlled level of difficulty.
        There are two components of the difficulty level: 
        - Size of the table (level+1)^2. The number of rows and colums are generated randomly.
        - Number of swaps: level*2. The swaps are also generated randomly. 
        Here only square grids
        
        Parameters:
        ------------------
        level from 1 to 3

        """
        #Difficulty: size of the grid
        size=(level+1)**2


        #number of rows and columns
        m=int(sqrt(size))
        n=int(sqrt(size))

        #Sorted_list with the determined size
        sorted_list=[]
        for i in range (1,size+1):
            sorted_list.append(i)

        #Grid creation
        grid=Interface(m,n,Grid.grid_from_tuple(tuple(sorted_list),m,n),500,500)

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


    def choose_level(self):
        exit = False

        while not exit: 

            for event in pygame.event.get(): #events: mouse, keyboard
            
                #Exit condition
                if event.type == pygame.QUIT: 
                    exit = True

                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if rect1.collidepoint(event.pos):
                        exit=True
                        grid=Interface.controlled_difficulty_bis(1)
                        Interface.draw_grid(grid)
                        Interface.swap_cells(grid,1)
                    elif rect2.collidepoint(event.pos):
                        exit=True
                        grid=Interface.controlled_difficulty_bis(2)
                        Interface.draw_grid(grid)
                        Interface.swap_cells(grid,2)
                    elif rect3.collidepoint(event.pos):
                        exit=True                        
                        grid=Interface.controlled_difficulty_bis(3)
                        Interface.draw_grid(grid)
                        Interface.swap_cells(grid,3)
                    



                            
                            

                            

    @classmethod
    def grid_from_file_bis(cls, file_name): 
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
            grid = Interface(m, n, initial_state,500,500)
        return grid
    

                

Interface.start(Interface.grid_from_file_bis("input\\grid2.in"))


