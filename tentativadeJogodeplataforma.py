import pygame

class Chunks(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.tabela = []

    def tela(self, x):
      if x == 0:
        pass
      elif x == 1:
        self.tabela = [["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
                  ["0","0","0","0","0","0","0","1","0","0","0","0","0","0","0"],
                  ["0","0","0","0","0","0","0","2","1","1","1","1","1","0","0"],
                  ["0","0","0","0","0","0","0","2","0","0","0","0","0","0","0"],
                  ["1","1","1","0","0","1","0","2","0","0","0","0","0","0","0"],
                  ["0","0","0","0","0","2","0","2","0","0","0","0","0","0","0"],
                  ["0","0","0","0","0","2","0","0","0","0","0","0","0","0","0"],
                  ["1","1","0","0","0","2","0","1","0","0","0","0","0","0","0"],
                  ["0","0","0","0","0","2","0","2","0","0","0","0","0","0","0"],
                  ["1","1","1","1","1","2","1","2","0","0","0","1","1","1","1"],
                  ["2","2","2","2","2","2","2","2","0","0","0","2","2","2","2"]]
      chão = []
      y = 0
      for row in self.tabela:
        x = 0
        for tile in row:
          if tile == "1":
            chão.append(FloorSprite((x*2) * 45, (y*2) * 45, 1))
            chão.append(FloorSprite((x*2 + 1) * 45, (y*2 + 1) * 45, 2))
            chão.append(FloorSprite((x*2) * 45, (y*2 + 1) * 45, 2))
            chão.append(FloorSprite((x*2 + 1) * 45, (y*2) * 45, 1))
          elif tile == "2":
            chão.append(FloorSprite((x*2) * 45, (y*2) * 45, 2))
            chão.append(FloorSprite((x*2 + 1) * 45, (y*2 + 1) * 45, 2))
            chão.append(FloorSprite((x*2) * 45, (y*2 + 1) * 45, 2))
            chão.append(FloorSprite((x*2 + 1) * 45, (y*2) * 45, 2))
          x += 1
        y += 1
      return chão

class BlockSprite(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('Block-standing.png').convert_alpha()
    self.img1 = pygame.transform.scale(img, (45, 45))
    self.image = self.img1
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)

    self.velocidadex = 2
    self.velocidadey = 0
    self.gravity = 0.2
    self.jumps = 0
    self.jump = 10
    self.zjump = 0

  
  def player_esquerda(self, x):
    self.rect.x -= self.velocidadex + x

  def player_direita(self, x):
    self.rect.x += self.velocidadex + x

  def player_jump(self):
    if self.jumps > 0:
      self.velocidadey = -6
      self.jumps -= 1
      self.zjump = 6

  def update(self):
    self.velocidadey += self.gravity
    if self.velocidadey > 10:
      self.velocidadey = 10
    self.rect.y += self.velocidadey
    self.zjump += 1
    if self.zjump == 5:
      self.jumps -= 1
    y = 0
    for row in CHUNKS.tabela:
      x = 0
      for tile in row:
        if tile == "0":
          pass
        else:
          if ((y*2) * 45) + 35 < bloco.rect.top < ((y*2) * 45) + 90 and ((x*2) * 45) -40 < bloco.rect.x < ((x*2) * 45) + 85:
            bloco.rect.top = ((y*2) * 45) + 90
            self.velocidadey = 0
          if ((y*2) * 45) <= bloco.rect.bottom < ((y*2) * 45) + 15 and ((x*2) * 45) -44 < bloco.rect.x < ((x*2) * 45) + 90:
            self.jumps = 2
            self.rect.bottom = ((y*2) * 45)
            if self.velocidadey > 0:
              self.velocidadey = 0
            self.zjump = 0
          if ((y*2) * 45) - 35 <= bloco.rect.y < ((y*2) * 45) + 90 and ((x*2) * 45) + 80 < bloco.rect.left < ((x*2) * 45) + 90:
            bloco.rect.left = ((x*2) * 45) + 90
          if ((y*2) * 45) - 35 <= bloco.rect.y < ((y*2) * 45) + 90 and ((x*2) * 45) < bloco.rect.right < ((x*2) * 45) + 10:
            bloco.rect.right = ((x*2) * 45)
        x += 1
      y += 1

class FloorSprite(pygame.sprite.Sprite):
  def __init__(self, x, y, z):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('Dirt-grass.png').convert_alpha()
    self.img1 = pygame.transform.scale(img, (45, 45))
    img = pygame.image.load('Dirt-1.png').convert_alpha()
    self.img2 = pygame.transform.scale(img, (45, 45))
    if z == 1:
      self.image = self.img1
    elif z == 2:
      self.image = self.img2
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)

  def change(self):
    self.image = self.img2


wait = 0   # variavel "branca"

### jogo ###
pygame.init()

WINDOW_SIZE = (1066, 800)                            # tamanho da janela
screen = pygame.display.set_mode(WINDOW_SIZE, 9, 32) # configura janela do jogo
clock = pygame.time.Clock()

bloco = BlockSprite(250, 250)
CHUNKS = Chunks()
chão = CHUNKS.tela(1)

todos_sprites = pygame.sprite.Group([bloco])
todos_sprites.add(chão)

running = True
font = pygame.font.Font(None, 24)                    # fonte qualquer
display = pygame.Surface((1280, 960))                # tamanho "real" da tela

while running:
  # Processamento de eventos (entradas de teclado e mouse)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:                                     #pra quando quiserem sair do jogo
      running = False
    
    elif event.type == pygame.KEYDOWN:                                # verifica se uma tecla foi pressionada
      if event.key == pygame.K_c:                      # pulo
        bloco.player_jump()

  display.fill((146, 244, 255)) # Apaga o quadro atual preenchendo a tela com a cor azul claro

  teclas = pygame.key.get_pressed()       # percebe quando uma tecla esta sendo segurada verificando movimento a direita, esquerda e o botão de pulo
  if teclas[pygame.K_LEFT]:
    bloco.player_esquerda(1)
  if teclas[pygame.K_RIGHT]:
    bloco.player_direita(1)
  if teclas[pygame.K_c]:
    bloco.gravity = 0.1
  else:
    bloco.gravity = 0.2

  surface_texto = font.render(f' clock{clock} ', True, 'black')  #texto para me ajudar a entender o que esta dando de errado quando as coisas dão errado
  display.blit(surface_texto, (0, 0))



  ### precisa pra funcionar/ coisas novas ###

  bloco.update()
  todos_sprites.draw(display)
  scale = pygame.transform.scale(display, WINDOW_SIZE) # cola a minha tela "real" com o novo tamanho de tela
  screen.blit(scale, (0, 0))
  
  pygame.display.flip() # Desenha o quadro atual na tela

  clock.tick(60)  # Pausa e indica a taxa de quadros por segundo (FPS)

pygame.quit()