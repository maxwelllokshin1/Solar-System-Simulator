import pygame
import math
import random
from constants import * # import all constants from constants.py
from main import *

# Initialize the sliders properties
sliderWidth = 300
sliderHeight = 5
sliderX = (SCREEN_WIDTH) - sliderWidth - 25
sliderRad = 10

class SUN:
    # Instantiate all attributes x, y, mass, img
    def __init__(self, x, y, mass, massScale, name):
        #self.info = info
        # cur_info = get_info(name)
        self.x = x
        self.y = y
        # print(f"sideralOrbit {self.info['sideralOrbit']}")
        # print(f"{name}: dist: {cur_info['semimajorAxis']}")
        self.mass = 1.99e30
        name+=".png"
        self.img = pygame.image.load(name)
        self.rad = SUN_RADIUS
        self.adjusted_x = 0
        self.adjusted_y = 0

        # self.scaled_images = {}

    
    # Draw the sun with attributes zoom_level, offset_x, offset_y
    def draw(self, zoom_level, offset_x, offset_y):
        # self.adjusted_x = (self.x - bgWidth//2) * (zoom_level/10) + bgWidth // 2 
        # self.adjusted_y = (self.y - bgHeight//2) * (zoom_level/10) + bgHeight // 2
        # if zoom_level not in self.scaled_images:
        self.rad = SUN_RADIUS * zoom_level   # How big the sun will be based on the zoom level
        img = pygame.transform.scale(self.img, (self.rad * 2, self.rad * 2)) # Scale the image based on zoom
            # win.blit(img, (self.adjusted_x - self.rad- offset_x, self.adjusted_y - self.rad - offset_y)) # Draw the image at center of screen
        win.blit(img, (self.x - self.rad- offset_x, self.y - self.rad - offset_y)) # Draw the image at center of screen

        #     self.scaled_images[zoom_level] = img # add the scaled image zoom_level to the array
        # return self.scaled_images[zoom_level]


