import pygame
import random
from pygame.locals import *

# Função para gerar uma posição aleatória na grade
def on_grid_random():
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    return (x * 10, y * 10)

# Função para verificar colisão entre dois objetos
def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

# Função para desenhar uma explosão na tela
def draw_explosion(position):
    explosion_radius = 20
    explosion_color = (255, 165, 0)
    pygame.draw.circle(screen, (50, 50, 50), position, explosion_radius + 5)
    pygame.draw.circle(screen, explosion_color, position, explosion_radius)
    pygame.display.update()
    pygame.time.delay(100)

# Função para mostrar um diálogo de saída
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

# Inicializa o Pygame
pygame.init()

# Configura a tela do jogo
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Jogo da Cobra')

# Carrega os recursos visuais
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((0, 255, 0))
apple = pygame.Surface((10, 10))
apple.fill((255, 0, 0))

# Define as direções
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Inicializa as variáveis do jogo
snake = [(200, 200), (210, 200), (220, 200)]
my_direction = LEFT
apple_pos = on_grid_random()
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 18)
score = 0
game_over = False

# Loop principal do jogo
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

    # Verifica a colisão com a maçã
    if collision(snake[0], apple_pos):
        draw_explosion(apple_pos)
        apple_pos = on_grid_random()
        snake.append((0, 0))
        score += 1

    # Limita a posição da cabeça da cobra às dimensões da tela
    snake[0] = (snake[0][0] % 600, snake[0][1] % 600)

    # Move a cobra
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

    # Desenha os elementos na tela
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

# Exibe a tela de "Game Over"
while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (600 / 2, 10)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()

    # Verifica eventos do teclado
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == K_SPACE:
                # Reinicia o jogo
                snake = [(200, 200), (210, 200), (220, 200)]
                my_direction = LEFT
                score = 0
                apple_pos = on_grid_random()
                game_over = False
                break
