import sys, pygame
from pygame.draw import rect
import numpy as np
import time


class snake:
    def __init__(self,screen_size,head_color=(0,0,255),head_position=[0,0],
                body_color=(0,255,0),body_sections=[],section_size=50,snake_speed=[1,0]) -> None:
        self.head_color = head_color
        self.head_position = head_position
        self.body_color = body_color
        self.body_sections = body_sections
        self.section_size = section_size
        self.snake_speed = snake_speed
        self.screen_size = screen_size
        self.stamina_base = int(self.screen_size[0]/self.section_size)*int(self.screen_size[1]/self.section_size)
        self.stamina = self.stamina_base
        
    def draw_snake(self,screen):
        for section in self.body_sections:
            x1=section[0]*self.section_size
            y1=section[1]*self.section_size
            rect(screen,self.body_color, (x1,y1,self.section_size,self.section_size))

        x1=self.head_position[0]*self.section_size
        y1=self.head_position[1]*self.section_size
        rect(screen, self.head_color, (x1,y1,self.section_size,self.section_size))

    def update_snake_position(self):
        # if len(self.body_sections)>0:
        if self.body_sections:
            for n in range(len(self.body_sections)-1,-1,-1):
                section = self.body_sections[n]
                section_n = self.body_sections[n-1]
                section[0] = section_n[0]
                section[1] = section_n[1]


            self.body_sections[0][0] = self.head_position[0]
            self.body_sections[0][1] = self.head_position[1]

        self.head_position[0] =  self.head_position[0]+ self.snake_speed[0]
        self.head_position[1] =  self.head_position[1]+ self.snake_speed[1]
        self.stamina -=1

class snake_game:
    def __init__(self,width:int=1000,height:int=1000,blackgrond_color=(0, 0, 0),
                section_size=50,food_color=(255,0,0)) -> None:
        pygame.init()
        self.size = self.width, self.height =  width,height
        self.blackgrond_color = blackgrond_color
        self.food_color = food_color
        self.section_size = section_size
        self.screen = pygame.display.set_mode(self.size)
        self.snake=snake(self.size,section_size=self.section_size)
        self.food=[]
        self.generate_food()

    def generate_food(self):
        if len(self.snake.body_sections)+1 == int(self.width/self.section_size)*int(self.height/self.section_size):
            print("Vitoria")
            sys.exit()
        self.food = np.random.randint([int(self.width/self.section_size),int(self.height/self.section_size)],size=2).tolist()
        while self.food in self.snake.body_sections or self.food ==self.snake.head_position:
            self.food = np.random.randint([int(self.width/self.section_size),int(self.height/self.section_size)],size=2).tolist()

    def draw_food(self):
        if self.food:
            x1=self.food[0]*self.section_size
            y1=self.food[1]*self.section_size
            rect(self.screen,self.food_color, (x1,y1,self.section_size,self.section_size))

    def eat_food(self):
        if self.snake.head_position == self.food:
            self.snake.body_sections.insert(0,self.snake.head_position.copy())
            self.generate_food()
            self.snake.stamina = self.snake.stamina_base
            return True


    def end_game(self):

        if int(self.width/self.section_size)<self.snake.head_position[0] or self.snake.head_position[0]<0:
            print("derrota 1")
            sys.exit()
        if int(self.height/self.section_size)<self.snake.head_position[1] or self.snake.head_position[1]<0:
            print("derrota 2")
            sys.exit()
        if self.snake.head_position in self.snake.body_sections:
            print("derrota 3")
            sys.exit()
        if self.snake.stamina<0:
            print("derrota 4")
            sys.exit()

    def first_slice(self,key):
        if not self.snake.body_sections:
            return True
        if key == pygame.K_LEFT:
            return self.snake.head_position[0]-1 != self.snake.body_sections[0][0]
        elif key == pygame.K_RIGHT:
            return self.snake.head_position[0]+1 != self.snake.body_sections[0][0]
        elif key == pygame.K_UP:
            return self.snake.head_position[1]-1 != self.snake.body_sections[0][1]
        elif key == pygame.K_DOWN:
            return self.snake.head_position[1]+1 != self.snake.body_sections[0][1]

    def user_actions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.first_slice(pygame.K_LEFT):
                    self.snake.snake_speed[0]=-1
                    self.snake.snake_speed[1]=0
                elif event.key == pygame.K_RIGHT and self.first_slice(pygame.K_RIGHT):
                    self.snake.snake_speed[0]=1
                    self.snake.snake_speed[1]=0
                elif event.key == pygame.K_UP and self.first_slice(pygame.K_UP):
                    self.snake.snake_speed[0]=0
                    self.snake.snake_speed[1]=-1
                elif event.key == pygame.K_DOWN and self.first_slice(pygame.K_DOWN):
                    self.snake.snake_speed[0]=0
                    self.snake.snake_speed[1]=1

    def game_draw(self):
        self.screen.fill(self.blackgrond_color)
        self.game_step_user()
        self.snake.draw_snake(self.screen)
        self.draw_food()
        

        pygame.display.update()
        pygame.display.flip()

    def game_step_user(self):
        self.user_actions()
        self.snake.update_snake_position()
        self.end_game()
        self.eat_food()
        
        

# def inputs_AI(self,head,body,food,speed):
#     inputs=[]
#     #danger LEFT
#     head_mov = [self.snake.head_position[0]+1,self.snake.head_position[1]]
#     if head["position"]["x"]+1 == int(self.width/self.section_size ) or (body["sections"] and head_mov in body["sections"]):
#         inputs.append(1)
#     else:
#         inputs.append(0)

#     #danger RIGHT
#     head_mov = [head["position"]["x"]-1,head["position"]["y"]]
#     if head["position"]["x"]-1 == 0 or (body["sections"] and head_mov in body["sections"]):
#         inputs.append(1)
#     else:
#         inputs.append(0)
#     #danger UP
#     head_mov = [head["position"]["x"],head["position"]["y"]-1]
#     if head["position"]["y"]-1 == 0 or (body["sections"] and head_mov in body["sections"]):
#         inputs.append(1)
#     else:
#         inputs.append(0)
#     #danger DOWN
#     head_mov = [head["position"]["x"],head["position"]["y"]+1]
#     if head["position"]["y"]+1 == int(height/SECTION_SIZE) or (body["sections"] and head_mov in body["sections"]):
#         inputs.append(1)
#     else:
#         inputs.append(0)



#     # direction
#     if speed[0]==-1:
#         inputs.append(1)
#     else:
#         inputs.append(0)
#     if speed[0]==1:
#         inputs.append(1)
#     else:
#         inputs.append(0)
#     if speed[1]==-1:
#         inputs.append(1)
#     else:
#         inputs.append(0)
#     if speed[1]==1:
#         inputs.append(1)
#     else:
#         inputs.append(0)

#     # food 
#     if food[0]>head["position"]["x"]:
#         inputs.append(1)
#     else:
#         inputs.append(0)
#     if food[0]<head["position"]["x"]:
#         inputs.append(1)
#     else:
#         inputs.append(0)
#     if food[0]>head["position"]["y"]:
#         inputs.append(1)
#     else:
#         inputs.append(0)
#     if food[0]<head["position"]["y"]:
#         inputs.append(1)
#     else:
#         inputs.append(0)


#     print(inputs)
#     return inputs

if __name__ == '__main__':
    game = snake_game()


    while 1:
        game.game_draw()
        # game.user_actions()
        
        time.sleep(0.1)
    