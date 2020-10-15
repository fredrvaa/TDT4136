class Task(object):
    """
    Task information

    This class is used to generate (or load) tasks which in turn is used to
    generated a map.
    
    Typical use cases:
    task = Task(rows=10, cols=10)
        Initializes a task which is used to initialize a blank map
    task = Task(start_pos = (27, 18), goal_pos = (40, 32), path_to_map = "csv_maps/Samfundet_map_1.csv")
        Initializes a task which is used to initialize a map corresponding to Task1 in assignment.
    """

    def __init__(self, start_pos = None, goal_pos = None, end_goal_pos = None, path_to_map = None, rows = None, cols = None):
        """
        Initialize task

        Args:
            start_pos(tuple(int,int)): grid position of start node
            goal_pos(tuple(int,int)): grid position of goal node
            end_goal_node(tuple(int,int)): grid position of end goal node
                This is used if goal should move during search
            path_to_map(str): path/to/csv/map
            rows(int): number of rows
                Only used when initializing blank maps -- when path_to_map=None
            cols(int): number of columns
                Only used when initializing blank maps -- when path_to_map=None
        """
        
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.end_goal_pos = end_goal_pos if end_goal_pos is not None else self.goal_pos
        self.path_to_map = path_to_map
        if not self.path_to_map:
            self.rows = rows
            self.cols = cols