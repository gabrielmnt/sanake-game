import random
import pygame

pygame.init()

# Screen dimensions
screen_x = 800
screen_y = 600

# Initialize display
dis = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('Snake Game by YourName')

clock = pygame.time.Clock()

# player/ food
snake_block = 20
initial_snake_speed = 5

# font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 50)

# Load images
menu_image = pygame.image.load('midia/snake_logo.png')
menu_image = pygame.transform.scale(menu_image, (screen_x, screen_y))
pause_image = pygame.image.load('midia/snake_menu.png')
pause_image = pygame.transform.scale(pause_image, (screen_x, screen_y))
lose_image = pygame.image.load('midia/snake_menu.png')
lose_image = pygame.transform.scale(lose_image, (screen_x, screen_y))
bg_game_image = pygame.image.load('midia/bg_game.png')
bg_game_image = pygame.transform.scale(bg_game_image, (screen_x, screen_y))

# sounds
food_snd = pygame.mixer.Sound("midia/eating_apple_1.mp3")
food_snd.set_volume(0.4)
mov_snd = pygame.mixer.Sound("midia/mov_snd.mp3")
mov_snd.set_volume(0.4)
game_over_snd = pygame.mixer.Sound("midia/game_over.mp3")
game_over_snd.set_volume(0.4)
menu_snd = pygame.mixer.Sound("midia/menu_snd.mp3")
menu_snd.set_volume(0.4)


# Draw the snake
def our_snake(snake_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, (255, 115, 0), [x[0], x[1], snake_size, snake_size], 0, 10)


# Display the current score
def your_score(score):
    value = score_font.render(f"00{score}", True, (0, 0, 0))
    if score >= 10:
        value = score_font.render(f"0{score}", True, (0, 0, 0))
        if score >= 100:
            value = score_font.render(f"{score}", True, (0, 0, 0))
    dis.blit(value, [screen_x - 100, 0])


# Display a message on the screen
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [screen_x / 6, screen_y / 3])


# Intro screen
def game_intro():
    intro = True
    while intro:
        dis.blit(menu_image, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Initial screen out
                    intro = False


# Pause screen
def game_paused():
    paused = True
    while paused:
        dis.blit(pause_image, (0, 0))

        # Buttons
        play_button = pygame.Rect(screen_x // 2 - 75, screen_y // 2 - 100, 150, 50)
        restart_button = pygame.Rect(screen_x // 2 - 75, screen_y // 2 - 25, 150, 50)
        menu_button = pygame.Rect(screen_x // 2 - 75, screen_y // 2 + 50, 150, 50)
        quit_button = pygame.Rect(screen_x // 2 - 75, screen_y // 2 + 125, 150, 50)

        pygame.draw.rect(dis, (0, 255, 0), play_button, 0, 50)
        pygame.draw.rect(dis, (255, 255, 102), restart_button, 0, 50)
        pygame.draw.rect(dis, (50, 153, 213), menu_button, 0, 50)
        pygame.draw.rect(dis, (213, 50, 80), quit_button, 0, 50)

        font = pygame.font.SysFont(None, 35)
        dis.blit(font.render('PLAY', True, (0, 0, 0)), (play_button.x + 45, play_button.y + 12))
        dis.blit(font.render('RESTART', True, (0, 0, 0)), (restart_button.x + 20, restart_button.y + 12))
        dis.blit(font.render('MENU', True, (0, 0, 0)), (menu_button.x + 40, menu_button.y + 12))
        dis.blit(font.render('QUIT', True, (0, 0, 0)), (quit_button.x + 40, quit_button.y + 12))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pause
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(menu_snd)
                pygame.mixer.music.stop()
                if play_button.collidepoint(event.pos):
                    paused = False
                elif restart_button.collidepoint(event.pos):
                    gameloop()
                elif menu_button.collidepoint(event.pos):
                    game_intro()
                    gameloop()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()


# Game over screen
def game_over_menu():
    game_over = True
    while game_over:
        dis.blit(lose_image, (0, 0))

        # Buttons
        restart_button = pygame.Rect(screen_x // 2 - 75, screen_y // 2 - 25, 150, 50)
        menu_button = pygame.Rect(screen_x // 2 - 75, screen_y // 2 + 50, 150, 50)
        quit_button = pygame.Rect(screen_x // 2 - 75, screen_y // 2 + 125, 150, 50)

        pygame.draw.rect(dis, (255, 255, 102), restart_button, 0, 50)
        pygame.draw.rect(dis, (50, 153, 213), menu_button, 0, 50)
        pygame.draw.rect(dis, (213, 50, 80), quit_button, 0, 50)

        font = pygame.font.SysFont(None, 35)
        dis.blit(font.render('RESTART', True, (0, 0, 0)), (restart_button.x + 20, restart_button.y + 12))
        dis.blit(font.render('MENU', True, (0, 0, 0)), (menu_button.x + 40, menu_button.y + 12))
        dis.blit(font.render('QUIT', True, (0, 0, 0)), (quit_button.x + 40, quit_button.y + 12))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(menu_snd)
                pygame.mixer.music.stop()
                if restart_button.collidepoint(event.pos):
                    gameloop()
                elif menu_button.collidepoint(event.pos):
                    game_intro()
                    gameloop()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()


# Main game loop
def gameloop():
    global initial_snake_speed
    snake_speed = initial_snake_speed
    game_over = False
    game_close = False

    x1 = screen_x / 2
    y1 = screen_y / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 2

    # Generate food position
    foodx = round(random.randrange(0, screen_x - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, screen_y - snake_block) / 20.0) * 20.0

    while not game_over:
        while game_close:
            game_over_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            # Commands
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_ESCAPE:
                    game_paused()
                # movement sounds
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s or pygame.K_UP or event.key == pygame.K_w or
                        event.key == pygame.K_d or event.key == pygame.K_a):
                    pygame.mixer.Sound.play(mov_snd)
                    pygame.mixer.music.stop()

        # Check for wall collision
        if x1 >= screen_x or x1 < 0 or y1 >= screen_y or y1 < 0:
            pygame.mixer.Sound.play(game_over_snd)
            pygame.mixer.music.stop()
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.blit(bg_game_image, (0, 0))
        pygame.draw.rect(dis, (255, 0, 0), [foodx, foody, snake_block, snake_block], 0,  10)
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for self collision
        for x in snake_list[:-2]:
            if x == snake_head:
                game_close = True
                pygame.mixer.Sound.play(game_over_snd)
                pygame.mixer.music.stop()

        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 2)

        pygame.display.update()

        # Check if snake ate the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_x - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, screen_y - snake_block) / 20.0) * 20.0
            length_of_snake += 1
            pygame.mixer.Sound.play(food_snd)
            pygame.mixer.music.stop()
            if snake_speed <= 10:
                snake_speed += .5
        clock.tick(snake_speed)

    pygame.quit()
    quit()


# home menu function
game_intro()
# main function
gameloop()
