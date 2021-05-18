import networkx as nx
import random
import numpy as np
import copy
from utils import plot_coloring

def getFitness(graph: nx.Graph, chromosome: list):
    numColors = len(set(chromosome))
    totalFitness = graph.number_of_nodes()*numColors
    for edge in graph.edges():
        if chromosome[edge[0]] == chromosome[edge[1]]:
            totalFitness += numColors
    if totalFitness == graph.number_of_nodes()*numColors:
        return totalFitness, True
    return totalFitness, False


def mutation(graph, chromosome, fitness, feasible):
    if feasible == False:
        colors = set(chromosome)
        copyColors = set(chromosome)
        for edge in graph.edges():
            if chromosome[edge[0]] == chromosome[edge[1]]:
                node_index = edge[random.randrange(0,2)]
                for neighbour in graph.neighbors(node_index):
                    colors.discard(chromosome[neighbour])
                if len(colors)==0:
                    chromosome[node_index]=random.choice(list(copyColors))
                    return chromosome
                chromosome[node_index]=random.choice(list(colors))
                return chromosome
    colors = set(chromosome)
    colorToRemove = random.choice(list(colors))
    colors.remove(colorToRemove)
    for gene in chromosome:
        if gene == colorToRemove:
            gene = random.choice(list(colors))
    return chromosome


def crossover(graph, chromosome1, chromosome2, feasible1):
    if feasible1 == True:
        cutPoint = random.randrange(0, len(chromosome1))
        resChromosome = []
        for i in range(cutPoint):
            resChromosome.append(chromosome1[i])
        for i in range(cutPoint, len(chromosome1)):
            resChromosome.append(chromosome2[i])
        return resChromosome
    cutPoint = 0
    for edge in graph.edges():
        if chromosome1[edge[0]] == chromosome1[edge[1]]:
            for index, gene in enumerate(chromosome1):
                if gene == edge[0]:
                    cutPoint = index
                    break
            break
    newChromosome1 = []
    newChromosome2 = []
    for i in range(cutPoint):
        newChromosome1.append(chromosome1[i])
        newChromosome2.append(chromosome2[i])
    for i in range(cutPoint, len(chromosome1)):
        newChromosome1.append(chromosome2[i])
        newChromosome2.append(chromosome1[i])
    fitness1 = getFitness(graph, newChromosome1)[0]
    fitness2 = getFitness(graph, newChromosome2)[0]
    if (fitness1 < fitness2):
        return newChromosome1
    return newChromosome2

def solveGA(graph: nx.Graph, max_iter: int):
    mutationProb = 0.9
    crossoverProb = 0.3
    popSize = 100
    numGenerations = max_iter
    numOffsprings = 1000
    population = []
    best = {}
    bestColors=[]
    nodes = graph.nodes()
    nodes_list=[]
    for node in nodes:
        nodes_list.append(node)
    nodes_list.sort()
    j=0
    last_node=nodes_list[len(nodes_list)-1]
    i=0
    while j<last_node:
        if nodes[i]==last_node:
            break
        if nodes[i]==j:
            i+=1
            j+=1
            continue
        graph.add_node(j)
        j+=1
    colorsList = [i for i in range(1, graph.number_of_nodes()+1)]
    for _i in range(popSize):
        random.shuffle(colorsList)
        chromosome = copy.deepcopy(colorsList)
        fitness_feasible = getFitness(graph, chromosome)
        population.append({'chromosome': chromosome, 'fitness': fitness_feasible[0], 'feasible': fitness_feasible[1], 'iteration': 0})
    population.sort(key=lambda x: x['fitness'])
    overallBest=best=population[0]
    colorsList.sort()
    numColors = graph.number_of_nodes()
    i=1
    global_iter=1
    while i<=numGenerations:
        print(f"Generation: global {global_iter}, local: {i}")
        print(f'Colors: {numColors}')
        print(f'Best: {str(best)}')
        print(f'OverallBest: {str(overallBest)}')
        if best != {} and best['feasible'] == True and len(set(best['chromosome']))<=numColors:
            numColors = len(set(best['chromosome'])) - 1
            colorsList=colorsList[0:numColors]
            assert len(colorsList)==numColors
            population=[]
            for _j in range(popSize):
                chromosome = [random.choice(colorsList) for _k in range(graph.number_of_nodes())]
                fitness_feasible = getFitness(graph, chromosome)
                population.append({'chromosome': chromosome, 'fitness': fitness_feasible[0], 'feasible': fitness_feasible[1], 'iteration': global_iter})
            population.sort(key=lambda x: (
                x['fitness'], int(x['feasible'] == False)))
            overallBest=best
            best={}
            i=1
            continue

        newPopulation = []
        while len(newPopulation) < numOffsprings:
            ind1 = random.randrange(0, popSize//2)
            ind2 = random.randrange(0, popSize//2)
            crossoverChromosome1 = population[ind1]['chromosome']
            feasible1 = population[ind1]['feasible']
            crossoverChromosome2 = population[ind2]['chromosome']
            if random.random() >= crossoverProb:
                newChromosome = crossover(
                    graph, crossoverChromosome1, crossoverChromosome2, feasible1)
                fitness_feasible = getFitness(graph, newChromosome)
                newPopulation.append(
                    {'chromosome': newChromosome, 'fitness': fitness_feasible[0], 'feasible': fitness_feasible[1], 'iteration': global_iter})

            ind = random.randrange(popSize//2+1, popSize)
            mutationChromosome = population[ind]['chromosome']
            fitness = population[ind]['fitness']
            feasible = population[ind]['feasible']

            if random.random() >= mutationProb:
                newChromosome = mutation(
                    graph, mutationChromosome, fitness, feasible)
                fitness_feasible = getFitness(graph, newChromosome)
                newPopulation.append(
                    {'chromosome': newChromosome, 'fitness': fitness_feasible[0], 'feasible': fitness_feasible[1], 'iteration': global_iter})

        population = []
        j = 0
        newPopulation.sort(key=lambda x: (
            x['fitness'], int(x['feasible'] == False)))

        if best == {} or best['fitness'] > newPopulation[0]['fitness']:
            best = newPopulation[0]

        print(
            f"Worst candidate before selection: {str(newPopulation[len(newPopulation)-1])}")
        while len(population) < popSize//2:
            population.append(newPopulation[j])
            j += 1
        population.append(newPopulation[0])
        while len(population) < popSize:
            population.append(newPopulation[random.randrange(popSize//2+1, len(newPopulation))])
        
        population.sort(key=lambda x: (
            x['fitness'], int(x['feasible'] == False)))
        
        print(
            f"Done with generation {global_iter}.\n\tCurrent generation best: {str(population[0])}\n\tCurrent generation worst: {str(population[popSize-1])}\n\tOverall best so far: {str(overallBest)}")

        bestColors.append(len(set(overallBest['chromosome'])))
        i+=1
        global_iter+=1
    plot_coloring("GA",graph,max_iter,bestColors)
    res={}
    for i,elem in enumerate(overallBest['chromosome']):
        res[i]=elem
    return len(set(overallBest['chromosome'])),res, overallBest['iteration']
