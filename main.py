import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fajna Gra")

#debug text
# test
def debug(info, x = 10 , y = 10):
    display_surface = pygame.display.get_surface()
    debug_surf = pygame.font.Font(None, 30).render(str(info), True, 'Black')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    display_surface.blit(debug_surf,debug_rect)

#set framerate
clock = pygame.time.Clock()
FPS = 60
#define gameworld variables
gravity = 0.5
#player action variables:
Player_move_left = False
Player_move_right = False
shoot = False

# load images
# obraz pocisku
fireball_img = pygame.image.load('fireball.png').convert_alpha()

#define colours
BG = (180,205,240)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, (100, 100, 0), (0, 300), (SCREEN_WIDTH, 300))


class Character(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale, speed, ammo):
        self.jump_counter = 0
        self.image = image
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.vel_jump = 0
        self.flip = False
        self.ammo = ammo            # amunicja
        self.start_ammo = ammo      # startowa amunicja
        self.reload = False
        self.shoot_cooldown = 0     # cooldown po strzale
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image,(image.get_width() * scale, image.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def move(self, moving_left, moving_right):
        #reset variables
        dx = 0
        dy = 0
        #assign variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True:
            if self.jump_counter < 2:
                self.vel_jump = -11
                self.jump_counter += 1
            self.jump = False

        #apply gravity
        self.vel_jump += gravity
        if self.vel_jump > 10:
            self.vel_jump = 10
        dy += self.vel_jump

        #check for collision
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.vel_jump = 0
            self.jump_counter = 0



        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

# metoda do strzelania
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            fireball = Fireball(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, self.flip)
            fireball_group.add(fireball)
            # zmniejszenie ammo o 1
            self.ammo -= 1
        # cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.reload:
            self.ammo = 25

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Doadałem cala klase do maina, bo i tak dużo zmian musialem wprowadzic w oryginalnym kodzie gry

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, flip):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = fireball_img
        self.direction = direction
        self.flip = flip
        self.scale = 0.05
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)



    def update(self):
        # ruch pocisku
        self.rect.x += (self.direction * self.speed)
        # sprawdzanie czy pocisk wyszedl poza ekran
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


        """
        # sprawdzenie kolizji z obiektami
        # do zrobienia na pozniej

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()
        """

# Bardzo dobrze idzie nam pisanie tej gry XD

player = Character('mariusz.jpg',200, 200, 0.05, 3, 25)
enemy = Character('rocky.jpg', 400, 200, 0.15, 2, 25)

fireball_group = pygame.sprite.Group()

run = True
while run:


    clock.tick(FPS)
    draw_bg()
    player.draw()
    player.move(Player_move_left, Player_move_right)
    enemy.draw()
    debug(pygame.mouse.get_pos())

    # potrzebne do strzelania
    fireball_group.update()
    fireball_group.draw(screen)

    # strzelanie:
    if shoot:
        player.shoot()

    #Event Handler
    for event in pygame.event.get():

        #quit game
        if event.type == pygame.QUIT:
            run = False

        #keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                Player_move_left = True
            if event.key == pygame.K_d:
                Player_move_right = True
            if event.key == pygame.K_w:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
            # strzelanie
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_r:
                player.reload = True


        #keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                Player_move_left = False
            if event.key == pygame.K_d:
                Player_move_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()


pygame.quit()
