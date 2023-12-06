import pygame
import numpy as np
import math
from holomorphic_dynamics import NewtonsMethod
from holomorphic_dynamics import HolomorphicDynamics

def start():

    pygame.init()

    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 400

    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def tick(screen):
    
    mode = 0
    SCREEN_HEIGHT, SCREEN_WIDTH = screen.get_size()
    screen_center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    roots = []
    moving = False

    screen.fill((0, 0, 0))
    # greate black numpy array to be used as the screen background
    background = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3))

    while True:

        pygame.surfarray.blit_array(screen, background)
        show_roots(roots, screen)

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            break
        elif key[pygame.K_q]:
            mode = 0
        elif key[pygame.K_a]:
            mode = 1
        elif key[pygame.K_SPACE]:
            complex_roots = []
            for root in roots:
                row, column = root.center
                x = column/SCREEN_WIDTH * 2 - 1
                y = row/SCREEN_HEIGHT * 2 - 1
                complex_roots.append(complex(x, y))
            hd = HolomorphicDynamics(NewtonsMethod(complex_roots), (SCREEN_HEIGHT, SCREEN_WIDTH))
            background = hd.color_points((-1, -1, 2, 2))
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if mode == 0:
                    roots.append(pygame.Rect((*pos, 10, 10)))
                elif  mode == 1:
                    moving = True
                    moving_root = get_moving_root(roots, pos)
            elif event.type == pygame.MOUSEMOTION and moving:
                moving_root.move_ip(event.rel)
                
                

        pygame.display.update()

    pygame.quit()

def show_roots(roots, screen):
    for root in roots:
        pygame.draw.rect(screen, (255, 255, 255), root)

def get_moving_root(roots: list[pygame.Rect], pos):
    for root in roots:
        if math.dist(root.center, pos) <= 20:
            return root
    

if __name__ == '__main__':

    screen = start()

    tick(screen)

        