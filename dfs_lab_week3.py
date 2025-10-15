import pygame
import random
import time
from maze_search_week3 import get_neighbors, random_move, dfs

# --- CONFIG ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Maze-specific sizes
MAZE_SIZES = [(10, 10), (15, 15), (20, 20)]  # (rows, cols) for Easy, Medium, Hard

START = (0, 0)
GOAL = (COLS - 1, ROWS - 1)

# --- MAZE SEEDS ---
MAZE_SEEDS = [42, 789, 456]  # Seeds for reproducible mazes
MAZE_DENSITIES = [0.15, 0.20, 0.35]  # Wall density for each difficulty
MAZE_NAMES = ["Easy", "Medium", "Hard"]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 150)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))  # Extra space for timer and steps
pygame.display.set_caption("DFS Lab Scaffold with Walls")
font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# Load agent image
try:
    agent_image = pygame.image.load("peter.jpeg")
except:
    agent_image = None  # Fallback to circle if image not found


def generate_walls(seed, density, rows, cols):
    """Generate wall positions with a specific seed for reproducibility."""
    random.seed(seed)
    walls = set()
    for x in range(cols):
        for y in range(rows):
            if random.random() < density:
                walls.add((x, y))
    # Ensure start and goal are clear
    walls.discard(START)
    goal = (cols - 1, rows - 1)
    walls.discard(goal)
    return walls


def draw_grid(rows, cols):
    cell_width = WIDTH // cols
    cell_height = HEIGHT // rows
    for x in range(0, cols * cell_width + 1, cell_width):
        pygame.draw.line(screen, GRAY, (x, 0), (x, rows * cell_height))
    for y in range(0, rows * cell_height + 1, cell_height):
        pygame.draw.line(screen, GRAY, (0, y), (cols * cell_width, y))


def draw_cell(pos, color, rows, cols):
    x, y = pos
    cell_width = WIDTH // cols
    cell_height = HEIGHT // rows
    pygame.draw.rect(screen, color, (x * cell_width, y * cell_height, cell_width, cell_height))


