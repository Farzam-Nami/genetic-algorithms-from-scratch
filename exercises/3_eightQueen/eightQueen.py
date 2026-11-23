import random
import numpy as np

queenCount=8
populationSize=20
parentsCount=20
population=[]
elitismPercent=0.01
elitesCount=max(1,round(elitismPercent*populationSize))
crossoverRate=0.9
mutationRate=0.01

#generating population
for i in range(populationSize):
    base=[i for i in range(queenCount)]
    random.shuffle(base)
    population.append(base)

def findMax(list):
    """Finds the index of the largest value in the supplied sequence."""
    max=0
    for i in range(len(list)):
        if list[i]>max:
            max=list[i]
            maxIndex=i
    return maxIndex 

def findMin(list):
    """Finds the index of the smallest value in the supplied sequence."""
    min=-1
    for i in range(len(list)):
        if (list[i]<min or min<0):
            min=list[i]
            minIndex=i
    return minIndex 
def chromosomeFitness(chromosome):
    """Counts the pairs of queens that do not attack one another."""
    fitness=0
    for i in range(len(chromosome)): #collumn=i,row=chromosome[i]
        for j in range(i+1,len(chromosome)):
            if(abs(i-j)!=abs(chromosome[i]-chromosome[j])):
                fitness+=1
    return fitness            
def printChessBoard(chromosome):
    """Prints an eight-by-eight board with queens at their encoded positions."""
    out=""
    for i in range(len(chromosome)):
        for j in range(len(chromosome)):
            if(chromosome[j]==i):
                out+=("x  ")
            else:
                out+=("-  ")
        out+='\n'
    print(out)            
def findElite(fitnessList,elitesCount):
    """Selects the indices of chromosomes with the highest fitness values."""
    global populationSize
    myfitnessList=np.copy(fitnessList)
    maxFitnessIndex=np.zeros(elitesCount)
    for i in range(elitesCount):
        maxFitnessIndex[i]=int(np.argmax(myfitnessList))
        myfitnessList[int(maxFitnessIndex[i])]=-1      
    return maxFitnessIndex
def crossover(Population,indexes,queenCount,rate):
    """Combines parent permutations while keeping each position value unique."""
    populationAfter=np.copy(Population)
    for i in range(len(indexes)):
        crossPoint=round(random.random()*(queenCount-1))
        parent1=Population[indexes[i][0]]
        parent2=Population[indexes[i][1]]
        child1=[None]*(queenCount)
        child2=[None]*(queenCount)
        if(random.random()>rate):
            child1=parent1
            child2=parent2
            continue
        child1[0:crossPoint]=parent1[0:crossPoint]
        for j in range(crossPoint,queenCount):
            for k in parent2:
                if(k not in child1):
                    child1[j]=k
                    break        
        child2[0:crossPoint]=parent2[0:crossPoint]
        for j in range(crossPoint,queenCount):
            for k in parent1:
                if(k not in child2):
                    child2[j]=k
                    break            
        populationAfter[(indexes[i])[0]]=child1
        populationAfter[(indexes[i])[1]]=child2
    return populationAfter
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
def mutate(population,rate,queenCount):
    """Randomly swaps two positions in selected chromosomes."""
    populationAfter=np.copy(population)
    mutationCount=1
    mutateIndex=np.zeros(mutationCount)
    for i in range(mutationCount):
        if(random.random()<rate):
            mutateIndex[i]=int(random.random()*len(population))
            chromosome=populationAfter[int(mutateIndex[i])]
            mutationPoint1=int(random.random()*queenCount)
            mutationPoint2=int(random.random()*queenCount)
            while(mutationPoint2==mutationPoint1):
                mutationPoint2=int(random.random()*queenCount)   
            tmp=chromosome[mutationPoint1]
            chromosome[mutationPoint1]=chromosome[mutationPoint2]
            chromosome[mutationPoint2]=tmp
            populationAfter[int(mutateIndex[i])]=chromosome      
    return populationAfter

def fitnessCalculator(population):
    """Calculates a fitness value for each chromosome in the population."""
    fitnessList=np.zeros(len(population))
    for i in range(len(population)):
        fitnessList[i]=chromosomeFitness(population[i])
    return fitnessList 

generation=0
noChange=0
while(True):
    populationFitness=fitnessCalculator(population)
    oldMax=max
    maxIndex=findMax(populationFitness)
    max=chromosomeFitness(population[maxIndex])

    
    if(noChange==1000):
            print("Chromosome: ",population[maxIndex])
            print("generation ",generation," best fitness:",max)
            printChessBoard(population[maxIndex])
            break
    if(generation==10000):
            print("Chromosome: ",population[maxIndex])
            print("generation ",generation," best fitness:",max)
            printChessBoard(population[maxIndex])
            break

    if(max==(queenCount*(queenCount-1)/2)):
        print("Chromosome: ",population[maxIndex])
        print("generation ",generation," best fitness:",max)
        printChessBoard(population[maxIndex])
        break
    if(max==oldMax):
            noChange+=1
    elif(max!=oldMax):
            noChange=0 

    eliteIndex=findElite(populationFitness,elitesCount)
    elites=[population[int(i)] for i in eliteIndex]

    selectedParentsIndex=parentSelection(populationFitness,parentsCount) 
    populationAfterCrossover=crossover(population,selectedParentsIndex,queenCount,crossoverRate) 

    populationAfterMutation=mutate(populationAfterCrossover,mutationRate,queenCount)

    populationAfterMutation=populationAfterMutation.tolist()
    population=populationAfterMutation
    populationFitness=fitnessCalculator(population)
    minIndex=findMin(populationFitness)
    population[minIndex]=elites[0]

    generation+=1