from os import times_result
from simpleBot3 import *
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

def runSetOfExperiments_aStar(numberOfRuns):
    dirtCollectedList = []
    computingTimeList = []
    for _ in range(numberOfRuns):
        dirtCollected, computingTime = aStarSearch_runOneExperiment()
        dirtCollectedList.append(dirtCollected)
        computingTimeList.append(computingTime)
    return dirtCollectedList,computingTimeList
        
def runSetOfExperiments_wandering(numberOfRuns):
    dirtCollectedList = []
    computingTimeList = []
    for _ in range(numberOfRuns):
        dirtCollected, computingTime = wandering_runOneExperiment()
        dirtCollectedList.append(dirtCollected)
        computingTimeList.append(computingTime)
    return dirtCollectedList,computingTimeList

def runSetOfExperiments_genetic(populationSize,generationTimes,numberOfRuns):
    dirtCollectedList = []
    computingTimeList = []
    for _ in range(numberOfRuns):
        dirtCollected, computingTime = geneticSearch_runOneExperiment(populationSize,generationTimes)
        dirtCollectedList.append(dirtCollected)
        computingTimeList.append(computingTime)
    return dirtCollectedList,computingTimeList
#experiments one -- hyper parameters for genetic algorithm
def generic_runExperimentsWithDifferentParameters(numberOfRuns):
    times_resultTable = {}
    dirt_resultsTable = {}
    dirt_resultsTable["g=50"],times_resultTable["g=50"] = runSetOfExperiments_genetic(50,50,numberOfRuns)
    dirt_resultsTable["g=70"],times_resultTable["g=70"] = runSetOfExperiments_genetic(50,70,numberOfRuns)
    dirt_resultsTable["g=100"],times_resultTable["g=100"] = runSetOfExperiments_genetic(50,100,numberOfRuns)
    dirt_resultsTable["g=300"],times_resultTable["g=300"] = runSetOfExperiments_genetic(50,200,numberOfRuns)
    dirt_results = pd.DataFrame(dirt_resultsTable)
    times_results = pd.DataFrame(times_resultTable)
    print("total dirt collected means: ")
    print(dirt_results.mean(axis=0))
    print("total computing time means: ")
    print(times_results.mean(axis=0))
    dirt_results.boxplot(grid=False)
    plt.show()
# experiments two -- contrack 3 different algorithms (genetic, a* and wandering) all with 300 steps. 
def runExperimentsMain(populationSize,generationTimes,numberOfRuns):
    times_resultTable = {}
    dirt_resultsTable = {}
    dirt_resultsTable["aStar"],times_resultTable["aStar"] = runSetOfExperiments_aStar(numberOfRuns)
    dirt_resultsTable["wandering"],times_resultTable["wandering"] = runSetOfExperiments_wandering(numberOfRuns)
    dirt_resultsTable["genetic"],times_resultTable["genetic"] = runSetOfExperiments_genetic(populationSize,generationTimes,numberOfRuns)
    dirt_results = pd.DataFrame(dirt_resultsTable)
    times_results = pd.DataFrame(times_resultTable)
    print(dirt_results)
    print(times_results)
    dirt_results.to_excel("dirt.xlsx")
    times_results.to_excel("time.xlsx")
    print(ttest_ind(dirt_results["aStar"],dirt_results["genetic"]))
    print("total dirt collected means: ")
    print(dirt_results.mean(axis=0))
    print("total computing time means: ")
    print(times_results.mean(axis=0))
    dirt_results.boxplot(grid=False)
    plt.show()
#runExperimentsWithDifferentParameters()
#runSetOfExperiments_aStar(5)
#runExperimentsMain(5,10,10)
generic_runExperimentsWithDifferentParameters(10)