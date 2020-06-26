import pygame

class BaseActor(pygame.sprite.Sprite):

    def __init__(self,x,y,image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y       

    def desenhar(self,screen):
        screen.blit(self.image,(self.x,self.y))

    def teste_colisao(self,sprite):
        if(self.image!=0):
            return self.rect.colliderect(sprite.rect) 
    
class Fairy(BaseActor):
    
    def __init__(self,x,y,image):
        super().__init__(x,y,image)
        self.mover_x = 0   
        self.mover_y = 0
        self.dead = False

    def movimento(self):
        self.x += self.mover_x
        self.y += self.mover_y

        self.rect.x = self.x
        self.rect.y = self.y 

        if self.x <= 0:
            self.x = 0
            self.mover_x = 0
            self.dead = True
        elif self.x + 25 >= 800:
            self.x = 775
            self.mover_x = 0
            self.dead = True

        if self.y <= 0:
            self.y = 0
            self.mover_y = 0
            self.dead = True
        elif self.y + 25 >= 650:
            self.y = 625
            self.mover_y = 0
            self.dead = True

        self.rect.x = self.x
        self.rect.y = self.y    

class Track(BaseActor):
    
     def __init__(self,x,y,image):
        super().__init__(x,y,image)
        