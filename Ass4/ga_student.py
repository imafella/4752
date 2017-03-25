import random, math, collections
from sudoku import Sudoku


def eval_sudoku(array):
    #return sum(array)  # un-comment this line and watch the GA optimize to all max numbers
    #return -sum(array) # un-comment this line and watch the GA optimize to all ones
    s = Sudoku(0)
    size = int(math.sqrt(len(array)))
    s.set_arr(array)
    fitness = 0
    # count unique values in each row
    for r in range(s.size()):
        vals = set()
        for c in range(s.size()):
            vals.add(s.get(r,c))
        fitness += len(vals)
    # count unique values in each column
    for c in range(s.size()):
        vals = set()
        for r in range(s.size()): 
            vals.add(s.get(r,c))
        fitness += len(vals)
    # count unique values in each square
    sqsize = int(math.sqrt(s.size()))
    for sr in range(sqsize):
        for sc in range(sqsize):
            vals = set()
            for r in range(sqsize):
                for c in range(sqsize):
                    vals.add(s.get(sr*sqsize+r, sc*sqsize+c))
            fitness += len(vals)
    return fitness

# the class that stores the genetic algorithm settings
class GASettings:
    # we need something in here so that python doesn't complain about blank classes
    description = 'Blank struct to hold our GA settings in'


def get_ga_settings(sudoko_size):
    settings = GASettings()
    settings.individual_values      = [(i+1) for i in range(sudoko_size)]   # list of possible values individuals can take
    settings.individual_size        = sudoko_size*sudoko_size               # length of an individual
    settings.fitness_function       = eval_sudoku                           # the fitness function of an individual
    settings.population_size        = 100                                   # total size of each population                             (experiment with this)
    settings.elitism_ratio          = 0.4                                   # select top x% of individuals to survive                   (experiment with this)
    settings.parent_roulette_ratio  = 0.2                                   # select x% of population as parents via roulette wheel     (experiment with this)
    settings.mutation_rate          = 0.2                                   # mutation rate percentage                                  (experiment with this)
    settings.crossover_index        = settings.individual_size // 2         # the index to split parents for recombination              
    return settings

#A Roulette spinner, Input: Dict{ID: fitness}, Output: ID
def roulette(options):
    max = sum(options)
    pick = random.uniform(0, max)
    current = 0
    for i, j in enumerate(options):
        current += j
        if current > pick:
            return i
#does the crossover input Array mom, Array dad, and settings, Output ChildA and ChildB crossovers
def crossover(mom, dad, settings):
    div = settings.crossover_index
    childA = mom[:div]
    momB = mom[div:]
    childB = dad[:div]
    dadB = dad[div:]
    childA.extend(dadB)
    childB.extend(momB)

    return childA, childB

# Mutate M of the offspring (Both inputs) and returns the mutated array
def main_mutate(M, offspring, settings):
    i = 0
    choice =  [0,1]
    pull = 0
    while i < 2*M:
        pull = i + random.choice(choice)
        offspring[pull][random.randint(1,len(offspring[pull]))-1] = random.choice(settings.individual_values)
        i+=2
    return offspring


#
# args:
#
#   population - A list of individuals, each of which are a 1D list representing a 'flattened'
#                sudoku candidate solution. 
#
#   settings   - An instance of a GAsettings object which uses the settings within it to compute
#                the next generation's population
#
# returns:
#
#   next_population - The next population after a one-generation genetic algorithm evolution
#
def evolve(population, settings):
    next_population = []
    # Generates the Fitness of each of the population
    pop_fitness = []
    for i in population:
        pop_fitness.append(eval_sudoku(i))


    P = int(settings.parent_roulette_ratio * len(population))

    # Gets random parents
    P = int(settings.parent_roulette_ratio * len(population))
    parents = []
    while len(parents) < P:
        parents.append(population[roulette(pop_fitness)])

    # Appends the E best from population to next_population
    E = int(settings.elitism_ratio * len(population))
    ugh = dict(zip(pop_fitness, population))
    pop_fitness.sort(reverse=True)
    for i in range(0, E-1):
        next_population.append(ugh[pop_fitness[i]])

    # Generates offspring by taking random parents using crossover
    offspring = []
    while len(offspring) + E < len(population):
        mother = random.choice(parents)
        father = random.choice(parents)
        if mother == father: continue
        a, b = crossover(mother, father, settings)
        offspring.append(a)
        offspring.append(b)

    # Mutates the offspring by one value and adds them to next_population
    M = int(settings.mutation_rate * len(offspring))
    for x in main_mutate(M, offspring, settings):
        next_population.append(x)

    return next_population
