import pygame
import math
import requests

pygame.init() #start the pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 900 # window to be playing on
WIDTH, HEIGHT = 1400*100, 900*100 # actual size of simulation


base_url = "https://api.le-systeme-solaire.net/rest/bodies/"


def get_info(name):
    url = f"{base_url}{name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # print("reterieved successufly")
        return data
    else:
        print(f"Failed to retrieve data {response.status_code} {name}")

# Sun_info = get_info('Sun')

# Earth_info = get_info('Earth')
# # print(Earth_info)
# print(f"{Earth_info['semimajorAxis']} {Earth_info['mainAnomaly']} {Earth_info['sideralOrbit']}")


# Mars_info = get_info('Mars')

# Venus_info = get_info('Venus')

# Jupiter_info = get_info('Jupiter')

# Saturn_info = get_info('Saturn')

# Neptune_info = get_info('Neptune')

# Uranus_info = get_info('Uranus')

# Mercury_info = get_info('Mercury')

# print(get_info('bodies'))

# print(get_info('Earth'))
# print(get_info('Earth'))
# print(get_info('Earth'))
# print(get_info('Earth'))
# print(get_info('Earth'))
# print(get_info('Earth'))
# print(get_info('Earth'))
# print(get_info('Earth'))

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
VELOCITY_SCALE = 500
DISTANCE_SCALE = 100000
MASS_SCALE = 1000

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


# cur_info = get_info('Earth')
# print(cur_info['semimajorAxis'])
# cur_info = get_info('Mars')
# print(cur_info['semimajorAxis'])
# cur_info = get_info('Jupiter')
# print(cur_info['semimajorAxis'])
# cur_info = get_info('Saturn')
# print(cur_info['semimajorAxis'])



# All planets distances relative to the sun
mercury_distance = 57909050
venus_distance = 108208475
earth_distance = 149598023
mars_distance = 227939200
jupiter_distance = 778340821 
saturn_distance = 1426666422 
uranus_distance = 2870658186   
neptune_distance = 4498396441 

# All Planets Velocities
mercury_velocity = 4250 
venus_velocity = 10360 
earth_velocity = 11190
mars_velocity = 5030.0  
jupiter_velocity = 60200.0 
saturn_velocity = 36090.0
uranus_velocity = 21380.0
neptune_velocity = 23560.0

# mercury_angle = (Earth_info['mainAnomaly'] / Earth_info['sideralOrbit']) * 360
# venus_angle = (Earth_info['mainAnomaly'] / Earth_info['sideralOrbit']) * 360
# earth_angle = (Earth_info['mainAnomaly'] / Earth_info['sideralOrbit']) * 360
# mars_angle = (Earth_info['mainAnomaly'] / Earth_info['sideralOrbit']) * 360
# jupiter_angle = (Earth_info['mainAnomaly'] / Earth_info['sideralOrbit']) * 360
# Mercury_angle = (Earth_info['mainAnomaly'] / Earth_info['sideralOrbit']) * 360
# Mercury_angle = (Earth_info['mainAnomaly'] / Earth_info['sideralOrbit']) * 360
# Mercury_angle = (Earth_info['mainAnomaly'] / Earth_info['sideralOrbit']) * 360
# Mercury_angle = (Earth_info['mainAnomaly'] / Earth_info['sideralOrbit']) * 360

offset_x = (WIDTH - SCREEN_WIDTH) //2
offset_y = (HEIGHT - SCREEN_HEIGHT) //2

# # planet_name = "Sun"

# # cur_info = get_info(planet_name)

# # if cur_info:
# #     print(f"{cur_info['mass']}")



# # Set mass of all planets
# # MERCURY_MASS = get_info("Mercury") 
# # VENUS_MASS = get_info("Venus")
# # EARTH_MASS = get_info("Earth")
# # MARS_MASS = get_info("Mars")
# # JUPITER_MASS = get_info("Jupiter")
# # SATURN_MASS = get_info("Saturn")
# # URANUS_MASS = get_info("Uranus")
# # NEPTUNE_MASS = get_info("Sun")
# SUN_MASS = 100

# # Set radius
# PLANET_RADIUS = 5
# SUN_RADIUS = 10

# # set FPS
# FPS = 240

# # set gravity
# GRAVITY = 10

# # set Velocity
# VELOCITY_SCALE = 100

# # all colors
# WHITE = (255,255,255)
# RED = (255,0,0)
# BLUE = (0,0,255)
# YELLOW = (255,255, 0)
# GREEN = (0,255,0)
# ORANGE = (255,165, 0)
# CYAN = (0, 255, 255)


# # IMAGES FOR ALL PLANETS, SUN, AND BACKGROUND
# BG = pygame.image.load("background.jpg")
# sun_pic = pygame.image.load("sun.png")


# # All planets distances relative to the sun
# mercury_distance = 57.91  
# venus_distance = 108.2   
# earth_distance = 149.6   
# mars_distance = 227.9  
# jupiter_distance = 778.3   
# saturn_distance = 1429   
# uranus_distance = 2871   
# neptune_distance = 4495  

# # All Planets Velocities
# mercury_velocity = 478.7 
# venus_velocity = 350.2   
# earth_velocity = 297.8   
# mars_velocity = 240.77   
# jupiter_velocity = 130.7 
# saturn_velocity = 150 # 969   
# uranus_velocity = 130 # 681   
# neptune_velocity = 110 # 543 

# # Since all planets will be located at top left of screen, adjust their offset according to the WIDTH, HEIGHT, and screen
# offset_x = (WIDTH - SCREEN_WIDTH) //2
# offset_y = (HEIGHT - SCREEN_HEIGHT) //2
