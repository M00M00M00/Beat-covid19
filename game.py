import pygame
import random
import math
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 221)
YELLOW = (255, 228, 0)

def playagain():
    ############## set values ###############
    tick_var = 60
    player_speed = 3
    virus_num = 50
    virus_time = 1 # 새로운 바이러스가 생성되는 시간(second)
    virus_speed_var = 0.1 # 바이러스가 하나 등장할 때 마다 바이러스의 속도가 증가하는 정도 
    virus_time_var = 0.012 # 바이러스가 하나 등장할 때 마다 다음 등장까지 걸리는 시간이 줄어드는 정도
    virus_speed = 1
    bubble_speed = 5
    ##########################################

    screen_width = 1000
    screen_height = 1000
    player_width = 40
    player_height = player_width * 2
    virus_width = 40
    virus_height = 40
    bubble_width = 40
    bubble_height = 40

    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()

    start_ticks = pygame.time.get_ticks()
    virus_ticks = pygame.time.get_ticks()
    attack_ticks = pygame.time.get_ticks()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BEAT COVID-19!")
    start_background = pygame.image.load("data\\image\\start background.png")
    start_background = pygame.transform.scale(start_background,(screen_width,screen_height))
    background = pygame.image.load("data\\image\\background.png")
    background = pygame.transform.scale(background,(screen_width,screen_height))
    # background = pygame.image.load("data\\image\\background2.jpg")
    # background = pygame.transform.scale(background,(screen_width,screen_height))
    player_image = pygame.image.load("data\\image\\player.png")
    player_image = pygame.transform.scale(player_image,(player_width,player_height))
    virus_image = pygame.image.load("data\\image\\virus.png")
    virus_image = pygame.transform.scale(virus_image,(virus_width,virus_height))
    bubble_image = pygame.image.load("data\\image\\bubble.png")
    bubble_image = pygame.transform.scale(bubble_image,(bubble_width,bubble_width))
    pygame.mixer.music.load('data\\sound\\bgm.wav')
    pygame.mixer.music.play(-1)
    pop_sound = pygame.mixer.Sound('data\\sound\\pop.wav')
    fail_sound = pygame.mixer.Sound('data\\sound\\fail.wav')
    shoot_sound = pygame.mixer.Sound('data\\sound\\shoot.wav')
    success_sound = pygame.mixer.Sound('data\\sound\\success.wav')

    score = 0
    to_x = 0
    to_y = 0
    virus_start_pos = []
    for i in range(screen_height):
        virus_start_pos.append([0,i])
        virus_start_pos.append([screen_width,i])
    for i in range(screen_width):
        virus_start_pos.append([i,0])
        virus_start_pos.append([i,screen_height])
    virus_count = 0
    bubble_count = 0
    attack_available = True
    bubbles = []
    bubble_activate = []

    class Player:
        def __init__(self,x,y):
            self.x = x
            self.y = y

    class Virus:
        def __init__(self):
            xy = random.choice(virus_start_pos)
            self.x = xy[0]
            self.y = xy[1]
            self.length = math.sqrt((self.x - (player.x + player_width/2))**2 + (self.y-(player.y + player_height/2))**2)
            self.to_x = ((player.x + player_width/2) - self.x)/self.length
            self.to_y = ((player.y + player_height/2) - self.y)/self.length

    class Bubble:
        def __init__(self,x,y,to_x,to_y):
            self.x = x
            self.y = y
            self.to_x = to_x
            self.to_y = to_y

    player = Player(screen_width/2 - player_width/2, screen_height/2 - player_height/2)
    viruses = [Virus() for _ in range(virus_num)]
    virus_activate = ['noact' for _ in range(virus_num)]

    run = True


    while run:
        screen.blit(start_background,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                quit()

            elif event.type == pygame.KEYDOWN:
                run = False

        pygame.display.update()

    run = True

    while run:
        screen.blit(background,(0,0))
        t = clock.tick(tick_var)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    to_x -= player_speed
                elif event.key == pygame.K_d:
                    to_x += player_speed
                elif event.key == pygame.K_s:
                    to_y += player_speed
                elif event.key == pygame.K_w:
                    to_y -= player_speed
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    to_x = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    to_y = 0

            if attack_available:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x = pygame.mouse.get_pos()[0]
                    mouse_y = pygame.mouse.get_pos()[1]
                    player_x = player.x + player_width/2
                    player_y = player.y + player_height/2
                    length = math.sqrt((mouse_x - player_x)**2 + (mouse_y - player_y)**2)
                    bubbles.append(Bubble(player.x + player_width/2, player.y + player_height/2,(mouse_x - player_x)/length,(mouse_y - player_y)/length))
                    bubble_activate.append(True)
                    shoot_sound.play()
                    attack_available = False


        player.x += to_x
        player.y += to_y
        if player.x < 0:
            player.x = 0
        if player.x > screen_width - player_width:
            player.x = screen_width - player_width
        if player.y < 0:
            player.y = 0
        if player.y > screen_height - player_height:
            player.y = screen_height - player_height
            
        screen.blit(player_image,(player.x,player.y))
        if 'noact' in virus_activate:
            if pygame.time.get_ticks() - virus_ticks > virus_time*1000:
                virus_activate[virus_count] = 'act'
                virus_count += 1
                virus_ticks = pygame.time.get_ticks()
                virus_speed += virus_speed_var
                virus_time -= virus_time_var
        
        for i in range(len(virus_activate)):
            if virus_activate[i] == 'act':
                if abs((viruses[i].x + virus_width/2) - (player.x + player_width/2)) > 5 and abs((viruses[i].y + virus_height/2) - (player.y + player_height/2)) > 5:
                        viruses[i].x += viruses[i].to_x * virus_speed
                        viruses[i].y += viruses[i].to_y * virus_speed
                        viruses[i].length = math.sqrt((viruses[i].x - (player.x + player_width/2))**2 + (viruses[i].y-(player.y + player_height/2))**2)
                        viruses[i].to_x = ((player.x + player_width/2) - viruses[i].x)/viruses[i].length
                        viruses[i].to_y = ((player.y + player_height/2) - viruses[i].y)/viruses[i].length
                elif abs((viruses[i].x + virus_width/2) - (player.x + player_width/2)) < (virus_width + player_width)/2 and abs((viruses[i].y + virus_height/2) - (player.y + player_height/2)) < (virus_height + player_height)/2:
                    run = False
                    fail_sound.play()
                else:
                    if abs((viruses[i].x + virus_width/2) - (player.x + player_width/2)) < 5 and abs((viruses[i].y + virus_height/2) - (player.y + player_height/2)) > 5:
                        viruses[i].y += viruses[i].to_y * virus_speed
                        viruses[i].length = math.sqrt((viruses[i].x - (player.x + player_width/2))**2 + (viruses[i].y-(player.y + player_height/2))**2)
                        viruses[i].to_x = ((player.x + player_width/2) - viruses[i].x)/viruses[i].length
                        viruses[i].to_y = ((player.y + player_height/2) - viruses[i].y)/viruses[i].length
                    elif abs((viruses[i].x + virus_width/2) - (player.x + player_width/2)) > 5 and abs((viruses[i].y + virus_height/2) - (player.y + player_height/2)) < 5:
                        viruses[i].x += viruses[i].to_x * virus_speed
                        viruses[i].length = math.sqrt((viruses[i].x - (player.x + player_width/2))**2 + (viruses[i].y-(player.y + player_height/2))**2)
                        viruses[i].to_x = ((player.x + player_width/2) - viruses[i].x)/viruses[i].length
                        viruses[i].to_y = ((player.y + player_height/2) - viruses[i].y)/viruses[i].length
                screen.blit(virus_image,(viruses[i].x,viruses[i].y))

        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        if pygame.time.get_ticks() - attack_ticks > virus_time*1000*0.5:
            attack_available = True
            attack_ticks = pygame.time.get_ticks()

        for i in range(len(bubbles)):
            if bubble_activate[i]:
                bubbles[i].x += bubbles[i].to_x * bubble_speed
                bubbles[i].y += bubbles[i].to_y * bubble_speed
                screen.blit(bubble_image,(bubbles[i].x,bubbles[i].y))
                if bubbles[i].x < 0 or bubbles[i].x > screen_width - bubble_width or bubbles[i].y < 0 or bubbles[i].y > screen_height - bubble_height:
                    bubble_activate[i] = False
                
                for j in range(len(viruses)):
                    if virus_activate[j] == 'act':
                        if abs((viruses[j].x + virus_width/2) - (bubbles[i].x + bubble_width/2)) < (virus_width + bubble_width)/2 and abs((viruses[j].y + virus_height/2) - (bubbles[i].y + bubble_height/2)) < (virus_height + bubble_height)/2:
                            virus_activate[j] = 'dead'
                            bubble_activate[i] = False
                            pop_sound.play()
                            score += 1
        font = pygame.font.Font('data\\font\\godoRounded R.ttf',60)
        text = font.render(str("Score: " + str(score)),True,WHITE)
        screen.blit(text,(10,-10))
        pygame.display.update()

        gameovercheck = True

        for i in virus_activate:
            if i == 'noact':
                gameovercheck = False
            elif i == 'act':
                gameovercheck = False

        if gameovercheck:
            success_sound.play()
            run = False
        
    run = True
    while run:
        if gameovercheck:
            font = pygame.font.Font('data\\font\\godoRounded R.ttf',120)
            text = font.render(str("Mission Success"),True,RED)
            screen.blit(text,(150,390))
            font2 = pygame.font.Font('data\\font\\godoRounded R.ttf',70)
            text2 = font2.render(str("press 'enter' to retry"),True,RED)
            screen.blit(text2,(250,485))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False

        if not gameovercheck:
            font = pygame.font.Font('data\\font\\godoRounded R.ttf',170)
            text = font.render(str("Game over!"),True,RED)
            screen.blit(text,(170,350))
            font2 = pygame.font.Font('data\\font\\godoRounded R.ttf',70)
            text2 = font2.render(str("press 'enter' to retry"),True,RED)
            screen.blit(text2,(250,485))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False
    
    playagain()

if __name__ == '__main__':
    playagain()

