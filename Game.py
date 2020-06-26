import pygame, sys, Actors
from pygame.locals import *

class StateMachine:
    
    def __init__(self):
        self.end = False
        self.next = None
        self.quit = False
        self.previous = None

class Textos:
    
    white = (255,255,255)
    black = (0,0,0) 
    
    def __init__(self):
        pygame.init()          
        self.basic_font = pygame.font.SysFont('arcade',40)     
        self.small_font = pygame.font.Font('freesansbold.ttf',20)  

    def menu_txt(self,displaysurf,game_name):
        logoSurf = self.basic_font.render(game_name,True,self.white)
        enterSurf = self.basic_font.render('Press ENTER',True,self.white)
        #scoreSurf = self.basic_font.render('Press SPACE for MAX SCORES',True,self.white)
        logoRect = logoSurf.get_rect()
        enterRect = enterSurf.get_rect()
        #scoreRect = scoreSurf.get_rect()
        logoRect.center = (400,250)
        enterRect.center = (400,300)   
        #scoreRect.center = (400,400)      
        displaysurf.blit(logoSurf,logoRect)
        displaysurf.blit(enterSurf,enterRect)
        #displaysurf.blit(scoreSurf,scoreRect)

class MainMenu(StateMachine):
    
    pink = (231,84,128)

    def __init__(self):
        StateMachine.__init__(self)
    
    def startup(self):
        pass

    def cleanup(self):
        pass

    def handle_events(self,event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN or event.key == K_KP_ENTER:
                self.next = 'fase1'
                self.end = True

    def update(self,displaysurf):
        t = Textos()

        displaysurf.fill(self.pink)
        t.menu_txt(displaysurf,'Faeries Racing') 

class MainGame(StateMachine):
    
    background = None
    game_over = False  
    pink = (231,84,128)
    white = (255,255,255)

    jogador1 = None
    jogador2 = None

    rastro1 = []
    rastro2 = []

    tamanho_rastro1 = 0
    tamanho_rastro2 = 0

    jogador1_flag = False
    jogador2_flag = False

    def __init__(self,**game_images):
        StateMachine.__init__(self)
        Textos.__init__(self)
        self.__dict__.update(game_images)

    def startup(self):      
        pass

    def cleanup(self):
        pass

    def handle_events(self,event):
        jogador1 = self.jogador1
        jogador2 = self.jogador2

        if event.type == KEYDOWN:
            if self.game_over:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    self.next = 'menu'                   
                    self.end = True          
            else:      
                if self.jogador1_flag and (event.key == K_a and not jogador1.dead):
                    jogador1.mover_x = -25
                    jogador1.mover_y = 0                                     
                elif event.key == K_d and not jogador1.dead:
                    jogador1.mover_x = 25
                    jogador1.mover_y = 0   
                    self.jogador1_flag = True   
                elif event.key == K_w and not jogador1.dead:
                    jogador1.mover_y = -25
                    jogador1.mover_x = 0
                    self.jogador1_flag = True
                elif event.key == K_s and not jogador1.dead:
                    jogador1.mover_y = 25
                    jogador1.mover_x = 0
                    self.jogador1_flag = True
                elif event.key == K_LEFT and not jogador2.dead:
                    jogador2.mover_x = -25
                    jogador2.mover_y = 0    
                    self.jogador2_flag = True
                elif self.jogador2_flag and (event.key == K_RIGHT and not jogador2.dead):
                    jogador2.mover_x = 25
                    jogador2.mover_y = 0 
                elif event.key == K_UP and not jogador2.dead:
                    jogador2.mover_y = -25
                    jogador2.mover_x = 0
                    self.jogador2_flag = True
                elif event.key == K_DOWN and not jogador2.dead:
                    jogador2.mover_y = 25
                    jogador2.mover_x = 0
                    self.jogador2_flag = True

    def actors_update(self):
        jogador1 = self.jogador1
        jogador2 = self.jogador2
        rastro1 = self.rastro1
        rastro2 = self.rastro2

        x_jogador1 = jogador1.x
        y_jogador1 = jogador1.y      
        x_jogador2 = jogador2.x
        y_jogador2 = jogador2.y  

        jogador1.movimento() 
        jogador2.movimento()

        if self.jogador1_flag and not jogador1.dead:          
            rastro1.append(Actors.Track(x_jogador1,y_jogador1,self.rastro1_image))
            self.tamanho_rastro1 = self.tamanho_rastro1 + 1   

        if self.jogador2_flag and not jogador2.dead:          
            rastro2.append(Actors.Track(x_jogador2,y_jogador2,self.rastro2_image))
            self.tamanho_rastro2 = self.tamanho_rastro2 + 1  
        
        if self.tamanho_rastro1 > 1:
            for i in range(self.tamanho_rastro1):
                if jogador1.teste_colisao(rastro1[i]):
                    jogador1.mover_x = 0
                    jogador1.mover_y = 0
                    jogador1.dead = True
                if jogador2.teste_colisao(rastro1[i]):
                    jogador2.mover_x = 0
                    jogador2.mover_y = 0
                    jogador2.dead = True

        if self.tamanho_rastro2 > 1:
            for i in range(self.tamanho_rastro2):
                if jogador2.teste_colisao(rastro2[i]):
                    jogador2.mover_x = 0
                    jogador2.mover_y = 0
                    jogador2.dead = True
                if jogador1.teste_colisao(rastro2[i]):
                    jogador1.mover_x = 0
                    jogador1.mover_y = 0
                    jogador1.dead = True

    def actors_draw(self,displaysurf):
        jogador1 = self.jogador1
        jogador2 = self.jogador2

        jogador1.desenhar(displaysurf)
        jogador2.desenhar(displaysurf)

        for i in range(self.tamanho_rastro1):
            self.rastro1[i].desenhar(displaysurf)

        for i in range(self.tamanho_rastro2):
            self.rastro2[i].desenhar(displaysurf)

    def update(self,displaysurf):  
        pass 

class FaseI(MainGame):
    
    def __init__(self,**game_images):
        super().__init__(**game_images)
    
    def startup(self):
        self.jogador1 = Actors.Fairy(25,300,self.jogador1_image)
        self.jogador2 = Actors.Fairy(750,300,self.jogador2_image)

    def update(self,displaysurf):
        displaysurf.fill(self.white)
        self.actors_update()
        self.actors_draw(displaysurf) 

class FaeriesRacingGame:

    state_dictionary = None
    state_name = None
    state = None

    def __init__(self,**settings):      
        self.__dict__.update(settings)
        self.end = False  
        pygame.display.set_caption("Faeries Racing")   
        self.displaysurf = pygame.display.set_mode(self.size)
        self.fpsclock = pygame.time.Clock()            

    def setup_states(self,state_dictionary,start_state):
        self.state_dictionary = state_dictionary
        self.state_name = start_state
        self.state = self.state_dictionary[self.state_name]
        self.state.startup()

    def flip_state(self):
        self.state.end = False
        previous,self.state_name = self.state_name,self.state.next
        self.state.cleanup()
        self.state = self.state_dictionary[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def update(self):
        if self.state.quit:
            self.end = True
        elif self.state.end:
            self.flip_state()

        self.state.update(self.displaysurf)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.end = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.end = True
            self.state.handle_events(event)

    def loop(self):
        while not self.end:
            self.event_loop()
            self.update()
            pygame.display.flip()
            pygame.display.update()
            self.fpsclock.tick(self.fps)

def main():

    settings = {
        'size' : (800,650),
        'fps' : 10           
    }

    game_images = {
        'jogador1_image' : "assets/waterfairy.png",
        'rastro1_image' : "assets/waterfairy1.png",
        'jogador2_image' : "assets/leaffairy.png",
        'rastro2_image' : "assets/leaffairy1.png",
    }

    dicionario_estados = {
        'menu' : MainMenu(),
        'fase1': FaseI(**game_images),
    }

    main_game = FaeriesRacingGame(**settings)
    main_game.setup_states(dicionario_estados,'menu')
    main_game.loop()

## MAIN ##
if __name__ == '__main__':
    main()

