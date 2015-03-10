import pygame,math,classes,process
from random import *
total_score=0
class Baseclass(pygame.sprite.Sprite):
    allsprite=pygame.sprite.Group()
    def __init__(self,x,y,width,height,image_string):
        pygame.sprite.Sprite.__init__(self)
        Baseclass.allsprite.add(self)
        self.image=pygame.image.load(image_string)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.width=width
        self.height=height
    def destroy(self,ClassName):
    	ClassName.List.remove(self)
    	Baseclass.allsprite.remove(self)
    	del self
class Hero_space(Baseclass):
    List=pygame.sprite.Group()
    going_right=True
    def __init__(self,x,y,width,height,image_string):
        Baseclass.__init__(self,x,y,width,height,image_string)
        Hero_space.List.add(self)
        self.velx,self.vely=0,5
        self.jumping,self.go_down=False,False
    def motion(self,SCREENWIDTH,SCREENHEIGHT):
        predicted_loc=self.rect.x+self.velx
        if predicted_loc<0:
            self.velx=0
        elif predicted_loc + self.width > SCREENWIDTH:
            self.velx=0
        self.rect.x+=self.velx
        self.__jump(SCREENHEIGHT)
    def __jump(self,SCREENHEIGHT):	
        max_jump=75
        if self.jumping:
            if self.rect.y<max_jump:
                self.go_down=True
            if self.go_down:
                self.rect.y+=self.vely
                predicted_loc=self.rect.y+self.vely
                if predicted_loc+self.height>=SCREENHEIGHT:
                    self.jumping=False
                    self.go_down=False
                else:
                    self.rect.y-=self.vely
    def destroy(self,ClassName):
        ClassName.List.remove(self)
        Baseclass.allsprite.remove(self)
        del self
class Enemy_space(Baseclass):
    List=pygame.sprite.Group()
    
    def __init__(self,x,y,width,height,image_string):
        Baseclass.__init__(self,x,y,width,height,image_string)
        Enemy_space.List.add(self)
        self.velx=randint(5,12)
        self.health=10
        self.half_health=self.health/2.0
        self.amplitude,self.period=randint(20,140),randint(5,6)/100.0
    @staticmethod
    def update_all(SCREENWIDTH):
    	for ob in Enemy_space.List:
            ob.fly(SCREENWIDTH)
            if ob.health <=0:
                #increments(total_score)
                global total_score
                total_score+=5
                



                ob.destroy(Enemy_space)
    #def increments(total_score):
        #global total_score
        #total_score+=5
        #return total_score
                
#update calls the update for every sprite in the list i.e one method calls the other method
    def fly(self,SCREENWIDTH):
        if self.rect.x+self.width>SCREENWIDTH or self.rect.x<0:
            self.image=pygame.transform.flip(self.image,True,False)
            self.velx=-self.velx
        self.rect.x+=self.velx
        #a*sin(bx+c) +y
        #a=amplitude
        #B=period
        #x=x position
        #c=shift
        self.rect.y=self.amplitude*math.sin(self.period*self.rect.x)+140
    #@staticmethod
    #def movement(SCREENWIDTH):
     #   for spaceships in Enemy_space.List:
      #      spaceships.fly(SCREENWIDTH)

class Pro(pygame.sprite.Sprite):
    List=pygame.sprite.Group()
    normal_list=[]
    def destroy(self,ClassName):
        ClassName.List.remove(self)
        Baseclass.allsprite.remove(self)
        del self
    def __init__(self,x,y,width,height,image_string):
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load(image_string)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.width=width
        self.height=height

        #try:
        #last_element=Pro.normal_list[-1]
        #difference=abs(self.rect.x-last_element.rect.x)
        try:
            last_element=Pro.normal_list[-1]
            difference=abs(self.rect.y-last_element.rect.y)
            if difference < self.height:
                return

        
        except Exception:
            pass
        Pro.normal_list.append(self)
        Pro.List.add(self)
        
        #except Exception:
        #	pass
        self.velx=None
    @staticmethod
    def movement():
        for projectile in Pro.List:
            projectile.rect.y-=projectile.velx























