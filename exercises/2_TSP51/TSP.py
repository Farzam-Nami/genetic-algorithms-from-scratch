import math
import random
import numpy as np
from pathlib import Path

cityCount=51
populationSize=50
parentsCount=40
population=[]
elitismPercent=0.02
elitesCount=round(elitismPercent*populationSize)
crossoverRate=0.95
mutationRate=0.05

#generating population
for i in range(populationSize):
    base=[i for i in range(cityCount)]
    random.shuffle(base)
    population.append(base)

#open cities location file
citiesX=[]
citiesY=[]    
with open(Path(__file__).resolve().parent / "TSP51.txt") as file:
        for line in file:
            citiesX.append(int(line.split()[1]))
            citiesY.append(int(line.split()[2])) 


def findMin(list):
    """Finds the index of the smallest value in the supplied sequence."""
    min=-1
    for i in range(len(list)):
        if (list[i]<min or min<0):
            min=list[i]
            minIndex=i
    return minIndex  
def findMax(list):
    """Finds the index of the largest value in the supplied sequence."""
    max=0
    for i in range(len(list)):
        if list[i]>max:
            max=list[i]
            maxIndex=i
    return maxIndex  
def calculateDistance(city1,city2):
     """Calculates Euclidean distance between two cities using their coordinates."""
     global citiesX,citiesY
     distance=math.sqrt((citiesY[city1]-citiesY[city2])**2+(citiesX[city1]-citiesX[city2])**2)
     return distance
def shortestPath(chromosome):
    """Calculates the total length of a closed tour through the listed cities."""
    path=0
    for i in range(len(chromosome)):
        j=i+1
        if(j==len(chromosome)):
             j=0    
        path+=calculateDistance(chromosome[i],chromosome[j])    
    return path
def chromosomeFitness(chromosome):
    """Returns inverse closed-tour distance, favoring shorter routes."""
    fitness=0
    for i in range(len(chromosome)):
        j=i+1
        if(j==len(chromosome)):
             j=0    
        fitness+=calculateDistance(chromosome[i],chromosome[j])    
    return 1/fitness    
def fitnessCalculator(population):
    """Calculates a fitness value for each chromosome in the population."""
    fitnessList=np.zeros(len(population))
    for i in range(len(population)):
        fitnessList[i]=chromosomeFitness(population[i])
    return fitnessList 
def findElite(fitnessList,elitesCount):
    """Selects the indices of chromosomes with the highest fitness values."""
    global populationSize
    myfitnessList=np.copy(fitnessList)
    maxFitnessIndex=np.zeros(elitesCount)
    for i in range(elitesCount):
        maxFitnessIndex[i]=int(np.argmax(myfitnessList))
        myfitnessList[int(maxFitnessIndex[i])]=-1      
    return maxFitnessIndex
def rouletteWheel(list):
    """Converts fitness values into probabilities for roulette-wheel selection."""
    totalWeight=0
    weights=list
    for i in range(len(weights)):
        totalWeight+=weights[i]
    itemsProbability=np.zeros(len(list))
    for i in range(len(weights)):
        if(totalWeight==0):
            itemsProbability[i]=1/len(weights)
        else:
            itemsProbability[i]=weights[i]/totalWeight
    return itemsProbability    
def parentSelection(PopulationFitness,parentsCount):
    """Selects and pairs chromosomes for reproduction."""
    itemsProbability=rouletteWheel(PopulationFitness)
    lst=[i for i in range(len(PopulationFitness))]
    selectedIndexes= random.choices(lst, itemsProbability, k=parentsCount)   
    random.shuffle(selectedIndexes)     
    parents=[]
    for i in range(0,len(selectedIndexes),2):
        parents.append([int(selectedIndexes[i]),int(selectedIndexes[i+1])])
    return parents   
def crossover(Population,indexes,cityCount,rate):
    """Combines parent permutations while keeping each position value unique."""
    populationAfter=np.copy(Population)
    for i in range(len(indexes)):
        crossPoint=round(random.random()*(cityCount-1))
        parent1=Population[indexes[i][0]]
        parent2=Population[indexes[i][1]]
        child1=[None]*(cityCount)
        child2=[None]*(cityCount)
        if(random.random()>rate):
            child1=parent1
            child2=parent2
            continue
        child1[0:crossPoint]=parent1[0:crossPoint]
        for j in range(crossPoint,cityCount):
            for k in parent2:
                if(k not in child1):
                    child1[j]=k
                    break        
        child2[0:crossPoint]=parent2[0:crossPoint]
        for j in range(crossPoint,cityCount):
            for k in parent1:
                if(k not in child2):
                    child2[j]=k
                    break            
        populationAfter[(indexes[i])[0]]=child1
        populationAfter[(indexes[i])[1]]=child2
    return populationAfter    
def mutate(population,rate,cityCount):
    """Randomly swaps two positions in selected chromosomes."""
    populationAfter=np.copy(population)
    mutationCount=3
    mutateIndex=np.zeros(mutationCount)
    for i in range(mutationCount):
        if(random.random()<rate):
            mutateIndex[i]=int(random.random()*len(population))
            chromosome=populationAfter[int(mutateIndex[i])]
            mutationPoint1=int(random.random()*cityCount)
            mutationPoint2=int(random.random()*cityCount)
            while(mutationPoint2==mutationPoint1):
                mutationPoint2=int(random.random()*cityCount)   
            tmp=chromosome[mutationPoint1]
            chromosome[mutationPoint1]=chromosome[mutationPoint2]
            chromosome[mutationPoint2]=tmp
            populationAfter[int(mutateIndex[i])]=chromosome      
    return populationAfter

#starting main function
generation=0
noChange=0
while(True):
    populationFitness=fitnessCalculator(population)

    oldMax=max
    maxIndex=findMax(populationFitness)
    max=shortestPath(population[maxIndex])

    if(noChange==3000):
            print("Stopped because we have no change in output!")
            print("Shortest path: ",max)
            print("Chromosome: ",population[maxIndex])
            break
    if(generation==20000):
            print("Stopped because we reached limit in generation!")
            print("Shortest path: ",max)
            print("Chromosome: ",population[maxIndex])
            break
    
    print("generation ",generation,":",max)
    if(max==oldMax):
            noChange+=1
    elif(max!=oldMax):
            noChange=0 

    eliteIndex=findElite(populationFitness,elitesCount)
    elites=[population[int(i)] for i in eliteIndex]
    
    selectedParentsIndex=parentSelection(populationFitness,parentsCount) 
    populationAfterCrossover=crossover(population,selectedParentsIndex,cityCount,crossoverRate)

    populationAfterMutation=mutate(populationAfterCrossover,mutationRate,cityCount)

    populationAfterMutation=populationAfterMutation.tolist()
    population=populationAfterMutation
    populationFitness=fitnessCalculator(population)
    minIndex=findMin(populationFitness)
    population[minIndex]=elites[0]

    generation+=1
    