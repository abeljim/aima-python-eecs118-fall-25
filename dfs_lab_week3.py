import pygame
import random
import time

# --- CONFIG ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

START = (0, 0)
GOAL = (COLS - 1, ROWS - 1)

# --- MAZE SEEDS ---
MAZE_SEEDS = [42, 123, 456]  # Seeds for reproducible mazes
MAZE_DENSITIES = [0.15, 0.25, 0.35]  # Wall density for each difficulty
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
    agent_image = pygame.transform.scale(agent_image, (CELL_SIZE, CELL_SIZE))
except:
    agent_image = None  # Fallback to circle if image not found


def generate_walls(seed, density):
    """Generate wall positions with a specific seed for reproducibility."""
    random.seed(seed)
    walls = set()
    for x in range(COLS):
        for y in range(ROWS):
            if random.random() < density:
                walls.add((x, y))
    # Ensure start and goal are clear
    walls.discard(START)
    walls.discard(GOAL)
    return walls


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_agent(pos):
    x, y = pos
    if agent_image:
        screen.blit(agent_image, (x * CELL_SIZE, y * CELL_SIZE))
    else:
        # Fallback to circle if image not loaded
        center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, GREEN, center, CELL_SIZE // 3)


def draw_timer(start_time, finished):
    elapsed = time.time() - start_time
    if finished:
        label = font.render(f"Finished in {elapsed:.2f}s", True, RED)
    else:
        label = font.render(f"Time: {elapsed:.2f}s", True, BLACK)
    screen.blit(label, (10, HEIGHT + 10))


def draw_steps(steps):
    label = font.render(f"Steps: {steps}", True, BLACK)
    screen.blit(label, (10, HEIGHT + 40))


def draw_maze_info(maze_num):
    label = small_font.render(f"Maze: {MAZE_NAMES[maze_num]} (Press 1/2/3 to switch)", True, BLACK)
    screen.blit(label, (10, HEIGHT + 70))


def get_neighbors(pos, walls):
    x, y = pos
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    valid = [
        (x + dx, y + dy)
        for dx, dy in moves
        if 0 <= x + dx < COLS and 0 <= y + dy < ROWS and (x + dx, y + dy) not in walls
    ]
    return valid


def random_move(pos, walls):
    neighbors = get_neighbors(pos, walls)
    if neighbors:
        return random.choice(neighbors)
    return pos


def main():
    running = True
    finished = False
    agent_pos = START
    visited = set()
    current_maze = 0  # Start with first maze (Easy)
    walls = generate_walls(MAZE_SEEDS[current_maze], MAZE_DENSITIES[current_maze])
    start_time = time.time()
    steps = 0

    while running:
        clock.tick(10)  # frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Switch mazes with number keys
                if event.key == pygame.K_1:
                    current_maze = 0
                    agent_pos = START
                    visited = set()
                    walls = generate_walls(MAZE_SEEDS[current_maze], MAZE_DENSITIES[current_maze])
                    start_time = time.time()
                    steps = 0
                    finished = False
                elif event.key == pygame.K_2:
                    current_maze = 1
                    agent_pos = START
                    visited = set()
                    walls = generate_walls(MAZE_SEEDS[current_maze], MAZE_DENSITIES[current_maze])
                    start_time = time.time()
                    steps = 0
                    finished = False
                elif event.key == pygame.K_3:
                    current_maze = 2
                    agent_pos = START
                    visited = set()
                    walls = generate_walls(MAZE_SEEDS[current_maze], MAZE_DENSITIES[current_maze])
                    start_time = time.time()
                    steps = 0
                    finished = False

        if not finished:
            next_pos = random_move(agent_pos, walls)
            visited.add(agent_pos)
            if next_pos != agent_pos:  # Only count as a step if agent moved
                steps += 1
            agent_pos = next_pos

            if agent_pos == GOAL:
                finished = True

        # --- Draw ---
        screen.fill(WHITE)
        draw_grid()

        # Draw visited cells
        for pos in visited:
            draw_cell(pos, BLUE)

        # Draw walls
        for w in walls:
            draw_cell(w, BLACK)

        # Draw start and goal
        draw_cell(START, YELLOW)
        draw_cell(GOAL, RED)

        # Draw agent
        draw_agent(agent_pos)

        # Draw timer and steps
        draw_timer(start_time, finished)
        draw_steps(steps)
        draw_maze_info(current_maze)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
