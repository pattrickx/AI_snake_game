import sys, pygame
from pygame.draw import rect
from pygame.draw import line
import numpy as np
import time
import math

class Snake:
    def __init__(self,screen_size,head_color=(0,0,255),head_position=[10,10],
                body_color=(0,255,0),body_sections=[],section_size=50,speed=[0,0]) -> None:
        self.head_color = head_color
        self.head_position = head_position
        self.body_color = body_color
        self.body_sections = body_sections
        self.section_size = section_size
        self.speed = speed
        self.screen_size = screen_size
        self.stamina_base = int(self.screen_size[0]/self.section_size)*int(self.screen_size[1]/self.section_size)
        self.stamina = self.stamina_base
        self.score=0
        self.lines=[]
    
        

    def draw_sensors(self,screen):
        # print("SDASDSAdas")
        for l in self.lines:
            line(screen,(0,255,255),l[0],l[1],width=3)
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

        self.head_position[0] =  self.head_position[0]+ self.speed[0]
        self.head_position[1] =  self.head_position[1]+ self.speed[1]
        self.stamina -=1

class snake_game:
    def __init__(self,width:int=500,height:int=500,blackgrond_color=(0, 0, 0),
                section_size=50,food_color=(255,0,0)) -> None:
        pygame.init()
        pygame.font.init()
        self.size = self.width, self.height =  width,height
        self.blackgrond_color = blackgrond_color
        self.food_color = food_color
        self.section_size = section_size
        self.screen = pygame.display.set_mode(self.size)
        self.snake=Snake(self.size,section_size=self.section_size)
        self.food=[]
        self.generate_food()
        
    def reset(self):
        self.snake.head_position=np.random.randint([int(self.width/self.section_size),int(self.height/self.section_size)],size=2).tolist()
        self.snake.body_sections=[]
        self.snake.score=0
        self.snake.stamina=self.snake.stamina_base
        self.snake.speed=[0,0]

        self.generate_food()

    def generate_food(self):
        if len(self.snake.body_sections)+1 == int(self.width/self.section_size)*int(self.height/self.section_size):
            print("Vitoria")
            self.snake.score = (len(self.snake.body_sections)*self.snake.stamina)**2
            return True
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
            self.snake.score = len(self.snake.body_sections)*self.snake.stamina
            self.snake.stamina = self.snake.stamina_base
            return True
        return False


    def end_game(self):

        if self.width<=self.snake.head_position[0]*self.section_size or self.snake.head_position[0]<0:
            print("derrota 1")
            return True
        if self.height<=self.section_size*self.snake.head_position[1] or self.snake.head_position[1]<0:
            print("derrota 2")
            return True
        if self.snake.head_position in self.snake.body_sections:
            print("derrota 3")
            return True
        if self.snake.stamina<0:
            print("derrota 4")
            return True
        return False

    def first_slice(self,key):
        return True
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

    def user_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.first_slice(pygame.K_LEFT):
                    self.snake.speed[0]=-1
                    self.snake.speed[1]=0
                elif event.key == pygame.K_RIGHT and self.first_slice(pygame.K_RIGHT):
                    self.snake.speed[0]=1
                    self.snake.speed[1]=0
                elif event.key == pygame.K_UP and self.first_slice(pygame.K_UP):
                    self.snake.speed[0]=0
                    self.snake.speed[1]=-1
                elif event.key == pygame.K_DOWN and self.first_slice(pygame.K_DOWN):
                    self.snake.speed[0]=0
                    self.snake.speed[1]=1

    def ai_action(self,move):
        
        if move[0] == 1 and self.first_slice(pygame.K_LEFT):
            self.snake.speed[0]=-1
            self.snake.speed[1]=0
        elif move[1] == 1 and self.first_slice(pygame.K_RIGHT):
            self.snake.speed[0]=1
            self.snake.speed[1]=0
        elif move[2] == 1 and self.first_slice(pygame.K_UP):
            self.snake.speed[0]=0
            self.snake.speed[1]=-1
        elif move[3] == 1 and self.first_slice(pygame.K_DOWN):
            self.snake.speed[0]=0
            self.snake.speed[1]=1

    def game_draw(self):
        self.screen.fill(self.blackgrond_color)
        self.snake.draw_snake(self.screen)
        self.draw_food()
        self.snake.draw_sensors(self.screen)

        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(f"Score: {self.snake.score} Stamina: {self.snake.stamina} Foods: {len(self.snake.body_sections)}", False, (255, 255, 255))
        # self.screen.blit(text_surface, (0,0))
        pygame.display.update()
        pygame.display.flip()

    def game_step_user(self):
        self.user_action()
        self.snake.update_snake_position()
        if self.end_game():
            # sys.exit()
            self.reset()
        self.eat_food() 
        if self.generate_food():
            self.reset()
        
    def game_step_ai(self,move):
        reward=1
        # self.snake.score+=1
        self.ai_action(move)
        self.snake.update_snake_position()
        if self.end_game():
            reward=-10
            return reward,True,self.snake.score,len(self.snake.body_sections)
        if self.eat_food():
            reward=10
            if self.generate_food():
                reward=100
                return reward,True,self.snake.score,len(self.snake.body_sections)
        return reward,False,self.snake.score,len(self.snake.body_sections)



    def angle(self,v1, v2):
        v2[0] = v2[0]-v1[0]
        v2[1] = v2[1]-v1[1]

        if v2[0]:
            theta = math.atan(v2[1]/v2[0])
            # Converting theta from radian to degree
            theta = 180 * theta/math.pi
            return theta
        elif v2[1]>0:
            return 90.0
        elif v2[1]<0:
            return -90
        return 0

    def inputs_AI(self):
        half = self.snake.section_size/2
        start_line = (half+self.snake.head_position[0]*self.snake.section_size,half+self.snake.head_position[1]*self.snake.section_size)
        inputs=[]
        self.snake.lines=[]
        #danger LEFT
        inputs.append(0)
        if self.snake.head_position[0]-1<0:
            inputs[-1]=0
        for n in range(self.snake.head_position[0]-1,-1,-1):
            head_mov = [n,self.snake.head_position[1]]
            if head_mov[0]<=0 or (self.snake.body_sections and head_mov in self.snake.body_sections):
            # if (self.snake.body_sections and head_mov in self.snake.body_sections):
                inputs[-1]=-(self.snake.head_position[0]-n)
                break
        self.snake.lines.append([start_line,(half+(self.snake.head_position[0]+inputs[-1])*self.snake.section_size,half+self.snake.section_size*self.snake.head_position[1])])

        # #danger LEFT UP
        # inputs.append(0)
        # if self.snake.head_position[0]-1<0 or self.snake.head_position[1]-1<0:
        #     inputs[-1]=1
        
        # min_direction = self.snake.head_position[0] if self.snake.head_position[0]< self.snake.head_position[1] else self.snake.head_position[1]
        # for n in range(1,min_direction+1,1):
        #     head_mov = [self.snake.head_position[0]-n,self.snake.head_position[1]-n]
        #     if head_mov[0]<=0 or head_mov[1]<=0 or (self.snake.body_sections and head_mov in self.snake.body_sections):
        #     # if (self.snake.body_sections and head_mov in self.snake.body_sections):
        #         inputs[-1]=n
        #         break

        # self.snake.lines.append([start_line,(half+(self.snake.head_position[0]-inputs[-1])*self.snake.section_size,half+self.snake.section_size*(self.snake.head_position[1]-inputs[-1]))])

        #danger UP
        inputs.append(0)
        if self.snake.head_position[1]-1<0:
            inputs[-1]=0
        for n in range(self.snake.head_position[1]-1,-1,-1):
            head_mov = [self.snake.head_position[0],n]
            if head_mov[1]<=0 or (self.snake.body_sections and head_mov in self.snake.body_sections):
            # if(self.snake.body_sections and head_mov in self.snake.body_sections):
                inputs[-1]=-(self.snake.head_position[1]-n)
                break
        self.snake.lines.append([start_line,(half+self.snake.head_position[0]*self.snake.section_size,half+self.snake.section_size*(self.snake.head_position[1]+inputs[-1]))])

        # #danger UP RIGHT
        # inputs.append(0)
        # if self.snake.head_position[0]+1>int(self.width/self.section_size) or self.snake.head_position[1]-1<0:
        #     inputs[-1]=1
        
        # min_direction = int(self.width/self.section_size )-self.snake.head_position[0] if int(self.width/self.section_size )-self.snake.head_position[0]< self.snake.head_position[1] else self.snake.head_position[1]
        # for n in range(1,min_direction+1,1):
        #     head_mov = [self.snake.head_position[0]+n,self.snake.head_position[1]-n]
        #     if head_mov[0]>=int(self.width/self.section_size) or head_mov[1]<=0 or (self.snake.body_sections and head_mov in self.snake.body_sections):
        #     # if (self.snake.body_sections and head_mov in self.snake.body_sections):
        #         inputs[-1]=n
        #         break
        # self.snake.lines.append([start_line,(half+(self.snake.head_position[0]+inputs[-1])*self.snake.section_size,half+self.snake.section_size*(self.snake.head_position[1]-inputs[-1]))])

        #danger RIGHT
        inputs.append(0)
        if self.snake.head_position[0]+1>int(self.width/self.section_size):
            inputs[-1]=0
        for n in range(self.snake.head_position[0]+1,int(self.width/self.section_size)+1,1):
            head_mov = [n,self.snake.head_position[1]]
            if head_mov[0]>=int(self.width/self.section_size) or (self.snake.body_sections and head_mov in self.snake.body_sections):
            # if (self.snake.body_sections and head_mov in self.snake.body_sections):
                inputs[-1]=n-self.snake.head_position[0]
                break

        self.snake.lines.append([start_line,((self.snake.head_position[0]+inputs[-1])*self.snake.section_size-half,half+self.snake.section_size*self.snake.head_position[1])])

        #danger RIGHT DOWN
        # inputs.append(0)
        # if self.snake.head_position[0]+1>int(self.width/self.section_size) or self.snake.head_position[1]+1>int(self.height/self.section_size):
        #     inputs[-1]=1
        
        # if self.snake.head_position[0]> self.snake.head_position[1]:
        #     min_direction = int(self.width/self.section_size )-self.snake.head_position[0]
        # else:
        #     min_direction = int(self.height/self.section_size)-self.snake.head_position[1]
        # for n in range(1,min_direction+1,1):
        #     head_mov = [self.snake.head_position[0]+n,self.snake.head_position[1]+n]
        #     if head_mov[0]>=int(self.width/self.section_size ) or head_mov[1]>=int(self.height/self.section_size) or (self.snake.body_sections and head_mov in self.snake.body_sections):
        #     # if (self.snake.body_sections and head_mov in self.snake.body_sections):
        #         inputs[-1]=n
        #         break

        # self.snake.lines.append([start_line,(half+(self.snake.head_position[0]+inputs[-1])*self.snake.section_size,half+self.snake.section_size*(self.snake.head_position[1]+inputs[-1]))])
        
        #danger DOWN
        inputs.append(0)
        if self.snake.head_position[1]+1>int(self.height/self.section_size):
            inputs[-1]=0
        for n in range(self.snake.head_position[1]+1,int(self.height/self.section_size)+1,1):
            head_mov = [self.snake.head_position[0],n]
            if head_mov[1]>=int(self.height/self.section_size) or (self.snake.body_sections and head_mov in self.snake.body_sections):
            # if (self.snake.body_sections and head_mov in self.snake.body_sections):
                inputs[-1]=n-self.snake.head_position[1]
                break

        self.snake.lines.append([start_line,(half+self.snake.head_position[0]*self.snake.section_size,self.snake.section_size*(self.snake.head_position[1]+inputs[-1])-half)])

        #danger DOWN LEFT
        # inputs.append(0)
        # if self.snake.head_position[0]-1<0 or self.snake.head_position[1]+1>int(self.height/self.section_size) :
        #     inputs[-1]=1
        
        # min_direction = self.snake.head_position[0] if self.snake.head_position[0]<int(self.height/self.section_size)-self.snake.head_position[1] else int(self.height/self.section_size)-self.snake.head_position[1]
        # for n in range(1,min_direction+1,1):
        #     head_mov = [self.snake.head_position[0]-n,self.snake.head_position[1]+n]
        #     if head_mov[0]<=0 or head_mov[1]>=int(self.height/self.section_size) or (self.snake.body_sections and head_mov in self.snake.body_sections):
        #     # if (self.snake.body_sections and head_mov in self.snake.body_sections):
        #         inputs[-1]=n
        #         break

        # self.snake.lines.append([start_line,(half+(self.snake.head_position[0]-inputs[-1])*self.snake.section_size,half+self.snake.section_size*(self.snake.head_position[1]+inputs[-1]))])
    


        inputs.append(self.food[0]-self.snake.head_position[0])
        # print((self.food[0]-self.snake.head_position[0])/int(self.width/self.section_size ))
        inputs.append(self.food[1]-self.snake.head_position[1])
        # if self.food[0]>self.snake.head_position[0]:
        #     inputs.append(1)
        # elif self.food[0]<self.snake.head_position[0]:
        #     inputs.append(-1)
        # else:
        #     inputs.append(0)
        # # if self.food[0]<self.snake.head_position[0]:
        # #     inputs.append(1)
        # # else:
        # #     inputs.append(0)
        # if self.food[1]>self.snake.head_position[1]:
        #     inputs.append(1)
        # elif self.food[1]<self.snake.head_position[1]:
        #     inputs.append(-1)
        # else:
        #     inputs.append(0)
        # if self.food[1]<self.snake.head_position[1]:
        #     inputs.append(1)
        # else:
        #     inputs.append(0)
        print(inputs)
        return np.array(inputs)


if __name__ == '__main__':
    game = snake_game()


    while 1:
        game.game_draw()
        # game.user_actions()
        
        time.sleep(0.1)
    