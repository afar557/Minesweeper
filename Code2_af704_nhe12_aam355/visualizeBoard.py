import pygame

def visualizeBoard (grid, label):
    dimension = len(grid)
    # Define colors for maze
    BLACK = (0, 0, 0)
    GRAY = (105, 105, 105)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    ORANGE = (255,127,80)
    
    # sets the WIDTH and HEIGHT of each grid spot
    WIDTH = 20
    HEIGHT = 20
    # sets the margin between each cell
    MARGIN = 3

    # Initialize pygame
    pygame.init()
    
    # Set size of screen
    WINDOW_SIZE = [(MARGIN * dimension+2) + (dimension*WIDTH), (MARGIN * dimension+2) + (dimension*WIDTH)]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    # Set title of screen
    pygame.display.set_caption(label)
    
    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # sets up maze
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
    
        # Set the screen background
        screen.fill(BLACK)

        font=pygame.font.SysFont('arial', 20)
        # Draw the grid
        for row in range(dimension):
            for column in range(dimension):
                if type(grid[row][column]) ==int: 
                    color = GREEN
                elif grid[row][column] == 'M':
                    color = RED
                elif grid[row][column] == 'm':
                    color = ORANGE
                elif grid[row][column] == '?':
                    color = WHITE

                # draw the maze
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
    
        # Limit to 60 frames per second
        clock.tick(60)

        # Adds number of neighbors that are mines into the board
        for x in range(dimension):
            for y in range(dimension):
                if type(grid[x][y]) == int: 
                    text=font.render(str(grid[x][y]), True, (0, 0, 0))        
                    rect=text.get_rect()
                    rect.x=(y*(WIDTH+MARGIN)) + MARGIN
                    rect.y=(x*(WIDTH+MARGIN)) + MARGIN
                    screen.blit(text, rect)
    
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
         
    # on exit.
    pygame.quit()
