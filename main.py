import sys, pygame
from pygame.draw import rect
import numpy as np
import time
pygame.init()

size = width, height =  1000,1000
speed = [1, 0]
blackgrond_color = (0, 0, 0)

screen = pygame.display.set_mode(size)

SECTION_SIZE=50
STAMINA_BASE =int(width/SECTION_SIZE)*int(height/SECTION_SIZE)
stamina = STAMINA_BASE
head = {"position":{"x":0,"y":0},"color":(0,0,255)}
body = {"color":(0,255,0),"sections":[]}

def update_snake_position(pos,head,body):
    if len(body["sections"])>0:

        for n in range(len(body["sections"])-1,-1,-1):
            section = body["sections"][n]
            section_n = body["sections"][n-1]
            section[0]=section_n[0]
            section[1]=section_n[1]

        section = body["sections"][0]
        section[0]=head["position"]["x"]
        section[1]=head["position"]["y"]
    head["position"]["x"] = head["position"]["x"]+pos[0]
    head["position"]["y"] = head["position"]["y"]+pos[1]

def draw_snake(screen,head,body):
    for section in body["sections"]:
        x1=section[0]*SECTION_SIZE
        y1=section[1]*SECTION_SIZE
        rect(screen,body["color"], (x1,y1,SECTION_SIZE,SECTION_SIZE))

    x1=head["position"]["x"]*SECTION_SIZE
    y1=head["position"]["y"]*SECTION_SIZE
    rect(screen, head["color"], (x1,y1,SECTION_SIZE,SECTION_SIZE))

def generate_food(head,body):
    if len(body["sections"])+1 == int(width/SECTION_SIZE)*int(height/SECTION_SIZE):
        print("Vitoria")
        sys.exit()
    food = np.random.randint([int(width/SECTION_SIZE),int(height/SECTION_SIZE)],size=2).tolist()
    while food in body["sections"] or food == [head["position"]["x"],head["position"]["y"]]:
        food = np.random.randint([int(width/SECTION_SIZE),int(height/SECTION_SIZE)],size=2).tolist()
        print(f"{food} tent")
    return food
    

def draw_food(screen,food):
    if food:
        x1=food[0]*SECTION_SIZE
        y1=food[1]*SECTION_SIZE
        rect(screen, (255,0,0), (x1,y1,SECTION_SIZE,SECTION_SIZE))

def eat_food(head,food,body,stamina):

    head_position = [head["position"]["x"],head["position"]["y"]]
    if head_position == food:
        body["sections"].insert(0,[head["position"]["x"],head["position"]["y"]])
        return generate_food(head,body),STAMINA_BASE
    return food,stamina

def end_game(head,body,stamina):

    if int(width/SECTION_SIZE)<head["position"]["x"] or head["position"]["x"]<0:
        print("derrota")
        sys.exit()
    if int(height/SECTION_SIZE)<head["position"]["y"] or head["position"]["y"]<0:
        print("derrota")
        sys.exit()
    if [head["position"]["x"],head["position"]["y"]] in body["sections"]:
        print("derrota")
        sys.exit()
    if stamina<0:
        print("derrota")
        sys.exit()

def first_slice(key,head,body):
    if not body["sections"]:
        return True
    if key == pygame.K_LEFT:
        return head["position"]["x"]-1 != body["sections"][0][0]
        
    elif key == pygame.K_RIGHT:
        return head["position"]["x"]+1 != body["sections"][0][0]
    elif key == pygame.K_UP:
        return head["position"]["y"]-1 != body["sections"][0][1]
    elif key == pygame.K_DOWN:
        return head["position"]["y"]+1 != body["sections"][0][1]
