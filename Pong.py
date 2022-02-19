import pygame
import os
import random

#Change directory
os.chdir(os.path.dirname(__file__))

#Initilaze
pygame.font.init()
#pygame.mixer.init()

#Screen settings
WIDTH, HEIGTH = (900, 600)
SCORE_SCREEN_WIDTH, SCORE_SCREEN_HEIGTH = (900, 100)
FIELD_SCREEN_WIDTH, FIELD_SCREEN_HEIGTH = (900, 500)
screen = pygame.display.set_mode((WIDTH, HEIGTH))
score_screen = pygame.Surface((SCORE_SCREEN_WIDTH, SCORE_SCREEN_HEIGTH))
field_screen = pygame.Surface((FIELD_SCREEN_WIDTH, FIELD_SCREEN_HEIGTH))
pygame.display.set_caption("Pong")
#icon = pygame.image.load('ship.png')
#pygame.display.set_icon(icon)

#Fonts
font = pygame.font.SysFont('forte',24)

#Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (230,230,230)
 
#Music and Sounds
#mixer.music.load('background.wav')
#pygame.mixer.music.set_volume(0.3)
#mixer.music.play(-1,fade_ms=5000)

class Player():
    size = (10, 60)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surface = pygame.Surface(Player.size)
        self.rect = self.surface.get_rect(topleft = (x,y))
        self.score = 0

    def move(self, factor):
        Y_CHANGE = 4
        self.y += Y_CHANGE * factor
        if self.y < 5:
            self.y = 5
        elif self.y > FIELD_SCREEN_HEIGTH-self.size[1]-5:
            self.y = FIELD_SCREEN_HEIGTH-self.size[1]-5
        self.rect.update((self.x,self.y),(Player.size))

class Ball():
    size = (10, 10)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surface = pygame.Surface(Ball.size)
        self.rect = self.surface.get_rect(topleft = (x,y))
        self.x_change = random.choice([-1,1])*1
        self.y_change = random.uniform(-3,3)*1
        
    def move(self, player1, player2):
        collision = self.collision(player1, player2)
        if collision:
            self.x_change *= -1.2
            self.y_change +=  random.uniform(-1,1)
        self.x += self.x_change
        
        if self.y + self.y_change < 0:
            self.y -= abs(self.y_change) - self.y
            self.y_change *= -1
        elif self.y + self.y_change > FIELD_SCREEN_HEIGTH - self.size[1]:           
            self.y -=  FIELD_SCREEN_HEIGTH-self.size[1] - self.y_change - self.y
            self.y_change *= -1
        else:
            self.y += self.y_change
            
        self.rect.update((self.x,self.y),(Ball.size))
        
    
    def collision(self, player1, player2):
        if self.rect.colliderect(player1.rect) or self.rect.colliderect(player2.rect):
            return True
        return False
    
    def respawn(self):
        self.x = field_screen.get_rect().center[0]
        self.y = field_screen.get_rect().center[1]
        self.x_change = random.choice([-1,1])*1
        self.y_change = random.uniform(-3,3)*1
        self.rect.update(field_screen.get_rect().center, (Player.size))
    
    def score(self, player1, player2):
        if self.rect.right <= 0:
            player2.score += 1
            goal_text = "Player 2 scored!"
        elif self.rect.left >= FIELD_SCREEN_WIDTH:
            player1.score += 1
            goal_text = "Player 1 scored!"
        
        if self.rect.right <= 0 or self.rect.left >= FIELD_SCREEN_WIDTH:
            if player1.score >= 5:
                win_text = "Player 1 wins!"
            elif player2.score >= 5:
                win_text = "Player 2 wins!"
                
            if player1.score >= 5 or player2.score >= 5:
                win_font = font.render(win_text, True, BLACK)
                screen.blit(win_font, (score_screen.get_rect().center[0]-win_font.get_width()/2, score_screen.get_rect().bottom-win_font.get_height()-10))
                pygame.display.update()
                pygame.time.delay(2000)
                return True
                
            else:
                goal_font = font.render(goal_text, True, BLACK)
                screen.blit(goal_font, (score_screen.get_rect().center[0]-goal_font.get_width()/2, score_screen.get_rect().bottom-goal_font.get_height()-10))
                pygame.display.update()
                pygame.time.delay(2000)
                self.respawn()
        return False   

def show_score(player1_score, player2_score):
    score1 = font.render("Player 1: "+str(player1_score), True, (0,0,0))
    score2 = font.render("Player 2: "+str(player2_score), True, (0,0,0))
    score_screen.blit(score1, (SCORE_SCREEN_WIDTH//4 - score1.get_width()//2, 30))
    score_screen.blit(score2, (3*SCORE_SCREEN_WIDTH//4 - score2.get_width()//2, 30))
    
def draw_center_line():
    for i in range(10, FIELD_SCREEN_HEIGTH, FIELD_SCREEN_HEIGTH//10):
        pygame.draw.rect(field_screen, WHITE, (FIELD_SCREEN_WIDTH//2 - 5, i, 10, FIELD_SCREEN_HEIGTH//20 ))

def draw_objects(player1, player2, ball):   
    screen.fill(GREY)
    score_screen.fill(WHITE)
    field_screen.fill(BLACK)
    
    show_score(player1.score, player2.score)
    draw_center_line()
    
    player1.surface.fill(WHITE)
    player2.surface.fill(WHITE)
    field_screen.blit(player1.surface, (player1.x, player1.y))
    field_screen.blit(player2.surface, (player2.x, player2.y))
    
    ball.surface.fill(WHITE)
    field_screen.blit(ball.surface, (ball.x, ball.y))
    
    screen.blit(score_screen, (0, 0))
    screen.blit(field_screen, (0, SCORE_SCREEN_HEIGTH))
    pygame.display.update()
    
def play_pong():
    player1 = Player(5, int(FIELD_SCREEN_HEIGTH/2-Player.size[1]/2))
    player2 = Player(FIELD_SCREEN_WIDTH-Player.size[0]-5, int(FIELD_SCREEN_HEIGTH/2-Player.size[1]/2))
    ball = Ball(*field_screen.get_rect().center)
    #set Clock
    FPS = 60
    clock = pygame.time.Clock()
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1.move(-1)
        if keys[pygame.K_s]:
            player1.move(1)
        if keys[pygame.K_UP]:
            player2.move(-1)
        if keys[pygame.K_DOWN]:
            player2.move(1)
        
        ball.move(player1, player2)
        draw_objects(player1, player2, ball)
        game_over = ball.score(player1, player2)
        
        if game_over:
            running = False 



if __name__ == "__main__":
    play_pong()
