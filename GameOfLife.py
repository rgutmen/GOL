import pygame
import numpy as np
import time

pygame.init()

# Board size
width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

# Background board color
bg = 25, 25, 25
screen.fill(bg)

# Num of cells
nxC, nyC = 50, 50
# Cell size
dimCW = width / nxC
dimCH = height / nyC

# Cells status; 1 = alive, 0 = dead
gameState = np.zeros((nxC, nyC))

# A sample figure
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

pauseExect = False

# Game start
while True:

    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)
    ev = pygame.event.get()
    for event in ev:
        # Un/pause the game pressing any key
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        mouseClick = pygame.mouse.get_pressed()
        # During the pause, with the click button make the cell alive, other button, died
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCH)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    # Calculate closer neighbors
    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExect:
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x)     % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, (y)     % nyC] + \
                          gameState[(x + 1) % nxC, (y)     % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[(x)     % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Rule 1: A death cell with 3 alive neighbors it will became alive
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                # Rule 2: An alive cell with less than 2 or more than 3 alive cells, it will became dead
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            poly = [(int(x       * dimCW), int(y       * dimCH)),
                    (int((x + 1) * dimCW), int(y       * dimCH)),
                    (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                    (int(x       * dimCW), int((y + 1) * dimCH))]

            # Draw the cell
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 50, 0), poly, 0)

    # gameState updated
    gameState = np.copy(newGameState)
    # Screen updated
    pygame.display.flip()