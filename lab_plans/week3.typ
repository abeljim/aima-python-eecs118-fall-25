= Week 3 Lab Plan: Depth-First Search (DFS) Pathfinding

== Overview
This lab session focuses on implementing Depth-First Search (DFS) algorithm for maze navigation. Students will work with a Pygame-based visualization tool to understand how DFS explores a maze and compares to random movement strategies. This lab bridges the gap between theoretical search algorithms and practical implementation.

== Learning Objectives
By the end of this lab, students will be able to:
- Understand the DFS algorithm and how it explores state spaces
- Implement DFS for pathfinding in a grid-based maze
- Compare DFS performance against random movement
- Work with stack-based data structures for search
- Analyze search algorithm efficiency (steps taken, time complexity)
- Understand the difference between explored nodes and optimal paths

== Prerequisites
- Completion of Week 2 lab (environment setup)
- Understanding of stacks and recursion
- Basic knowledge of search algorithms from lectures
- Familiarity with Python data structures (lists, sets, tuples)

== Important: Update Your Environment

=== Pull Latest Changes
Before starting this lab, make sure to pull the latest changes from the repository:

*Using Git (CLI)*:
```bash
cd aima-python-eecs118-fall-25
git pull origin master
```

*Using GitHub Desktop*:
- Open the repository in GitHub Desktop
- Click "Fetch origin" button at the top
- If updates are available, click "Pull origin"

=== Update Conda Environment
The `environment.yml` file has been updated with new dependencies (including Pygame). Update your conda environment:

```bash
conda activate aima-python
conda env update -f environment.yml --prune
```

If you encounter issues, you can recreate the environment from scratch:
```bash
conda deactivate
conda env remove -n aima-python
conda env create -f environment.yml
conda activate aima-python
```

== Lab Activities

=== 1. Understanding the Scaffold (15 minutes)

==== Run the Initial Program
```bash
python dfs_lab_week3.py
```

==== Explore the Interface
Students should familiarize themselves with:

+ *Controls*:
  - `SPACE`: Start/Pause/Resume the simulation
  - `1/2/3`: Switch between Easy/Medium/Hard difficulty mazes
  - The simulation won't start until you press SPACE

+ *Visual Elements*:
  - *Yellow cell*: Start position (top-left corner: 0,0)
  - *Red cell*: Goal position (bottom-right corner)
  - *Black cells*: Walls/obstacles
  - *Blue cells*: Visited positions
  - *Green circle/image*: The agent

+ *Maze Sizes*:
  - *Easy (1)*: 10x10 grid
  - *Medium (2)*: 15x15 grid
  - *Hard (3)*: 20x20 grid
  - The grid only renders the used space for cleaner visualization

+ *Information Display*:
  - *Timer*: Tracks elapsed time (pauses when simulation is paused)
  - *Steps*: Number of moves made by the agent
  - *Maze difficulty*: Current maze and controls

==== Observe Random Movement
- Start the simulation and watch the agent move randomly
- Note how inefficient random movement is for reaching the goal
- Try different difficulty levels
- *Question*: Why does random movement struggle in harder mazes?

=== 2. Understanding the Code Structure (20 minutes)

The code is now organized into two files:

==== `maze_search_week3.py` - Your Implementation File
This is where you'll implement your DFS algorithm. It contains:

*`get_neighbors(pos, walls, rows, cols)`*
```python
def get_neighbors(pos, walls, rows, cols):
    x, y = pos
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    valid = [
        (x + dx, y + dy)
        for dx, dy in moves
        if 0 <= x + dx < cols and 0 <= y + dy < rows and (x + dx, y + dy) not in walls
    ]
    return valid
```
- Returns all valid neighboring cells (not out of bounds, not walls)
- Movement directions: right, left, down, up
- *Question*: Why does order matter for DFS?

*`random_move(pos, walls, rows, cols)`*
```python
def random_move(pos, walls, rows, cols):
    import random
    neighbors = get_neighbors(pos, walls, rows, cols)
    if neighbors:
        return random.choice(neighbors)
    return pos
```
- Current baseline: picks a random valid neighbor

*`dfs(start, goal, walls, rows, cols)`*
- Currently returns empty lists: `return [], []`
- *Task*: This is what you'll implement!
- Should return: `(path, visited_order)`

==== `dfs_lab_week3.py` - Visualization Code
- Contains all the pygame visualization
- You don't need to modify this file
- It imports and uses functions from `maze_search_week3.py`

=== 3. Implementing DFS (Main Exercise - 45 minutes)

==== Understanding DFS Algorithm

Depth-First Search uses a *stack* to explore paths. Here's the conceptual algorithm:

```
DFS(start, goal):
    1. Initialize a stack with the start position
    2. Initialize an empty set for visited nodes
    3. While the stack is not empty:
        a. Pop a position from the stack
        b. If this position is the goal, success!
        c. If this position hasn't been visited:
            - Mark it as visited
            - Get all valid neighbors
            - Push unvisited neighbors onto the stack
    4. If stack is empty and goal not found, no path exists
```

==== Your Task

Implement the `dfs()` function in `maze_search_week3.py`.

