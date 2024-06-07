import pygame
import sys
import random
import time

class Button:
    def __init__(self, x, y, width, height, image_path=None, color=None, hover_color=None, hover_scale=1.1):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path) if image_path else None
        self.color = color if color else (255, 255, 255)
        self.hover_color = hover_color if hover_color else self.color
        self.hover_scale = hover_scale
        if self.image:
            self.original_size = self.image.get_size()
        self.hovered = False

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, self.color if not self.hovered else self.hover_color, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

def animate_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.1)  # adjust this value for the speed of the animation
    
def draw_text(text, font, text_color, x, y, width):
    # Split the text into words
    words = text.split()

    # Initialize variables for the lines of text
    lines = []
    line = ''

    # Iterate through words and build lines
    for word in words:
        # Render the word
        rendered_word = font.render(word, True, text_color)
        # Check if adding the word exceeds the width
        if rendered_word.get_width() + font.render(line, True, text_color).get_width() < width:
            line += word + ' '
        else:
            lines.append(line)
            line = word + ' '

    # Append the last line
    lines.append(line)

    # Render each line and blit them to the screen
    y_offset = y
    for line in lines:
        img = font.render(line, True, text_color)
        screen.blit(img, (x, y_offset))
        y_offset += font.get_height()


class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
    def draw(self, screen):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, 'red', (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, 'green', (self.x, self.y, self.w * ratio, self.h))

def change_image_color(image, color):
    # Create a copy of the original image
    colored_image = image.copy()
    # Fill the copy with the specified color
    colored_image.fill(color, special_flags=pygame.BLEND_MULT)
    return colored_image

# Function to revert to the original image color
def revert_image_color(image, original_image):
    return original_image

# Initialize game and font
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Character
char_Color = (234, 0, 124)
charX = 0
charY = 30
charWidth = 60
charHeight = 60

# Screen size
WIDTH = 1000
HEIGHT = 650

# Set screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ASSETS IMAGES
BGcolor = (255, 255, 255)
background_image = pygame.image.load('images/BG.jpg')
choose_image = pygame.image.load('images/choosepokemon.jpg')
battle_background = pygame.image.load('images/field.png')
battle_background = pygame.transform.scale(battle_background, (WIDTH, HEIGHT))

# Starter IMAGES
bulbasaur = pygame.image.load("images/bulbasaur.png").convert_alpha()
bulbasaur_back = pygame.image.load("images/BulbasaurBack.png").convert_alpha()
scaled_bulbasaur_back = pygame.transform.scale(bulbasaur_back, (500, 500))
scaled_bulbasaur_back_damage = scaled_bulbasaur_back.copy()
charmander_back = pygame.image.load("images/CharmanderBack.png").convert_alpha()
scaled_charmander_back = pygame.transform.scale(charmander_back, (500, 500))
scaled_charmander_back_damage = scaled_charmander_back.copy()
squirtle = pygame.image.load("images/squirtle.png").convert_alpha()
squirtle_back = pygame.image.load("images/SquirtleBack.png").convert_alpha()
scaled_squirtle_back = pygame.transform.scale(squirtle_back, (500, 500))
scaled_squirtle_back_damage = scaled_squirtle_back.copy()
charmander = pygame.image.load("images/charmander.png").convert_alpha()
mew = pygame.image.load("images/MewFront.png").convert_alpha()
scaled_mew = pygame.transform.scale(mew, (300, 300))
scaled_mew_damage = scaled_mew.copy()

