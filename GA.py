import random
from simpleBot3 import getDirtPoint
def createOneRandomPath():
    totalSteps = 20
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

def PMX():
    list1 = [(1,2),(1,4),(9,0),(6,1),(7, 1),(5, 2)]
    list2 = [(1,2),(1,4),(8,1),(4,7),(5, 8),(5, 2)]
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
    offspring1 = []
    for pos in left1:
        if pos in fragment2:
            pos = fragment1[fragment2.index(pos)]
            while pos in fragment2:
                pos = fragment1[fragment2.index(pos)]
            offspring1.append(pos)
            continue
        offspring1.append(pos)
    for i in range(0, len(fragment2)):
        offspring1.insert(k11, fragment2[i])
        k11 += 1
    del list2[k1: k2]
    left2 = list2
    offspring2 = []
    for pos in left2:
        if pos in fragment1:
            pos = fragment2[fragment1.index(pos)]
            while pos in fragment1:
                pos = fragment2[fragment1.index(pos)]
            offspring2.append(pos)
            continue
        offspring2.append(pos)
    for i in range(0, len(fragment1)):
        offspring2.insert(k22, fragment1[i])
        k22 += 1
    return offspring1,offspring2

def inversion_Mutation():
    list1 = [(1,2),(1,4),(9,0),(6,1),(7, 1),(5, 2)]
    finallist = list1.copy()
    status = True
    while status:
        k1 = random.randint(1, len(list1) - 2)
        k2 = random.randint(1, len(list1) - 2)
        if k1 < k2:
            status = False
    print(k1, k2)
    finallist[k1] = list1[k2]
    finallist[k2] = list1[k1]
    print(finallist)


def geneticSearch():
    #generate random paths (10 random solutions, each got 20 steps from (9,9) to (0,0) )
    candidatePaths = []
    for i in range(5):
        tempPath = createOneRandomPath()
        print(tempPath)
        tempScore =  getDirtPoint(tempPath.copy())
        print(tempScore)
        candidatePaths.append((tempPath,tempScore))
    #best_solution = (best_path, best_dirt_point) 
    ##############  for loop (100 times)
    #random choose 2 as populations
    # get dirt_point for each one(def a function with a path input and reutrn the dirt_collected)
    # cross over(PMX) --got child1 & child2
    # inversion_Mutation for each child 
    # get dirt_point for each (4 paths)
    # 2 bests solutions go to the next generation
    #if the best one >= current best solution  -----  best_solution changed 
    ##############

    #finaly return the best_path
    print(candidatePaths)   

getDirtPoint(createOneRandomPath())

#geneticSearch()