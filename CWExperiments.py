from os import times_result
from sympy import false
from simpleBot3 import *
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
#set of experiments for A-star
#input number of experiments
def runSetOfExperiments_aStar(numberOfRuns):
    dirtCollectedList = []
    computingTimeList = []
    for _ in range(numberOfRuns):
        dirtCollected, computingTime = aStarSearch_runOneExperiment()
        dirtCollectedList.append(dirtCollected)
        computingTimeList.append(computingTime)
    return dirtCollectedList,computingTimeList

#set of experiments for wandering solution
#input number of experiments        
def runSetOfExperiments_wandering(numberOfRuns):
    dirtCollectedList = []
    computingTimeList = []
    for _ in range(numberOfRuns):
        dirtCollected, computingTime = wandering_runOneExperiment()
        dirtCollectedList.append(dirtCollected)
        computingTimeList.append(computingTime)
    return dirtCollectedList,computingTimeList

#set of experiments for genetic algorithm
#input number of experiments
def runSetOfExperiments_genetic(populationSize,generationTimes,numberOfRuns):
    dirtCollectedList = []
    computingTimeList = []
    for _ in range(numberOfRuns):
        dirtCollected, computingTime = geneticSearch_runOneExperiment(populationSize,generationTimes)
        dirtCollectedList.append(dirtCollected)
        computingTimeList.append(computingTime)
    return dirtCollectedList,computingTimeList

#experiments one -- hyper parameters for genetic algorithm
#input total number of experiments
def generic_runExperimentsWithDifferentParameters(numberOfRuns):
    times_resultTable = {}
    dirt_resultsTable = {}
    print("start genetic searching round 1....")
    dirt_resultsTable["GA1"],times_resultTable["GA1"] = runSetOfExperiments_genetic(10,50,numberOfRuns)
    print("start genetic searching round 2....")
    dirt_resultsTable["GA2"],times_resultTable["GA2"] = runSetOfExperiments_genetic(20,70,numberOfRuns)
    print("start genetic searching round 3....")
    dirt_resultsTable["GA3"],times_resultTable["GA3"] = runSetOfExperiments_genetic(30,100,numberOfRuns)
    print("start genetic searching round 4....")
    dirt_resultsTable["GA4"],times_resultTable["GA4"] = runSetOfExperiments_genetic(50,200,numberOfRuns)
    dirt_results = pd.DataFrame(dirt_resultsTable)
    times_results = pd.DataFrame(times_resultTable)
    dirt_results.to_excel("dirt_genetic.xlsx")
    times_results.to_excel("time_genetic.xlsx")
    print("total dirt collected means: ")
    print(dirt_results.mean(axis=0))
    print("total computing time means: ")
    print(times_results.mean(axis=0))
    dirt_results.boxplot(grid=False)
    plt.show()
    times_results.boxplot(grid =False)
    plt.show()

# experiments two -- contrack 3 different algorithms (genetic, a* and wandering) all with 300 steps.
# input genetic population size and generation size, and total number of experiments
def runExperimentsMain(populationSize,generationTimes,numberOfRuns):
    print("Main experiment start:")
    times_resultTable = {}
    dirt_resultsTable = {}
    print("start aStar searching....")
    dirt_resultsTable["aStar"],times_resultTable["aStar"] = runSetOfExperiments_aStar(numberOfRuns)
    print("start wandering....")
    dirt_resultsTable["wandering"],times_resultTable["wandering"] = runSetOfExperiments_wandering(numberOfRuns)
    print("start genetic searching....")
    dirt_resultsTable["genetic"],times_resultTable["genetic"] = runSetOfExperiments_genetic(populationSize,generationTimes,numberOfRuns)
    dirt_results = pd.DataFrame(dirt_resultsTable)
    times_results = pd.DataFrame(times_resultTable)
    dirt_results.to_excel("dirt.xlsx")
    times_results.to_excel("time.xlsx")
    print(ttest_ind(dirt_results["aStar"],dirt_results["genetic"]))
    print("total dirt collected means: ")
    print(dirt_results.mean(axis=0))
    print("total computing time means: ")
    print(times_results.mean(axis=0))
    dirt_results.boxplot(grid=False)
    plt.show()
    times_results.boxplot(grid=False)
    plt.show()

# main function input the total numebr of experiments
def main(numberOfRuns):
    generic_runExperimentsWithDifferentParameters(numberOfRuns)
    runExperimentsMain(50,100,numberOfRuns)


main(2)


