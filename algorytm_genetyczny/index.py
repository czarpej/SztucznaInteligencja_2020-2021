# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:19:42 2021

@author: Czarny
"""

import numpy as np
import time as time
from genetic_algo import GeneticAlgorithm
import matplotlib.pyplot as plt

def random_knapsack_problem(n=50, scale=10**5, seed=None):
    if seed is not None:
        np.random.seed(seed)    
    items = np.ceil(scale * np.random.rand(n, 2)).astype("int32")
    C = int(np.ceil(0.5 * 0.5 * n * scale))
    v = items[:, 0]
    c = items[:, 1]
    return v, c, C

def knapsack_problem_dp_solve(v, c, C):
    n = v.size
    a = np.zeros((C + 1, n), dtype="int32") # a[i, j] = best pack of knapsack with capacity i using objects from set {1, ..., j}
    b = np.empty((C + 1, n), dtype="object") # back pointers
    for j in range(n):
        b[0, j] = (0, 0)        
    for i in range(1, C + 1):
        if c[0] <= i:
            a[i, 0] = v[0]
            b[i, 0] = (int(i - c[0]), 0)
        else:
            b[i, 0] = (i, -1)
        for j in range(1, n):
            i_prev = int(np.floor(i - c[j]))
            if c[j] > i:
                a[i, j] = a[i, j - 1]
                b[i, j] = (i, j - 1)
            elif a[i, j - 1] >= a[i_prev, j - 1] + v[j]:
                a[i, j] = a[i, j - 1]
                b[i, j] = (i, j - 1)
            else:
                a[i, j] = a[i_prev, j - 1] + v[j]
                b[i, j] = (i_prev, j - 1)
    i = C
    j = n - 1
    solution = np.zeros(n, dtype="int8")
    while i > 0 and j >= 0:
        if b[i, j][0] < i:
            solution[j] = 1
        i, j = b[i, j]
    best_pack_value = a[C, n - 1] 
    return best_pack_value, solution

def knapsack_fitness_hard(x, v, c, C):
    return x.dot(v) if x.dot(c) <= C else 0                               
            

n = 50
scale = 10**3
history = True
v, c, C = random_knapsack_problem(n=n, scale=scale, seed=0)
print("RANDOM KNAPSACK PROBLEM:")
print("v: " + str(v))
print("c: " + str(c))
print("C: " + str(C))

print("SOLVING VIA DYNAMIC PROGRAMMING...")
t1 = time.time()
best_pack_value, solution = knapsack_problem_dp_solve(v, c, C)
t2 = time.time()
print("SOLVING VIA DYNAMIC PROGRAMMING DONE IN: " + str(t2 - t1) + " s.")
print("BEST PACK VALUE: " + str(best_pack_value))
print("SOLUTION: " + str(solution))

ga = GeneticAlgorithm(n=n, m=1000, T=100, prob_cross_over=0.9, prob_mutation=10.0**(-3), selection="selection_rank", crossover="crossover_twopoint", 
                      fitness=knapsack_fitness_hard, fitness_params={"v": v, "c": c, "C": C}, seed=0, history=history)
print("SOLVING VIA GENETIC ALGORITHM...")
t1 = time.time()
best_pack_value_ga, solution_ga, history_f_mean, history_f_best = ga.execute()
t2 = time.time()
print("SOLVING VIA GENETIC ALGORITHM DONE IN: " + str(t2 - t1) + " s.")
print("BEST PACK VALUE: " + str(best_pack_value_ga))
print("SOLUTION: " + str(solution_ga))
print("BEST PACK VALUE RATIO: " + str(best_pack_value_ga / best_pack_value))
print("BIT MATCH RATIO: " + str(np.sum(solution == solution_ga) / n))

if history:
    plt.plot(history_f_mean, color="blue")
    plt.plot(history_f_best, color="red")
    plt.show()