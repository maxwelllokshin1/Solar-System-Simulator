import pygame

pygame.init() #start the pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 900 # window to be playing on
WIDTH, HEIGHT = 1400*10, 900*10 # actual size of simulation

# Set mass of all planets
MERCURY_MASS = 10 
VENUS_MASS = 12
EARTH_MASS = 15
MARS_MASS = 18
JUPITER_MASS = 40
SATURN_MASS = 45
URANUS_MASS = 30
NEPTUNE_MASS = 30
SUN_MASS = 100

# Set radius
PLANET_RADIUS = 5
SUN_RADIUS = 10

# set FPS
FPS = 60

# set gravity
GRAVITY = 10

# set Velocity
VELOCITY_SCALE = 100

# all colors
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255, 0)
GREEN = (0,255,0)
ORANGE = (255,165, 0)
CYAN = (0, 255, 255)


# IMAGES FOR ALL PLANETS, SUN, AND BACKGROUND
BG = pygame.image.load("background.jpg")
sun_pic = pygame.image.load("sun.png")
mercury_pic = pygame.image.load("mercury.png")
venus_pic = pygame.image.load("venus.png")
earth_pic = pygame.image.load("earth.png")
mars_pic = pygame.image.load("mars.png")
jupiter_pic = pygame.image.load("jupiter.png")
saturn_pic = pygame.image.load("saturn.png")
urnaus_pic = pygame.image.load("uanus.png")
neptune_pic = pygame.image.load("neptune.png")