import math
import random

print("TRAVELLING SALESMAN\n")
print("Enter the number of cities\n")
numCities = int(input())
print("Enter the cost matrix\n")
costs = []
for i in range(0, 4):
    costs.append([-1] * numCities)

for i in range(0, 4):
    for j in range(0, 4):
        costs[i][j] = int(input())

#Chromosomes are numCities - 1 bits long
L_chromosome = numCities - 1
#Number of chromosomes
N_chromosomes = 10
#probability of mutation
prob_m = 0.5
#Population
F0=[]
#Fitness of population
fitness_values=[]

def random_chromosome():
    alreadyFilled = 0
    chromosome = []
    citiesUsed = {}
    while alreadyFilled != (numCities - 1):
        city = random.randint(1, numCities - 1)
        if city not in citiesUsed:
            chromosome.append(city)
            citiesUsed[city] = True
            alreadyFilled += 1
    return chromosome

#Create the first generation
for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)

def decode_chromosome(chromosome):
    fullPath = []
    fullPath.append(0)
    for city in chromosome:
        fullPath.append(city)
    fullPath.append(0)
    return fullPath

def f(x):
    totalCost = 0
    global costs
    for i in range(0, len(x) - 1):
        totalCost += costs[x[i]][x[i + 1]]
    return totalCost

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

def partiallyMappedCrossover(chromosome1, chromosome2):
    mapCities = {}
    descendant1 = [-1] * len(chromosome1)
    descendant2 = [-1] * len(chromosome2) 

    cutPoint1 = random.randint(0, len(chromosome1) - 1)
    cutPoint2 = random.randint(0, len(chromosome1) - 1)

    if cutPoint1 > cutPoint2:
        auxCut = cutPoint1
        cutPoint1 = cutPoint2
        cutPoint2 = auxCut

    for i in range(cutPoint1, cutPoint2 + 1):
        descendant1[i] = chromosome2[i]
        descendant2[i] = chromosome1[i]
        if chromosome1[i] not in mapCities:
            mapCities[chromosome1[i]] = chromosome2[i]
        else:
            transition = mapCities[chromosome1[i]]
            mapCities[transition] = chromosome2[i]
            mapCities.pop(chromosome1[i])
            mapCities[chromosome2[i]] = transition
            continue
        if chromosome2[i] not in mapCities:
            mapCities[chromosome2[i]] = chromosome1[i]
        else:
            transition = mapCities[chromosome2[i]]
            mapCities[transition] = chromosome1[i]
            mapCities.pop(chromosome2[i])
            mapCities[chromosome1[i]] = transition
            continue

    for i in range(0, len(chromosome1)):
        if i >= cutPoint1 and i <= cutPoint2:
            continue
        else:
            if chromosome1[i] not in mapCities:
                descendant1[i] = chromosome1[i]
            else:
                descendant1[i] = mapCities[chromosome1[i]]
            if chromosome2[i] not in mapCities:
                descendant2[i] = chromosome2[i]
            else:
                descendant2[i] = mapCities[chromosome2[i]]

    return descendant1, descendant2

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
    F0.sort(cmp = compare_chromosomes)
    print( "Best solution so far:" )
    print("Path: ")
    print(decode_chromosome(F0[0]))
    print("With cost: " + str(f(decode_chromosome(F0[0]))))
                                                                    
    #elitism, the two best chromosomes go directly to the next generation
    F1[0]=F0[0]
    F1[1]=F0[1]
    for i in range(0,(N_chromosomes-2)/2):
        roulette=create_wheel()
        #Two parents are selected
        p1=random.choice(roulette)
        p2=random.choice(roulette)
        #Two descendants are generated
        o1, o2 = partiallyMappedCrossover(F0[p1], F0[p2])
        #Each descendant is mutated with probability prob_m
        #Individual can have exchange mutation
        if random.random() < prob_m:
            s1 = random.randint(0, len(o1) - 1)
            s2 = random.randint(0, len(o1) - 1)
            auxCity = o1[s1]
            o1[s1] = o1[s2]
            o1[s2] = auxCity
        #Individual can have exchange mutation
        if random.random() < prob_m:
            s1 = random.randint(0, len(o1) - 1)
            s2 = random.randint(0, len(o1) - 1)
            auxCity = o2[s1]
            o2[s1] = o2[s2]
            o2[s2] = auxCity
            
        #The descendants are added to F1
        F1[2+2*i]=o1
        F1[3+2*i]=o2

    #The new generation replaces the old one
    F0[:]=F1[:]

F0.sort(cmp=compare_chromosomes)
evaluate_chromosomes()

for k in range(0, 50):
    print("\nGeneration: " + str(k))
    nextgeneration()

