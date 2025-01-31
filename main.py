import pygame
import math
import keyboard
from constants import *
from planet_classes import *
from background import *

pygame.init() #start the pygame
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create game screen
pygame.display.set_caption("Solar System Sim") # name title

def main():

    background_handler = ScaledBackground(BG, max_zoom_level=20)

    running = True
    clock = pygame.time.Clock()

    desc_checkbox = CHECKBOX(checkboxX,checkbox_size,"Toggle Planet Descriptions")
    sliderList_checkbox = CHECKBOX(checkboxX,checkbox_size,"Toggle sliders")

    allTogglable = [desc_checkbox, sliderList_checkbox]
   
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

    # Create Sun and Planets
    sun = SUN(WIDTH // 2, HEIGHT // 2, SUN_MASS, sun_pic)
    Mercury = PLANET(WIDTH // 2 - mercury_distance, HEIGHT // 2, 0, mercury_velocity/VELOCITY_SCALE, MERCURY_MASS, "Mercury", mercury_pic, 0, 0)
    Venus = PLANET(WIDTH // 2 - venus_distance, HEIGHT // 2, 0, venus_velocity/VELOCITY_SCALE, VENUS_MASS, "Venus", venus_pic, 0, 0)
    Earth = PLANET(WIDTH // 2 - earth_distance, HEIGHT // 2, 0, earth_velocity/VELOCITY_SCALE, EARTH_MASS, "Earth", earth_pic, 0, 0)
    Mars = PLANET(WIDTH // 2 - mars_distance, HEIGHT // 2, 0, mars_velocity/VELOCITY_SCALE, MARS_MASS, "Mars", mars_pic, 0, 0)
    Jupiter = PLANET(WIDTH // 2 - jupiter_distance, HEIGHT // 2, 0, jupiter_velocity/VELOCITY_SCALE, JUPITER_MASS, "Jupiter", jupiter_pic, 0, 0)
    Saturn = PLANET(WIDTH // 2 - saturn_distance, HEIGHT // 2, 0, saturn_velocity/VELOCITY_SCALE, SATURN_MASS, "Saturn", saturn_pic, 0 ,0 )
    Uranus = PLANET(WIDTH // 2 - uranus_distance, HEIGHT // 2, 0, uranus_velocity/VELOCITY_SCALE, URANUS_MASS, "Uranus", urnaus_pic, 0 ,0 )
    Neptune = PLANET(WIDTH // 2 - neptune_distance, HEIGHT // 2, 0, neptune_velocity/VELOCITY_SCALE, NEPTUNE_MASS, "Neptune", neptune_pic, 0, 0)


    # Add all planets to array
    objects = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

    selected_planet = None # Current planet selected
    planetClicked = False # Is the planet cilcked?
    camera_follow = False # Flag to indicate if the camera is following a planet

    # Moving screen?
    moveScreen = False

    # The zoom
    zoom_level = 10.0

    # IN PROCESS
    fps_multiplier = 1

    # slider (pos, name, multiplier)
    sunMass = SLIDER(sliderWidth / 10, "SUN MASS", int(sun.mass), 1000)
    zoom = SLIDER( sliderWidth, "ZOOM IN/OUT", int(zoom_level), 10)
    speedUp = SLIDER(sliderWidth/5, "SPEED UP/ SLOW DOWN", int(fps_multiplier), 1000)

    allSliders = [sunMass, zoom, speedUp] # slider array


    # Since all planets will be located at top left of screen, adjust their offset according to the WIDTH, HEIGHT, and screen
    offset_x = (WIDTH - SCREEN_WIDTH) //2
    offset_y = (HEIGHT - SCREEN_HEIGHT) //2

    move_camera_x = offset_x/10* (int(zoom_level))
    move_camera_y = offset_y/10* (int(zoom_level))

    updateVal = 0

    mouseImg = pygame.transform.scale(pygame.image.load("mouse.png"), (25, 25)) # Scale the image based on zoom
    pygame.mouse.set_visible(False)


    # Run program
    while running:
        clock.tick(FPS) # Run based on FPS
        updateVal+=1
        if updateVal > 1:
            updateVal = 0

            mouse_pos = pygame.mouse.get_pos()  # get the mouse position

            scaled_bg = background_handler.get_scaled_image(zoom_level)
            bg_x = -move_camera_x * 0.5
            bg_y = -move_camera_y * 0.5

            # move_camera_x = (offset_x/10)* (int(zoom_level))
            # move_camera_y = (offset_y/10) * (int(zoom_level))
            print((move_camera_x,move_camera_y))

            win.blit(scaled_bg, (bg_x, bg_y))

            # move_camera_x = SCREEN_WIDTH + (SCREEN_WIDTH/10)*zoom_level
            # move_camera_y = SCREEN_HEIGHT + (SCREEN_HEIGHT/10)*zoom_level

            # print((move_camera_x, move_camera_y))

            if keyboard.is_pressed('s'):
                dx = 0
                dy = 10
            elif keyboard.is_pressed('w'):
                dx = 0
                dy = -10
            elif keyboard.is_pressed('a'):
                dx = -10
                dy = 0
            elif keyboard.is_pressed('d'):
                dx = 10
                dy = 0
            else:
                dx = 0
                dy = 0
            
            move_camera_x += dx 
            move_camera_y += dy 


            if not camera_follow:
                move_camera_x = max(SCREEN_WIDTH, min(move_camera_x, WIDTH - SCREEN_WIDTH))
                move_camera_y = max(SCREEN_HEIGHT, min(move_camera_y, HEIGHT - SCREEN_HEIGHT))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    moveScreen = False
                    last_mouse_pos = None

                if event.type == pygame.MOUSEMOTION:
                    for obj in objects:
                        obj.handle_hover(mouse_pos, move_camera_x, move_camera_y)

                    if not sliderList_checkbox.checked:
                        for sliders in allSliders:
                            sliders.handle_hover(mouse_pos)
                            if sliders.toggleSlider:
                                sliders.pos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                                deltaSlider = max(0, (sliders.pos / sliderWidth) * sliders.deltaAmnt)
                                sliders.changingVal = int(deltaSlider)
                                match sliders.name:
                                    case "SUN MASS":
                                        sun.mass = deltaSlider
                                    case "ZOOM IN/OUT":
                                        zoom_level = deltaSlider
                                    case "SPEED UP/ SLOW DOWN":
                                        fps_multiplier = deltaSlider


                    # if sunSlider:
                    #     sunMass.pos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                    #     sun.mass = (sunMass.pos / sliderWidth) * 1000  
                    #     sunMass.changingVal = int(sun.mass)
                    # if zoomSlider:
                    #     zoom.pos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                    #     zoom_level = (zoom.pos / sliderWidth) * 10
                    #     zoom.changingVal = int(zoom_level)
                    # if speedUpSlider:
                    #     speedUp.pos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                    #     fps_multiplier = (speedUp.pos / sliderWidth) * 1000
                    #     speedUp.changingVal = int(fps_multiplier)
                        # adjusted_fps = int(FPS * fps_multiplier)  # Adjust FPS based on multiplier
                        # clock.tick(adjusted_fps)
                        # sun.mass = SUN_MASS * speed_multiplier


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        desc_checkbox.handle_click(mouse_pos)
                        sliderList_checkbox.handle_click(mouse_pos)
                        if not sliderList_checkbox.checked:
                            for sliders in allSliders:
                                sliders.handle_click(mouse_pos)

                    if 0 <= mouse_pos[0] <= SCREEN_WIDTH and 0 <= mouse_pos[0] <= SCREEN_HEIGHT:
                        moveScreen = True
                        last_mouse_pos = mouse_pos

                    
                    if not selected_planet:
                        for obj in objects:
                            if math.sqrt((mouse_pos[0] + move_camera_x - obj.adjusted_x)**2 + ((mouse_pos[1] + move_camera_y) - obj.adjusted_y)**2) <= PLANET_RADIUS*(2*zoom_level):
                                selected_planet = obj
                                planetClicked = True
                                camera_follow = True
                                break
                    elif selected_planet and desc_checkbox.checked:
                        selected_planet = movePlanet((selected_planet.x, selected_planet.y), (mouse_pos[0] + offset_x, mouse_pos[1] + offset_y), selected_planet)
                        selected_planet = None
                    elif selected_planet and math.sqrt((mouse_pos[0] + move_camera_x - selected_planet.adjusted_x)**2 + ((mouse_pos[1] + move_camera_y) - selected_planet.adjusted_y)**2) <= PLANET_RADIUS*(2*zoom_level) and camera_follow:
                        camera_follow = False
                        selected_planet = None

            if camera_follow and selected_planet and not desc_checkbox.checked:
                move_camera_x = selected_planet.x - SCREEN_WIDTH//2 - selected_planet.rad
                move_camera_y = selected_planet.y - SCREEN_HEIGHT//2 - selected_planet.rad

            if selected_planet and desc_checkbox.checked:
                pygame.draw.line(win, WHITE, (selected_planet.adjusted_x - move_camera_x, selected_planet.adjusted_y - move_camera_y), mouse_pos, 2)


            for obj in objects:
                obj.draw(zoom_level, move_camera_x, move_camera_y, scaled_bg.get_width(), scaled_bg.get_height())
                obj.move(sun)

                off_screen = False # obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
                collided_sun = math.sqrt((obj.x - sun.x)**2 + (obj.y - sun.y)**2) <= SUN_RADIUS*zoom_level
                
                if off_screen or collided_sun:
                    objects.remove(obj)

            sun.draw(zoom_level, move_camera_x, move_camera_y, scaled_bg.get_width(), scaled_bg.get_height())

            draw_UI_Checkboxes(allTogglable)

            if not sliderList_checkbox.checked:
                draw_UI_Sliders(allSliders)

            win.blit(mouseImg, (mouse_pos[0], mouse_pos[1]))

            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":

    main()