def draw_agent(pos, rows, cols):
    x, y = pos
    cell_width = WIDTH // cols
    cell_height = HEIGHT // rows
    if agent_image:
        scaled_image = pygame.transform.scale(agent_image, (cell_width, cell_height))
        screen.blit(scaled_image, (x * cell_width, y * cell_height))
    else:
        # Fallback to circle if image not loaded
        center = (x * cell_width + cell_width // 2, y * cell_height + cell_height // 2)
        pygame.draw.circle(screen, GREEN, center, min(cell_width, cell_height) // 3)


def draw_timer(start_time, elapsed_time, started, paused, finished):
    if finished:
        label = font.render(f"Finished in {elapsed_time:.2f}s", True, RED)
    elif started and not paused:
        current_elapsed = elapsed_time + (time.time() - start_time)
        label = font.render(f"Time: {current_elapsed:.2f}s", True, BLACK)
    elif paused:
        label = font.render(f"Time: {elapsed_time:.2f}s (PAUSED)", True, BLACK)
    else:
        label = font.render(f"Time: 0.00s", True, BLACK)
    screen.blit(label, (10, HEIGHT + 10))


def draw_steps(steps):
    label = font.render(f"Steps: {steps}", True, BLACK)
    screen.blit(label, (10, HEIGHT + 40))


def draw_maze_info(maze_num, started, paused, finished):
    info_text = f"Maze: {MAZE_NAMES[maze_num]} (Press 1/2/3 to switch)"
    if not started:
        info_text += " | Press SPACE to start"
    elif paused:
        info_text += " | Press SPACE to resume"
    elif finished:
        info_text += " | Press SPACE to restart"
    else:
        info_text += " | Press SPACE to pause"
    label = small_font.render(info_text, True, BLACK)
    screen.blit(label, (10, HEIGHT + 70))


def main():
    running = True
    started = False
    paused = False
    finished = False
    agent_pos = START
    visited = set()
    current_maze = 0  # Start with first maze (Easy)
    current_rows, current_cols = MAZE_SIZES[current_maze]
    current_goal = (current_cols - 1, current_rows - 1)
    walls = generate_walls(MAZE_SEEDS[current_maze], MAZE_DENSITIES[current_maze], current_rows, current_cols)
    start_time = 0
    elapsed_time = 0
    steps = 0

    # Run DFS to get the path and visited order
    path, visited_order = dfs(START, current_goal, walls, current_rows, current_cols)
    current_step = 0  # Track current position in the path/visited order
    use_dfs = len(visited_order) > 0  # Use DFS if it returns results, otherwise fall back to random

    while running:
        clock.tick(10)  # frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Start/restart/pause with SPACE
                if event.key == pygame.K_SPACE:
                    if not started or finished:
                        # Start or restart
                        started = True
                        paused = False
                        finished = False
                        agent_pos = START
                        visited = set()
                        current_step = 0
                        start_time = time.time()
                        elapsed_time = 0
                        steps = 0
                    elif started and not finished:
                        # Toggle pause
                        paused = not paused
                        if paused:
                            # Store elapsed time when pausing
                            elapsed_time += time.time() - start_time
                        else:
                            # Reset start time when resuming
                            start_time = time.time()
                # Switch mazes with number keys
                elif event.key == pygame.K_1:
                    current_maze = 0
                    agent_pos = START
                    visited = set()
                    current_rows, current_cols = MAZE_SIZES[current_maze]
                    current_goal = (current_cols - 1, current_rows - 1)
                    walls = generate_walls(MAZE_SEEDS[current_maze], MAZE_DENSITIES[current_maze], current_rows, current_cols)
                    path, visited_order = dfs(START, current_goal, walls, current_rows, current_cols)
                    use_dfs = len(visited_order) > 0
                    current_step = 0
                    start_time = 0
                    elapsed_time = 0
                    steps = 0
                    finished = False
                    started = False
                    paused = False
                elif event.key == pygame.K_2:
                    current_maze = 1
                    agent_pos = START
                    visited = set()
                    current_rows, current_cols = MAZE_SIZES[current_maze]
                    current_goal = (current_cols - 1, current_rows - 1)
                    walls = generate_walls(MAZE_SEEDS[current_maze], MAZE_DENSITIES[current_maze], current_rows, current_cols)
                    path, visited_order = dfs(START, current_goal, walls, current_rows, current_cols)
                    use_dfs = len(visited_order) > 0
                    current_step = 0
                    start_time = 0
                    elapsed_time = 0
                    steps = 0
                    finished = False
                    started = False
                    paused = False
                elif event.key == pygame.K_3:
                    current_maze = 2
                    agent_pos = START
                    visited = set()
                    current_rows, current_cols = MAZE_SIZES[current_maze]
                    current_goal = (current_cols - 1, current_rows - 1)
                    walls = generate_walls(MAZE_SEEDS[current_maze], MAZE_DENSITIES[current_maze], current_rows, current_cols)
                    path, visited_order = dfs(START, current_goal, walls, current_rows, current_cols)
                    use_dfs = len(visited_order) > 0
                    current_step = 0
                    start_time = 0
                    elapsed_time = 0
                    steps = 0
                    finished = False
                    started = False
                    paused = False

        if started and not paused and not finished:
            if use_dfs:
                # Use DFS visited order to animate the search
                if current_step < len(visited_order):
                    agent_pos = visited_order[current_step]
                    visited.add(agent_pos)
                    steps += 1
                    current_step += 1

                    if agent_pos == current_goal:
                        finished = True
                        # Store final elapsed time
                        elapsed_time += time.time() - start_time
                else:
                    # If we've gone through all visited positions but haven't reached goal
                    # (shouldn't happen if DFS found a path)
                    finished = True
                    elapsed_time += time.time() - start_time
            else:
                # Fall back to random movement if DFS not implemented
                next_pos = random_move(agent_pos, walls, current_rows, current_cols)
                visited.add(agent_pos)
                if next_pos != agent_pos:  # Only count as a step if agent moved
                    steps += 1
                agent_pos = next_pos

                if agent_pos == current_goal:
                    finished = True
                    # Store final elapsed time
                    elapsed_time += time.time() - start_time

        # --- Draw ---
        screen.fill(WHITE)
        draw_grid(current_rows, current_cols)

        # Draw visited cells
        for pos in visited:
            draw_cell(pos, BLUE, current_rows, current_cols)

        # Draw walls
        for w in walls:
            draw_cell(w, BLACK, current_rows, current_cols)

        # Draw start and goal
        draw_cell(START, YELLOW, current_rows, current_cols)
        draw_cell(current_goal, RED, current_rows, current_cols)

        # Draw agent
        draw_agent(agent_pos, current_rows, current_cols)

        # Draw timer and steps
        draw_timer(start_time, elapsed_time, started, paused, finished)
        draw_steps(steps)
        draw_maze_info(current_maze, started, paused, finished)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
