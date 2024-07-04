# Example file showing a basic pygame "game loop"
import pygame
import math
import numpy as np

# pygame setup
pygame.init()
WID,HEI=1000, 900
SCR = pygame.display.set_mode((WID,HEI))
pygame.display.set_caption("GRAVITY")

BLUE = (100, 149, 237)
RED = (188, 39, 50)
G = 6.67428e-11
EARTH_MASS=2e+19
MARS_MASS=2e+19
MERCURY_MASS=8e+17
# OFFSET=0.0001
dt=0.0008


def nor_tang(vector1,vector2):
    sub_vec=np.subtract(vector2,vector1)
    unit_norm=sub_vec/np.linalg.norm(sub_vec)

    unit_tang=np.array([-unit_norm[1],unit_norm[0]],dtype=np.float64)

    return unit_norm,unit_tang


class Planet:
    def __init__(self,x,y,r,color,mass):
        self.x = x 
        self.y = y 
        self.r = r
        self.color = color
        self.mass = mass

        self.orbit=[]

        self.x_vel=0
        self.y_vel=0

    def draw_planet(self,window):
        x=self.x + WID/2
        y=self.y + HEI/2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x  + WID / 2
                y = y  + HEI / 2
                updated_points.append((x, y))

            pygame.draw.lines(window, self.color, False, updated_points, 2)
        pygame.draw.circle(window,self.color,(x,y),self.r)

    def handle_collision(self, planet2):

        
        # creating tangential and normal components with the defined function nor_tang()
        vel_self=np.array([self.x_vel,self.y_vel],dtype=np.float64)
        vel_planet2=np.array([planet2.x_vel,planet2.y_vel],dtype=np.float64)
        norm_vec , tang_vec = nor_tang(vel_self,vel_planet2)

        v1n=np.dot(norm_vec,vel_self)
        v2n=np.dot(norm_vec,vel_planet2)

        v1t=np.dot(tang_vec,vel_self)
        v2t=np.dot(tang_vec,vel_planet2)

        # creating new norm and tang compnents acording to elastic collision formulas.
        
        # veloity for self
        new_v1n=((v1n*(self.mass-planet2.mass))+(2*planet2.mass*v2n))/(self.mass+planet2.mass)
        new_v1t=v1t

        new_v1n_vec=np.dot(new_v1n,norm_vec)
        new_v1t_vec=np.dot(new_v1t,tang_vec)

        new_vec=np.add(new_v1n_vec,new_v1t_vec)
        
        # velocity for planet2
        new_v2n=((v2n*(planet2.mass-self.mass))+(2*self.mass*v1n))/(self.mass+planet2.mass)
        new_v2t=v2t

        new_v2n_vec=np.dot(new_v2n,norm_vec)
        new_v2t_vec=np.dot(new_v2t,tang_vec)

        new_vec1=np.add(new_v2n_vec,new_v2t_vec)


        # assigning new velocites
        self.x_vel=new_vec[0]
        self.y_vel=new_vec[1]
        planet2.x_vel=new_vec1[0]
        planet2.y_vel=new_vec1[1]


    def distance(self,planet2):
        diff_x=(planet2.x-self.x)**2 
        diff_y=(planet2.y-self.y)**2 
        diff=diff_x + diff_y
        dist=math.sqrt(diff)
        if dist <= self.r + planet2.r:
            self.handle_collision(planet2)
        
        return dist

    def force(self,planet2):
        dist=self.distance(planet2)
        total_force=(G * self.mass * planet2.mass)/dist**2
        
        a1=total_force/self.mass
        
        return a1

    def acc_comp(self,planet2):
        a1=self.force(planet2)

        diff_x=(planet2.x-self.x)
        diff_y=(planet2.y-self.y)
        

        if diff_x == 0:  # Planets have the same x-coordinate
            if diff_y > 0:  # Planet2 is above Planet1
                theta = math.pi/2
            else:
                theta = 3 * math.pi/2
        else:
            if diff_y==0 :
                if diff_x>0:
                    theta=0
                else:
                    theta=math.pi
            else:
                if diff_x>0:
                    theta=math.atan(diff_y/diff_x)
                else:
                    theta=math.atan(diff_y/diff_x) +math.pi

        
    
        a1x=a1 * math.cos(theta)
        a1y=a1 * math.sin(theta)
        

        self.x_vel= self.x_vel + (a1x * dt)
        self.y_vel= self.y_vel + (a1y * dt)
        
        self.x = self.x + (self.x_vel * dt) 
        self.y = self.y + (self.y_vel * dt)  
        self.orbit.append((self.x, self.y))  

def main():
    clock = pygame.time.Clock()
    running = True
	
    earth=Planet(-300,0,25,BLUE,EARTH_MASS)
    earth.x_vel=0
    earth.y_vel=-900

    mars=Planet(300,0,25,RED,MARS_MASS)
    # mars.x_vel= 10
    mars.y_vel=900
    mars.x_vel=0

    # mercury=Planet(350,200,25,RED,MERCURY_MASS)
    # mercury.y_vel=-500
    # mercury.x_vel=-50
    planets=[earth,mars]
    while running:
        # poll for events
        clock.tick(60)
        SCR.fill((0, 0, 0))
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the SCR with a color to wipe away anything from last frame
        

        # RENDER YOUR GAME HERE
        for planet in planets:
            planet.draw_planet(SCR)
            earth.acc_comp(mars)
            mars.acc_comp(earth)

        
        
        
        pygame.display.update()       
        
        
        # flip() the display to put your work on SCR
        

        # limits FPS to 60

    pygame.quit()

main()