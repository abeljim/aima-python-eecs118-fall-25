"""
Search algorithms for maze navigation.
Students should implement their search algorithms here.
"""


def get_neighbors(pos, walls, rows, cols):
    """
    Get valid neighboring positions (not walls, within bounds).

    Args:
        pos: Current position as (x, y) tuple
        walls: Set of wall positions
        rows: Number of rows in the maze
        cols: Number of columns in the maze

    Returns:
        List of valid neighbor positions
    """
    x, y = pos
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    valid = [
        (x + dx, y + dy)
        for dx, dy in moves
        if 0 <= x + dx < cols and 0 <= y + dy < rows and (x + dx, y + dy) not in walls
    ]
    return valid


def random_move(pos, walls, rows, cols):
    """
    Make a random move from current position.
    This is the baseline implementation - students should replace this with DFS.

    Args:
        pos: Current position as (x, y) tuple
        walls: Set of wall positions
        rows: Number of rows in the maze
        cols: Number of columns in the maze

    Returns:
        Next position to move to
    """
    import random
    neighbors = get_neighbors(pos, walls, rows, cols)
    if neighbors:
        return random.choice(neighbors)
    return pos


def dfs(start, goal, walls, rows, cols):
    """
    Depth-First Search implementation.
    TODO: Students should implement this function.

    Args:
        start: Starting position as (x, y) tuple
        goal: Goal position as (x, y) tuple
        walls: Set of wall positions
        rows: Number of rows in the maze
        cols: Number of columns in the maze

    Returns:
        Tuple of (path, visited_order) where:
        - path: List of positions from start to goal (or empty if no path found)
        - visited_order: List showing order of exploration for visualization
    """
    # TODO: Implement DFS here
    # Hint: Use a stack to keep track of positions to explore
    # Hint: Keep track of the path taken to reach each position
    # Hint: Use get_neighbors() to find valid moves from a position

    return [], []  # Replace with your implementation
