import math
import random
from sys import stdin, stdout

# Asking for values
stdout.write("KNAPSACK\n")
stdout.write("Enter the number of objects and the capacity\n")
numObjects, capacity = map(int, stdin.readline().split())
values = list()
weights  = list()
stdout.write("Enter the value of each object\n")
for i in range(numObjects):
    values.append(int(stdin.readline()))
stdout.write("Enter the size of each object\n")
for i in range(numObjects):
    weights.append(int(stdin.readline()))
stdout.write("Enter the number of generations\n")
numGenerations = int(stdin.readline())

#Chromosomes are N bits long
L_chromosome= numObjects
#Crossover point
crossover_point=L_chromosome/2
#Number of chromosomes
N_chromosomes=10
#Probability of mutation
prob_m=0.5
#Population
F0=[]
#Fitness of each population
fitness_values=[]

def random_chromosome():
    chromosome=[]
    for i in range(0,L_chromosome):
        if random.random()<0.1:
            chromosome.append(0)
        else:
            chromosome.append(1)
    return chromosome

#Create first generation
for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)

def decode_chromosome(chromosome):
    TW = 0
    TV = 0
    for i in range(0,numObjects):
        TW += weights[i]*chromosome[i]
        TV += values[i]*chromosome[i]
    return TV,TW


#Fitness function
def f(x):
    #x = (TV, TW)
    alfa = 1.0
    beta = 2.0
    excess = x[1] - capacity
    
    if excess <= 0:
        fitness = alfa * x[0]
    else:
        fitness = (alfa * x[0]) - (beta * excess)
    return fitness


def evaluate_chromosomes():
    global F0
    for p in range(N_chromosomes):
        v=decode_chromosome(F0[p])
        fitness_values[p]=f(v)
        

def compare_chromosomes(chromosome1,chromosome2):
    vc1=decode_chromosome(chromosome1)
    vc2=decode_chromosome(chromosome2)
    fvc1=f(vc1)
    fvc2=f(vc2)
    if fvc1 < fvc2:
        return 1
    elif fvc1 == fvc2:
        return 0
    else: #fvg1<fvg2
        return -1

Lwheel=N_chromosomes*10

def create_wheel():
    global F0,fitness_values

    maxv=max(fitness_values)
    acc=0
    for p in range(N_chromosomes):
        acc+=maxv-fitness_values[p]
    fraction=[]
    for p in range(N_chromosomes):
        fraction.append( float(maxv-fitness_values[p])/acc)
        if fraction[-1]<=1.0/Lwheel:
            fraction[-1]=1.0/Lwheel
    fraction[0]-=(sum(fraction)-1.0)/2
    fraction[1]-=(sum(fraction)-1.0)/2

    wheel=[]

    pc=0

    for f in fraction:
        Np=int(f*Lwheel)
        for i in range(Np):
            wheel.append(pc)
        pc+=1

    return wheel
        
F1=F0[:]

def nextgeneration():
    F0.sort(cmp=compare_chromosomes)
    stdout.write( "\nBest solution so far:" )
    print(F0[0])
    auxDecode = decode_chromosome(F0[0])
    stdout.write("With value: " + str(auxDecode[0]) + " weight : " + str(auxDecode[1]))
             
    #elitism, the two best chromosomes go directly to the next generation
    F1[0]=F0[0]
    F1[1]=F0[1]
    for i in range(0,(N_chromosomes-2)/2):
        roulette=create_wheel()
        #Two parents are selected
        p1=random.choice(roulette)
        p2=random.choice(roulette)
        #Two descendants are generated
        o1=F0[p1][0:crossover_point]
        o1.extend(F0[p2][crossover_point:L_chromosome])
        o2=F0[p2][0:crossover_point]
        o2.extend(F0[p1][crossover_point:L_chromosome])
        #Each descendant is mutated with probability prob_m
        if random.random() < prob_m:
            o1[int(round(random.random()*(L_chromosome-1)))]^=1
        if random.random() < prob_m:
            o2[int(round(random.random()*(L_chromosome-1)))]^=1
        #The descendants are added to F1
        F1[2+2*i]=o1
        F1[3+2*i]=o2
    #The new generation replaces the old one
    F0[:]=F1[:]



F0.sort(cmp=compare_chromosomes)
evaluate_chromosomes()

for s in range(numGenerations + 1):
    stdout.write("\n\nGeneration: " + str(s))
    nextgeneration()


