import sys, pygame
from time import sleep
from random import randint, random, uniform
import math
import matplotlib.pyplot as plt
import numpy as np
agents = []
"""
    activityRad: radius of activity circle
    infectionRad: radius of infection circle
    infectionChance: chance of infection every n ticks
    recoveryChance: arbritary recovery change every n ticks
"""
activityRad = 15
infectionRad = 15
infectionChance = 0.1
recoveryChance = 0.001
deathChance = 0.000
population = 600

pygame.init()
done = False
gamespeed = 0.001
size = 500
speed = 2
screen = pygame.display.set_mode((size, size))

#stats
recovered = [0]
died = [0]
infected = [0]
susceptible = [population]



class human:
    """
    status: 0-vunrable, 1-infected, 2-recovered
    initialPos: initial xy
    currentPos: current xy

    """

    def __init__(self, initialPos):
        self.status = 0
        self.initialPos = initialPos
        self.currentPos = initialPos.copy()
        self.moveAngle = uniform(0, math.pi * 2)

    # function to infect agent if they are susceptable and within range 25% of the time
    def infect(self):
        for i in agents:
            if self.status == 1 and i.status == 0 and math.sqrt((i.currentPos[0] - self.currentPos[0]) ** 2 + (
                    i.currentPos[1] - self.currentPos[1]) ** 2) < infectionRad and random() < infectionChance:
                i.status = 1
                infected[-1] += 1
                susceptible[-1] -= 1
    def recover(self):
        if random() < recoveryChance and self.status == 1:
            self.status = 2
            recovered[-1] += 1
            infected[-1] -=1
    def die(self):
        if random() < deathChance and self.status == 1:
            agents.remove(self)
            died[-1] += 1
            infected[-1] -= 1
    def update(self):
        if math.sqrt((self.currentPos[0] - self.initialPos[0]) ** 2 + (
                self.currentPos[1] - self.initialPos[1]) ** 2) > activityRad:
            self.currentPos = self.initialPos.copy()
            self.moveAngle = self.moveAngle = uniform(0, math.pi * 2)
        elif self.currentPos == self.initialPos:
            self.moveAngle = uniform(0, math.pi * 2)
        self.currentPos[0] += int((speed * math.cos(self.moveAngle)))
        self.currentPos[1] += int((speed * math.sin(self.moveAngle)))
        if self.status == 0:
            color = (104, 238, 33)
        elif self.status == 1:
            color = (238, 57, 32)
        else:
            color = (230, 231, 208)
        pygame.draw.circle(screen, color, (self.currentPos[0], self.currentPos[1]), int(size / 200))


# initialise agents list
for i in range(population):
    agents.append(human([randint(0, size), randint(0, size)]))

clock = 0
log = 50
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
        if event.type == pygame.KEYDOWN:
            print(1)
            if event.key == pygame.K_SPACE:
                agents[randint(0, len(agents) - 1)].status = 1
    if len(susceptible) > 130:
        done = True

    screen.fill((0, 0, 0))
    activityRad = int((susceptible[-1]/ population) * 15)
    print(activityRad)
    for i in agents:
        i.update()
        i.infect()
        i.recover()
        i.die()
    if not(clock%log):
        susceptible.append(susceptible[-1])
        recovered.append(recovered[-1])
        died.append(died[-1])
        infected.append(infected[-1])
        print(susceptible)
        print(recovered)
        print(died)
        print(infected)
    clock += 1
    sleep(gamespeed)
    pygame.display.update()

plt.plot(recovered, label='Recovered', color = "cyan")
plt.plot(died, label= "deaths", color = "black")
plt.plot(susceptible, label = "susceptible", color = "green")
plt.plot(infected, label = "infected", color = "red")
plt.xlabel("Time")
plt.legend(loc="upper right")

plt.show()