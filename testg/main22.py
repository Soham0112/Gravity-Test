import pygame
import math
import numpy as np

# pygame setup
pygame.init()
WID, HEI = 1000, 900
SCR = pygame.display.set_mode((WID, HEI))
pygame.display.set_caption("GRAVITY")

# Planets constants and values
BLUE = (100, 150, 250)
RED = (200, 30, 50)
YELLOW = (200, 200, 50)
G = 1e-11
EARTH_MASS = 5e+20
MARS_MASS = 5e+20
MERCURY_MASS = 8e+17
dt = 0.001

def nor_tang(vector1, vector2):
    sub_vec = np.subtract(vector2, vector1)
    unit_norm = sub_vec / np.linalg.norm(sub_vec)
    unit_tang = np.array([-unit_norm[1], unit_norm[0]])
    return unit_norm, unit_tang

# drawing planets based on one class planet.
class Planet:
    def __init__(self, x, y, r, color, mass, x_vel, y_vel):
        self.x = x 
        self.y = y 
        self.r = r
        self.color = color
        self.mass = mass
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.orbit = []

    def draw_planet(self, window):
        x = self.x + WID / 2
        y = HEI / 2 - self.y
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x  + WID / 2
                y = y  + HEI / 2
                updated_points.append((x, y))

            pygame.draw.lines(window, self.color, False, updated_points, 2)
        pygame.draw.circle(window, self.color, (int(x), int(y)), self.r)
        

    def update_position(self):
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt
        self.orbit.append((self.x, self.y))

# All the vector calculation will come under one class. Class Vector_cal:
class Vector_cal:
    def __init__(self):
        pass

    def distance(self, planet1, planet2):
        diff_x = (planet2.x - planet1.x) ** 2 
        diff_y = (planet2.y - planet1.y) ** 2 
        return diff_x + diff_y

    def acc_mag(self, planet1, planet2):
        dist = self.distance(planet1, planet2)
        a1 = (G * planet2.mass) / dist
        a2 = (G * planet1.mass) / dist
        return a1, a2
    
    def acc_comp(self, planet1, planet2):
        a1, a2 = self.acc_mag(planet1, planet2)
        diff_x = planet2.x - planet1.x
        diff_y = planet2.y - planet1.y
        
        theta = math.atan2(diff_y, diff_x)

        a1x = a1 * math.cos(theta)
        a1y = a1 * math.sin(theta)
        a2x = a2 * math.cos(theta + math.pi)
        a2y = a2 * math.sin(theta + math.pi)

        planet1.x_vel += a1x * dt
        planet1.y_vel += a1y * dt
        planet2.x_vel += a2x * dt  # Corrected from subtraction to addition
        planet2.y_vel += a2y * dt  # Corrected from subtraction to addition

def main():
    clock = pygame.time.Clock()
    running = True
	
    earth = Planet(0, 300, 25, BLUE, EARTH_MASS,800,0)
    mars = Planet(0, -300, 25, RED, MARS_MASS,-800,0)
    planets = [earth, mars]
    vector_cal = Vector_cal()

    while running:
        clock.tick(60)
        SCR.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Apply gravitational forces between each pair of planets
        vector_cal.acc_comp(earth, mars)
        # vector_cal.acc_comp(mars, earth)

        # Update position of each planet after computing new velocities
        for planet in planets:
            planet.update_position()
            planet.draw_planet(SCR)
        
        pygame.display.update()

    pygame.quit()

main()
