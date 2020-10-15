import pygame
import time
import os

from map_obj import MapObj
from a_star import AStar
from task import Task


# TASK1-5 corresponding with tasks in Assignment 2
TASK0 = Task(rows = 50, cols = 50) # Initial map is blank
TASK1 = Task(start_pos = (27, 18), goal_pos = (40, 32), path_to_map = "csv_maps/Samfundet_map_1.csv")
TASK2 = Task(start_pos = (40, 32), goal_pos = (8, 5), path_to_map = "csv_maps/Samfundet_map_1.csv")
TASK3 = Task(start_pos = (28, 32), goal_pos = (6, 32), path_to_map = "csv_maps/Samfundet_map_2.csv")
TASK4 = Task(start_pos = (28, 32), goal_pos = (6, 32), path_to_map = "csv_maps/Samfundet_map_Edgar_full.csv")
TASK5 = Task(start_pos = (14, 18), goal_pos = (6, 36), end_goal_pos = (6, 7), path_to_map = "csv_maps/Samfundet_map_2.csv")

TASKS = [TASK0,TASK1,TASK2,TASK3,TASK4,TASK5]

# Goal moves each MOVE_RATE iteration of A*
MOVE_RATE = 4

class Visualizer(object):
    """
    Pygame visualizer of a map with cells
    """

    def __init__(self, cell_size = 16):
        """
        Initializes visualizer

        Args:
            cell_size(int): how many pixels a cell in the grid is
        """

        self.map_obj = MapObj(TASK0)
        self.curr_task_num = 0
        self.cell_size = cell_size
        self.win_width = self.cell_size * self.map_obj.cols
        self.win_height = self.cell_size * self.map_obj.rows

        self.running = True
        self.a_star_running = False
        self.drawing_weight = 1

        self.a_star = None

        self.tick_counter = 0

        self.window = pygame.display.set_mode((self.win_width,self.win_height))
        pygame.display.set_caption("A* Visualizer")

        pygame.font.init() 
        self.font = pygame.font.Font(pygame.font.get_default_font(), cell_size)

        self._main()

    def _main(self):
        """
        Main loop running the visualization
        """

        while self.running:
            #Event Tasking
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: # Start A*
                        if self.map_obj.start_pos and self.map_obj.start_pos:
                            self.map_obj.clean()
                            self.a_star = AStar(self.map_obj)
                            self.a_star_running = True
                        else:
                            print("Set start and goal positions before running A*")
                    elif event.key == pygame.K_r: # Reset map
                        self.map_obj.reset()
                        self.a_star_running = False
                    elif event.key == pygame.K_p: # Take sceenshot
                        os.makedirs("A_star_visualization_images", exist_ok=True)
                        pygame.image.save(self.window, f"A_star_visualization_images/task{self.curr_task_num}.png")
                    elif event.key == pygame.K_ESCAPE: # Quit application
                        self.running = False
                        pygame.quit()
                        quit()
                    else:
                        try:
                            # Sets map to task specified in TASKS
                            # TASK1-5 are the tasks given in assignment
                            self.curr_task_num = int(pygame.key.name(event.key))
                            task = TASKS[self.curr_task_num]
                            self.map_obj = MapObj(task)
                            self._recalc_window()
                        except:
                            print("Not a mapped key")
                    
                # Draws weighted "STANDARD" cells
                if pygame.mouse.get_pressed()[0]: # Left mouse click
                    pos = pygame.mouse.get_pos()
                    row, col = self._get_grid_pos(pos)
                    cell = self.map_obj.cells[row][col]
                    self.map_obj.set_cell_state(cell, "STANDARD", self.drawing_weight)
                
                # Draws "START" and "GOAL" cells
                elif pygame.mouse.get_pressed()[1]: # Middle mouse click
                    pos = pygame.mouse.get_pos()
                    row, col = self._get_grid_pos(pos)
                    cell = self.map_obj.cells[row][col]
                    if self.map_obj.start_pos is None and cell.state not in ["START", "GOAL"]:
                        self.map_obj.set_cell_state(cell, "START", cell.weight)
                    elif self.map_obj.goal_pos is None and cell.state not in ["START", "GOAL"]:
                        self.map_obj.set_cell_state(cell, "GOAL", cell.weight)
                    elif cell.state in ["START", "GOAL"]:
                        self.map_obj.set_cell_state(cell, "STANDARD", cell.weight)
                    self.a_star_running = False
                    self.map_obj.clean()

                # DRAWS "BARRIER" cells
                elif pygame.mouse.get_pressed()[2]: # Right mouse click
                    # Gets cell from mouseclick
                    pos = pygame.mouse.get_pos()
                    row, col = self._get_grid_pos(pos)
                    cell = self.map_obj.cells[row][col]
                    # Set cell state to barrier
                    self.map_obj.set_cell_state(cell, "BARRIER", -1)

            # Update map with A* update
            if self.a_star_running:
                self.tick_counter += 1
                if not self.tick_counter % MOVE_RATE:
                    self.map_obj.move_goal()
                self.a_star_running = self.a_star.update()

            # Draw window
            self._draw()
            
            # Update display and clock
            pygame.display.update()

    def _recalc_window(self):
        """
        Recalculates window size

        This should be called when the size of self.map_obj is changed.
        """

        self.win_width = self.cell_size * self.map_obj.cols
        self.win_height = self.cell_size * self.map_obj.rows

        self.window = pygame.display.set_mode((self.win_width,self.win_height))

    def _draw(self):
        """
        Draws state of self.map_obj to screen
        """

        self.window.fill((255,255,255))

        # Draws all cells
        for j, row_cells in enumerate(self.map_obj.cells):
            for i, cell in enumerate(row_cells):
                x = i * self.cell_size
                y = j * self.cell_size
                pygame.draw.rect(self.window, cell.color, (x, y, self.cell_size, self.cell_size))
                if cell.state == "START":
                    letter = self.font.render("S",1,(0,0,0))
                    self.window.blit(letter,(x + self.cell_size / 8, y + self.cell_size / 8))
                elif cell.state == "GOAL":
                    letter = self.font.render("G",1,(0,0,0))
                    self.window.blit(letter,(x + self.cell_size / 8, y + self.cell_size / 8))

                
        # Draws grid on top of cells
        for col in range(self.map_obj.cols):
            x1 = x2 = col * self.cell_size
            y1 = 0
            y2 = self.win_height
            pygame.draw.line(self.window, (100,100,100), (x1,y1), (x2,y2))
            
        for row in range(self.map_obj.rows):
            x1 = 0
            x2 = self.win_width
            y1 = y2 = row * self.cell_size
            pygame.draw.line(self.window, (100,100,100), (x1,y1), (x2,y2))


    def _get_grid_pos(self, pos):
        """
        Get grid position from mouse position

        Args:
            pos(tuple(int,int)): (x,y) position

        Return:
            row(int), col(int): grid position
        """

        row = pos[1] // self.cell_size
        col = pos[0] // self.cell_size
        return row, col 