# Create PLANET class
class PLANET:
    # Define all attributes x, y, vel_x, vel_y, mass, name, img
    def __init__(self, name):

        print(f"{name}: ")

        #self.info = info
        cur_info = get_info(name)
        daysInYear = cur_info['sideralOrbit']
        randDay = random.randint(0, int(daysInYear))

        print("(randDay, daysInYear)", (randDay, daysInYear))
        angle = (randDay / daysInYear) * 360
        if(angle > 180):
            angle -= 360

        print("angle", angle)
        
        displacement = cur_info['semimajorAxis']
        if(abs(angle) <= 60):
            displacement = (cur_info['perihelion']+displacement)/2
            if(abs(angle) <= 30):
                displacement = cur_info['perihelion']
        elif(abs(angle) >= 120):
            displacement = (cur_info['aphelion']+displacement)/2
            if(abs(angle) >= 150):
                displacement = cur_info['aphelion']

        displacement /= SCALE

        print(f"displacement {displacement}")

        self.x =  WIDTH//2 + ((displacement)*math.cos(math.radians(angle)))
        self.y =  HEIGHT//2 - ((displacement)*math.sin(math.radians(angle)))

        velocity = (2*math.pi * displacement) / daysInYear

        velocity /= 10
        print(f"velocity {velocity}")

        self.vel_x = ((velocity)*math.cos(math.radians(angle)))
        self.vel_y = ((velocity)*math.sin(math.radians(angle)))

        temp = -self.vel_x
        self.vel_x = self.vel_y
        self.vel_y = temp

        print("(self.vel_x, self.vel_y)", (self.vel_x, self.vel_y))


        # self.vel_x = vel_x/VELOCITY_SCALE
        # self.vel_y = vel_y/VELOCITY_SCALE
        unitCircle = 2 * math.pi
        radius = displacement ** (3/2)
        productFirst = unitCircle * radius
        productSecond = productFirst / daysInYear
        self.mass = (productSecond**2)/(GRAVCONST)

        print(f"mass {self.mass}")
        self.name = name
        name+=".png"
        self.img = pygame.image.load(name)
        self.cameraX = (self.x - WIDTH//2) + WIDTH // 2
        self.cameraY = (self.y - HEIGHT//2) + HEIGHT // 2
        self.hoverPlanet = False
        self.rad = PLANET_RADIUS
        
    
    # Move this object
    def move(self, obj=None):

        # move based on how much gravity will pull the planets using suns mass
        displacement = math.sqrt((self.x - obj.x)**2 + (self.y - obj.y) ** 2) # Calculates distance from the sun
        force = (GRAVCONST * obj.mass) / ((displacement*SCALE) ** 2) # Force Equation from PHYSICS
        
        acceleration = force/SCALE  # Calculate acceleration using force / mass
        angle = math.atan2(obj.y - self.y, obj.x - self.x) # now find the angle using opp/adj

        acceleration_x = acceleration * math.cos(angle) # find the component for x using Ax forumla
        acceleration_y = acceleration * math.sin(angle) # find component for y using Ay formula

        # change the velocities based on acceleration
        self.vel_x += acceleration_x  
        self.vel_y += acceleration_y

        timeVelX = self.vel_x / 1
        timeVelY = self.vel_y / 1

        # change positions based off velocities
        self.x += timeVelX
        self.y += timeVelY
    

    # Draw the planet 
    def draw(self, zoom_level, offset_x, offset_y):
        # change the position based on the zoomdawas

        # change the radius based on zoom
        self.rad = PLANET_RADIUS * zoom_level 

        # all text stuff
        if self.hoverPlanet:
            fontSize = math.floor(16 * zoom_level) # font size based on zoom level
            font = pygame.font.SysFont("Comic-Sans", fontSize) # font style
            text = font.render(self.name, True, WHITE)  # how the text should look
            win.blit(text, text.get_rect(center=(self.cameraX - offset_x,self.cameraY - self.rad - 10 - offset_y)))  # pasting the text on the planets

        # create the planet image based on radius
        img = pygame.transform.scale(self.img, (self.rad*2, self.rad*2)) 
        win.blit(img, (self.cameraX - self.rad - offset_x, self.cameraY - self.rad - offset_y)) # draw planet image
        if self.hoverPlanet:
            pygame.draw.circle(win, (255,255,255), (self.cameraX - offset_x, self.cameraY - offset_y), self.rad, 5)

        pygame.draw.line(win, WHITE, (self.cameraX - offset_x, self.cameraY - offset_y), (self.cameraX - offset_x + (self.vel_x*10), self.cameraY - offset_y), 2) 
        pygame.draw.line(win, WHITE, (self.cameraX - offset_x, self.cameraY - offset_y), (self.cameraX - offset_x, self.cameraY - offset_y - (self.vel_y*10)), 2) 
        # pygame.draw.line(win, WHITE, (self.cameraX - offset_x, self.cameraY - offset_y), (self.cameraX - offset_x, self.cameraY - offset_y - (self.vel_y*10)), 2)        
    
    def handle_hover(self, mouse_pos, offset_x, offset_y):
        if math.sqrt((mouse_pos[0] + offset_x - self.cameraX)**2 + ((mouse_pos[1] + offset_y) - self.cameraY)**2) <= self.rad:
            self.hoverPlanet = True
        else:
            self.hoverPlanet = False


class SLIDER:
    def __init__(self, pos, name, changingVal, deltaAmnt):
        self.pos = pos
        self.name = name
        self.changingVal = changingVal
        self.deltaAmnt = deltaAmnt
        self.toggleSlider = False
        self.toggleHover = False
        self.y = 0

    def draw_slider(self, y):
        self.y = y
        pygame.draw.rect(win, WHITE, (sliderX, y, sliderWidth, sliderHeight))
        if self.toggleHover:
            pygame.draw.circle(win, (150,0,0), (sliderX + self.pos, self.y + sliderHeight // 2), sliderRad)
        else:
            pygame.draw.circle(win, (150,150,150), (sliderX + self.pos, self.y + sliderHeight // 2), sliderRad)
        
        font = pygame.font.SysFont("Comic-Sans", 20)
        text = font.render(f"{self.name}: {self.changingVal}", True, WHITE)
        win.blit(text, (sliderX , self.y-35))
    
    def handle_hover(self, mouse_pos):
        if math.sqrt((mouse_pos[0] - (sliderX + self.pos))**2 + (mouse_pos[1] - self.y)**2) <= sliderRad*3:
            self.toggleHover = True
        elif self.toggleSlider == False:
            self.toggleHover = False
    def handle_click(self, mouse_pos):
        checkClickedSlider = math.sqrt((mouse_pos[0] - (sliderX + self.pos))**2 + (mouse_pos[1] - self.y)**2) <= sliderRad*3
        if checkClickedSlider and self.toggleSlider:
            self.toggleSlider = False
        elif checkClickedSlider:
            self.toggleSlider = True
        else:
            self.toggleSlider = False

class CHECKBOX:
    def __init__(self, x, size, label):
        self.x = x
        self.y = 50
        self.size = size
        self.label = label
        self.checked = False  # The initial state is unchecked

    def draw_checkbox(self, y):
        self.y = y
        # Draw the checkbox
        pygame.draw.rect(win, WHITE, (self.x, self.y, self.size, self.size), 5)
        if self.checked:
            pygame.draw.line(win, WHITE, (self.x+5, self.y+5), (self.x + self.size - 5, self.y + self.size- 5), 7)
            # pygame.draw.line(win, WHITE, (self.x, self.y + self.size), (self.x + self.size, self.y), 2)

        # Draw the label next to the checkbox
        font = pygame.font.SysFont("Comic-Sans", 20)
        text = font.render(self.label, True, WHITE)
        win.blit(text, (self.x + self.size + 10, self.y))

    def handle_click(self, mouse_pos):
        # Check if the mouse clicked inside the checkbox area
        if self.x <= mouse_pos[0] <= self.x + self.size and self.y <= mouse_pos[1] <= self.y + self.size:
            self.checked = not self.checked  # Toggle the state of the checkbox

def movePlanet(Location, mouse, obj):
    t_x, t_y = Location # Second location when clicked  
    m_x, m_y = mouse # Initial clicked point

    vel_x = ((m_x - t_x)*2) / VELOCITY_SCALE
    vel_y = ((m_y - t_y)*2) / VELOCITY_SCALE
    
    obj.vel_x += vel_x
    obj.vel_y += vel_y

    return obj

def draw_UI_Sliders(allSliders):
    y = 50
    deltaY = 75
    tempY = y
    for s in allSliders:
        tempY += deltaY

    pygame.draw.rect(win, (50,50,50), (sliderX - ( y/5), y/5, sliderWidth * (sliderWidth/275), tempY - y))

    for s in allSliders:
        s.draw_slider(y)
        y += deltaY

checkbox_size = 35
checkboxX = 50

def draw_UI_Checkboxes(toggleList):
    y = 50
    deltaY = checkbox_size + 10

    for t in toggleList:
        t.draw_checkbox(y)
        y += deltaY