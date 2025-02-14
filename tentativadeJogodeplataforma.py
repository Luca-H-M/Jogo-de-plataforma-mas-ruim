import pygame

class BlockSprite(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('Block-standing.png').convert_alpha()
    self.img_1 = pygame.transform.scale(img, (30, 30))
    self.image = self.img_1
    self.rect = self.image.get_rect()
    self.rect.topleft = (250, 250)

    self.velocidadex = 2
    self.velocidadey = 0
    self.gravity = 0.2
  
  def player_esquerda(self, x):
    self.rect.x -= self.velocidadex + x

  def player_direita(self, x):
    self.rect.x += self.velocidadex + x

  def gravity_update(self):
    if self.velocidadey < 10:
      self.velocidadey += self.gravity
    else:
      self.velocidadey = 10
    if self.rect.y > 930:
      self.velocidadey *= -1
    self.rect.y += self.velocidadey
    print(self.rect.y)


class FloorSprite(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('Dirt-grass.png').convert_alpha()
    self.img1 = pygame.transform.scale(img, (30, 30))
    img = pygame.image.load('Dirt-1.png').convert_alpha()
    self.img2 = pygame.transform.scale(img, (30, 30))
    self.image = self.img1
    self.rect = self.image.get_rect()
    self.rect.topleft = (250, 820)

  def change(self):
    self.image = self.img2




# estatisticas do jogador, tamanho, posição e velocidade
playerposy = 800
playerheight = 30
playerposx = 30
playerwidth = 30

speedy = 0
speedx = 0
xaccelspeed = 2


# estatisticas do jogo, gravidade, pulos, dashes, etc
gravity = 0.2314
airdrag = 5

jumps = 1
coyote = 0
dash = 1
dashtimer = 0

wait = 0   # variavel "branca"

### jogo ###
pygame.init()

WINDOW_SIZE = (1066, 800)                            # tamanho da janela
screen = pygame.display.set_mode(WINDOW_SIZE, 9, 32) # configura janela do jogo
clock = pygame.time.Clock()

bloco = BlockSprite()
chão = FloorSprite()

todos_sprites = pygame.sprite.Group([bloco, chão])

running = True
font = pygame.font.Font(None, 24)                    # fonte qualquer
display = pygame.Surface((1280, 960))                # tamanho "real" da tela
gamescreen = 0                                       # vai controlar quando o personagem muda de tela (se eu chegar longe o suficiente)

while running:
  # Processamento de eventos (entradas de teclado e mouse)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:                                     #pra quando quiserem sair do jogo
      running = False
    
    elif event.type == pygame.KEYDOWN:                                # verifica se uma tecla foi pressionada
      if event.key == pygame.K_c and jumps != 0:                      # pulo
        speedy = -6
        speedx *= 1.5

      if event.key == pygame.K_x and dash > 0:                      # direção de dashes
        teclas = pygame.key.get_pressed()   
        if teclas[pygame.K_LEFT] and teclas[pygame.K_RIGHT] == False:
          speedx -= 8
        if teclas[pygame.K_UP] and teclas[pygame.K_DOWN] == False:
          speedy -= 8
        if teclas[pygame.K_DOWN] and teclas[pygame.K_UP] == False:
          speedy = +16
        if teclas[pygame.K_RIGHT]and teclas[pygame.K_LEFT] == False:
          speedx += 8
        
        dash -= 1

  display.fill((146, 244, 255)) # Apaga o quadro atual preenchendo a tela com a cor azul claro


  player = pygame.Surface([playerwidth, playerheight])  # cria o jogador, talvez seja substituido por um sprite
  player.fill((0, 0, 0))
  display.blit(player, (playerposx, playerposy))

  
  if gamescreen == 0:                                   # tela atual do jogo, talvez seja usado talvez não 
    floor1height = 80
    floor1width = 3400                                   # informações das posições dos "blocos", vai ser alterado futuramente
    floor1posx = 0
    floor1posy = 880
  floor1 = pygame.Surface([floor1width, floor1height])
  floor1.fill((89, 51, 29))
  display.blit(floor1, (floor1posx, floor1posy))


  speedy = speedy + gravity                             # delimita os padrões da velocidade no eixo y
  if speedy > 10:
    speedy = 10
  playerposy += speedy
  if floor1posy + 15 > playerposy + 30 > floor1posy and floor1posx - 30 < playerposx < floor1posx + floor1width: # faz o jogador não atravessar o chão, vai ser alterado
    playerposy = floor1posy - 30
    speedy = 0

  
  if speedx != 0:                         # delimita os padrões da velocidade no eixo x
    speedx -= (speedx / airdrag) +  (speedx / abs(speedx))
    if -0.1 < speedx < 0.1:
      speedx = 0

  teclas = pygame.key.get_pressed()       # percebe quando uma tecla esta sendo segurada verificando movimento a direita, esquerda e o botão de pulo
  if teclas[pygame.K_LEFT] and not 0 > dashtimer > -10:
    speedx -= xaccelspeed
    bloco.player_esquerda(1)
  if teclas[pygame.K_RIGHT] and not 0 > dashtimer > -10:
    speedx += xaccelspeed
    bloco.player_direita(1)
  if teclas[pygame.K_c]:
    gravity = 0.1314
  else:
    gravity = 0.2314
  playerposx += speedx


  if speedy == 0:               # percebe quando o jogador esta no chão, ele devolve o pulo e o timer do "pulo coyote
    coyote = 5
    jumps = 1
    if dashtimer < -2:
      dash = 1
  else:
    coyote -= 1
  if coyote < 0:
    jumps = 0
    coyote = -1


  if dash == 0:                 # delimita a fisica do dash, talvez tenham alguns ajustes
    dashtimer -= 1
  else:
    dashtimer = 0

  if -5 < dashtimer < 0:
    airdrag = -3
    gravity = 0.15
  elif -15 < dashtimer < -10 and speedy < -9:
    gravity = 4
    airdrag = -3
  else:
    airdrag = 5



  surface_texto = font.render(f'dashtimer{dashtimer} speedx{speedx} ', True, 'black')  #texto para me ajudar a entender o que esta dando de errado quando as coisas dão errado
  display.blit(surface_texto, (0, 0))

  if bloco.rect.colliderect(chão):
    chão.change()
    bloco.rect.bottom = chão.rect.top +0.5
    bloco.velocidadey = 0
  else:
    bloco.gravity_update()
  todos_sprites.draw(display)

  scale = pygame.transform.scale(display, WINDOW_SIZE) # cola a minha tela "real" com o novo tamanho de tela
  screen.blit(scale, (0, 0))
  
  pygame.display.flip() # Desenha o quadro atual na tela

  clock.tick(60)  # Pausa e indica a taxa de quadros por segundo (FPS)

pygame.quit()