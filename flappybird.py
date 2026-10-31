import pygame, pyautogui, time, random

w,h=pyautogui.size()
pygame.init()

background=pygame.transform.scale(pygame.image.load("bg.png"),(w,h))
ground=pygame.transform.scale(pygame.image.load("ground.png"),(w*1.5,h//4))

clock=pygame.time.Clock()
pipefrequency=1500
lastpipe=pygame.time.get_ticks()-pipefrequency

run=True
scrollground=0
screen=pygame.display.set_mode((w,h))
gamestate='start'
score=0


class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pipe.png")
        self.rect=self.image.get_rect()
        if position=="top":
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=x,y-100
        if position=="bottom":
            self.rect.topleft=x,y+100
    def update(self):
        self.rect.x-=10
        if self.rect.right<0:
            self.kill()
            
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for i in range(3):
            img=pygame.image.load(f"bird{i+1}.png")
            self.images.append(img)

        self.image=self.images[0]
        self.rect=self.image.get_rect()
        self.rect.center=x,y
        self.velocity=0
        
    def update(self):
        global gamestate
        if gamestate=="play":
            self.velocity+=1
            if self.velocity>8:
                self.velocity=8
            if pygame.mouse.get_pressed()[0] and gamestate=="play":
                self.velocity=-10
            self.rect.y+=self.velocity            
            self.counter+=1
            if self.counter==10:
                self.index+=1
                if self.index>2:
                    self.index=0
                self.counter=0
            self.image=self.images[self.index]
            self.image=pygame.transform.rotate(self.image,self.velocity*(-2))
        elif gamestate=="end":
            self.image=pygame.transform.rotate(self.image,-90)
            gamestate="stopfornow"
birdgroup=pygame.sprite.Group()
pipegroup=pygame.sprite.Group()
flappy=Bird(100,h/2)
birdgroup.add(flappy)
        
while run:
    screen.blit(background,(0,0))
    birdgroup.draw(screen)
    birdgroup.update()
    pipegroup.draw(screen)
    screen.blit(ground,(scrollground,h-h//4))
    if gamestate=="play":
        pipegroup.update()
        if pygame.sprite.groupcollide(birdgroup,pipegroup,False,False):
            gamestate="end"
        scrollground-=10
        if scrollground<-w//2:
            scrollground=0
        currenttime=pygame.time.get_ticks()
        print(currenttime)
        if flappy.rect.bottom>=h-h//4:
            gamestate="end"
        
        if currenttime-lastpipe>pipefrequency:
            pipeheight=random.randint(-100,100)
            toppipe=Pipe(w,h/2+pipeheight,"top")
            bottompipe=Pipe(w,h/2+pipeheight,"bottom")
            pipegroup.add(toppipe)
            pipegroup.add(bottompipe)
            lastpipe=currenttime
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
        if e.type==pygame.MOUSEBUTTONDOWN and gamestate!="play":
            gamestate="play"
            pipegroup.empty()
            score=0
    pygame.display.update()