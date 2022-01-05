import random
import numpy as np

def init_population(pop_size, gene_pool, state_length):
    population = []
    for _ in range(pop_size):
        new_individual = "".join(random.choices(gene_pool, k=state_length))
        population.append(new_individual)

    return population

def fitness_fn(sample):
    counter=0
    length=min(len(sample),len(target))
    for i in range(length):
        if sample[i] == target[i]:
            counter+=1
    return counter

def takefirst(elem):
    return elem[0]

def select(r, population, fitness_fn):
    weight=[]
    for x in population:
        weight.append(fitness_fn(x))
    return random.choices(population,k=r,weights=weight)

def recombine(x, y):
    n=min(len(x),len(y))
    c=random.randrange(1,n)
    return x[:c]+y[c:]

def mutate(x, gene_pool, pmut):
    if random.uniform(0, 1) >= pmut:
        return x

    n = len(x)
    g = len(gene_pool)
    c = random.randrange(0, n)
    r = random.randrange(0, g)

    new_gene = gene_pool[r]
    return x[:c] + new_gene + x[c + 1:]  

class PhraseGeneration(object):
    def __init__(self, target, alphabet):
        self.target = target
        self.alphabet = alphabet

    def init_population(self, pop_size):
        return init_population(pop_size, self.alphabet, len(self.target))

    def fitness(self, sample):
        fitvalue=fitness_fn(sample)
        return fitvalue
    
    def reproduce(self, population, mutation_rate):
        """
        TODO: generate the next generation of population

        hint: make a new individual with 
        
        mutate(recombine(*select(2, population, fitness_fn)), gene_pool, pmut)

        """
        number=len(population)
        next_gen=[]
        for i in range(number):
            next_gen.append(mutate(recombine(*select(2, population, self.fitness)), gene_pool, mutation_rate))
        return next_gen

    def replacement(self, old, new):
        """
        you can use your own strategy, for example retain some solutions from the old population
        """
        hybrid=[]
        for i in old:
            hybrid.append(i)
        for j in new:
            hybrid.append(j)
        hybrid=select((int)((len(old)+len(new))/2),hybrid,self.fitness)
        return new

def genetic_algorithm(
        problem, 
        ngen, n_init_size, mutation_rate, 
        log_intervel=100
    ):

    population = problem.init_population(n_init_size)
    best = max(population, key=problem.fitness)
    history = [(0, list(map(problem.fitness, population)))]

    for gen in range(ngen):
        next_gen    = problem.reproduce(population, mutation_rate)
        population  = problem.replacement(population, next_gen)

        if gen % log_intervel == 0:
            current_best = max(population, key=problem.fitness)
            if problem.fitness(current_best) > problem.fitness(best): best = current_best
            print(f"Generation: {gen}/{ngen},\tBest: {best},\tFitness={problem.fitness(best)}")         
            history.append((gen, list(map(problem.fitness, population))))
    
    history.append((ngen-1, list(map(problem.fitness, population))))
    return best, history

if __name__ =='__main__':
    ngen = 2000
    max_population = 120
    mutation_rate = 0.2

    sid = 11911425 # replace this with your own sid
    target = f"Genetic Algorithm by {sid}" 
    u_case = [chr(x) for x in range(65, 91)]
    l_case = [chr(x) for x in range(97, 123)]
    digit_case = [chr(x) for x in range(48,58)]
    gene_pool = u_case + l_case + [' '] + digit_case# all English chracters and white space

    alphabet = gene_pool 

    problem = PhraseGeneration(target, alphabet)

    # and run it
    solution, history = genetic_algorithm(problem, ngen, max_population, mutation_rate)
    solution