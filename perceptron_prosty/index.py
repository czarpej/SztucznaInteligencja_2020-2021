# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:27:25 2020

@author: Czarny
"""

import numpy as np
from matplotlib import pyplot as plt
from simple_perceptron import *

np.random.seed()  # wyniki meda powtarzalne
m = 1000  # ilosc przykladow; zakladamy, ze jest parzyste
m_half = int(m / 2)

X1 = np.random.rand(m, 1)  # losuje od 0 do 1
print(X1)
X2u = np.random.rand(m_half, 1) * 0.4 + 0.6  # mnozymy razy rozstep + pewne przesuniecie; ustawia sie tym mnozeniem wielkosc szczeliny; im mniejsza szczelina tym wiecej krokow wykona i dluzej bedzie dzialac, bo musi sie jakos tam wstrzelic
X2b = np.random.rand(m_half, 1) * 0.4

X = np.c_[X1, np.r_[X2u, X2b]]  # sklejamy po kolumnach, w srodku sklejamy 
y = np.r_[np.ones(m_half), -np.ones(m_half)]  # sklejamy wierszowo, aby bylo jedno pod drugim, a nie jedno obok drugiego
print(X)

plt.scatter(X[:, 0], X[:, 1], c=y, s=2)  # os OX to pierwsza kolumna, os OY to druga kolumna; c rozdziela widoczne dane kolorami, s to wielkosc punktow
plt.show()

clf = SimplePerceptron(eta=0.001)  # w tym algorytmie wspolczynnik uczenia nie ma zadnego znaczenia; on wplywa jedynie na wielkosc skalowania wspolczynnikow prostej - im mniejszy wspolczynnik uczenia tym mniejsze wspolczynniki prostej i proporcjonalnie w druga strone
w, k = clf.fit(X, y)  # tutaj nie zajmujemy sie podzialem na dane trenujace i testowe 
print(w, k)  # w to wektor wspolczynnikow rownania prostej; moze tez byc wielewymiarow
print("TRAIN ACC:", clf.score(X, y))

plt.scatter(X[:, 0], X[:, 1], c=y, s=2)  # os OX to pierwsza kolumna, os OY to druga kolumna; c rozdziela widoczne dane kolorami, s to wielkosc punktow
# w_0 * 1 + w_1*x_1 + w_2*x_2 = 0
x1 = np.array([0, 1])
x2 = -(w[0] + w[1] * x1) / w[2]  # nie bedzie dzielenia przez 0, bo gdyby bylo to prosta byla by prosta pionowa
plt.plot(x1, x2)
plt.show()