*Function Signature*:
```python
def dfs(start, goal, walls, rows, cols):
    """
    Args:
        start: Starting position as (x, y) tuple
        goal: Goal position as (x, y) tuple
        walls: Set of wall positions
        rows: Number of rows in the maze
        cols: Number of columns in the maze

    Returns:
        Tuple of (path, visited_order) where:
        - path: List of positions from start to goal
        - visited_order: List showing order of exploration
    """
```

*Key Considerations*:
+ Your DFS should compute the *entire path* at once (not frame-by-frame)
+ Use a stack to keep track of positions to explore
+ Keep track of the path taken to reach each position
+ Use `get_neighbors()` to find valid neighboring cells
+ Return both the solution path and the order cells were visited

*Implementation Hints*:
```python
# Pseudocode structure:
stack = [(start, [start])]  # (current_position, path_to_here)
visited = set()
visited_order = []

while stack is not empty:
    current, path = stack.pop()

    if current already visited:
        continue

    mark current as visited
    add current to visited_order

    if current == goal:
        return (path, visited_order)

    for each neighbor of current:
        if neighbor not visited:
            add (neighbor, path + [neighbor]) to stack

return ([], visited_order)  # No path found
```

*What to modify*:
- Only edit `maze_search_week3.py`
- Implement the `dfs()` function
- The `get_neighbors()` function is already provided - use it!

*What NOT to change*:
- Don't modify `dfs_lab_week3.py`
- Don't change `get_neighbors()` or `random_move()` (yet)

=== 4. Testing and Comparison (20 minutes)

==== Test Your Implementation
+ Run your DFS implementation on the Easy maze
+ Observe the search pattern - does it explore depth-first?
+ Check if it successfully reaches the goal
+ Test on Medium and Hard mazes

==== Performance Analysis
Compare DFS vs Random Movement:

#figure(
  table(
    columns: 3,
    [*Metric*], [*Random Movement*], [*DFS*],
    [Steps to goal], [?], [?],
    [Time to goal], [?], [?],
    [Cells explored], [?], [?],
    [Success rate], [?], [?],
  )
)

*Questions for Discussion*:
+ Does DFS always find a path if one exists?
+ Does DFS find the _shortest_ path?
+ What happens when DFS encounters dead ends?
+ How does wall density affect DFS performance?

=== 5. Extensions (Optional Challenge Activities)

==== Challenge 1: Path Visualization
Modify the code to highlight the actual path taken (not just visited cells):
- Store the path from start to goal
- Draw the path in a different color (e.g., GREEN)

```python
# Add to drawing section:
for pos in path:
    draw_cell(pos, GREEN)
```

==== Challenge 2: Backtracking Visualization
Show when DFS backtracks:
- Use different colors for active exploration vs backtracking
- Add a counter for backtrack operations

==== Challenge 3: Compare with BFS
Implement Breadth-First Search (BFS) as well:
- Use a queue instead of a stack
- Compare path length and exploration patterns
- Which finds shorter paths?

==== Challenge 4: Add Diagonal Movement
Modify `get_neighbors()` to include diagonal moves:
```python
moves = [(1, 0), (-1, 0), (0, 1), (0, -1),
         (1, 1), (1, -1), (-1, 1), (-1, -1)]
```
How does this affect DFS performance?

==== Challenge 5: Interactive Maze Editor
Add mouse click functionality to:
- Add/remove walls by clicking
- Change start/goal positions
- Create custom maze challenges

== Common Issues and Debugging

=== Issue 1: Agent Gets Stuck
*Problem*: Agent stops moving but hasn't reached goal

*Solution*: Check if visited set is being updated correctly and if all neighbors are being explored

=== Issue 2: Stack Overflow
*Problem*: Recursion depth exceeded (if using recursive DFS)

*Solution*: Use iterative DFS with explicit stack instead

=== Issue 3: Wrong Path
*Problem*: Agent doesn't reach the goal or takes invalid moves

*Solution*: Verify `get_neighbors()` is filtering walls correctly

=== Issue 4: Performance Issues
*Problem*: Simulation runs too slow or fast

*Solution*: Adjust `clock.tick(10)` value (line 132) - higher = faster

== Deliverables

Students should be able to demonstrate:
+ Working DFS implementation in `maze_search_week3.py` that successfully navigates all three maze difficulties
+ Comparison data between random movement and DFS
+ Understanding of when DFS is appropriate vs other search algorithms
+ Code that properly imports and uses functions from `maze_search_week3.py`

== Additional Resources

- AIMA Chapter 3: Solving Problems by Searching
- Pygame documentation: #link("https://www.pygame.org/docs/")[pygame.org]
- Visualization of DFS: #link("https://visualgo.net/en/dfsbfs")[visualgo.net/en/dfsbfs]
- Python data structures (stack/queue): #link("https://docs.python.org/3/tutorial/datastructures.html")[docs.python.org]

== Lab Submission (If Applicable)

If your instructor requires submission:
+ Submit your modified `maze_search_week3.py` file with completed `dfs()` function
+ Include a brief report (1-2 paragraphs) comparing DFS to random movement
+ Screenshot of successful completion on Hard difficulty
+ Answer to discussion questions from section 4

== Next Week Preview

Week 4 will build on this lab by exploring:
- Informed search strategies (A\*, Greedy Best-First)
- Heuristic functions for pathfinding
- Comparison of uninformed vs informed search
