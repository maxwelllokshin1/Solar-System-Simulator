import pygame
import math
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

    # Moving screen?
    moveScreen = False

    # The zoom
    zoom_level = 10.0

    # Since all planets will be located at top left of screen, adjust their offset according to the WIDTH, HEIGHT, and screen
    offset_x = (WIDTH - SCREEN_WIDTH) //2
    offset_y = (HEIGHT - SCREEN_HEIGHT) //2

    # Last mouse position
    last_mouse_pos = None

    # IN PROCESS
    fps_multiplier = 1

    # slider (pos, name, multiplier)
    sunMass = SLIDER(sliderWidth / 10, "SUN MASS", int(sun.mass), 1000)
    zoom = SLIDER( sliderWidth, "ZOOM IN/OUT", int(zoom_level), 10)
    speedUp = SLIDER(sliderWidth/5, "SPEED UP/ SLOW DOWN", int(fps_multiplier), 1000)

    allSliders = [sunMass, zoom, speedUp] # slider array

     # Run program
    while running:
        clock.tick(FPS) # Run based on FPS

        mouse_pos = pygame.mouse.get_pos()  # get the mouse position

        # Current backgorund information
        scaled_bg = background_handler.get_scaled_image(zoom_level)
        width_bg = (scaled_bg.get_width() - SCREEN_WIDTH) //2
        height_bg = (scaled_bg.get_height() - SCREEN_HEIGHT) //2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                moveScreen = False
                last_mouse_pos = None

            if event.type == pygame.MOUSEMOTION:
                if desc_checkbox.checked:
                    for obj in objects:
                        obj.handle_hover(mouse_pos, offset_x, offset_y)

                if not sliderList_checkbox.checked:
                    for sliders in allSliders:
                        sliders.handle_hover(mouse_pos)
                        if sliders.toggleSlider:
                            sliders.pos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                            deltaSlider = max(1, (sliders.pos / sliderWidth) * sliders.deltaAmnt)
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
                if moveScreen and last_mouse_pos:
                    dx = (mouse_pos[0] - last_mouse_pos[0]) / 10
                    dy = (mouse_pos[1] - last_mouse_pos[1]) / 10
                    offset_x -= dx  
                    offset_y -= dy

                offset_x = max(SCREEN_WIDTH, min(offset_x, WIDTH - SCREEN_WIDTH))
                offset_y = max(SCREEN_HEIGHT, min(offset_y, HEIGHT - SCREEN_HEIGHT))


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

                if desc_checkbox.checked:
                    if not selected_planet:
                        for obj in objects:
                            if math.sqrt((mouse_pos[0] + offset_x - obj.adjusted_x)**2 + ((mouse_pos[1] + offset_y) - obj.adjusted_y)**2) <= PLANET_RADIUS*(2*zoom_level):
                                print("CLICKED ", obj.name, " ", ((mouse_pos[0] + offset_x) - obj.x))
                                selected_planet = obj
                                planetClicked = True
                                break
                                
                    elif selected_planet and planetClicked:
                        planetClicked = False

                    print("OFFSET: ", offset_x * (zoom_level/10), " ", offset_y * (zoom_level/10))
                    if selected_planet and not planetClicked:
                        selected_planet = movePlanet((selected_planet.x, selected_planet.y), (mouse_pos[0] + offset_x, mouse_pos[1] + offset_y), selected_planet)
                        selected_planet = None

        # Draw the scaled background (no need to scale every time)
        win.blit(background_handler.get_scaled_image(zoom_level), (0-width_bg, 0-height_bg))

        if selected_planet and planetClicked:
            pygame.draw.line(win, WHITE, (selected_planet.adjusted_x - offset_x, selected_planet.adjusted_y - offset_y), mouse_pos, 2)


        for obj in objects:
            obj.draw(zoom_level, offset_x, offset_y)
            obj.move(sun)

            # obj.x += obj.vel_x * speed_multiplier  # Apply speed multiplier to velocity
            # obj.y += obj.vel_y * speed_multiplier

            off_screen = False # obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided_sun = math.sqrt((obj.x - sun.x)**2 + (obj.y - sun.y)**2) <= SUN_RADIUS*zoom_level
            
            if off_screen or collided_sun:
                objects.remove(obj)

        sun.draw(zoom_level, offset_x, offset_y)

        draw_UI_Checkboxes(allTogglable)

        if not sliderList_checkbox.checked:
            draw_UI_Sliders(allSliders)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()