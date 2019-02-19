"""balls!"""

import pygame
import random
from pygame.locals import*
import math
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BALL_SIZE = 4
LOWSPEED=-6
HIGHSPEED=6
BALLMASS=1.0
CHANCEANGRY=100
TIMEBEFORERELAX=3

Smiley = pygame.sprite.Group()
others = pygame.sprite.Group()
Angry= pygame.sprite.Group()

class Ball(pygame.sprite.Sprite):
    """
        Class to keep track of a ball's location and vector.
        """
    def __init__(self,Group):
        
        pygame.sprite.Sprite.__init__(self, Group, others)
        #first bit is sign next 7 x movement next(nr 9) is y sign 10-16 is y movement
        self.moveVector= [0,0]
        self.b=random.randrange(1,10)
        self.c=(BALL_SIZE*self.b)**2
        self.mass=self.c*BALLMASS
        self.angryFace=self.getAngry()
        self.relaxFace=self.getRelax()
        self.image=self.relaxFace
        self.rect = self.image.get_rect().clip(0,0,self.b*BALL_SIZE,self.b*BALL_SIZE)
        self.timeLastHit=100
    def collisionCheck(self, ball2):
        col=pygame.sprite.collide_circle(self, ball2)
        if col:
            self.timeLastHit=min(self.timeLastHit,0)
            ball2.timeLastHit=min(ball2.timeLastHit,0)
        return col
    def move(self,x,y):
        self.rect.move_ip(x,y)
    def getCenter(self):
        center=[self.rect[0]+self.b*BALL_SIZE/2.0,self.rect[1]+self.b*BALL_SIZE/2.0]
        return center
    def getRelax(self):
        path = "/Users/martinskoglund1/Desktop/Flushed_Face_Emoji.png"
        imag3 = pygame.image.load(path)
        basewidth = self.b*BALL_SIZE
        wpercent = (basewidth / float(imag3.get_rect().size[0]))
        hsize = int((float(imag3.get_rect().size[1]) * wpercent))
        imag3 =pygame.transform.smoothscale(imag3, (hsize, hsize))
        return imag3
    def getAngry(self):
        path = "/Users/martinskoglund1/Desktop/angrySmiley1.png"
        imag3 = pygame.image.load(path)
        basewidth = self.b*BALL_SIZE
        wpercent = (basewidth / float(imag3.get_rect().size[0]))
        hsize = int((float(imag3.get_rect().size[1]) * wpercent))
        imag3 =pygame.transform.smoothscale(imag3, (hsize, hsize))
        return imag3
    def turnAngry(self):
        self.image=self.angryFace
        Angry.add(self)
    def turnRelax(self):
        self.image=self.relaxFace
        Angry.remove(self)
def squareNorm(v):
    n=v[0]**2+v[1]**2
    return float(n+0.001)
def dotProduct(v1,v2):
    v=v1[0]*v2[0]+v1[1]*v2[1]
    return float(v)
def vektM(v1,v2):
    v=[v1[0]-v2[0],v1[1]-v2[1]]
    return v
def sMult(scalar, vector):
    v=[scalar*float(vector[0]),scalar*float(vector[1])]
    return v
def collision(v1,v2,m1,m2,x1,x2):
    #v1, v2 are the old movevectors#
    #masspart
    m11=(2*m2/(m1+m2))
    #dotproductpart
    dot=dotProduct(vektM(v1,v2),vektM(x1,x2))
    #normbit
    norm=squareNorm(vektM(x1,x2))
    #pointvector
    pointV=vektM(x1,x2)
    newV1=vektM(v1,sMult(m11*dot/norm,pointV))
    return newV1

def make_ball(Group):
    """
        Function to make a new, random ball.
        """
    ball = Ball(Group)
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    x = random.randrange(ball.b*BALL_SIZE, SCREEN_WIDTH - ball.b*BALL_SIZE)
    y = random.randrange(ball.b*BALL_SIZE, SCREEN_HEIGHT - ball.b*BALL_SIZE)
    ball.rect.move_ip(x,y)
    
    # Speed and direction of rectangle
    for i in (0,1):
        ball.moveVector=setMoveVector(i,LOWSPEED,HIGHSPEED,ball.moveVector)
    return ball

def setMoveVector(index,loRange,range,vector):
    vector[index]=random.randrange(loRange,range)
    return vector

def getSign(x):
    return math.copysign(1, x)
def turn(b1,b2):
    if random.randrange(0,100)<CHANCEANGRY:
        if b1 in Angry and b2 not in Angry:
            b2.turnAngry()

def main():
    """
        This is our main program.
        """
    pygame.init()
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Bouncing Balls")
    
    # Loop until the user clicks the close button.
    done = False
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    angryBall=make_ball(Smiley)
    Angry.add(angryBall)
    angryBall.turnAngry()
    angryBall.timeLastHit=-100
    ball = make_ball(Smiley)
    
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_SPACE:
                    ball = make_ball(Smiley)
        # --- Logic
        for ball in Smiley:
            #remove ball from others
            others.remove(ball)
            ball.timeLastHit+=0.03
            if ball.timeLastHit>TIMEBEFORERELAX:
                ball.turnRelax()
            # Move the ball's center
            x = ball.moveVector[0]
            y = ball.moveVector[1]
            ball.move(x,y)
            
            # Bounce the ball if needed
            if ball.rect[1] > SCREEN_HEIGHT - ball.b*BALL_SIZE or ball.rect[1] < 0:
                ball.moveVector[1]*= -1
                ball.move(ball.moveVector[0]/2,ball.moveVector[1]/2)
            if ball.rect[0] > SCREEN_WIDTH - ball.b*BALL_SIZE or ball.rect[0] < 0:
                ball.moveVector[0]*= -1
                ball.move(ball.moveVector[0],ball.moveVector[1])
            #check for collision
            posColliders=pygame.sprite.spritecollideany(ball, others, collided = None)
            if posColliders:
                for b1 in others:
                    if ball.collisionCheck(b1):
                        v1=ball.moveVector
                        v2=b1.moveVector
                        m1=ball.mass
                        m2=b1.mass
                        x1=ball.getCenter()
                        x2=b1.getCenter()
                        vect=collision(v1,v2,m1,m2,x1,x2)
                        ball.moveVector=vect
                        ball.move(vect[0],vect[1])
                        vect=collision(v2,v1,m2,m1,x2,x1)
                        b1.moveVector=vect
                        b1.move(vect[0],vect[1])
                        turn(ball,b1)
                        turn(b1,ball)
            
                        
            #add sprite bakc to others group#
            others.add(ball)
        # --- Drawing
        # Set the screen background
        screen.fill(BLACK)
        
        # Draw the balls
        for ball in Smiley:
            #pygame.draw.circle(screen, WHITE, [ball.x, ball.y], BALL_SIZE)
            screen.blit(ball.image,ball.rect)
# --- Wrap-up
# Limit to 60 frames per second
        clock.tick(60)

# Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
    
    # Close everything down
    pygame.quit()
if __name__ == "__main__":
    main()

