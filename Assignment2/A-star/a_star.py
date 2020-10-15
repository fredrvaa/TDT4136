class AStar(object):
    """
    A* object containing methods for performing the A* algorithm on a gridmap
    """

    def __init__(self, map_obj):
        """
        Initialize A*

        Args:
            map_obj (MapObj): map consisting of a grid of cells
                This map is augmnented during the course of the A* algorithm.
        """

        self.map_obj = map_obj

        self.open = []
        self.closed = []
        self.path = []

        # Add start node into open list
        start_cell = self.map_obj.get_start_cell()
        start_cell.f = 0
        start_cell.g = 0
        start_cell.h = self._h(start_cell, self.map_obj.get_goal_cell())
        self.open.append(self.map_obj.get_start_cell())

    def update(self):
        """
        Update step for A* algorithm

        Return:
            running (boolean): wether or not the algorithm has terminated

        Each update step updates self.map_obj and the cells stored within it.
        This modifies the state of each cell.

        States:
        START - Cell is the start cell
        GOAL - Cell is the goal cell
        BARRIER - Cell can not be visited
        OPEN - Cell is in A* open set
        CLOSED - Cell is in A* closed set
        PATH - Cell is in shortest path from START to GOAL
        
        If the goal is reached, the path is recostructed and each cell in the
        path is set to state: PATH.

        The algorithm is based on pseudocode from
        https://en.wikipedia.org/wiki/A*_search_algorithm
        
        """

        if len(self.open):
            current_cell = self.open[0]
            current_index = 0
            for i, cell in enumerate(self.open):
                if cell.f < current_cell.f:
                    current_cell = cell
                    current_index = i

            self.open.pop(current_index)

            if current_cell.state not in ["START", "GOAL"]:
                self.map_obj.set_cell_state(current_cell, "CLOSED")  
            
            if current_cell == self.map_obj.get_goal_cell():
                c = current_cell
                while c is not None:
                    if c.state not in ["START", "GOAL"]:
                        self.map_obj.set_cell_state(c, "PATH")
                    self.path.append(c)
                    c = c.parent
                return False

            for neighbour in current_cell.neighbours:
                if neighbour.state in ["CLOSED", "BARRIER", "START"]: continue

                g = current_cell.g + neighbour.weight
                if g < neighbour.g:
                    neighbour.parent = current_cell
                    neighbour.g = g
                    neighbour.h = self._h(neighbour, self.map_obj.get_goal_cell())
                    neighbour.f = neighbour.g + neighbour.h

                    in_open = False
                    for open_cell in self.open:
                        if neighbour == open_cell:
                            in_open = True
                            break

                    if not in_open:
                        self.open.append(neighbour)
                        if neighbour.state not in ["START", "GOAL"]:
                            self.map_obj.set_cell_state(neighbour, "OPEN")  
        
            return True
        else:
            return False
            

    def _h(self, cell1, cell2):
        """
        Heuristic for calculating distance between two cells

        Args:
            cell1(Cell): first cell
            cell2(Cell): second cell
        
        Return:
            distance(int): manhatten distance between cell1 and cell2
        """
        
        return abs(cell1.row - cell2.row) + abs(cell1.col - cell2.col)
