import pygame,math,random
pygame.init()
G=0.00001
height=700
width=1300
fps=30
frame=0.1
disp= pygame.display.set_mode((width,height))
pygame.display.update()
pygame.display.set_caption("Let's predict the Universe")
clock = pygame.time.Clock()
state = True

#pygame.draw.circle(disp,(255,0,255),(400,300),5,0)

disp.fill((0,0,0))
#pygame.draw.circle(disp,(255,255,255),[400,300],10,0)
pygame.display.update()
planets=list()
MaxMass=10000
MinMass=200
MassScale=(MinMass/MaxMass)/30
class planet():
    def __init__(self,x,y,mass,diameter):
        self.x=x
        self.y=y
        self.m=mass
        self.d=diameter
        self.dx=0
        self.dy=0
#         self.density=mass/(math.pi*((diameter/2)**2))
#         self.r=int(self.density*MassScale*255)
#         self.g=int(((self.density*MassScale))*255)
#         self.b=int(((self.density*MassScale))*255)
        
        #self.color=(self.r,self.g,self.b)
        self.color=(255,255,255)
        #print(float(self.density*MassScale))
    def draw(self):
        self.x+=self.dx*frame*10
        self.y+=self.dy*frame*10
        
        pygame.draw.circle(disp,self.color,(self.x+self.dx,height-self.y+self.dy),self.d,0)


# p1=planet(300,200,5000,10)
# p1.dx=-0.01
# p2=planet(200,300,5000,10)
# p2.dx=0.01
# 
# planets.append(p1)
# planets.append(p2)

for i in range(100):
    p=planet(random.randint(50,width-50),random.randint(50,height-50),random.randint(1000,10000),5)
    planets.append(p)
def R_area(p,q):
    area = (p.d**2/4)*math.pi+(q.d**2/4)*math.pi
    return area
def collision(p,q):
    mass=p.m+q.m
    x = ((p.x) + (q.x))/2
    y = ((p.y) + (q.y))/2
    #x=cx/mass
    #y=cy/mass
    dx=(((p.dx*p.m)+(q.dx*q.m))/mass)
    dy=((p.dy*p.m)+(q.dy*q.m))/mass
    
    d=math.sqrt(R_area(p,q)*4/math.pi)

#     planets.remove(p)
#     planets.remove(q)
    np=planet(x,y,mass,d)
    np.dx=dx
    np.dy=dy
    planets.append(np)
    #np.draw()
    
def ds(p,q):
    distance_squared= math.sqrt((p.x-q.x)**2+(p.y-q.y)**2)
    if distance_squared >= (p.d+q.d)**2:
        return distance_squared
    else:
        collision(p,q)
        return 0
def force(p,q):
    distance=ds(p,q)
    if distance != 0:
        force=-p.m*q.m*G/distance
        return force
    else:
        return 0
def acc(p,q):
    f=force(p,q)
    if f !=0:
        acc=f/p.m
        #print(acc)
        return acc
    else:
        return 0
def angle(p,q):
    if p.x==q.x and p.y>q.y:
        angle=math.pi/2
    elif p.x==q.x and p.y<q.y:
        angle=math.pi*3/2
    else:
        angle=math.atan((p.y-q.y)/(p.x-q.x))
    #print(angle)
    return angle
def comp(p,q):#this diviede acc into x and y comp
    a=acc(p,q)
    if a ==0:
        planets.remove(p)
        planets.remove(q)
    else:
        if p.x<q.x:
            p.dx-=a*math.cos(angle(p,q))
            p.dy-=a*math.sin(angle(p,q))
        else:
            p.dx+=a*math.cos(angle(p,q))
            p.dy+=a*math.sin(angle(p,q))
count=0
while state:
    count+=1
    #no of frames to skip
    c=count%10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = False
    #calculating part
    for rp in planets:
        for p in planets:
            if rp != p:
                comp(rp,p)
            if rp not in planets:
                break
    #drawing part
    if c ==0:
        disp.fill((0,0,0))
        for g in planets:
            g.draw()
    pygame.display.update()
    #clock.tick(fps)
    if count ==1000:
        state=False
pygame.quit()