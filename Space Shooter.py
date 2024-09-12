import pygame
import os
pygame.font.init()
pygame.mixer.init()



WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH,HEIGHT)) # setting main surface
pygame.display.set_caption("Space Shooter") # Üstte yazacak metin

WHITE = (255,255,255)
BLACK = (0,0,0)

BORDER = pygame.Rect(WIDTH/2-5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets','Gun+Silencer.mp3'))

HEALT_FONT =pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

FPS = 120 # on different computers our game is running at a different speed because its based on how quickly the while loop below is running
VEL= 2
BULLET_VEL = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 80,40

PURPLE_HIT = pygame.USEREVENT +1
GRAY_HIT = pygame.USEREVENT +2

GRAY_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets','gray','Ship3.png'))
GRAY_SPACESHIP = pygame.transform.flip(pygame.transform.scale(GRAY_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),0,0)

PURPLE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets','purple','Ship2.png'))
PURPLE_SPACESHIP = pygame.transform.flip(pygame.transform.scale(PURPLE_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),0,0)


PURPLE_BULLET_IMAGE = pygame.image.load(os.path.join('assets','03.png'))

GRAY_BULLET_IMAGE =pygame.image.load(os.path.join('assets','02.png'))
GRAY_BULLET = pygame.transform.flip(GRAY_BULLET_IMAGE,180,0)

SPACE =pygame.image.load(os.path.join('assets','background.png'))

def draw_window(purple,gray,purple_bullets,gray_bullets,gray_health,purple_health):
    WIN.blit(SPACE,(0,0))  # filling screen with specific RGB color
    pygame.draw.rect(WIN,BLACK,BORDER)

    gray_health_text = HEALT_FONT.render("Health: "+str(gray_health),1, WHITE)
    purple_health_text = HEALT_FONT.render("Health: " + str(purple_health), 1, WHITE)
    WIN.blit(gray_health_text,(WIDTH - gray_health_text.get_width()-10,10))
    WIN.blit(purple_health_text, (10, 10))

    WIN.blit(PURPLE_SPACESHIP,(purple.x,purple.y)) # use it when you want to draw surface on to the screen (top left corner is the 0,0 point)
    WIN.blit(GRAY_SPACESHIP, (gray.x,gray.y))



    for bullet in gray_bullets:
        WIN.blit(PURPLE_BULLET_IMAGE,bullet)



    for bullet in purple_bullets:
        WIN.blit(GRAY_BULLET,bullet)



    pygame.display.update()  # update display after drawing something on to screen


def purple_handle_movement(key_pressed,purple):
    if key_pressed[pygame.K_a] and purple.x - VEL > 0:  # LEFT
        purple.x -= VEL

    if key_pressed[pygame.K_d] and purple.x + VEL + purple.width  < BORDER.x:  # RIGHT
        purple.x += VEL

    if key_pressed[pygame.K_w] and purple.y - VEL  > 0:  # UP
        purple.y -= VEL

    if key_pressed[pygame.K_s] and purple.y + VEL +purple.height < HEIGHT:  # DOWN
        purple.y += VEL

def gray_handle_movement(key_pressed,gray):
    if key_pressed[pygame.K_LEFT] and gray.x - VEL > BORDER.x +BORDER.width:  # LEFT
        gray.x -= VEL

    if key_pressed[pygame.K_RIGHT] and gray.x + VEL + gray.width  < WIDTH:  # RIGHT
        gray.x += VEL

    if key_pressed[pygame.K_UP] and gray.y - VEL > 0:  # UP
        gray.y -= VEL

    if key_pressed[pygame.K_DOWN] and gray.y + VEL +gray.height < HEIGHT:  # DOWN
        gray.y += VEL



def handle_bullets(purple_bullets,gray_bullets,purple,gray):
    for bullet in purple_bullets:
        bullet.x += BULLET_VEL
        if gray.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GRAY_HIT))

            purple_bullets.remove(bullet)
        if bullet.x > WIDTH:
            purple_bullets.remove(bullet)


    for bullet in gray_bullets:
        bullet.x -= BULLET_VEL
        if purple.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PURPLE_HIT))

            gray_bullets.remove(bullet)
        if bullet.x <0:
            gray_bullets.remove(bullet)



def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,HEIGHT/2- draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    purple = pygame.Rect(65,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    gray = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    purple_bullets = []
    gray_bullets = []

    gray_health = 10
    purple_health = 10

    clock = pygame.time.Clock() # while loop will run 120 times per second
    run = True
    while run:
        clock.tick(FPS) # it controls the speed of this while loop
        for event in pygame.event.get(): # list of events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(purple_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(purple.x + purple.width, purple.y+purple.height//2-13,38,26)
                    purple_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()




                if event.key == pygame.K_KP_ENTER and len(gray_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(gray.x-25,gray.y+ gray.height // 2 - 15, 38, 26)
                    gray_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == GRAY_HIT:
                gray_health -=1
                BULLET_HIT_SOUND.play()

            if event.type == PURPLE_HIT:
                purple_health -=1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if gray_health <= 0:
            winner_text = "Purple Wins"

        if purple_health <= 0:
            winner_text = "Gray Wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        print(purple_bullets,gray_bullets)
        key_pressed = pygame.key.get_pressed()

        purple_handle_movement(key_pressed,purple)
        gray_handle_movement(key_pressed,gray)


        handle_bullets(purple_bullets,gray_bullets,purple,gray)


        draw_window(purple,gray,gray_bullets,purple_bullets,gray_health,purple_health)


    main()


"""
dosyayı başka bir dosyaya modül olarak import ettiğimizde buradaki kodlar çalışacağı için
sadece dosyayı direkt olarak açtığımızda çalışmasını sağlıyoruz
"""
if __name__ == "__main__": # "__main__" ana dosyayı çalıştırdık anlamına gelir
    main()                 # __name__ ise dosya adı