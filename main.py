# General imports
import pygame, utils, os
from classes.GameState import GameState
from classes.Button import Button
import song_library
from classes.Widget import Widget
from classes.quicksprite import QuickSprite

game_state = None
current_song = 0
songButton = None

# the set_song used for the event
def set_song():
    global game_state
    global current_song
    global songButton
    current_song = (0, current_song + 1)[len(song_library.songs) - 1 > current_song]
    print(current_song)
    game_state.set_song(song_library.songs[current_song])
    songButton.set_text(song_library.songs[current_song].bg_game_header)

def main():
    global game_state
    global songButton
    # Initialize pygame
    pygame.init()
    # Set screen size. Don't change this unless you know what you are doing!
    screen = pygame.display.set_mode((1280, 720))
    # Set the window title
    pygame.display.set_caption("IAT Challengeweek: Interaction Hero")

    # Keeps track of all sprites to be updated every frame
    allsprites = pygame.sprite.Group()

    # Song to be used in game. Only one can be used.
    song = song_library.songs[0]

    # Create game_state instance, this holds all required game info
    game_state = GameState(allsprites, song)

    # Checks if the program is running on a Raspberry Pi
    is_running_on_rpi = utils.is_running_on_rpi()
    if is_running_on_rpi:
        # Below are some pin input numbers, feel free to change them. However,
        # !!! ALWAYS READ THE PIN DOCUMENTATION CAREFULLY !!!
        # Pay special attention to the difference between GPIO pin numbers and BOARD pin numbers
        # For example GPIO17 is addressed 17 rather than 11 (See pin numbering diagram.)
        # https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
        gpio_pin_numbers = [2, 3, 4, 17]  # Max 4 pins 
        gpio_buttons = init_rpi_buttons(gpio_pin_numbers)
        game_state.add_gpio_pins(gpio_pin_numbers)

    # Prepare game objects
    clock = pygame.time.Clock()
    startButton = Button(500, 300, 140, 50, 'Start', game_state.restart, song.get_font_filename(), allsprites, game_state, 'prestart')
    difficultyButton = Button(500, 350, 140, 50, 'Easy', game_state.toggle_difficulty, song.get_font_filename(), allsprites, game_state, 'prestart')
    quitButton = Button(500, 400, 140, 50, 'Quit', quit, song.get_font_filename(), allsprites, game_state, 'prestart')
    songButton = Button(500, 500, 300, 50, song_library.songs[0].bg_game_header, set_song, song.get_font_filename(), allsprites, game_state, 'prestart')
    game_state.diff_button = difficultyButton

    startButton.setBg((255,0,0))
    startButton.setLbg((255, 51, 0))
    difficultyButton.setBg((255,0,0))
    difficultyButton.setLbg((255, 51, 0))
    songButton.setBg((0, 133, 2))
    songButton.setLbg((0, 199, 3))

    restartButton = Button(500, 300, 140, 50, 'Restart', game_state.restart, song.get_font_filename(), allsprites, game_state, 'postgame')
    backToMenuButton = Button(500, 350, 140, 50, 'Menu', game_state.back_to_menu, song.get_font_filename(), allsprites, game_state, 'postgame')
    restartButton.setBg((255,0,0))
    restartButton.setLbg((255, 51, 0))
    backToMenuButton.setBg((255, 153, 0))
    backToMenuButton.setLbg((204, 102, 0))

    score_widget = Widget(100, 400, 200, 50, ' Score', song.get_font_filename(), allsprites, game_state, 'playing')
    high_score_widget = Widget(100, 450, 300, 50, ' high score', song.get_font_filename(), allsprites, game_state, 'postgame')
    score_widget_pg = Widget(100, 400, 300, 50, ' Score:', song.get_font_filename(), allsprites, game_state, 'postgame')

    logo = QuickSprite(430, 100, 412, 164, game_state, "iatvision.PNG", allsprites, "prestart")

    # Main loop
    going = True
    while going:

        # Update the clock, argument is max fps
        clock.tick(60)

        # Every 'tick' or programcycle the gamestate update() is called
        game_state.update()

        # Get all events from the last cycle and store them as variable
        # This is stored as a variable because pygame.even.get() empties this list
        eventlist = pygame.event.get()

        # Check if there are any global quit events
        for event in eventlist:
            # If yes, the game loop won't start again
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.unicode == pygame.K_ESCAPE:
                going = False

        # This runs before the user starts the game
        if game_state.state == 'prestart':
            for event in eventlist:
            # Checks if a mouse is clicked 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    startButton.check_click()
                    quitButton.check_click()
                    difficultyButton.check_click()
                    songButton.check_click()

        # This runs when the users starts a game
        elif game_state.state == 'playing':
            # the score and high score widgets
            score_widget.setText("score: " + str(game_state.get_score()))
            high_score_widget.setText("highscore: " + str(game_state.get_high_score()))
            # Loop through all potential hitboxes
            for hitbox in game_state.hitboxes:
                # Every hitbox needs to check all events
                for event in eventlist:
                    if event.type == pygame.KEYDOWN and event.unicode == hitbox.event_key:
                        game_state.check_for_hit(hitbox)
                    elif event.type == pygame.KEYUP:
                        hitbox.unpunch()
                        
                # When on RPi also check for GPIO input
                if is_running_on_rpi:
                    for button in gpio_buttons:
                        # When a buttons is pressed in this loop and wasn't pressed in the last loop
                        if button.is_pressed() and button.gpio_key is hitbox.gpio_event_key and button.is_available():
                            button.use()  # Set the button as unavailable for the next loop
                            game_state.check_for_hit(hitbox)
                        # When a button was not pressed in this loop
                        elif not button.is_pressed():
                            button.wake()  # Set the button as available again
                            hitbox.unpunch()

        elif game_state.state == 'postgame':
            score_widget_pg.setText("score: " + str(game_state.get_last_score()))
            if (game_state.get_high_score() is not None):
                if (game_state.get_high_score() < game_state.get_score()):
                    high_score_widget.setText("highscore: " + str(game_state.get_score()))
            for event in eventlist:
            # Checks if a mouse is clicked 
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    restartButton.check_click()
                    backToMenuButton.check_click()
        # This calls the update() function on all sprites
        allsprites.update()
        
        # Draw Everything
        screen.blit(game_state.get_background(), (0, 0))  # First draw a new background
        allsprites.draw(screen)  # Next draw all updated sprites
        pygame.display.update()  # Finally render everything to the display


def init_rpi_buttons(gpio_pin_numbers):
    # Initialize Raspberry Pi input pins
    
    gpio_buttons = []
    
    from gpiozero import Button
    from classes.GpioButton import GpioButton

    # Here you can configure which pins you use on your Raspberry Pi
    gpio_pins = gpio_pin_numbers  # Max 4 pins 
    bounce_time_in_sec = 0.1

    gpio_buttons.append(GpioButton(Button(gpio_pins[0], bounce_time=bounce_time_in_sec)))
    gpio_buttons.append(GpioButton(Button(gpio_pins[1], bounce_time=bounce_time_in_sec)))
    gpio_buttons.append(GpioButton(Button(gpio_pins[2], bounce_time=bounce_time_in_sec)))
    gpio_buttons.append(GpioButton(Button(gpio_pins[3], bounce_time=bounce_time_in_sec)))

    print('The following pins are configured as (gpio) button inputs:', gpio_pins)

    return gpio_buttons


if __name__ == "__main__":
    main()
