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
FPS = 240

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


# All planets distances relative to the sun
mercury_distance = 57.91  
venus_distance = 108.2   
earth_distance = 149.6   
mars_distance = 227.9  
jupiter_distance = 778.3   
saturn_distance = 1429   
uranus_distance = 2871   
neptune_distance = 4495  

# All Planets Velocities
mercury_velocity = 478.7 
venus_velocity = 350.2   
earth_velocity = 297.8   
mars_velocity = 240.77   
jupiter_velocity = 130.7 
saturn_velocity = 150 # 969   
uranus_velocity = 130 # 681   
neptune_velocity = 110 # 543 