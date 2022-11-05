import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fajna Gra")

#debug text
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

#define colours
BG = (180,205,240)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, (100, 100, 0), (0, 300), (SCREEN_WIDTH, 300))


class Character(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale, speed):
        self.jump_counter = 0
        self.image = image
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.vel_jump = 0
        self.flip = False
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

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),self.rect)

player = Character('mariusz.jpg',200, 200, 0.05, 3)
enemy = Character('rocky.jpg', 400, 200, 0.15, 2)



run = True
while run:


    clock.tick(FPS)
    draw_bg()
    player.draw()
    player.move(Player_move_left,Player_move_right)
    enemy.draw()
    debug(pygame.mouse.get_pos())
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

        #keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                Player_move_left = False
            if event.key == pygame.K_d:
                Player_move_right = False

    pygame.display.update()


pygame.quit()