import sys, pygame, serial, random, copy
from pygame.locals import *
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')
UP='up'
DOWN='down'
LEFT='left'
RIGHT='right'
HIGHER='forward'
LOWER='back'
FPS=2
FPSCLOCK = pygame.time.Clock()

EDGECOLLISION = False #false teleports when leaving grid
WORMCOLLISION = True #toggle

ser=serial.Serial('/dev/ttyACM0')
empty='000'*5**3
canvas='000'*5**3
def draw(canvas,color,coords):
    x,y,z=coords
    canvas=canvas[:3*(x*5**2+z*5+y)]+color+canvas[3*(x*5**2+z*5+y)+3:]
    return canvas
def read(canvas,coords):
    x,y,z=coords
    return canvas[3*(x*5**2+z*5+y):3*(x*5**2+z*5+y)+3]
ser.write(' '+canvas+' ')

def makeapplecoords():
    return [random.randint(0,4),random.randint(0,4),random.randint(0,4)]
def validCoordinates(coords):
    for i in coords:
        if not (i<5 and i>=0):
            return False
    return True
def makevalidcoords(coords):
    for i in range(len(coords)):
        if coords[i]<0:
            coords[i]=4
        elif coords[i]>4:
            coords[i]=0
    return coords

def validmove(direction,move):
    if direction==UP and move==DOWN or direction==DOWN and move==UP:
        return False
    if direction==RIGHT and move==LEFT or direction==LEFT and move==RIGHT:
        return False
    if direction==HIGHER and move==LOWER or direction==LOWER and move==HIGHER:
        return False
    return True
dot=[2,2,2]
snake=[]
snake.append([2,2,2])
#snake.append([2,2,2])
#snake.append([2,2,2])
#snake.append([2,2,2])
canvas=draw(canvas,'010',dot)
moveslist= []
apple=makeapplecoords()
direction=None
while True: # main game loop
    #move= None
    canvas=empty
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            move=None
            if event.key == K_LEFT:
                move = LEFT
            elif event.key in (K_RIGHT, K_d):
                move = RIGHT
            elif event.key in (K_UP, K_w):
                move = UP
            elif event.key in (K_DOWN, K_s):
                move = DOWN
            elif event.key == (K_a):
                move=HIGHER
            elif event.key == (K_z):
                move=LOWER
            if move:
                moveslist.append(move)
    while moveslist:
        if validmove(direction,move):
            direction=moveslist[0]
            del moveslist[0]
            break
        else:
            del moveslist[0]

    if direction:
        move=direction
        dot=copy.copy(snake[0])
        if move==UP:
            dot[2]-=1
        elif move==DOWN:
            dot[2]+=1
        elif move==RIGHT:
            dot[0]+=1
        elif move==LEFT:
            dot[0]-=1
        elif move==HIGHER:
            dot[1]-=1
        elif move==LOWER:
            dot[1]+=1
        if not validCoordinates(dot):
            if EDGECOLLISION:
                pygame.quit()
                sys.exit()
            else:
                dot=makevalidcoords(dot)
        snake.insert(0, dot)
        if dot==apple:
            apple=makeapplecoords()
        else:
            del snake[-1]
            if WORMCOLLISION and len(snake)>4:
                if snake[0] in snake[4:]:
                    pygame.quit()
                    sys.exit()
    print(snake)

    for dot in snake:
        canvas=draw(canvas,'010',dot)
    canvas=draw(canvas,'100',apple)
    pygame.display.update()
    ser.write(' '+canvas+' ')
    FPSCLOCK.tick(FPS)