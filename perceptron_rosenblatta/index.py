# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:27:25 2020

@author: Czarny
"""

import numpy as np
from matplotlib import pyplot as plt

from rosenblatt_perceptron import RosenblattPerceptron

def tests(clf, X, y):
    centreNumber = np.arange(20, 101, 5)
    sigma = np.arange(0.1, 1.1, 0.1)
    kmax = np.arange(500, 5001, 100)
    
    i = 0
    for m in centreNumber:
        for eta in sigma:
            for k in kmax:
                i += 1
                clf.m_ = m
                clf.eta_ = eta
                clf.k_max_ = k
                w, k = clf.fit(X, y)
                # print(w, k)
                if clf.k_ < k:
                    print("TRAIN ACC:", clf.score(X, y))
                print(i)
                

def plotContourf(X1, X2, y, color):
    plt.contourf(
        X1,
        X2,
        y,
        cmap=plt.cm.get_cmap(color)
    )
    

def plotScatter(X, y, dotsSize, color):
    plt.scatter(
        X[:, 0],
        X[:, 1],
        c=y,
        s=dotsSize,
        cmap=plt.cm.get_cmap(color)    
    )


np.random.seed(0)  # wyniki meda powtarzalne
m = 1000  # ilosc przykladow; zakladamy, ze jest parzyste

# dane
X = []
for i in range(m):
    X.append([np.random.uniform(0, 2 * np.pi), np.random.uniform(-1, 1)])
X = np.array(X)

# etykiety
y = []
for i, pkt in enumerate(X):
    y.append(-1 if np.abs(np.sin(pkt[0])) > np.abs(pkt[1]) else 1)

# normalizacja danych na osi OX do przedzialu <-1, 1>
Xt = (X[:, 0] / np.pi) - 1
X = np.c_[Xt, X[:, 1]]

# wykres danych
plt.scatter(X[:, 0], X[:, 1], c=y, s=2)
# plt.show()

# dane oraz nowa przestrzen cech
dimension = 70
clf = RosenblattPerceptron(m=dimension, eta=0.1, k_max=5000, sigma=0.3)
z = clf.generateZ(X)
c = clf.c_

# uczenie algorytmu i obliczanie celnosci
w, k = clf.fit(z, y)
print("TRAIN ACC:", clf.score(z, y))

# testy
# tests(clf, X, y)

# jak perceptron zaklasyfikowal wynik
zz = clf.returnDimension()

X3 = clf.decision_function(zz).reshape(dimension, dimension)  # zmiana wymiarowosci
X3_normalized = clf.class_labels_[(X3 > 0.0) * 1]
# print(clf.score(z, y))

# print("z.shape", z.shape)
# print("X3.shape", X3.shape)
# print("X3_normalized.shape", X3_normalized.shape)

# wykresy
colors = ["Blues", "viridis"]
dotsSize = 2

# wykres 1
plt.figure()
plotContourf(clf.X1, clf.X2, X3_normalized, colors[0])
plotScatter(X, y, dotsSize, colors[1])
plt.xlabel("x1")
plt.ylabel("x2")
plt.show()

# wykres 2
plt.figure()
plotContourf(clf.X1, clf.X2, X3, colors[0])
plotScatter(X, y, dotsSize, colors[1])
plt.xlabel("x1")
plt.ylabel("x2")
plt.show()

# wykres 3
figure = plt.figure()
axes = figure.gca(projection='3d')
axes.plot_surface(
    clf.X1,
    clf.X2,
    X3,
    cmap=plt.cm.get_cmap(colors[1]),
    linewidth=0,
    antialiased=False
)
axes.set_xlabel("x1")
axes.set_ylabel("x2")
axes.set_zlabel("x3")
plt.show()

