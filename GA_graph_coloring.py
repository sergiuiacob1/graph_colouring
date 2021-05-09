import networkx as nx
import random
import numpy as np
import copy

def getFitness(graph: nx.Graph, chromosome: list):
    numColors = len(set(chromosome))
    totalFitness = graph.number_of_nodes()*numColors
    for edge in graph.edges():
        if chromosome[edge[0]]==chromosome[edge[1]]:
            totalFitness+=graph.number_of_nodes()
    if totalFitness==graph.number_of_nodes()*numColors:
        return totalFitness, True
    return totalFitness, False


def mutation(graph, chromosome, fitness, feasible):
    if feasible==False:
        bestChromosome=[]
        bestFitness = -1
        colors = set(chromosome)
        for edge in graph.edges():
            if chromosome[edge[0]]==chromosome[edge[1]]:
                for color in colors:
                    if color!=chromosome[edge[0]]:
                        newChromosome = chromosome
                        newChromosome[edge[0]]=color
                        newFitness=getFitness(graph,newChromosome)[0]
                        if newFitness<bestFitness or bestFitness==-1:
                            bestFitness = newFitness
                            bestChromosome = newChromosome
                    if color!=chromosome[edge[1]]:
                        newChromosome = chromosome
                        newChromosome[edge[1]]=color
                        newFitness=getFitness(graph,newChromosome)[0]
                        if newFitness<bestFitness or bestFitness==-1:
                            bestFitness = newFitness
                            bestChromosome = newChromosome
                break
        return bestChromosome
    colors = set(chromosome)
    colorToRemove = random.choice(list(colors))
    colors.remove(colorToRemove)
    for gene in chromosome:
        if gene==colorToRemove:
            gene = random.choice(list(colors))
    return chromosome


def crossover(graph, chromosome1, chromosome2, feasible1):
    if feasible1==True:
        cutPoint = random.randrange(0,len(chromosome1))
        resChromosome=[]
        for i in range(cutPoint):
            resChromosome.append(chromosome1[i])
        for i in range(cutPoint,len(chromosome1)):
            resChromosome.append(chromosome2[i])
        return resChromosome
    cutPoint=0
    for edge in graph.edges():
        if chromosome1[edge[0]]==chromosome1[edge[1]]:
            for index,gene in enumerate(chromosome1):
                if gene==edge[0]:
                    cutPoint=index
                    break
            break
    newChromosome1=[]
    newChromosome2=[]
    for i in range(cutPoint):
        newChromosome1.append(chromosome1[i])
        newChromosome2.append(chromosome2[i])
    for i in range(cutPoint,len(chromosome1)):
        newChromosome1.append(chromosome2[i])
        newChromosome2.append(chromosome1[i])
    fitness1 = getFitness(graph,newChromosome1)[0]
    fitness2 = getFitness(graph,newChromosome2)[0]
    if (fitness1<fitness2):
        return newChromosome1
    return newChromosome2
    



def solveGA(graph: nx.Graph):
    mutationProb=0.8
    crossoverProb=0.3
    popSize=10000
    numGenerations=2000
    numOffsprings=50000
    initialColors=[i for i in range(1,graph.number_of_nodes()+1)]
    population=[]
    print(f"GRAPH EDGES: {str(graph.edges())}")
    for _i in range(popSize):
        random.shuffle(initialColors)
        fitness_feasible = getFitness(graph, initialColors)
        population.append({'chromosome': copy.deepcopy(initialColors), 'fitness': fitness_feasible[0], 'feasible': fitness_feasible[1], 'iteration': 0})
    population.sort(key=lambda x: x['fitness'])

    numColors=graph.number_of_nodes()
    for i in range(numGenerations):
        print(f"Generation {i}")
        print(f'Colors: {numColors}')
        if (population[0]['fitness']<=graph.number_of_nodes()*numColors):
            numColors-=1
        
        newPopulation=[]
        while len(newPopulation)<numOffsprings:
            ind1 = random.randrange(0,popSize//2)
            ind2 = random.randrange(0,popSize//2)
            crossoverChromosome1 = population[ind1]['chromosome']
            feasible1 = population[ind1]['feasible']
            crossoverChromosome2 = population[ind2]['chromosome']
            if random.random()>=crossoverProb:
                newChromosome = crossover(graph, crossoverChromosome1, crossoverChromosome2, feasible1)
                fitness_feasible = getFitness(graph, newChromosome)
                newPopulation.append({'chromosome': newChromosome, 'fitness': fitness_feasible[0], 'feasible': fitness_feasible[1], 'iteration': i})
            
            #print("Done with crossover")

            ind = random.randrange(popSize//2+1,popSize)
            mutationChromosome = population[ind]['chromosome']
            fitness = population[ind]['fitness']
            feasible = population[ind]['feasible']

            if random.random()>=mutationProb:
                newChromosome = mutation(graph, mutationChromosome, fitness, feasible)
                fitness_feasible = getFitness(graph, newChromosome)
                newPopulation.append({'chromosome': newChromosome, 'fitness': fitness_feasible[0], 'feasible': fitness_feasible[1], 'iteration': i})

            #print("Done with mutation")

        population=[]
        last=[]
        j=0
        newPopulation.sort(key=lambda x: (x['fitness'], int(x['feasible']==False), x['iteration']))
        print(f"Worst candidate before selection: {str(newPopulation[len(newPopulation)-1])}")
        while len(population)<popSize:
            if str(newPopulation[j])!=str(last):
                population.append(newPopulation[j])
                last=newPopulation[j]
            j+=1
        
        print(f"Done with generation {i}.\n\tCurrent best: {str(population[0])}\n\tCurrent worst: {str(population[popSize-1])}")
        

    return len(set(population[0]['chromosome'])), population[0]['chromosome'], population[0]['iteration']