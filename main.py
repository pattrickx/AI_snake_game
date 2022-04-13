import sys, pygame
from pygame.draw import rect
import numpy as np
import time
pygame.init()

size = width, height =  1000,1000
speed = [1, 0]
blackgrond_color = (0, 0, 0)
direc=1

screen = pygame.display.set_mode(size)

section_size=50
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
        x1=section[0]*section_size
        y1=section[1]*section_size
        rect(screen,body["color"], (x1,y1,section_size,section_size))

    x1=head["position"]["x"]*section_size
    y1=head["position"]["y"]*section_size
    rect(screen, head["color"], (x1,y1,section_size,section_size))

def generate_food(head,body):
    if len(body["sections"])+1 == int(width/section_size)+int(height/section_size):
        print("Vitoria")
        sys.exit()
    food = np.random.randint([int(width/section_size),int(height/section_size)],size=2).tolist()
    while food in body["sections"] or food == [head["position"]["x"],head["position"]["y"]]:
        food = np.random.randint([int(width/section_size),int(height/section_size)],size=2).tolist()
        print(f"{food} tent")
    return food
    

def draw_food(screen,food):
    if food:
        x1=food[0]*section_size
        y1=food[1]*section_size
        rect(screen, (255,0,0), (x1,y1,section_size,section_size))

def eat_food(head,food,body):

    head_position = [head["position"]["x"],head["position"]["y"]]
    if head_position == food:
        body["sections"].insert(0,[head["position"]["x"],head["position"]["y"]])
        return generate_food(head,body)   
    return food

def end_game(head,body):

    if int(width/section_size)<head["position"]["x"] or head["position"]["x"]<0:
        print("derrota")
        sys.exit()
    if int(height/section_size)<head["position"]["y"] or head["position"]["y"]<0:
        print("derrota")
        sys.exit()
    if [head["position"]["x"],head["position"]["y"]] in body["sections"]:
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

foods = generate_food(head,body)
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

    # elif head["position"]["x"]*section_size+section_size >= width:
    #     speed[0]=0
    #     speed[1]=1
    # elif head["position"]["y"]*section_size+section_size >= height:
    #     speed[0]=-1
    #     speed[1]=0
    # elif head["position"]["x"]<=0:
    #     speed[0]=0
    #     speed[1]=-1

    # if head["position"]["x"]*section_size+section_size >= width:
    #     direc = 0
    # if head["position"]["x"] <= 0:
    #     direc = 1
    # base = section_size 
    # if head["position"]["x"]*section_size+section_size >= width-1:
    #     base = 0

    # if head["position"]["y"] <= base or head["position"]["y"]*section_size+section_size >= height:
    #     if speed[0] == 1:
    #         speed[0] = 0
    #         speed[1] = 1 if head["position"]["y"] <= 0 else -1
    #     else :
    #         speed[0] = 1 if direc == 1 else -1
    #         speed[1] = 0
    end_game(head,body)

    foods = eat_food(head,foods,body)
    draw_food(screen,foods)
    draw_snake(screen,head,body)

    pygame.display.update()
    pygame.display.flip()
    time.sleep(0.05)