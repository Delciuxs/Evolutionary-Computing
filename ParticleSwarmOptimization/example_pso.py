#File: pso_wikipedia.py
#Example of PSO based on the wikipedia entry
#Jorge Luis Rosas Trigueros, Ph.D.
#Last modification: 6 mar 19

from Tkinter import *
import random
import copy
import math

#Constraints for the variable
lower_limit=[-20]
upper_limit=[20]
#Number of particles
n_particles=10
#Number of dimentions
n_dimensions=1

#Fitness function
def f(x):
    global n_dimensions
    result=0
    for d in range(n_dimensions):
        result += 0.05*(x[d]-10)*(x[d]-10)-4*math.cos(x[d]-10)
    return result

def init_X_V(up,lo,n_p,n_d):
    X=[]
    V=[]
    for i in range(n_p):
        X.append([])
        V.append([])
        for d in range(n_d):
            X[i].append(lo[d] + (up[d] - lo[d]) * random.random())
            V[i].append(2*(up[d]-lo[d])*random.random()-(up[d]-lo[d]))
    return X,V
    


# Initialize the particle positions and their velocities
#X,V=init_X_V(upper_limit,lower_limit,n_particles,n_dimensions)
X,V=init_X_V([5],lower_limit,n_particles,n_dimensions)
 
#Create copies of the population and obtain the best individual
X_lbest=copy.deepcopy(X)
X_gbest= copy.deepcopy(X_lbest[0])

for I in range(0, n_particles):
    if f(X_lbest[I])<f(X_gbest):
        X_gbest=copy.deepcopy(X_lbest[I])


def iteration():
    global X,X_lbest,X_gbest,V
    # Loop until convergence, in this example a finite number of iterations chosen
    w.delete(ALL)
    weight=0.7
    C1=0.2
    C2=0.1
 
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
          
    graph_f()
    graph_population(X,V,w,s,s,xo,yo,'blue',0.4)
    graph_population([X_gbest],V,w,s,s,xo,yo,'red',0.1)
    w.update()
    



#Graphing Code
master = Tk()
xmax=400
ymax=400
xo=200
yo=200
s=10

w = Canvas(master, width=xmax, height=ymax)
w.pack()
       
b = Button(master, text="Next Iteration", command=iteration)
b.pack()

N=100


def graph_f():
    xini=-20.
    xfin=20.
    dx=(xfin-xini)/N
    xold=xini
    yold=f([xold]) #evaluate_quality([xold])
    for i in range(1,N):
        xnew=xini+i*dx
        ynew=f([xnew]) #evaluate_quality([xnew])
        w.create_line(xo+xold*s,yo-yold*s,xo+xnew*s,yo-ynew*s)
        xold=xnew
        yold=ynew

def graph_population(F,V,mycanvas,escalax,escalay,xcentro,ycentro,color,r):
    n_p=len(F)
    for I in range(0, n_p):
        p=F[I]#[0]
        y=f(p) #evaluate_quality(p)

        mycanvas.create_oval(xcentro+(p[0]-r)*escalax,ycentro-(y-r)*escalay,
                             xcentro+(p[0]+r)*escalax, ycentro-(y+r)*escalay,
                             fill=color)
        mycanvas.create_line(xcentro+p[0]*escalax,ycentro-y*escalay,
                             xcentro+(p[0]+V[I][0]*escalax)*escalax,ycentro-y*escalay,fill=color)

graph_f()
graph_population(X,V,w,s,s,xo,yo,'blue',0.2)

mainloop()



