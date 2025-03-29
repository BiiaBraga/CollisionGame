# Biblioteca PyGame
import pygame
# Biblioteca para geracao de numeros pseudoaleatorios
import random
# Modulo da biblioteca PyGame que permite o acesso as teclas utilizadas
from pygame.locals import *

pygame.init()

pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.load('msc_fundo.mp3')
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound('msc_colisao.mp3')
barulho_colisao.set_volume(0.05)
# Classe que representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pacman = pygame.image.load('pacman.png')

        super(Player, self).__init__()
        self.surf = pacman
        self.rect = self.surf.get_rect()

    # Determina acao de movimento conforme teclas pressionadas

    def update(self, pressed_keys):

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Mantem o jogador nos limites da tela do jogo
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600


# Classe que representa os inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        ghost = pygame.image.load('Novopink.png')
        super(Enemy, self).__init__()
        self.surf = ghost
        self.rect = self.surf.get_rect(
            # Coloca na extrema direita (entre 820 e 900) e sorteia sua posicao em relacao a coordenada y (entre 0 e 600)
            center=(random.randint(820, 900), random.randint(0, 600))
        )
        self.speed = random.uniform(1, 8)  # Sorteia sua velocidade, entre 1 e 15

    # Funcao que atualiza a posiçao do inimigo em funcao da sua velocidade e termina com ele quando ele atinge o limite esquerdo da tela (x < 0)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


    # texto pontuação
def textoPontuação(pontos):
    font = pygame.font.SysFont('tahoma', 30, "Bold", 'Italic')
    texto = font.render("Pontuação: " + str(pontos), True, (239, 0, 255), (0, 0, 0))
    textRect = texto.get_rect()
    textRect.center = (650, 20)
    screen.blit(texto, textRect)
    pygame.display.update()

#Texto Game Over
def textoGameOver():
    font = pygame.font.SysFont('tahoma', 27, "Bold", 'Italic')
    texto1 = font.render("IT'S OK TO LOSE :) GIVE US A GOOD GRADE... THANKS!", True, (239, 0, 255), (0, 0, 0))
    textRect1 = texto1.get_rect()
    textRect1.center = (400, 200)
    screen.blit(texto1, textRect1)
    pygame.display.flip()

#Texto Game Over
def textoTotalPontos(ponto):
    font = pygame.font.SysFont('tahoma', 50, "Bold", 'Italic')
    texto = font.render("Pontuação Maxima:  " + str(ponto), True, (239, 0, 255), (0, 0, 0))
    textRect = texto.get_rect()
    textRect.center = (400, 300)
    screen.blit(texto, textRect)
    pygame.display.flip()

azul = (0, 0, 0)
preto = (0, 0, 0)
# Inicializa pygame
pygame.init()

# Cria a tela com resolução 800x600px
screen = pygame.display.set_mode((800, 600))

# Cria um evento para adicao de inimigos
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 800)  # Define um intervalo para a criacao de cada inimigo (milisegundos)

# Cria o jogador (nosso retangulo)
player = Player()

# Define o plano de fundo, com a cor preta (RGB)
background = pygame.Surface(screen.get_size())
background.fill(azul)
enemies = pygame.sprite.Group()  # Cria o grupo de inimigos
all_sprites = pygame.sprite.Group()  # Cria o grupo de todos os Sprites
all_sprites.add(player)  # Adicionar o player no grupo de todos os Sprites

running = True  # Flag para controle do jogo

c = 20  # variavel de controle do clock
clock = pygame.time.Clock()
pygame.font.init()
pontos = 0
cont = 0
controle = 0

velo = 0

while running:

    tex = True
    if tex:    # permite a contagem de pontos
        cont += 1

        if cont == 100:
            cont = 0

        if cont == 99:
            pontos += 1

        if cont == 1:
            controle += 1
        if controle == 5:
            velo -= 10
            controle = 0

            c += 10


        textoPontuação(pontos)  # texto pontuação

    if cont >= 200:
        textoGameOver() #texto Game Over
        textoTotalPontos(pontos) # texto total de pontos



    clock.tick(c) # controla a velocidade do clock

    # Laco para verificacao do evento que ocorreu
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Verifica se a tecla ESC foi pressionada
                running = False
        elif event.type == QUIT:  # Verifica se a janela foi fechada
            running = False


        elif (event.type == ADDENEMY):  # Verifica se e o evento de criar um inimigo

            new_enemy = Enemy()  # Cria um novo inimigo
            enemies.add(new_enemy)  # Adiciona o inimigo no grupo de inimigos
            all_sprites.add(new_enemy)  # Adiciona o inimigo no grupo de todos os Sprites
        elif pontos >= 10:
            new_enemy = Enemy()  # Cria um novo inimigo
            enemies.add(new_enemy)  # Adiciona o inimigo no grupo de inimigos
            all_sprites.add(new_enemy) # Adiciona o inimigo no grupo de todos os Sprites
    screen.blit(background, (0, 0))  # Atualiza a exibicao do plano de fundo do jogo (neste caso nao surte efeito)
    pressed_keys = pygame.key.get_pressed()  # Captura as as teclas pressionadas
    player.update(pressed_keys)  # Atualiza a posicao do player conforme teclas usadas
    enemies.update()  # Atualiza posicao dos inimigos
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)  # Atualiza a exibicao de todos os Sprites

    if pygame.sprite.spritecollideany(player, enemies):  # Verifica se ocorreu a colisao do player com um dos inimigos
        player.kill()  # Se ocorrer a colisao, encerra o player
        cont += 200  # atribui valor 200 à variavel de controle de pontos
        tex = False # para a contagem de pontos
        background.fill(preto)
        barulho_colisao.play()
        c = 1 #Atribui valor 10 à velocidade do clock


    pygame.display.flip()  # Atualiza a projecao do jogo
# Biblioteca PyGame
