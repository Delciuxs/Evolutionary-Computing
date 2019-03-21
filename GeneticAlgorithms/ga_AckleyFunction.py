#https://en.wikipedia.org/wiki/Test_functions_for_optimization

import math
import random

#Chromosomes are 32 bits long, 16 bits for X and 16 bits for Y
L_chromosome = 16 * 2
N_chains = 2 ** (L_chromosome / 2)
#Lower and upper limits of search space
limitsX = [-20.0, 20.0]
limitsY = [-20.0, 20.0]
#Crossover point
crossover_point = L_chromosome / 2
#Number of chromosomes
N_chromosomes = 50
#probability of mutation
prob_m = 0.1
#Population
F0 = []
#Fitness of each population
fitness_values = []

def random_chromosome():
    chromosome=[]
    for i in range(0,L_chromosome):
        if random.random() < 0.1:
            chromosome.append(0)
        else:
            chromosome.append(1)
    return chromosome

#Create first generation
for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)

#Binary codification
def decode_chromosome(chromosome):
    global L_chromosome,N_chains,limitsX, limitsY
    valueX = 0
    valueY = 0

    for p in range(L_chromosome / 2):
        valueY += (2**p) * chromosome[-1 -p]
    for p in range(L_chromosome / 2, L_chromosome):
        valueX += (2**(p - (L_chromosome / 2)))*chromosome[-1 -p]

    x = float(limitsX[0]+(limitsX[1]-limitsX[0])*float(valueX)/(N_chains-1))
    y = float(limitsY[0]+(limitsY[1]-limitsY[0])*float(valueY)/(N_chains-1))
    return x, y

#Fitness Function
def f(v):
    return ((-20)*(math.exp((-0.2)*(math.sqrt((0.5)*(math.pow(v[0],2)+math.pow(v[1],2)))))) 
            - math.exp((0.5)*(math.cos(2 * math.pi * v[0]) + math.cos(2 * math.pi * v[1]))) 
            + math.e + 20)
    
def evaluate_chromosomes():
    global F0

    for p in range(N_chromosomes):
        v = decode_chromosome(F0[p])
        fitness_values[p] = f(v)
        

def compare_chromosomes(chromosome1,chromosome2):
    vc1 = decode_chromosome(chromosome1)
    vc2 = decode_chromosome(chromosome2)
    fvc1 = f(vc1)
    fvc2 = f(vc2)
    if fvc1 > fvc2:
        return 1
    elif fvc1 == fvc2:
        return 0
    else: #fvg1<fvg2
        return -1


Lwheel = N_chromosomes * 10

def create_wheel():
    global F0,fitness_values

    maxv = max(fitness_values)
    acc = 0
    for p in range(N_chromosomes):
        acc += maxv - fitness_values[p]
    fraction = []
    for p in range(N_chromosomes):
        fraction.append( float(maxv - fitness_values[p]) / acc)
        if fraction[-1] <= 1.0 / Lwheel:
            fraction[-1] = 1.0 / Lwheel
    fraction[0] -= (sum(fraction)-1.0) / 2
    fraction[1] -= (sum(fraction)-1.0) / 2

    wheel = []
    pc = 0

    for f in fraction:
        Np = int(f * Lwheel)
        for i in range(Np):
            wheel.append(pc)
        pc += 1
    return wheel
        
F1 = F0[:]

def nextgeneration():
    F0.sort(cmp = compare_chromosomes)
    print( "Best solution so far:" )
    v = decode_chromosome(F0[0])
    print( "f(" + str(v[0]) + "," + str(v[1]) + ")= " +
           str(f(v)))
                                                                    
    #elitism, the two best chromosomes go directly to the next generation
    F1[0] = F0[0]
    F1[1] = F0[1]
    for i in range(0,(N_chromosomes-2)/2):
        roulette = create_wheel()
        #Two parents are selected
        p1 = random.choice(roulette)
        p2 = random.choice(roulette)
        #Two descendants are generated
        o1 = F0[p1][0:crossover_point]
        o1.extend(F0[p2][crossover_point:L_chromosome])
        o2 = F0[p2][0:crossover_point]
        o2.extend(F0[p1][crossover_point:L_chromosome])
        #Each descendant is mutated with probability prob_m
        if random.random() < prob_m:
            o1[int(round(random.random()*(L_chromosome-1)))] ^= 1
        if random.random() < prob_m:
            o2[int(round(random.random()*(L_chromosome-1)))] ^= 1
        #The descendants are added to F1
        F1[2 + 2 * i] = o1
        F1[3 + 2 * i] = o2

    F0[:] = F1[:]


F0.sort(cmp = compare_chromosomes)
evaluate_chromosomes()

for i in range(51):
    print("Generation: " + str(i))
    nextgeneration()