def inputs_AI(head,body,food,speed):
    inputs=[]
    #danger LEFT
    head_mov = [head["position"]["x"]+1,head["position"]["y"]]
    if head["position"]["x"]+1 == int(width/SECTION_SIZE) or (body["sections"] and head_mov in body["sections"]):
        inputs.append(1)
    else:
        inputs.append(0)

    #danger RIGHT
    head_mov = [head["position"]["x"]-1,head["position"]["y"]]
    if head["position"]["x"]-1 == 0 or (body["sections"] and head_mov in body["sections"]):
        inputs.append(1)
    else:
        inputs.append(0)
    #danger UP
    head_mov = [head["position"]["x"],head["position"]["y"]-1]
    if head["position"]["y"]-1 == 0 or (body["sections"] and head_mov in body["sections"]):
        inputs.append(1)
    else:
        inputs.append(0)
    #danger DOWN
    head_mov = [head["position"]["x"],head["position"]["y"]+1]
    if head["position"]["y"]+1 == int(height/SECTION_SIZE) or (body["sections"] and head_mov in body["sections"]):
        inputs.append(1)
    else:
        inputs.append(0)



    # direction
    if speed[0]==-1:
        inputs.append(1)
    else:
        inputs.append(0)
    if speed[0]==1:
        inputs.append(1)
    else:
        inputs.append(0)
    if speed[1]==-1:
        inputs.append(1)
    else:
        inputs.append(0)
    if speed[1]==1:
        inputs.append(1)
    else:
        inputs.append(0)

    # food 
    if food[0]>head["position"]["x"]:
        inputs.append(1)
    else:
        inputs.append(0)
    if food[0]<head["position"]["x"]:
        inputs.append(1)
    else:
        inputs.append(0)
    if food[0]>head["position"]["y"]:
        inputs.append(1)
    else:
        inputs.append(0)
    if food[0]<head["position"]["y"]:
        inputs.append(1)
    else:
        inputs.append(0)


    print(inputs)
    return inputs


food = generate_food(head,body)
draw_snake(screen,head,body)
while 1:
    screen.fill(blackgrond_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and first_slice(pygame.K_LEFT,head,body):
                speed[0]=-1
                speed[1]=0
            elif event.key == pygame.K_RIGHT and first_slice(pygame.K_RIGHT,head,body):
                speed[0]=1
                speed[1]=0
            elif event.key == pygame.K_UP and first_slice(pygame.K_UP,head,body):
                speed[0]=0
                speed[1]=-1
            elif event.key == pygame.K_DOWN and first_slice(pygame.K_DOWN,head,body):
                speed[0]=0
                speed[1]=1

    update_snake_position(speed,head,body)

    # if speed[1]==-1:
    #     speed[0]=1
    #     speed[1]=0

    # elif head["position"]["x"]*SECTION_SIZE+SECTION_SIZE >= width:
    #     speed[0]=0
    #     speed[1]=1
    # elif head["position"]["y"]*SECTION_SIZE+SECTION_SIZE >= height:
    #     speed[0]=-1
    #     speed[1]=0
    # elif head["position"]["x"]<=0:
    #     speed[0]=0
    #     speed[1]=-1

    # if head["position"]["x"]*SECTION_SIZE+SECTION_SIZE >= width:
    #     direc = 0
    # if head["position"]["x"] <= 0:
    #     direc = 1
    # base = SECTION_SIZE 
    # if head["position"]["x"]*SECTION_SIZE+SECTION_SIZE >= width-1:
    #     base = 0

    # if head["position"]["y"] <= base or head["position"]["y"]*SECTION_SIZE+SECTION_SIZE >= height:
    #     if speed[0] == 1:
    #         speed[0] = 0
    #         speed[1] = 1 if head["position"]["y"] <= 0 else -1
    #     else :
    #         speed[0] = 1 if direc == 1 else -1
    #         speed[1] = 0
    inputs_AI(head,body,food,speed)
    end_game(head,body,stamina)

    food,stamina = eat_food(head,food,body,stamina)
    draw_food(screen,food)
    draw_snake(screen,head,body)
    stamina-=1
    print(stamina)

    pygame.display.update()
    pygame.display.flip()
    time.sleep(0.1)