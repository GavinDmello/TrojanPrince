import pygame,sys,classes,random,Main
pygame.init()
pause=0
SCREENWIDTH=800
SCREENHEIGHT=600
#screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT),0 ,32)
def end_game(total):
    if total<30:
        
        screen.fill((0,0,0))
        myfont=pygame.font.SysFont("monospace",15)
        lable=myfont.render("Score: "+str(total)+"You lose, Try harder the next :)",1,(255,255,0))
        screen.blit(lable,(200,200))
        pygame.display.flip()
        pygame.time.delay(3000)

        pygame.quit()
        sys.exit(0)


    else:
        screen.fill((0,0,0))
        myfont=pygame.font.SysFont("monospace",15)
        lable=myfont.render("Your score:"+str(total)+" You win, Good stuff :)",1,(255,255,0))
        screen.blit(lable,(200,200))
        pygame.display.flip()
        pygame.time.delay(3000)

        pygame.quit()
        sys.exit(0)

def process(bug,FPS,total_frames):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        classes.Hero_space.going_right=True
        bug.image=pygame.image.load('images/hero_space.png').convert_alpha()
        bug.velx=-10
        
        
        
    elif keys[pygame.K_RIGHT]:
        classes.Hero_space.going_right=True
        bug.image=pygame.image.load('images/hero_space.png').convert_alpha()
        bug.velx=+10
        
    elif keys[pygame.K_w]:
    	bug.jumping=True


    else:
        bug.velx=0
    if keys[pygame.K_SPACE]:
        
        p=classes.Pro(bug.rect.x,bug.rect.y,41,31,"images/projectiles/bullet1.png")
        pygame.mixer.music.play(0)
        if classes.Hero_space.going_right:
            p.velx=8
            
        else :
            p.image=pygame.transform.flip(p.image,True,False)
            p.velx=-8
            
    spawn(FPS,total_frames)
    collisions()
def process1(bug,FPS,total_frames):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        classes.Hero_space.going_right=True
        bug.image=pygame.image.load('images/newhero.png').convert_alpha()
        bug.velx=-5
        
    elif keys[pygame.K_RIGHT]:
        classes.Hero_space.going_right=True
        bug.image=pygame.image.load('images/newhero.png').convert_alpha()
        bug.velx=+5
    elif keys[pygame.K_w]:
        bug.jumping=True

    else:
        bug.velx=0
    if keys[pygame.K_SPACE]:
        
        p=classes.Pro(bug.rect.x,bug.rect.y,41,31,"images/projectiles/bullet1.png")
        pygame.mixer.music.play(0)
        if classes.Hero_space.going_right:
            p.velx=8
        else :
            p.image=pygame.transform.flip(p.image,True,False)
            p.velx=-8
    spawn(FPS,total_frames)
    collisions()

def spawn(FPS,total_frames):
	four_seconds=FPS*2
	if total_frames %four_seconds ==0:
		r=random.randint(1,2)
		x=1

		if r==2:
			x=640-100
		fly=classes.Enemy_space(x,100,100,100,"images/enemy_space.png")
def collisions():
	#pygame.sprite.spritecollide(object,group,dokill)
	for ob in classes.Enemy_space.List:
		col=pygame.sprite.spritecollide(ob,classes.Pro.List,True)
		if len(col)>0:
			for hit in col:
				ob.health-=ob.half_health

