import math
import random
from sys import stdin, stdout

#Asking for the input
stdout.write("COIN CHANGE PROBLEM\n")
stdout.write("Enter the change and the amount of coins: \n")
change, numCoins = map(int, stdin.readline().split())
denominations = list()
stdout.write("Enter the denominations:\n")
for i in range(numCoins):
    denominations.append(int(stdin.readline()))
denominations.sort()
stdout.write("Enter the number of generations: \n")
numGenerations = int(stdin.readline())
maxAmountCoinsUsed = int(math.log(int(change / denominations[0]), 2)) + 1

#Chromosomes are numCoinxs * maxAmountACoinCanBeUsed
L_chromosome= maxAmountCoinsUsed * len(denominations)
#Crossover Point
crossover_point=L_chromosome/2
#Number of chromosomes
N_chromosomes=100
#Probability of mutation
prob_m=0.75
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
    T = 0
    N = 0
    for i in range(len(denominations)):
        n_i = 0
        for s in range(0, maxAmountCoinsUsed):
            n_i += (2**s) * chromosome[maxAmountCoinsUsed - 1 - s + i * maxAmountCoinsUsed]
        T += denominations[i] * n_i
        N += n_i
    return N,T

#Fitness function
def f(x):
    # x = (N,T)
    alfa = 8.0
    beta = 10.0
    return (alfa * x[0]) + (beta * abs(change - x[1]))

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
    if fvc1 > fvc2:
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
    stdout.write("\nBest solution so far:" )
    print(F0[0])
    auxDecode = decode_chromosome(F0[0])
    stdout.write("With num Coins: " + str(auxDecode[0]) + " change : " + str(auxDecode[1]))
                                                                    
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

for i in range(numGenerations + 1):
    stdout.write("\n\nGeneration: " + str(i))
    nextgeneration()

