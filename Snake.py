# Importar blibiotecas necessárias
import pygame, random
from pygame.locals import *

# Função para definir um local aleatório para a maçã
def on_grid_random():
    x = random.randint(10, 580)
    y = random.randint(10, 580)
    return (x//10 * 10, y//10 * 10)

# Função para verificar colisão com a maçã
def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

# Função para verificar colisão com os limites do mapa
def collision1(c1):
    if c1[0] == 0 or c1[1] == 0 or c1[0] == 600 or c1[1] == 600:
        return True

# Função para verificar colisão com ela mesmo
def collision2(c1, c2):
    for c in range(1,len(snake)):
        if c1[0][0] == c2[c][0] and c1[0][1] == c2[c][1] and apple_count != 0:
            return True

# Variáveis para definição do movimento
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Variável para ativar a função em que a cobrinha recebe várias cores aleatórias
C = False

# Variável para a quantidade de maçãs capturadas
apple_count = 0

# Iniciação da biblioteca
pygame.init()

# Definição da tela (Interface Gráfica)
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('snake')

# Criação da cobrinha
snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((255, 255, 255))

# Criação da maçã
apple = pygame.Surface((10, 10))
apple_pos = on_grid_random()
apple.fill((255, 0, 0))

# Direção inicial
my_direction = RIGHT

# Criação do timer
clock = pygame.time.Clock()
time = 0

# Estrutura de repetição que verifica os comandos (Input's)
while True:
    clock.tick(20)
    time += 0.05
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if (event.key == K_UP or event.key == K_w) and my_direction != DOWN:
                my_direction = UP
        if event.type == KEYDOWN:
            if (event.key == K_DOWN or event.key == K_s) and my_direction != UP:
                my_direction = DOWN
        if event.type == KEYDOWN:
            if (event.key == K_RIGHT or event.key == K_d) and my_direction != LEFT:
                my_direction = RIGHT
        if event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a) and my_direction != RIGHT:
                my_direction = LEFT
        if event.type == KEYDOWN:
            if event.key == K_c:
                C = True
        if event.type == KEYDOWN:
            if event.key == K_f:
                C = False

    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random()
        snake.append((0, 0))
        apple_count += 1

    if collision1(snake[0]):
        print("Pontuacão: "+str(apple_count)+" | Tempo vivo: "+str(time).split(".")[0]+"s")
        time = 0
        r1 = random.randint(0,255)
        r2 = random.randint(0,255)
        r3 = random.randint(0,255)
        snake = [(200, 200), (210, 200), (220, 200)]
        snake_skin = pygame.Surface((10, 10))
        snake_skin.fill((r1, r2, r3))
        my_direction = RIGHT
        apple_count = 0

    if collision2(snake,snake):
        print("Pontuacão: "+str(apple_count)+" | Tempo vivo: "+str(time).split(".")[0]+"s")
        time = 0
        r1 = random.randint(0,255)
        r2 = random.randint(0,255)
        r3 = random.randint(0,255)
        snake = [(200, 200), (210, 200), (220, 200)]
        snake_skin = pygame.Surface((10, 10))
        snake_skin.fill((r1, r2, r3))
        my_direction = RIGHT
        apple_count = 0    

    for i in range(len(snake)-1,0,-1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)

    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)

    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])

    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    screen.fill((0,0,0))
    screen.blit(apple, apple_pos)
    for pos in snake:
        screen.blit(snake_skin,pos)

    if C:
        snake_skin.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    pygame.display.update()
    
