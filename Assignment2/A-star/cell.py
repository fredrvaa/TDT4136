import math

# Color configuration based on state
COLORS = {
    "STANDARD":(255, 255, 255),
    "BARRIER":(0, 0, 0),
    "START":(255, 102, 102),
    "GOAL":(102, 255, 153),
    "OPEN":(255, 153, 0),
    "CLOSED":(0, 153, 204),
    "PATH":(255, 204, 102)
}

# Darkens shade of cells with higher weight. Best results in range 0.2-0.5
DARKEN_FACTOR = 0.2

def set_color(state, weight):
    """
    Sets color based on state

    Args:
        weight(int): weight of a standard cell
    
    Return:
        color((int,int,int)): RGB color

    This function darkens color of STANDARD cells based on weight.
    """

    if weight > 1 and state == "STANDARD":
        color = tuple([c * (1 - DARKEN_FACTOR)**weight for c in COLORS[state]])
    else:
        color = COLORS[state]
    return color

class Cell(object):
    """
    Individual cell component used to create map
    """
    
    def __init__(self, row, col, state, weight):
        """
        Initializes cell

        Args:
            row(int): row position of cell
            col(int): column position of cell
            state(str): cell state
            weight(int): weight of cell
                This weight is associated with how costly it is to move through this
                cell for a given algorithm.

        A* dependent variables are also initialized here.
        If more algorithms were to be implemented, storing them in the cell
        class would not be the best option, but since we only concider A* here
        it is tolerable.
        """
        
        self.row = row
        self.col = col
        self.state = state
        self.weight = weight
        self.color = set_color(self.state, self.weight)

        # A* dependent variables
        self.neighbours = []
        self.parent = None
        self.g = math.inf
        self.h = math.inf
        self.f = self.g + self.h

    def set_state(self, state, weight = None):
        """
        Sets cell state

        Args:
            state(str): cell state
            weight(int): weight of cell
                It is often desirable to only change state, and not having to reset
                weight. Thus default weight is None;
        """

        self.state = state
        if weight is not None:
            self.weight = weight
        self.color = set_color(self.state, self.weight)

    def reset_scores(self):
        """
        Resets A* scores
        """

        self.g = math.inf
        self.h = math.inf
        self.f = self.g + self.h

    def __eq__(self, other):
        """
        Overriden dunder method which compares equality of two cells based
        purely on grid position

        Args:
            other(Cell): cell to compare with

        Return:
            equality(bool): equality based on grid position
        """

        return self.row == other.row and self.col == other.col
