import pygame, pyautogui, time, random

w,h=pyautogui.size()
pygame.init()

background=pygame.transform.scale(pygame.image.load("nightsky.jpg"),(w,h))
ground=pygame.transform.scale(pygame.image.load("stonewall.png"),(w*1.5,h//4))
# wizard=pygame.transform.scale(pygame.image.load("wizard1.png"),(300,300))

run=True
scrollground=0
screen=pygame.display.set_mode((w,h))

clock=pygame.time.Clock()
rockfrequency=2500
lastrock=pygame.time.get_ticks()-rockfrequency

class Rock(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("rock.png")
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

class Wizard(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for i in range(2):
            img=pygame.image.load(f"wizard{i+1}.png")
            img=pygame.transform.scale(img,(100,100))
            self.images.append(img)

        self.image=self.images[0]
        self.rect=self.image.get_rect()
        self.rect.center=x,y
        self.velocity=0
        
    def update(self):
        self.velocity+=1
        if self.velocity>8:
            self.velocity=8
        if pygame.mouse.get_pressed()[0]:
            self.velocity=-10
        self.rect.y+=self.velocity            
        self.counter+=1
        if self.counter==10:
            
            self.index+=1
            if self.index>1:
                self.index=0
            self.image=self.images[self.index]
            self.counter=0
        
wizardgroup=pygame.sprite.Group()
rockgroup=pygame.sprite.Group()
Gandalf=Wizard(100,h/2)
wizardgroup.add(Gandalf)

while run:
    screen.blit(background,(0,0))
    # screen.blit(ground,(scrollground,h-h//4))
    scrollground-=10
    wizardgroup.draw(screen)
    wizardgroup.update()
    rockgroup.draw(screen)
    rockgroup.update()
    if scrollground<-h//2:
        scrollground=0
    currenttime=pygame.time.get_ticks()
    print(currenttime)
    if currenttime-lastrock>rockfrequency:
        rockheight=random.randint(-100,100)
        toprock=Rock(w,h/2+rockheight,"top")
        bottomrock=Rock(w,h/2+rockheight,"bottom")
        rockgroup.add(toprock)
        rockgroup.add(bottomrock)
        lastrock=currenttime
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
        
    pygame.display.update()