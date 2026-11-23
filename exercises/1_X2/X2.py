import random

import numpy as np
bits=8
searchSpaceSize = 2**bits

populationSize = 31
population=[]
elitismRate=0.02
elitesCount=round(elitismRate*populationSize)
crossoverRate=0.8
mutationRate=0.02

# Generate chromosomes represented by integers from 0 to 255.
for _ in range(populationSize):
    population.append(random.randrange(searchSpaceSize))

def findMax(population):
    """Returns the largest value in the current population."""
    max=0
    for i in range(len(population)):
        if population[i]>max:
            max=population[i]
    return max        
def fitnessCalculator(population):
    """Calculates a fitness value for each chromosome in the population."""
    fitnessList=np.zeros(len(population))
    for i in range(len(population)):
        fitnessList[i]=population[i]*population[i]
    return fitnessList 
   
def findElite(fitnessList,elitesCount):
    """Selects the indices of chromosomes with the highest fitness values."""
    global populationSize
    maxFitnessIndex=np.zeros(elitesCount)
    for i in range(elitesCount):
        maxFitnessIndex[i]=int(np.argmax(fitnessList))
        fitnessList[int(maxFitnessIndex[i])]=-1      
    return maxFitnessIndex

def binaryEncode(decimalList):
    """Represents each decimal chromosome as an eight-bit binary string."""
    binaryList=[]
    for i in range(len(decimalList)):
        binaryList.append(format(decimalList[i],'08b'))
    return binaryList

def decimal(binaryList):
    """Converts binary chromosome strings back to decimal values."""
    decimalList=[]
    for i in range(len(binaryList)):
        decimalList.append(int(binaryList[i],2))
    return decimalList   

def rouletteWheel(list):
    """Converts fitness values into probabilities for roulette-wheel selection."""
    totalWeight=0
    weights=fitnessCalculator(list)
    for i in range(len(weights)):
        totalWeight+=weights[i]
    itemsProbability=np.zeros(len(list))
    for i in range(len(weights)):
        if(totalWeight==0):
            itemsProbability[i]=1/len(weights)
        else:
            itemsProbability[i]=weights[i]/totalWeight
    return itemsProbability    
          

def parentSelection(noElitePopulation,parentsCount):
    """Selects and pairs chromosomes for reproduction."""
    population=np.copy(noElitePopulation)
    selectedIndexes=np.zeros(parentsCount)
    for j in range(parentsCount):
        itemsProbability=rouletteWheel(population)
        parent=(random.random())
        lowerBound=0
        upperBound=0
        for i in range(len(itemsProbability)):
            upperBound+=itemsProbability[i] 
            if (parent>=lowerBound and parent<upperBound):
                selectedIndexes[j]=(i)
                break
            lowerBound+=itemsProbability[i]
        population[int(selectedIndexes[j])]=0
    random.shuffle(selectedIndexes)     
    parents=[]
    for i in range(0,len(selectedIndexes),2):
        parents.append([int(selectedIndexes[i]),int(selectedIndexes[i+1])])

    return parents     
  
def crossover(encodedPopulation,indexes,bits):
    """Combines parent chromosomes at a crossover point."""
    populationAfter=np.copy(encodedPopulation)

    for i in range(len(indexes)):
        crossPoint=round(random.random()*(bits-1))
        parent1=encodedPopulation[indexes[i][0]]
        parent2=encodedPopulation[indexes[i][1]]
        child1=[0]*bits
        child2=[0]*bits
        child1[0:crossPoint]=parent1[0:crossPoint]
        child1[crossPoint:]=parent2[crossPoint:]
        child2[0:crossPoint]=parent2[0:crossPoint]
        child2[crossPoint:]=parent1[crossPoint:]
        populationAfter[(indexes[i])[0]]=(''.join(child1))
        populationAfter[(indexes[i])[1]]=(''.join(child2))

    return populationAfter    
def mutate(population,rate,bits):
    """Applies random mutations to selected chromosomes."""
    populationAfter=np.copy(population)
    mutationCount=round(rate*len(population))
    mutateIndex=np.zeros(mutationCount)
    for i in range(mutationCount):
        mutateIndex[i]=int(random.random()*len(population))
        chromosome=list(populationAfter[int(mutateIndex[i])])
        mutationPoint=int(random.random()*bits)
        if(int(chromosome[mutationPoint])==0):
            chromosome[mutationPoint]='1'
        else:
            chromosome[mutationPoint]='0'
        populationAfter[int(mutateIndex[i])]=''.join(chromosome)      

    return populationAfter
             
generation=0
noChange=0
while(True):
    if(noChange==20):
        print("Stopped because no change in output!\nFinal output:",oldMax)
        break
    if(generation==50):
        print("Stopped because generation reached limit!\nFinal output:",oldMax)
        break
    #calculate fitness
    populationFitness=fitnessCalculator(population)
    oldMax=max
    max=findMax(populationFitness)
    print("generation ",generation,":",max)
    if(max==oldMax):
        noChange+=1
    elif(max!=oldMax):
        noChange=0
    #finding elite(s) in population   
    eliteIndex=findElite(populationFitness,elitesCount)
    elites=[population[int(i)] for i in eliteIndex]
    noElitePopulation=np.delete(population,[int(i) for i in eliteIndex]) 
    noElitePopulationEncoded=binaryEncode(noElitePopulation)

    # Roulette-wheel selection followed by one-point crossover.
    parentsCount=int((len(noElitePopulationEncoded)*crossoverRate)//2)*2
    selectedParentsIndex=parentSelection(noElitePopulation,parentsCount)
    populationAfterCrossover=crossover(noElitePopulationEncoded,selectedParentsIndex,bits)

    # Flip a randomly selected bit in selected chromosomes.
    populationAfterMutation=mutate(populationAfterCrossover,mutationRate,bits)

    populationAfterDecimal=decimal(populationAfterMutation)
    population[0:elitesCount]=elites
    population[elitesCount:]=populationAfterDecimal
    
    generation+=1
    

