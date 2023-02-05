__annotations__['Autor'] = "Flavio Eduardo Ribeiro Correia de Almeida"
__annotations__['Email'] = "flavioeduardo670@gmail.com"
__annotations__['Github'] = "https://github.com/flavioeduardo670"

__version__ = "2.0.0"

__all__ = [
    "randint",
    "pygame"
    "Root",
    "Snake",
    "Apple",
    "main",
    "define"
]



# Nome das variáveis que guardam os objetos Root, Snake e Apple, respectivamente
TELA = "root"
COBRA = "snake"
MAÇA = "apple"



from random import randint as rd

try:
    import pygame
    from pygame.locals import *
except ImportError:
    raise ImportError("Instale a biblioteca pygame")


# Função usada para definir variáveis de forma mais dinâmica
def define(nome: str = '', valor = None) -> None:
    if nome == '' or valor == None:
        pass
    else:
        globals()[nome] = valor


class Root:
    """
    Este é o objeto da tela, ao qual conterá os objetos Snake e Apple.
    O seu unico parâmetro é o tamanho da janela (por padrão tem o tamanho de 600x600).
    Nele está guardado os elementos do game, como a pontuação, o tick, as fontes, etc.
    Contém as funções para renderizar todo o jogo, para fazer o game over e o restart do jogo.
    """

    def __init__(self, size: set = (600, 600)) -> None:
        pygame.init()
        self.elements = []
        self.size: set = size
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.score: int = 0
        self.pause: bool = False

    # Adiciona elemnetos ao objeto "Root"
    def __add__(self, objeto) -> None:
        pygame.display.set_caption(str(objeto))
        self.elements.append(objeto)

    # Configura a saída para o print(Root)
    def __repr__(self) -> str:
        el: str = ''
        for elements in self.elements:
            el += "\n"
            el += str(elements)

        return "Os elementos contidos em Root sâo: " + el

    # Renderiza linhas na tela
    def drawLines(self) -> None:
        for x in range(0, self.size[0], 10):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, self.size[1]))
        for y in range(0, self.size[1], 10):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (self.size[0], y))

    # Verifica a colisão entre dois objetos
    def collision(self, c1: set = None, c2: set = None) -> bool:
        if c1 == None or c2 == None:
            pass
        else:
            return (c1[0] == c2[0]) and (c1[1] == c2[1])

    # Renderiza a tela de score
    def drawRec(self) -> None:
        score_font = self.font.render('Score: %s' % (self.score), True, (255, 255, 255))
        score_rect = score_font.get_rect()
        score_rect.topleft = (self.size[0] - self.size[0] / 5, 10)
        self.screen.blit(score_font, score_rect)

    # Verifica qual tecla foi pressionada (UP, DOWN, LEFT OU RIGHT) e modifica o movimento da cobrinha, ou finaliza o jogo
    def verifyEvent(self, snake) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_UP and snake.direction != snake.DOWN:
                    snake.direction = snake.UP
                if event.key == K_DOWN and snake.direction != snake.UP:
                    snake.direction = snake.DOWN
                if event.key == K_LEFT and snake.direction != snake.RIGHT:
                    snake.direction = snake.LEFT
                if event.key == K_RIGHT and snake.direction != snake.LEFT:
                    snake.direction = snake.RIGHT
                if event.key == K_SPACE:
                    self.pause = not self.pause


    # Roda a rotina do gameover (Mostra 'Game Over' na tela, reseta o score e verifica se o usuário deseja um restart)
    def gameOver(self, *args) -> None:

        while True:
            GOfont = pygame.font.Font('freesansbold.ttf', 75) # Define a fonte do "Game over"
            RIfont = pygame.font.Font('freesansbold.ttf', 25) # Define a fonte do restart
            GOscreen = GOfont.render('Game Over', True, (255, 0, 0)) # Mostra na tela o "Game Over"
            GIscreen = RIfont.render('Pressione \'R\' para Reiniciar', True, (255, 255, 255)) # Mostra na tela o restart
            GOrect = GOscreen.get_rect() # Cria o retângulo do Game Over
            GIrect = GIscreen.get_rect() # Cria o retângulo do restart
            GOrect.center = (self.size[0] // 2, self.size[1] // 2) # Centratliza o "Game Over"
            GIrect.center = (self.size[0] // 2, (self.size[1] // 10) * 9) # Localiza o restart na parte inferior no centro
            self.screen.blit(GOscreen, GOrect) # Renderiza o Game Over
            self.screen.blit(GIscreen, GIrect) # Renderiza o restart
            pygame.display.update() # Atualiza a tela

            # Verifica a tecla pressionada
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    # Verifica se o jogador pressionou 'R' e reinicia o jogo no caso de ser verdadeiro
                    if event.key == K_r:
                        self.score = 0
                        del args
                        main()


class Snake:
    """
    Este é o objeto que representa o jogador.
    Nele está guardado a informação do tamnho da cobrinha, sua posição e sua direção.
    Também contém as funçõs que verificam sua colisão, a função que realiza seu movimento, etc.
    """

    UP: int = 0
    RIGHT: int = 1
    DOWN: int = 2
    LEFT: int = 3

    def __init__(self, snake) -> None:
        self.__snake = snake
        self.skin = pygame.Surface((10,10))
        self.skin.fill((255,255,255))
        self.direction = self.RIGHT

    # Configura a saída do print(Snake)
    def __repr__(self) -> str:
        return 'Snake'

    # Configura o Snake[n] para retornar o self.__snake[n]
    def __getitem__(self, index: int = 0) -> set:
        return self.__snake[index]

    # Configura o operador '+' para adicionar um pixel de tamanho da cobrinha
    def __add__(self, item: set = (0, 0)) -> None:
        self.__snake.append(item)

    # Verifica a colisão consigo mesma
    def collisionItself(self) -> bool:
        lteste: list = []
        for i in range(1, len(self[::]) - 1):
            lteste.append(self[0] == self[i])
        return any(lteste)

    # Verifica a colisão com a borda
    def collisionBoard(self, size: list = None) -> bool:
        return self[0][0] == size[0] or self[0][1] == size[1] or self[0][0] < 0 or self[0][1] < 0

    # Realiza o movimento de acordo com sua direção
    def movDir(self) -> None:

        for i in range(len(self[::]) - 1, 0, -1):
            self.__snake[i] = (self[i-1][0], self[i-1][1])

        if self.direction == self.UP:
            self.__snake[0] = (self[0][0], self[0][1] - 10)
        if self.direction == self.DOWN:
            self.__snake[0] = (self[0][0], self[0][1] + 10)
        if self.direction == self.RIGHT:
            self.__snake[0] = (self[0][0] + 10, self[0][1])
        if self.direction == self.LEFT:
            self.__snake[0] = (self[0][0] - 10, self[0][1])    


class Apple:
    """
    Este é o objeto que representa a maçã.
    Nele está guardado a informação de sua posição e função que a modifica para um pixel aleatório.
    """

    def __init__(self, size: set = (0, 0)) -> None:
        self.__pos: set = None
        self.limitX: int = size[0] // 10
        self.limitY: int = size[1] // 10
        self.random()
        self.apple = pygame.Surface((10,10))
        self.apple.fill((0,255,0))

    # Configura a saída do print(Apple)
    def __repr__(self) -> str:
        return 'Apple'

    # Configura Apple[0] para retornar sua posição
    def __getitem__(self, index: int = 0) -> set:
        if index == 0:
            return self.__pos
        else:
            return None

    # Modifica sua posição para um pixel aleatório
    def random(self) -> None:
        x = rd(0, self.limitX)
        y = rd(0, self.limitY)
        self.__pos = (x * 10, y * 10)




# Função principal que define os objetos e roda todo o jogo em seu loop
def main() -> None:

    # Declara a variável com o objeto 'Root' e define o tamanho da tela
    define(TELA, Root((1080, 720)))
    root = globals()[TELA]

    # Declara a variável com o objeto 'Snake' e define o seu tamanho e posição inicial
    define(COBRA, Snake([(200, 200), (210, 200), (220,200)]))
    snake = globals()[COBRA]

    # Declara a variável com o objeto 'Apple' e define seus limites de surgimento
    define(MAÇA, Apple(root.size))
    apple = globals()[MAÇA]

    # Obs.: Quando rodado o arquivo no '__main__', ocorre uma redundância na declaração das variaveis root, snake e apple

    # Adiciona os objetos 'snake' e 'apple' ao objeto 'root'
    root + snake
    root + apple

    root + 'Jogo da cobrinha' # Coloca o título na janela do jogo

    # Loop principal do game
    while True:
        root.clock.tick(15) # Set em 15 tick's por segundo

        root.verifyEvent(snake)

        # Verifica a colisão entre a cobrinha e a maçã
        if root.collision(snake[0], apple[0]):
            apple.random()
            snake + (0, 0)
            root.score += 1

        # Verifica a colisão com as bordas e consigo mesmo
        if any([snake.collisionBoard(root.size), snake.collisionItself()]): break

        # Realiza o movimento da cobrinha de acordo com sua direção se o jogo não estiver pausado
        if root.pause != True: snake.movDir()
        
        root.screen.fill((0,0,0))   # Pinta o fundo de preto
        root.screen.blit(apple.apple, apple[0])   # Renderiza a maça
        
        # Features:
        # Adiciona linhas quando chega a marca de 5 pontos
        if root.score >= 5:
            root.drawLines()
        # Deixa a cobra colorida quando atinge a marca de 10 pontos
        if root.score >= 10:
            snake.skin.fill((rd(0, 255), rd(0, 255), rd(0, 255)))
        
        root.drawRec()  # Renderiza o texto de score
        
        # Renderiza toda a cobra na tela
        for pos in snake[::]:
            root.screen.blit(snake.skin, pos)

        # Atualiza a tela
        pygame.display.update()
    
    # Roda a rotina do Game Over
    root.gameOver(snake)



if __name__ == '__main__':
    main()
