import math
import pygame
import pygame_gui

from opensimplex import OpenSimplex

# Screen constants
WIDTH = 800
HEIGHT = 600

# Initialise Screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.RESIZABLE)
pygame.display.set_caption("Circle Noise")

# Initialise noise function
noise = OpenSimplex()

# UI Manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
# UI Sliders
density_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((WIDTH - 210, HEIGHT - 45), (200, 20)), 8, (0.1, 24), manager)
intensity_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((WIDTH - 210, HEIGHT - 20), (200, 20)), 5, (0, 12), manager)
ui_text = pygame_gui.elements.UILabel(pygame.Rect((5, HEIGHT - 30), (310, 30)), "U - Hide/Show UI | S - Freeze Circle", manager)

# Variables
noiseSpeed = 1.55
drawUI = True
isStatic = False
fillShape = False
points = []
# Calculating framerate and delta
framerate = 60
delta = 1 / framerate

zoff = 0
running = True
while running:
    # Clear the screen and wait for the next frame
    screen.fill([0, 0, 0])
    pygame.time.delay(int(delta * 100))
    noiseScalar = intensity_slider.current_value
    noiseDensity = density_slider.current_value
    # Exit if program is closed and check if the key 'U' is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                drawUI = not drawUI
            if event.key == pygame.K_s:
                isStatic = not isStatic
        if event.type == pygame.VIDEORESIZE:
            WIDTH = event.dict['size'][0]
            HEIGHT = event.dict['size'][1]
            screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.RESIZABLE)
            density_slider.kill()
            intensity_slider.kill()
            ui_text.kill()
            density_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((WIDTH - 210, HEIGHT - 45), (200, 20)),8, (0.1, 24), manager)
            intensity_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((WIDTH - 210, HEIGHT - 20), (200, 20)), 5, (0, 12), manager)
            ui_text = pygame_gui.elements.UILabel(pygame.Rect((5, HEIGHT - 30), (310, 30)),"U - Hide/Show UI | S - Freeze Circle", manager)
        manager.process_events(event)

    theta = 0.0
    points.clear()
    while theta <= math.tau:
        xoff = (math.cos(theta) + 1) / 2 * noiseDensity
        yoff = (math.sin(theta) + 1) / 2 * noiseDensity
        r = min(HEIGHT, WIDTH) / 4 + noise.noise3d(xoff, yoff, zoff) * noiseScalar * 10
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        pos = (x + WIDTH / 2, y + HEIGHT / 2)
        points.append(pos)
        theta += 0.005
    pygame.draw.polygon(screen, (255,255,255), points, 1 * (not fillShape))
    zoff += noiseSpeed * delta * (not isStatic)

    # Update manager and screen
    if drawUI:
        manager.update(delta)
        manager.draw_ui(screen)
    pygame.display.update()