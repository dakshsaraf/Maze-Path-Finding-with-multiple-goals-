# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)

from queue import PriorityQueue
from copy import deepcopy

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def find_path(start,end,parent_map):
    sol = [end[0]]
    temp = parent_map[end]
    while(temp != start):
        sol.append(temp[0])
        temp = parent_map[temp]
    sol.append(start[0])
    return sol[::-1]

def get_neighbours(maze,node):
    nbr_list = []
    for nbr in maze.getNeighbors(node[0][0],node[0][1]):
        objectives = list(deepcopy(node[1]))
        if nbr in objectives:
            objectives.remove(nbr)
        nbr_node = (nbr,tuple(objectives))
        nbr_list.append(nbr_node)
    return nbr_list

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    start = maze.getStart()
    objectives = tuple(maze.getObjectives())
    start_state = (start,objectives) 
    queue = [start_state]
    visited = set(start_state)
    parent_map = {}
    
    # state = (node,[objectives])
    while(len(queue)>0):
        node = queue.pop(0)
        if(len(node[1]) == 0):
            return find_path(start_state,node,parent_map)

        for nbr in get_neighbours(maze,node):
            if nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)
                parent_map[nbr] = node
    return []

def manhattanDistance(start,end):
    return abs(start[0]-end[0])+abs(start[1]-end[1])

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    start = maze.getStart()
    objectives = tuple(maze.getObjectives()) 
    start_state = (start,objectives)
    open_set = PriorityQueue()
    g_map = {}
    parent_map = {}
    
    open_set.put((manhattanDistance(start_state[0],start_state[1][0]),start_state))
    g_map[start_state] = 0
    
    while(len(open_set.queue)>0):
        node = open_set.get()[1]
        if(len(node[1]) == 0):
            return find_path(start_state,node,parent_map)

        for nbr in get_neighbours(maze,node):
            new_g = g_map[node] + 1 
            if nbr not in g_map or new_g < g_map[nbr]:
                g_map[nbr] = new_g
                h = 0
                if(len(nbr[1])!=0): h = manhattanDistance(nbr[0],nbr[1][0])
                open_set.put((new_g+h,nbr))
                parent_map[nbr] = node
    return []

def cornerHeuristic(node):
    position, objectives = node
    heuristic = 0
    unvisited = list(deepcopy(objectives))
    while unvisited:
        distance, corner = min([(manhattanDistance(position, corner), corner) for corner in unvisited])
        heuristic += distance
        position = corner
        unvisited.remove(corner)

    return heuristic


def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    start = maze.getStart()
    objectives = tuple(maze.getObjectives()) 
    start_state = (start,objectives)
    open_set = PriorityQueue()
    g_map = {}
    parent_map = {}
    
    open_set.put((cornerHeuristic(start_state),start_state))
    g_map[start_state] = 0
    
    while(len(open_set.queue)>0):
        node = open_set.get()[1]
        if(len(node[1]) == 0):
            return find_path(start_state,node,parent_map)

        for nbr in get_neighbours(maze,node):
            new_g = g_map[node] + 1 
            if nbr not in g_map or new_g < g_map[nbr]:
                g_map[nbr] = new_g
                open_set.put((new_g+cornerHeuristic(nbr),nbr))
                parent_map[nbr] = node
    return []



def bfs_helper_heuristic(maze, start, end):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    start = start
    objectives = tuple([end])
    start_state = (start,objectives) 
    queue = [start_state]
    visited = set(start_state)
    parent_map = {}
    
    # state = (node,[objectives])
    while(len(queue)>0):
        node = queue.pop(0)
        if(len(node[1]) == 0):
            return find_path(start_state,node,parent_map)

        for nbr in get_neighbours(maze,node):
            if nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)
                parent_map[nbr] = node
    return []

def multi_heuristic(node,maze):

    # position, objectives = node
    # distances = [len(bfs_helper_heuristic(maze,position,i)) for i in objectives]
    # return max(distances) if len(distances) > 0 else 0
    
    
    #REDO WITH MINIMUM SPANNING TREE

    return 0

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    objectives = tuple(maze.getObjectives()) 
    start_state = (start,objectives)
    open_set = PriorityQueue()
    g_map = {}
    parent_map = {}
    
    open_set.put((multi_heuristic(start_state,maze),start_state))
    g_map[start_state] = 0
    
    while(len(open_set.queue)>0):
        node = open_set.get()[1]
        if(len(node[1]) == 0):
            return find_path(start_state,node,parent_map)

        for nbr in get_neighbours(maze,node):
            new_g = g_map[node] + 1 
            if nbr not in g_map or new_g < g_map[nbr]:
                g_map[nbr] = new_g
                open_set.put((new_g+multi_heuristic(nbr,maze),nbr))
                parent_map[nbr] = node
    return []


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
