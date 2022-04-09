from asyncio.windows_events import NULL
from re import X
from unittest import result
from aStar import *
import tkinter as tk
import random
import math
import numpy as np
import sys
import time


class Counter:
    def __init__(self,canvas):
        self.dirtCollected = 0
        self.canvas = canvas
        self.canvas.create_text(70,50,text="Dirt collected: "+str(self.dirtCollected),tags="counter")
        
    def itemCollected(self, canvas):
        self.dirtCollected +=1
        self.canvas.itemconfigure("counter",text="Dirt collected: "+str(self.dirtCollected))


class Bot:

    def __init__(self,namep,canvasp):
        self.x = 950
        self.y = 950
        self.theta = -3.0*math.pi/4.0
        #self.theta = 0
        self.name = namep
        self.ll = 60 #axle width
        self.vl = 0.0
        self.vr = 0.0
        self.turning = 0
        self.moving = random.randrange(50,100)
        self.currentlyTurning = False
        self.canvas = canvasp

    def draw(self,canvas):
        points = [ (self.x + 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x + 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta)  \
                ]
        canvas.create_polygon(points, fill="blue", tags=self.name)

        self.sensorPositions = [ (self.x + 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y - 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                                 (self.x - 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y + 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta)  \
                            ]
    
        centre1PosX = self.x 
        centre1PosY = self.y
        canvas.create_oval(centre1PosX-15,centre1PosY-15,\
                           centre1PosX+15,centre1PosY+15,\
                           fill="gold",tags=self.name)

        wheel1PosX = self.x - 30*math.sin(self.theta)
        wheel1PosY = self.y + 30*math.cos(self.theta)
        canvas.create_oval(wheel1PosX-3,wheel1PosY-3,\
                                         wheel1PosX+3,wheel1PosY+3,\
                                         fill="red",tags=self.name)

        wheel2PosX = self.x + 30*math.sin(self.theta)
        wheel2PosY = self.y - 30*math.cos(self.theta)
        canvas.create_oval(wheel2PosX-3,wheel2PosY-3,\
                                         wheel2PosX+3,wheel2PosY+3,\
                                         fill="green",tags=self.name)

        sensor1PosX = self.sensorPositions[0]
        sensor1PosY = self.sensorPositions[1]
        sensor2PosX = self.sensorPositions[2]
        sensor2PosY = self.sensorPositions[3]
        canvas.create_oval(sensor1PosX-3,sensor1PosY-3, \
                           sensor1PosX+3,sensor1PosY+3, \
                           fill="yellow",tags=self.name)
        canvas.create_oval(sensor2PosX-3,sensor2PosY-3, \
                           sensor2PosX+3,sensor2PosY+3, \
                           fill="yellow",tags=self.name)
        
    # cf. Dudek and Jenkin, Computational Principles of Mobile Robotics
    def move(self,canvas,registryPassives,dt):
        if self.vl==self.vr:
            R = 0
        else:
            R = (self.ll/2.0)*((self.vr+self.vl)/(self.vl-self.vr))
        omega = (self.vl-self.vr)/self.ll
        ICCx = self.x-R*math.sin(self.theta) #instantaneous centre of curvature
        ICCy = self.y+R*math.cos(self.theta)
        m = np.matrix( [ [math.cos(omega*dt), -math.sin(omega*dt), 0], \
                        [math.sin(omega*dt), math.cos(omega*dt), 0],  \
                        [0,0,1] ] )
        v1 = np.matrix([[self.x-ICCx],[self.y-ICCy],[self.theta]])
        v2 = np.matrix([[ICCx],[ICCy],[omega*dt]])
        newv = np.add(np.dot(m,v1),v2)
        newX = newv.item(0)
        newY = newv.item(1)
        newTheta = newv.item(2)
        newTheta = newTheta%(2.0*math.pi) #make sure angle doesn't go outside [0.0,2*pi)
        self.x = newX
        self.y = newY
        self.theta = newTheta        
        if self.vl==self.vr: # straight line movement
            self.x += self.vr*math.cos(self.theta) #vr wlog
            self.y += self.vr*math.sin(self.theta)
        if self.x<0.0:
            self.x=999.0
        if self.x>1000.0:
            self.x = 0.0
        if self.y<0.0:
            self.y=1000.0
        if self.y>999.0:
            self.y = 0.0
        canvas.delete(self.name)
        self.draw(canvas)
        
    def distanceTo(self,obj):
        xx,yy = obj.getLocation()
        return math.sqrt( math.pow(self.x-xx,2) + math.pow(self.y-yy,2) )
    
    def distanceToRightSensor(self,lx,ly):
        return math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) + \
                          (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )

    def distanceToLeftSensor(self,lx,ly):
        return math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) + \
                            (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )

    def collectDirt(self, canvas, registryPassives, count):
        toDelete = []
        for idx,rr in enumerate(registryPassives):
            if isinstance(rr,Dirt):
                if self.distanceTo(rr)<30:
                    canvas.delete(rr.name)
                    toDelete.append(idx)
                    count.itemCollected(canvas)
        for ii in sorted(toDelete,reverse=True):
            del registryPassives[ii]
        return registryPassives

    def transferFunction(self,path):
            if not path:
                return 
            target = (path[0][0]*100 +50,path[0][1]*100+50)
            chargerR = self.distanceToRightSensor(target[0],target[1])
            chargerL = self.distanceToLeftSensor(target[0],target[1])
            
            if chargerR>chargerL:
                self.vl = 2.0
                self.vr = -2.0
            elif chargerR<chargerL:
                self.vl = -2.0
                self.vr = 2.0
            if abs(chargerR-chargerL)<chargerL*0.01: #approximately the same
                self.vl = 5.0
                self.vr = 5.0
            if chargerL<=200.0:
                path.pop(0)
            
    def wandering_transferFunction(self):
        # wandering behaviour
        if self.currentlyTurning==True:
            self.vl = -2.0
            self.vr = 2.0
            self.turning -= 1
        else:
            self.vl = 5.0
            self.vr = 5.0
            self.moving -= 1
        if self.moving==0 and not self.currentlyTurning:
            self.turning = random.randrange(20,40)
            self.currentlyTurning = True
        if self.turning==0 and self.currentlyTurning:
            self.moving = random.randrange(50,100)
            self.currentlyTurning = False
