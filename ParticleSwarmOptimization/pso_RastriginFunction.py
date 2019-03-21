#https://en.wikipedia.org/wiki/Test_functions_for_optimization

import random
import copy
import math

limits = [[-15,15], [-15,15]]
n_particles=50
n_dimensions=2


def f(v):
    global n_dimensions
    evaluate = 0;
    for i in range(0, len(v)):
        evaluate += ((math.pow(v[i],2)) - ((10)*(math.cos(2 * math.pi * v[i]))))
    evaluate += (10 * n_dimensions)
    return evaluate

def init_X_V(limits,n_p,n_d):
    X = []
    V = []

    for i in range(n_p):
        X.append([])
        V.append([])
        for d in range(n_d):
            X[i].append(limits[d][0] + (limits[d][1] - limits[d][0]) * random.random())
            V[i].append(2*(limits[d][1]-limits[d][0])*random.random()-(limits[d][1]-limits[d][0]))
    return X,V
    
# Initialize the particle positions and their velocities
X,V=init_X_V(limits,n_particles,n_dimensions)

X_lbest=copy.deepcopy(X)
X_gbest= copy.deepcopy(X_lbest[0])

for I in range(0, n_particles):
    if f(X_lbest[I])<f(X_gbest):
        X_gbest=copy.deepcopy(X_lbest[I])

def iteration():
    global X,X_lbest,X_gbest,V
    # Loop until convergence, in this example a finite number of iterations chosen
    weight=0.8
    C1=0.2
    C2=0.5
 
    print "Best particle in:",X_gbest," gbest: ",f(X_gbest)
    # Update the particle velocity and position
    for I in range(0, n_particles):
        for J in range(0, n_dimensions):
          R1 = random.random()#uniform_random_number()
          R2 = random.random()#uniform_random_number()
          V[I][J] = (weight*V[I][J]
                    + C1*R1*(X_lbest[I][J] - X[I][J]) 
                    + C2*R2*(X_gbest[J] - X[I][J]))
          X[I][J] = X[I][J] + V[I][J]
        if f(X[I])<f(X_lbest[I]):
            X_lbest[I]=copy.deepcopy(X[I])
            if f(X_lbest[I])<f(X_gbest):
                X_gbest=copy.deepcopy(X_lbest[I])
          
for s in range(51):
    print("iteration " + str(s))
    iteration()





