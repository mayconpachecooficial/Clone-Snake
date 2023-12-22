import pygame
import random
from pygame.locals import *

def on_grid_random():
    x = random.randint(0,59)
    y = random.randint(0,59)
    return (x * 10, y * 10)

def collision(c1,c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Jogo da Cobra')

snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((0, 255, 0))

apple_pos = on_grid_random()
apple = pygame.Surface((10,10))
apple.fill((255, 0, 0))

my_direction = LEFT

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0

game_over = False

def show_quit_dialog():
    font_dialog = pygame.font.Font('freesansbold.ttf', 24)
    text = font_dialog.render('Você quer sair?', True, (255, 255, 255))
    screen.blit(text, (200, 250))

    pygame.draw.rect(screen, (0, 255, 0), (200, 300, 80, 30))  
    pygame.draw.rect(screen, (255, 0, 0), (300, 300, 80, 30))  
    
    font_buttons = pygame.font.Font('freesansbold.ttf', 18)
    text_yes = font_buttons.render('Sim', True, (0, 0, 0))
    text_no = font_buttons.render('Não', True, (0, 0, 0))
    screen.blit(text_yes, (220, 305))
    screen.blit(text_no, (320, 305))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 200 < mouse_x < 280 and 300 < mouse_y < 330:  
                    pygame.quit()
                    exit()
                elif 300 < mouse_x < 380 and 300 < mouse_y < 330:  
                    return

def draw_explosion(position):
    explosion_radius = 20
    explosion_color = (255, 165, 0)  

    pygame.draw.circle(screen, (50, 50, 50), position, explosion_radius + 5)
    pygame.draw.circle(screen, explosion_color, position, explosion_radius)
    pygame.display.update()
    pygame.time.delay(100)  

while not game_over:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and my_direction != DOWN:
                my_direction = UP 
            elif event.key == K_DOWN and my_direction != UP:
                my_direction = DOWN
            elif event.key == K_LEFT and my_direction != RIGHT:
                my_direction = LEFT 
            elif event.key == K_RIGHT and my_direction != LEFT:
                my_direction = RIGHT
            elif event.key == K_q:
                show_quit_dialog()

    if collision(snake[0], apple_pos):
        draw_explosion(apple_pos)  
        apple_pos = on_grid_random()
        snake.append((0, 0))    
        score = score + 1

    snake[0] = (snake[0][0] % 600, snake[0][1] % 600)

    for i in range(len(snake) - 1, 0, -1):    
        snake[i] = (snake[i - 1][0], snake[i - 1][1])

    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    elif my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    elif my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    elif my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1]) 

    screen.fill((0, 0, 0))
    screen.blit(apple, apple_pos)
    
    for x in range(0, 600, 10):  
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
    for y in range(0, 600, 10): 
        pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

    score_font = font.render('Pontuação: %s' % (score), True, (255, 255, 255))
    score_rect = score_font.get_rect()
    score_rect.topleft = (600 - 120, 10)
    screen.blit(score_font, score_rect)

    for pos in snake:
        screen.blit(snake_skin, pos)

    pygame.display.update()

while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (600 / 2, 10)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()

    def initialize_game():
        global snake, my_direction, score, game_over, apple_pos
        snake = [(200, 200), (210, 200), (220, 200)]
        my_direction = LEFT
        score = 0
        game_over = False
        apple_pos = on_grid_random()

    initialize_game()  

    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_UP and my_direction != DOWN:
                    my_direction = UP 
                if event.key == K_DOWN and my_direction != UP:
                    my_direction = DOWN
                if event.key == K_LEFT and my_direction != RIGHT:
                    my_direction = LEFT 
                if event.key == K_RIGHT and my_direction != LEFT:
                    my_direction = RIGHT   
    
        if collision(snake[0], apple_pos):
            apple_pos = on_grid_random()
            snake.append((0, 0))    
            score = score + 1

        if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
            game_over = True    
            break

        for i in range(1, len(snake) - 1):
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                game_over = True    
                break

        if game_over:
            break
        
        for i in range(len(snake) - 1, 0, -1):    
            snake[i] = (snake[i - 1][0], snake[i - 1][1])

        if my_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 10)
        if my_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 10)
        if my_direction == RIGHT:
            snake[0] = (snake[0][0] + 10, snake [0][1])
        if my_direction == LEFT:
            snake[0] = (snake[0][0] - 10, snake [0][1]) 

        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)
    
        for x in range(0, 600, 10): 
            pygame.draw.line(screen, (40, 40, 40), (x, 0),(x, 600))
        for y in range(0, 600, 10): 
            pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

        score_font = font.render('Score: %s' % (score), True, (255, 255, 255))
        score_rect = score_font.get_rect()
        score_rect.topleft = (600 - 120, 10)
        screen.blit(score_font, score_rect)

        for pos in snake:
            screen.blit(snake_skin, pos)

        pygame.display.update()

    while True:
        game_over_font = pygame.font.Font('freesansbold.ttf', 75)
        game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (600 / 2, 10)
        screen.blit(game_over_screen, game_over_rect)
        pygame.display.update()

        pygame.time.wait(500)

        
        choice = True  # Inicie com a escolha em "Sim"

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == K_SPACE:
                    initialize_game()
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    choice = not choice  
                elif event.key == K_RETURN:
                    if choice:
                        initialize_game()  
                    else:
                        pygame.quit()
                        exit()

            screen.fill((0, 0, 0))  
    
            font_choice = pygame.font.Font('freesansbold.ttf', 36)
            text_sim = font_choice.render('Sim', True, (255, 255, 255))
            text_nao = font_choice.render('Não', True, (255, 255, 255))
    
            if choice:
                pygame.draw.rect(screen, (255, 0, 0), (195, 300, 160, 40), 2)  
            else:
                pygame.draw.rect(screen, (255, 0, 0), (395, 300, 160, 40), 2)  
    
                screen.blit(text_sim, (200, 300))
                screen.blit(text_nao, (400, 300))

                pygame.display.update()
                clock.tick(10)

# O restante do seu código continua aqui, dependendo da escolha feita.



   