#MUSIC PATH
pygame.mixer.music.load("music/Intro.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

# Fonts
font = pygame.font.SysFont('none', 30)
font_welcome = pygame.font.SysFont('none', 70)
# Dif Fonts for text
fps_text = font.render("", True, (255, 255, 255))
welcome_text = font_welcome.render("Welcome to Pymon", True, (255, 255, 255))
start_text = font.render("Click to START", True, (255, 255, 255))
choose_text = font_welcome.render("Choose a starter", True, (255, 255, 255))

choose_pokemon = font.render("Choose", True, (255,255,255))
choose_button = pygame.Rect(700, 400, 110, 60)

#DIVIDER for moves
attack_text = font.render('Attack' , True , 'white') 
div_moves = pygame.Rect(700, 450, 110, 60)

run_text = font.render('Run' , True , 'white') 
div_moves2 = pygame.Rect(850, 450, 110, 60)

vine_whip = font.render('Vine Whip' , True , 'white') 
tackle = font.render('Tackle' , True , 'white') 
ember = font.render('Ember' , True , 'white') 
scratch = font.render('Scratch' , True , 'white') 
water_gun = font.render('Water Gun' , True , 'white') 
bite = font.render('Bite' , True , 'white') 
div_moves3 = pygame.Rect(700, 560, 110, 60)
div_moves4 = pygame.Rect(850, 560, 110, 60)


poke_hp_counter = 100
mew_hp_counter = 100
bulb_name = font.render('Bulbasaur' , True , 'black') 
char_name = font.render('Charmander' , True , 'black') 
squi_name = font.render('Squirtle' , True , 'black') 
mew_name = font.render('Mew' , True , 'black') 
pokemon_hp = font.render(str(poke_hp_counter) , True , 'black') 
mew_hp = font.render(str(mew_hp_counter) , True , 'black') 

# Change icon of game
icon = pygame.image.load('icon.png')

# Set title and icon
pygame.display.set_caption('PyMon')
pygame.display.set_icon(icon)

# Clock object
clock = pygame.time.Clock()

# Create rectangles for the text
rectWelcome = welcome_text.get_rect()
rectWelcome.center = (WIDTH // 2, HEIGHT // 2)

rectStart = start_text.get_rect()
rectStart.centerx = rectWelcome.centerx
rectStart.top = rectWelcome.bottom + 20

rectChoose = choose_text.get_rect()
rectChoose.top = 50
rectChoose.centerx = WIDTH // 2

#HEALTH BAR
pokemon_health = HealthBar(50, 350, 300, 20, 100)
mew_health = HealthBar(300, 60, 300, 20, 100)


# Create POKEMON button INSTANCE
bulbasaur_button = Button(40, ((HEIGHT - bulbasaur.get_height()) // 2), bulbasaur.get_width(), bulbasaur.get_height(), 'images/bulbasaur.png')
charmander_button = Button((WIDTH // 2) - (charmander.get_width() // 2), (HEIGHT - charmander.get_height()) // 2, charmander.get_width(), charmander.get_height(), 'images/charmander.png')
squirtle_button = Button((WIDTH - squirtle.get_width() - 40), (HEIGHT - squirtle.get_height()) // 2, squirtle.get_width(), squirtle.get_height(), 'images/squirtle.png')


# Main game loop
main = True
change_background = False
chosen_pokemon = None  # Variable to store the chosen Pokémon
button_pressed = False
is_next = False
is_attack = False

show_div_moves = True
show_div_moves2 = True

while main:
    screen.blit(background_image, (0, 0))  # Initial background
    screen.blit(fps_text, (10, 10))
    screen.blit(welcome_text, rectWelcome)
    screen.blit(start_text, rectStart)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not change_background:
            main = False
            change_background = True  # Change the background when screen is clicked
            
            pygame.mixer.music.stop()
            #PLAY CHOOSE MUSIC
            pygame.mixer.music.load("music/Choose.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(loops=-1)
        
    pygame.display.flip()

while change_background:
    screen.blit(choose_image, (0, 0))
    screen.blit(choose_text, rectChoose)

    button_pressed = False  # Reset button pressed flag at the beginning of each iteration

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check if any of the Pokémon buttons are clicked
        if not chosen_pokemon:  # Only check buttons if a Pokémon hasn't been chosen yet
            if bulbasaur_button.is_clicked(event):
                chosen_pokemon = "Bulbasaur"  # Set the chosen Pokémon
            elif charmander_button.is_clicked(event):
                chosen_pokemon = "Charmander"  # Set the chosen Pokémon
            elif squirtle_button.is_clicked(event):
                chosen_pokemon = "Squirtle"  # Set the chosen Pokémon

        # Handle choose button click
        if chosen_pokemon and choose_button.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = True
                print("You Choose a POKEMON")
                change_background = False
                is_next = True  # Proceed to the next loop


                #PLAY CHOOSE MUSIC
                # pygame.mixer.music.load("music/Battle.mp3")
                # pygame.mixer.music.set_volume(0.5)
                # pygame.mixer.music.play(loops=-1)

    if chosen_pokemon:
        if chosen_pokemon == "Bulbasaur":
            screen.blit(bulbasaur, (40, (HEIGHT - bulbasaur.get_height()) // 2))
            draw_text("Bulbasaur are small, amphibian and plant Pokémon that move on all four legs. They have blue-green bodies with darker blue-green spots. The seed on a Bulbasaur's back is planted at birth and then sprouts and grows along with it. The bulb absorbs sunlight which allows it to grow.", font, (255, 255, 255), 350, 250, 500)
        elif chosen_pokemon == "Charmander":
            screen.blit(charmander, (40, (HEIGHT - charmander.get_height()) // 2))
            draw_text("Charmander is a bipedal, reptilian Pokémon. Most of its body is colored orange, while its underbelly is light yellow and it has blue eyes. It has a flame at the end of its tail, which is said to signify its health.", font, (255, 255, 255), 350, 250, 500)
        elif chosen_pokemon == "Squirtle":
            screen.blit(squirtle, (40, (HEIGHT - squirtle.get_height()) // 2))
            draw_text("Squirtle is a small, light-blue Pokémon with an appearance similar to a turtle. With its aerodynamic shape and grooved surface, Squirtle's shell helps it wade through the water very quickly. It also offers protection in battle.", font, (255, 255, 255), 350, 250, 500)

        # Draw the choose button
        a, b = pygame.mouse.get_pos()
        if choose_button.collidepoint((a, b)):
            pygame.draw.rect(screen, (180, 180, 180), choose_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), choose_button)

        screen.blit(choose_pokemon, (choose_button.x + 20, choose_button.y + 20))
    else:
        # Draw the remaining Pokémon buttons
        bulbasaur_button.draw(screen)
        charmander_button.draw(screen)
        squirtle_button.draw(screen)

    pygame.display.flip()


while is_next:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(battle_background, (0, 0))
    pokemon_health.draw(screen)
    screen.blit(mew_name, (300, 40))
    mew_health.draw(screen)
    screen.blit(mew_hp, (300, 80))
    screen.blit(pokemon_hp, (50, 370))

    if chosen_pokemon == "Bulbasaur":
        screen.blit(bulb_name, (50, 330))
        screen.blit(scaled_bulbasaur_back, (60, 300))
        screen.blit(scaled_mew, (550, 30))
    elif chosen_pokemon == "Charmander":
        screen.blit(char_name, (50, 330))
        screen.blit(scaled_charmander_back, (60, 300))
        screen.blit(scaled_mew, (550, 30))
    elif chosen_pokemon == "Squirtle":
        screen.blit(squi_name, (50, 330))
        screen.blit(scaled_squirtle_back, (60, 300))
        screen.blit(scaled_mew, (550, 30))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if div_moves.collidepoint(event.pos) and not button_pressed:
                button_pressed = True
                is_next = False
                is_attack = True
                print("User use Attack")

                pygame.mixer.music.stop()
                #PLAY CHOOSE MUSIC
                pygame.mixer.music.load("music/Battle.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(loops=-1)
            if div_moves2.collidepoint(event.pos) and not button_pressed:
                button_pressed = True
                print("User Run")
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            button_pressed = False

    # HOVER EFFECT ON BUTTONS
    a, b = pygame.mouse.get_pos()
    if div_moves.collidepoint((a, b)):
        pygame.draw.rect(screen, (180, 180, 180), div_moves)
        pygame.draw.rect(screen, (100, 100, 100), div_moves2)
    elif div_moves2.collidepoint((a, b)):
        pygame.draw.rect(screen, (180, 180, 180), div_moves2)
        pygame.draw.rect(screen, (100, 100, 100), div_moves)
    else:
        pygame.draw.rect(screen, (100, 100, 100), div_moves)
        pygame.draw.rect(screen, (100, 100, 100), div_moves2)
    
    screen.blit(attack_text, (div_moves.x + 20, div_moves.y + 20))
    screen.blit(run_text, (div_moves2.x + 35, div_moves2.y + 20))

    pygame.display.flip()

    if is_attack:
        break  # Exit the loop if is_attack becomes True

while is_attack:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        button_pressed = False

        screen.blit(battle_background, (0, 0))
        pokemon_health.draw(screen)
        mew_health.draw(screen)
        screen.blit(mew_name, (300, 40))
        screen.blit(scaled_mew, (550, 30))
        screen.blit(mew_hp, (300, 80))
        screen.blit(pokemon_hp, (50, 370))

        # HOVER EFFECT ON BUTTONS
        a, b = pygame.mouse.get_pos()
        if div_moves3.collidepoint((a, b)):
            pygame.draw.rect(screen, (180, 180, 180), div_moves3)
            pygame.draw.rect(screen, (100, 100, 100), div_moves4)
        elif div_moves4.collidepoint((a, b)):
            pygame.draw.rect(screen, (180, 180, 180), div_moves4)
            pygame.draw.rect(screen, (100, 100, 100), div_moves3)
        else:
            pygame.draw.rect(screen, (100, 100, 100), div_moves3)
            pygame.draw.rect(screen, (100, 100, 100), div_moves4)

        if chosen_pokemon == 'Bulbasaur':
            screen.blit(bulb_name, (50, 330))
            screen.blit(scaled_bulbasaur_back, (60, 300))
            screen.blit(vine_whip, (div_moves3.x + 5, div_moves3.y + 20))
            screen.blit(tackle, (div_moves4.x + 20, div_moves4.y + 20))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if div_moves3.collidepoint(event.pos) and not button_pressed:
                    button_pressed = True
                    print("Pokemon use Vine Whip")
                    vine_whip_sound = pygame.mixer.Sound("music/VineWhip.mp3")
                    vine_whip_sound.set_volume(0.3)
                    vine_whip_sound.play()
                    if mew_health.hp >= 0 or pokemon_health.hp >= 0:
                        attack_damage = random.randint(10, 30)
                        print(f"Pokemon Damage: {attack_damage}")
                        mew_health.hp -= attack_damage
                        mew_hp_counter -= attack_damage
                        mew_hp = font.render(str(mew_hp_counter), True, 'black')
                        print(f"Mew remaining health: {mew_health.hp}")
                        mew_damage = random.randint(10, 40)
                        print(f"Mew Damage: {mew_damage}")
                        pokemon_health.hp -= mew_damage
                        poke_hp_counter -= mew_damage
                        pokemon_hp = font.render(str(poke_hp_counter), True, 'black')
                        print(f"Pokemon remaining health: {pokemon_health.hp}")


                        # DAMAGE EFFECT
                        colored_image = change_image_color(scaled_bulbasaur_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_bulbasaur_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
                        #CHANGE PART 2
                        colored_image = change_image_color(scaled_bulbasaur_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_bulbasaur_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
                elif div_moves4.collidepoint(event.pos) and not button_pressed:
                    button_pressed = True
                    # is_attack = False
                    print("Pokemon Use Tackle")
                    tackle_sound = pygame.mixer.Sound("music/Tackle.mp3")
                    tackle_sound.set_volume(0.3)
                    tackle_sound.play()
                    if mew_health.hp >= 0 or pokemon_health.hp >= 0:
                        attack_damage = random.randint(15, 20)
                        print(f"Pokemon Damage: {attack_damage}")
                        mew_health.hp -= attack_damage
                        mew_hp_counter -= attack_damage
                        mew_hp = font.render(str(mew_hp_counter), True, 'black')
                        print(f"Pokemon remaining health: {mew_health.hp}")
                        mew_damage = random.randint(10, 40)
                        print(f"Mew Damage: {mew_damage}")
                        pokemon_health.hp -= mew_damage
                        poke_hp_counter -= mew_damage
                        pokemon_hp = font.render(str(poke_hp_counter), True, 'black')
                        print(f"Pokemon remaining health: {pokemon_health.hp}")

                        # DAMAGE EFFECT
                        colored_image = change_image_color(scaled_bulbasaur_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_bulbasaur_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
                        #CHANGE PART 2
                        colored_image = change_image_color(scaled_bulbasaur_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_bulbasaur_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONUP:
                button_pressed = False
        elif chosen_pokemon == 'Charmander':
            screen.blit(char_name, (50, 330))
            screen.blit(scaled_charmander_back, (60, 300))
            screen.blit(ember, (div_moves3.x + 20, div_moves3.y + 20))
            screen.blit(scratch, (div_moves4.x + 20, div_moves4.y + 20))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if div_moves3.collidepoint(event.pos) and not button_pressed:
                    button_pressed = True
                    print("Pokemon use Ember")
                    ember_sound = pygame.mixer.Sound("music/Ember.mp3")
                    ember_sound.set_volume(0.3)
                    ember_sound.play()
                    if mew_health.hp >= 0 or pokemon_health.hp >= 0:
                        attack_damage = random.randint(10, 30)
                        print(f"Pokemon Damage: {attack_damage}")
                        mew_health.hp -= attack_damage
                        mew_hp_counter -= attack_damage
                        mew_hp = font.render(str(mew_hp_counter), True, 'black')
                        print(f"Mew remaining health: {mew_health.hp}")
                        mew_damage = random.randint(10, 40)
                        print(f"Mew Damage: {mew_damage}")
                        pokemon_health.hp -= mew_damage
                        poke_hp_counter -= mew_damage
                        pokemon_hp = font.render(str(poke_hp_counter), True, 'black')
                        print(f"Pokemon remaining health: {pokemon_health.hp}")

                        # DAMAGE EFFECT
                        colored_image = change_image_color(scaled_charmander_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_charmander_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
                        #CHANGE PART 2
                        colored_image = change_image_color(scaled_charmander_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_charmander_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
                elif div_moves4.collidepoint(event.pos) and not button_pressed:
                    button_pressed = True
                    print("Pokemon Use Scratch")
                    scratch_sound = pygame.mixer.Sound("music/Scratch.mp3")
                    scratch_sound.set_volume(0.3)
                    scratch_sound.play()
                    if mew_health.hp >= 0 or pokemon_health.hp >= 0:
                        attack_damage = random.randint(15, 20)
                        print(f"Pokemon Damage: {attack_damage}")
                        mew_health.hp -= attack_damage
                        mew_hp_counter -= attack_damage
                        mew_hp = font.render(str(mew_hp_counter), True, 'black')
                        print(f"Pokemon remaining health: {mew_health.hp}")
                        mew_damage = random.randint(10, 40)
                        print(f"Mew Damage: {mew_damage}")
                        pokemon_health.hp -= mew_damage
                        poke_hp_counter -= mew_damage
                        pokemon_hp = font.render(str(poke_hp_counter), True, 'black')
                        print(f"Pokemon remaining health: {pokemon_health.hp}")

                        # DAMAGE EFFECT
                        colored_image = change_image_color(scaled_charmander_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_charmander_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
                        #CHANGE PART 2
                        colored_image = change_image_color(scaled_charmander_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_charmander_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONUP:
                button_pressed = False
        elif chosen_pokemon == 'Squirtle':
            screen.blit(squi_name, (50, 330))
            screen.blit(scaled_squirtle_back, (60, 300))
            screen.blit(water_gun, (div_moves3.x + 5, div_moves3.y + 20))
            screen.blit(bite, (div_moves4.x + 20, div_moves4.y + 20))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if div_moves3.collidepoint(event.pos) and not button_pressed:
                    button_pressed = True
                    print("Pokemon use Water Gun")
                    water_gun_sound = pygame.mixer.Sound("music/WaterGun.mp3")
                    water_gun_sound.set_volume(0.3)
                    water_gun_sound.play()
                    if mew_health.hp >= 0 or pokemon_health.hp >= 0:
                        attack_damage = random.randint(10, 30)
                        print(f"Pokemon Damage: {attack_damage}")
                        mew_health.hp -= attack_damage
                        mew_hp_counter -= attack_damage
                        mew_hp = font.render(str(mew_hp_counter), True, 'black')
                        print(f"Mew remaining health: {mew_health.hp}")
                        mew_damage = random.randint(10, 40)
                        print(f"Mew Damage: {mew_damage}")
                        pokemon_health.hp -= mew_damage
                        poke_hp_counter -= mew_damage
                        pokemon_hp = font.render(str(poke_hp_counter), True, 'black')
                        print(f"Pokemon remaining health: {pokemon_health.hp}")

                        # DAMAGE EFFECT
                        colored_image = change_image_color(scaled_squirtle_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_squirtle_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
                        #CHANGE PART 2
                        colored_image = change_image_color(scaled_squirtle_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_squirtle_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
                elif div_moves4.collidepoint(event.pos) and not button_pressed:
                    button_pressed = True
                    print("Pokemon Use Bite")
                    bite_sound = pygame.mixer.Sound("music/Bite.mp3")
                    bite_sound.set_volume(0.3)
                    bite_sound.play()
                    if mew_health.hp >= 0 or pokemon_health.hp >= 0:
                        attack_damage = random.randint(15, 20)
                        print(f"Pokemon Damage: {attack_damage}")
                        mew_health.hp -= attack_damage
                        mew_hp_counter -= attack_damage
                        mew_hp = font.render(str(mew_hp_counter), True, 'black')
                        print(f"Pokemon remaining health: {mew_health.hp}")
                        mew_damage = random.randint(10, 40)
                        print(f"Mew Damage: {mew_damage}")
                        pokemon_health.hp -= mew_damage
                        poke_hp_counter -= mew_damage
                        pokemon_hp = font.render(str(poke_hp_counter), True, 'black')
                        print(f"Pokemon remaining health: {pokemon_health.hp}")

                        # DAMAGE EFFECT
                        colored_image = change_image_color(scaled_squirtle_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_squirtle_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()
                        #CHANGE PART 2
                        colored_image = change_image_color(scaled_squirtle_back_damage, (255,0,0))
                        colored_image2 = change_image_color(scaled_mew_damage, (255,0,0))
                        screen.blit(colored_image, (60, 300))
                        screen.blit(colored_image2, (550, 30))
                        pygame.display.flip()
                        time.sleep(0.5)
                        screen.blit(scaled_squirtle_back_damage, (60, 300))
                        screen.blit(scaled_mew_damage, (550, 30))
                        pygame.display.flip()

            elif event.type == pygame.MOUSEBUTTONUP:
                button_pressed = False

    pygame.display.update()
    clock.tick(60)

    if mew_health.hp <= 0:
            print("Congratulations!")
            pygame.quit()
            sys.exit()
    elif pokemon_health.hp <= 0:
        print("You Loose")
        pygame.quit()
        sys.exit()
    elif mew_health.hp and pokemon_health.hp <= 0:
        print("Its A TIE")
        pygame.quit()
        sys.exit()
    

    # fps = clock.get_fps()
    # fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
    # screen.blit(fps_text, (10, 10))

    # pygame.display.flip()
    # clock.tick(60)

# pygame.quit()
# sys.exit()
