import pygame as pg
from random import randint
import time
pg.init()
window = pg.display.set_mode((800,600))
pg.display.set_caption("Shooter")
miss_enemy=0
score=0
gameover = 'image/victory.png'
level = 1
count_animation = 0
class GameSprite():
    def __init__(self,img,x,y,width,height,speed):
        self.image=pg.transform.scale(pg.image.load(img),(width,height))
        self.width=width
        self.height=height
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed=speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def control(self):
        keys = pg.key.get_pressed()
        if keys [pg.K_LEFT] and self.rect.x>0:
            self.rect.x-=self.speed
        if keys [pg.K_RIGHT] and self.rect.x<700:
            self.rect.x+=self.speed
class Enemy(GameSprite):
    def enemyspawn(self):
        self.rect.y=0
        self.rect.x=randint(0,700)
    def move(self):
        global miss_enemy
        if self.rect.y<600:
            self.rect.y+=self.speed
        else:
            miss_enemy+=1
            self.enemyspawn()
    def dead(self):
        global bullets, score
        for i in bullets:
            if pg.sprite.collide_rect(self,i):
                score+=1
                self.enemyspawn()
                bullets.remove(i)
class Boss(GameSprite):
    def __init__(self,img,x,y,width,height,speed,health,direction):
        super().__init__(img,x,y,width,height,speed)
        self.health=health
        self.direction=direction
    def bossmove(self):
        global count_animation
        if self.direction==1:
            self.rect.x+=self.speed
        if self.direction==2:
            self.rect.x-=self.speed
        if self.rect.x>500:
            self.direction=2
        if self.rect.x<0:
            self.direction=1
        self.image=pg.transform.scale(pg.image.load(f'image/boss/{count_animation}.gif'),(self.width,self.height))
        count_animation+=1
        if count_animation>2:
            count_animation=0
    def damage(self):
        global bullets
        for i in bullets:
            if pg.sprite.collide_rect(self,i):
                bullets.remove(i)
                self.health-=1
class Bullet(GameSprite):
    def move(self):
        self.rect.y-=self.speed
background=GameSprite("image/backgr.png",0,0,800,600,0)
player=Player("image/mainship.png",400,500,100,100,8)
boss=Boss('image/boss/0.gif',250,0,300,200,5,100,1)
enemies=[]
bullets=[]
for i in range(10):
    enemies.append(Enemy("image/enemy.png",randint(0,700),0,100,100,2))
game=True
music = pg.mixer.Sound('sound/bgsound.mp3')
music.set_volume(0.01)
music.play(-1)
while game:
    pg.time.Clock().tick(60)
    for i in pg.event.get():
        if i.type==pg.QUIT:
            exit()
        if i.type==pg.MOUSEBUTTONDOWN:
            bullets.append(Bullet('image/bullet.png',player.rect.x+40,player.rect.y,20,35,15))
    if score>29:
        level+=1
        score=0
        enemies.append(Enemy("image/enemy.png",randint(0,700),0,100,100,2))
    if miss_enemy>9:
        gameover='image/lose.png'
        game=False
        music.stop()
    background.reset()
    if level>4:
        boss.bossmove()
        boss.reset()
        hp=GameSprite('image/hp.png',0,0,boss.health*8,40,0)
        hp.reset()
        boss.damage()

    player.reset()
    player.control()
    if boss.health<=0:
        gameover="image/victory.png"
        game = False
    for i in enemies:
        i.reset()
        i.move()
        i.dead()
        if pg.sprite.collide_rect(i,player):
            gameover='image/lose.png'
            game = False
            music.stop()
    for i in bullets:
        i.reset()
        i.move()
    label=pg.font.SysFont('ComicSans',25).render(f"Score:{score}",True,'white')
    window.blit(label,(20,20))
    label=pg.font.SysFont('ComicSans',25).render(f"Miss:{miss_enemy}",True,'white')
    window.blit(label,(20,50))
    label=pg.font.SysFont('ComicSans',25).render(f"Level:{level}",True,'green')
    window.blit(label,(700,20))
    pg.display.flip()
bg=GameSprite(gameover,0,0,800,600,0)
while True:
    pg.time.Clock().tick(60)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
    bg.reset()
    pg.display.flip()