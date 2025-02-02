import pygame
import math
import keyboard
from constants import *
from planet_classes import *
from background import *

pygame.init() #start the pygame
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create game screen
pygame.display.set_caption("Solar System Sim") # name title

def change_hue(surface, hue_shift):
    """Changes the hue of a surface by the given amount."""
    pixel_array = pygame.PixelArray(surface)
    
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            color_int = pixel_array[x, y]  # Get the integer value of the pixel

            # Extract RGBA components from the color_int value
            r = (color_int >> 16) & 0xFF
            g = (color_int >> 8) & 0xFF
            b = color_int & 0xFF
            a = (color_int >> 24) & 0xFF  # Extract alpha channel if it exists

            # Create a pygame.Color object
            color = pygame.Color(r, g, b, a)

            # Get the HSLA values
            h, s, l, a = color.hsla

            # Apply the hue shift and wrap it around 360
            color.hsla = ((h + hue_shift) % 360, s, l, a)

            # Set the new color back to the pixel
            pixel_array[x, y] = color

    pixel_array.close()


def main():

    background_handler = ScaledBackground(BG, max_zoom_level=20)

    running = True
    clock = pygame.time.Clock()

    desc_checkbox = CHECKBOX(checkboxX,checkbox_size,"Toggle Planet Descriptions")
    sliderList_checkbox = CHECKBOX(checkboxX,checkbox_size,"Toggle sliders")

    allTogglable = [desc_checkbox, sliderList_checkbox]  

    # Create Sun and Planets
    sun = SUN(WIDTH // 2, HEIGHT // 2, SUN_MASS, sun_pic)
    Mercury = PLANET(mercury_distance, HEIGHT // 2, 0, mercury_velocity, MERCURY_MASS, "mercury")
    Venus = PLANET(venus_distance, HEIGHT // 2, 0, venus_velocity, VENUS_MASS, "venus")
    Earth = PLANET(earth_distance, HEIGHT // 2, 0, earth_velocity, EARTH_MASS, "earth")
    Mars = PLANET(mars_distance, HEIGHT // 2, 0, mars_velocity, MARS_MASS, "mars")
    Jupiter = PLANET(jupiter_distance, HEIGHT // 2, 0, jupiter_velocity, JUPITER_MASS, "jupiter")
    Saturn = PLANET(saturn_distance, HEIGHT // 2, 0, saturn_velocity, SATURN_MASS, "saturn")
    Uranus = PLANET(uranus_distance, HEIGHT // 2, 0, uranus_velocity, URANUS_MASS, "uranus")
    Neptune = PLANET(neptune_distance, HEIGHT // 2, 0, neptune_velocity, NEPTUNE_MASS, "neptune")


    # Add all planets to array
    objects = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

    selected_planet = None # Current planet selected
    camera_follow = False # Flag to indicate if the camera is following a planet

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

    move_camera_x = offset_x # /10* (int(zoom_level))
    move_camera_y = offset_y # /10* (int(zoom_level))

    updateVal = 0

    mouseImg = pygame.transform.scale(pygame.image.load("mouse.png"), (50, 50)) # Scale the image based on zoom
    pygame.mouse.set_visible(False)

    tempMoveX = 0
    tempMoveY = 0

    hue_shift = 0
    # Run program
    while running:
        clock.tick(FPS) # Run based on FPS
        updateVal+=1
        if updateVal > 1:
            updateVal = 0

            mouse_pos = pygame.mouse.get_pos()  # get the mouse position

            scaled_bg = background_handler.get_scaled_image(zoom_level)

            bgScalingX = (offset_x*(zoom_level/10) - (offset_x/10) + (tempMoveX/2))
            bgScalingY = (offset_y*(zoom_level/10) - (offset_y/10) + (tempMoveY/2))
            bgScalingX = max(0, min(scaled_bg.get_width() - SCREEN_WIDTH, bgScalingX))
            bgScalingY = max(0, min(scaled_bg.get_height() - SCREEN_HEIGHT, bgScalingY))

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

            if keyboard.is_pressed('h'):
                hue_shift = (hue_shift + 10) % 360  # Shift the hue by 10 degrees, wrap around at 360 degrees
                # Apply the new hue shift to mouseImg
                change_hue(mouseImg, hue_shift)
            
            move_camera_x += dx 
            move_camera_y += dy 
            tempMoveX += dx
            tempMoveY += dy


            if not camera_follow:
                move_camera_x = max(0, min(move_camera_x, WIDTH - SCREEN_WIDTH))
                move_camera_y = max(0, min(move_camera_y, HEIGHT - SCREEN_HEIGHT))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


                if event.type == pygame.MOUSEMOTION:
                    for obj in objects:
                        obj.handle_hover(mouse_pos, move_camera_x, move_camera_y)

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


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        desc_checkbox.handle_click(mouse_pos)
                        sliderList_checkbox.handle_click(mouse_pos)
                        if not sliderList_checkbox.checked:
                            for sliders in allSliders:
                                sliders.handle_click(mouse_pos)

                    
                    if not selected_planet:
                        for obj in objects:
                            if math.sqrt((mouse_pos[0] + move_camera_x - obj.cameraX)**2 + ((mouse_pos[1] + move_camera_y) - obj.cameraY)**2) <= PLANET_RADIUS*(2*zoom_level):
                                selected_planet = obj
                                camera_follow = True
                                break
                    elif selected_planet and desc_checkbox.checked:
                        selected_planet = movePlanet((selected_planet.x, selected_planet.y), (mouse_pos[0] + offset_x, mouse_pos[1] + offset_y), selected_planet)
                        selected_planet = None
                    elif selected_planet and math.sqrt((mouse_pos[0] + move_camera_x - selected_planet.cameraX)**2 + ((mouse_pos[1] + move_camera_y) - selected_planet.cameraY)**2) <= PLANET_RADIUS*(2*zoom_level) and camera_follow:
                        camera_follow = False
                        selected_planet = None

            if camera_follow and selected_planet and not desc_checkbox.checked:
                move_camera_x = selected_planet.x - SCREEN_WIDTH//2 - selected_planet.rad
                move_camera_y = selected_planet.y - SCREEN_HEIGHT//2 - selected_planet.rad






            win.blit(scaled_bg, (-bgScalingX , -bgScalingY ))

            if selected_planet and desc_checkbox.checked:
                pygame.draw.line(win, WHITE, (selected_planet.cameraX - move_camera_x, selected_planet.cameraY - move_camera_y), mouse_pos, 2)


            for obj in objects:
                obj.draw(zoom_level, move_camera_x, move_camera_y)
                obj.move(sun)

                off_screen = False # obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
                collided_sun = math.sqrt((obj.x - sun.x)**2 + (obj.y - sun.y)**2) <= SUN_RADIUS*(zoom_level/10)
                
                if off_screen or collided_sun:
                    objects.remove(obj)

            sun.draw(zoom_level, move_camera_x, move_camera_y)

            draw_UI_Checkboxes(allTogglable)

            if not sliderList_checkbox.checked:
                draw_UI_Sliders(allSliders)
            win.blit(mouseImg, (mouse_pos[0]-(mouseImg.get_width()/2), mouse_pos[1]-(mouseImg.get_height()/2)))

            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":

    main()