class Dirt:
    def __init__(self,namep,xx,yy):
        self.centreX = xx
        self.centreY = yy
        self.name = namep

    def draw(self,canvas):
        body = canvas.create_oval(self.centreX-1,self.centreY-1, \
                                  self.centreX+1,self.centreY+1, \
                                  fill="grey",tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY

def buttonClicked(x,y,registryActives):
    for rr in registryActives:
        if isinstance(rr,Bot):
            rr.x = x
            rr.y = y

def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=1000,height=1000)
    canvas.pack()
    return canvas

def placeDirt(registryPassives,canvas):
    #places dirt in a specific configuration
    map = np.zeros( (10,10), dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
                map[xx][yy] = random.randrange(1,3)
    for yy in range(0,10):
        map[8][yy] = 10
    for xx in range(1,8):
        map[xx][0] = 10
    map[0][0] = 1
    map[9][9] = 0
    i = 0
    for xx in range(10):
        for yy in range(10):
            for _ in range(map[xx][yy]):
                dirtX = xx*100 + random.randrange(0,99)
                dirtY = yy*100 + random.randrange(0,99)
                dirt = Dirt("Dirt"+str(i),dirtX,dirtY)
                registryPassives.append(dirt)
                dirt.draw(canvas)
                i += 1
    #print(np.transpose(map))
    return map

def register(canvas):
    registryActives = []
    registryPassives = []
    noOfBots = 1
    for i in range(0,noOfBots):
        bot = Bot("Bot"+str(i),canvas)
        registryActives.append(bot)
        bot.draw(canvas)
    map = placeDirt(registryPassives,canvas)
    count = Counter(canvas)
    canvas.bind( "<Button-1>", lambda event: buttonClicked(event.x,event.y,registryActives) )
    return registryActives, registryPassives, count, map

def moveIt(canvas,registryActives,registryPassives,count,moves,window,path):
    moves += 1
    for rr in registryActives:
        rr.transferFunction(path)
        rr.move(canvas,registryPassives,1.0)
        registryPassives = rr.collectDirt(canvas,registryPassives, count)
        numberOfMoves = 300
        if moves>numberOfMoves:
            print("total dirt collected in",numberOfMoves,"moves is",count.dirtCollected)
            window.destroy()
            return
        if not path:
            print("total dirt collected in",moves,"moves is",count.dirtCollected)
            window.destroy()
            return
    canvas.after(1,moveIt,canvas,registryActives,registryPassives,count,moves,window,path)

def aStar_moveIt(canvas,registryActives,registryPassives,count,moves,window,path):
    moves += 1
    for rr in registryActives:
        rr.transferFunction(path)
        rr.move(canvas,registryPassives,1.0)
        registryPassives = rr.collectDirt(canvas,registryPassives, count)
        numberOfMoves = 2000
        if moves>numberOfMoves:
            print("total dirt collected in",numberOfMoves,"moves is",count.dirtCollected)
            window.destroy()
            return
        if not path:
            print("total dirt collected in",moves,"moves is",count.dirtCollected)
            window.destroy()
            return
    canvas.after(20,aStar_moveIt,canvas,registryActives,registryPassives,count,moves,window,path)

def wandering_moveIt(canvas,registryActives,registryPassives,count,moves,window):
    moves += 1
    for rr in registryActives:
        rr.wandering_transferFunction()
        rr.move(canvas,registryPassives,1.0)
        registryPassives = rr.collectDirt(canvas,registryPassives, count)
        numberOfMoves = 2000
        if moves>numberOfMoves:
            print("total dirt collected in",numberOfMoves,"moves is",count.dirtCollected)
            window.destroy()
            return
    canvas.after(20,wandering_moveIt,canvas,registryActives,registryPassives,count,moves,window)


def createOneRandomPath():
    totalSteps = 15
    allCoordinates = []
    path = []
    path.append( (9,9) )
    for xx in range(10):
        for yy in range(10):
            allCoordinates.append((xx,yy))
    index = random.sample(range(1, 99), totalSteps-2)
    for x in index:
        path.append(allCoordinates[x])
    path.append( (0,0) )
    return path

def createRandomPath():
    totalSteps = 19
    path = []
    path.append( (9,9) )
    currentPosition = (9,9)
    while currentPosition != (0,0):
        if currentPosition[0]>0:
            possPosition1x = currentPosition[0]-1
            possPosition1y = currentPosition[1]
            pos1 = True
        if currentPosition[1]>0:
            possPosition2x = currentPosition[0]
            possPosition2y = currentPosition[1]-1
            pos2 = True
        pos1Bigger = random.random()>=0.5
        if (pos1 and not pos2) or (pos1 and pos2 and pos1Bigger):
            path.append( (possPosition1x,possPosition1y) )
            currentPosition = (possPosition1x,possPosition1y)
        if (pos2 and not pos1) or (pos1 and pos2 and not pos1Bigger):
            path.append( (possPosition2x,possPosition2y) )
            currentPosition = (possPosition2x,possPosition2y)
        pos1 = False
        pos2 = False
    print(path)
    #path.append( (0,0) )
    return path


def PMX(parent1,parent2):
    list1 = parent1[0].copy()
    list2 = parent2[0].copy()
    status = True
    while status:
        k1 = random.randint(1, len(list1) - 2)
        k2 = random.randint(1, len(list2) - 2)
        if k1 < k2:
            status = False
    k11 = k1
    k22 = k1
    fragment1 = list1[k1: k2]
    fragment2 = list2[k1: k2]
    list1[k1: k2] = fragment2
    list2[k1: k2] = fragment1
    del list1[k1: k2]
    left1 = list1
    offspring1List = []
    for pos in left1:
        if pos in fragment2:
            pos = fragment1[fragment2.index(pos)]
            while pos in fragment2:
                pos = fragment1[fragment2.index(pos)]
            offspring1List.append(pos)
            continue
        offspring1List.append(pos)
    for i in range(0, len(fragment2)):
        offspring1List.insert(k11, fragment2[i])
        k11 += 1
    del list2[k1: k2]
    left2 = list2
    offspring2List = []
    for pos in left2:
        if pos in fragment1:
            pos = fragment2[fragment1.index(pos)]
            while pos in fragment1:
                pos = fragment2[fragment1.index(pos)]
            offspring2List.append(pos)
            continue
        offspring2List.append(pos)
    for i in range(0, len(fragment1)):
        offspring2List.insert(k22, fragment1[i])
        k22 += 1
    offspring1 = (offspring1List.copy(),getDirtPoint(offspring1List))
    offspring2 = (offspring2List.copy(),getDirtPoint(offspring2List))
    return offspring1,offspring2

def inversion_Mutation(offspring):
    Pm = 0.1
    ret = random.random()
    list1 = offspring[0].copy()
    Score1 = offspring[1]
    finallist = list1.copy()
    if ret >= Pm :
        return (finallist,Score1)
    status = True
    while status:
        k1 = random.randint(1, len(list1) - 2)
        k2 = random.randint(1, len(list1) - 2)
        if k1 < k2:
            status = False
    finallist[k1] = list1[k2]
    finallist[k2] = list1[k1]
    finalResult = (finallist.copy(),getDirtPoint(finallist))
    return finalResult

def getDirtPoint(candidatePath):
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, map = register(canvas)
    moves = 0
    moveIt(canvas,registryActives,registryPassives, count, moves, window,candidatePath)
    window.withdraw()
    window.mainloop()
    return count.dirtCollected

def geneticSearch():
    print("start genetic searching....")
    candidatePaths = []
    #generate random paths (5-10 random solutions, each got 20 steps from (9,9) to (0,0) randomly)
    for i in range(50):
        #tempPath = createOneRandomPath()
        tempPath = createRandomPath()
        print(tempPath)
        tempScore =  getDirtPoint(tempPath.copy())
        print(tempScore)
        candidatePaths.append((tempPath,tempScore))
    # main generations(input rounds)
    for i in range(10):
        print("current generation round: " + str(i)) 
        #rank all cadidate solutions
        candidatePaths.sort(key=lambda tuple: tuple[1], reverse=True)
        #choose best of 2 as populations(parents)
        parent_index1 = 0
        parent_index2 = 1
        parent1 = candidatePaths[parent_index1]
        parent2 = candidatePaths[parent_index2]
        # cross over(PMX) --got child1 & child2
        offspring1,offspring2 = PMX(parent1,parent2)
        # inversion_Mutation for each child(pm = 0.2)
        offspring11 = inversion_Mutation(offspring1)
        offspring22 = inversion_Mutation(offspring2)
        # rank 2 parents and 2 children (4 paths)
        currentList = [parent1,parent2,offspring11,offspring22]
        currentList.sort(key=lambda tuple: tuple[1], reverse=True)
        # 2 bests solutions replace worst 2 of the candidate solutions(Steady-State strong elitism)
        candidatePaths[-1] = currentList[0]
        candidatePaths[-2] = currentList[1]   
    candidatePaths.sort(key=lambda tuple: tuple[1], reverse=True)    
    #return the best_path
    return candidatePaths[0][0]

def aStarSearch_runOneExperiment():
    start_time = time.time()
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, map = register(canvas)
    moves = 0
    path = aStarSearch(map)
    aStar_moveIt(canvas,registryActives,registryPassives, count, moves, window,path)
    window.mainloop()
    computation_time = time.time() - start_time
    print("computation time; "+ str(computation_time)) 
    return count.dirtCollected

def geneticSearch_runOneExperiment():
    path = geneticSearch()
    start_time = time.time()
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, map = register(canvas)
    moves = 0
    moveIt(canvas,registryActives,registryPassives, count, moves, window,path)
    window.mainloop()
    computation_time = time.time() - start_time
    print("computation time: "+ str(computation_time))
    return count.dirtCollected

def wandering_runOneExperiment():
    start_time = time.time()
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, map = register(canvas)
    moves = 0
    wandering_moveIt(canvas,registryActives,registryPassives, count, moves, window)
    window.mainloop()
    computation_time = time.time() - start_time
    print("computation time: "+ str(computation_time))
    return count.dirtCollected

geneticSearch_runOneExperiment()
#aStarSearch_runOneExperiment()
#wandering_runOneExperiment()