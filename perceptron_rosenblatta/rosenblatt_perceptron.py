# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:37:49 2020

@author: Czarny
"""

from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np
import math


class RosenblattPerceptron(BaseEstimator, ClassifierMixin):
    def __init__(self, eta=1.0, m=20, k_max: int=500, sigma=0.3):
        self.class_labels_ = None
        self.w_ = None  # wektor wspolczynnikow
        self.k_ = 0  # liczba krokow algorytmu, jedynie dla informacji
        self.eta_ = eta
        self.m_ = m  # liczba centrow (w tym wymiarowosc przestrzeni cech)
        self.k_max_ = k_max  # ograniczenie na liczbe iteracji
        self.sigma_ = sigma  # wspolczynnik szerokosci dzwonu (wykorzystywany w obliczaniu odleglosci pkt od centrow dla macierzy bedaca nowa przestrzenia cech)
        
    def generateCentre(self, low1=-1, high1=1, low2=-1, high2=1):
        c = []
        
        # uwtorzenie macierzy pkt (przestrzen dwuwymiarowa)
        for i in range(self.m_):
            c.append([np.random.uniform(low1, high1), np.random.uniform(low2, high2)])
        c = np.array(c)
        self.c_ = c
        
        return c
    
    def generateZ(self, X):
        m, n = X.shape  # rozmiar danych
        c = self.generateCentre()  # centra
        z = np.zeros((m, self.m_))  # zbior cech
        
        # petla po nowej macierzy cech z
        for i in range(len(z)):
            for j in range(len(z[i])):
                z[i, j] = self.dist2(X[i], c[j])  # dla i-tego pkt odleglosc do j-tego centrum
              
        self.z_ = z
        
        return z
    
    def fit(self, X, y):                      
        # wymiarowosci i etykietki
        m, n = X.shape  # rozmiar danych
        self.class_labels_ = np.unique(y)  # dowiadujemy sie jakie etykietki sa w y
        
        # normalizacja etykietek
        y_normalized = np.ones(m).astype("int8")  # do zamiany etykietek, dla zabezpieczenia - te ktore sa string na liczby 1, -1
        y_normalized[y == self.class_labels_[0]] = -1  # zamiana etykietek na wlasne
        
        # inicjalizacja wektora wag oraz wyzerowanie licznika krokow
        self.w_ = np.zeros(n + 1)  # inicjalizacja wartosci etykietek z kapelusza, losowo, albo jak tutaj 0
        self.k_ = 0  # jakby ktos ponownie uzyl funkcji fit
        
        # doklejenie kolumny jedynek na poczatku macierzy cech
        X = np.c_[np.ones((m, 1)), X]
        
        # pozornie nieskonczona petla while
        while True:
            # oprozniamy listy zle sklasyfikowane
            E = []  # lista punktow zle sklasyfikowanych
            E_y = []  # lista etykiet punktow zle sklasyfikowanych
            
            # ta petla zbiera pkt zle sklasyfikowane i zapamietujemy ich wspolrzedne
            for i in range(m):
                x = X[i]  # wyjecie z tabelki uczacej i-ty przyklad na wierzch
                f = -1 if self.w_.dot(x.T) <= 0 else 1  # dot jest operacja mnozenia macierzowego; macierz wag mnozona przez wiersz transponowany, czyli o takiej samej ilosci wierszy, zamiast kolumn
                
                if f != y_normalized[i]:
                    E.append(x)
                    E_y.append(y_normalized[i])
                    break
                    
            if len(E) == 0:
                break

            # teraz poprawka, trzeba sobie wylosowac jakis pkt sposrod zle sklasyfikowanych
            i = int(np.random.rand() * len(E))

            x = E[i]
            y = E_y[i]

            # wzor na poprawke
            self.w_ = self.w_ + self.eta_ * y * x    
            
            # zwiekszenie licznika krokow
            self.k_ += 1
            
            # warunek stopu
            if self.k_ >= self.k_max_:
                break
            
        return self.w_, self.k_
    
    def dist(self, x, c):
        # print(x, c)
        # print(x.shape, c.shape)
        return np.sqrt(((x[0] - c[0]) ** 2) + ((x[1] - c[1]) ** 2))
    
    # len(x) must be equal with len(c)
    def dist2(self, x, c):
        operation = (((x[0] - c[0]) ** 2) + ((x[1] - c[1]) ** 2))
            
        return math.exp(- (operation / (2 * (self.sigma_ ** 2))))
    
    def predict(self, X):
        return self.class_labels_[(self.decision_function(X) > 0) * 1]
    
    # nie zwraca prawdopodobienstw, a rzeczywiste wartosci
    def decision_function(self, X):
        m, n = X.shape
        return self.w_.dot(np.c_[np.ones((m, 1)), X].T)
    
    def returnDimension(self):   
        # rowno rozmieszczone probki z danego przedzialu, ilosc probek uzalezniona od ilosci wymiarow
        x1 = np.linspace(-1, 1, self.m_)
        x2 = np.linspace(-1, 1, self.m_)
        # print(x1, x2)
        
        # macierze wspolrzednych
        self.X1, self.X2 = np.meshgrid(x1, x2)
        # print("X1", self.X1)
        # print("X2", self.X2)
        
        # polaczenie macierzy pkt w trzeci wymiar
        shape3 = np.stack((self.X1, self.X2), axis=2)
        # print("shape3", shape3)
        
        # zmiana wymiarowosci z trzech wymiarow na dwa
        # print("shape3.shape", shape3.shape)
        shape3 = shape3.reshape(self.m_ ** 2, 2)  # do kwadratu, zeby sie zmiescilo, aby mialo gdzie upchac trzeci wymiar
        # print("reshape shape3.shape", shape3.shape)
    
        # nowa macierz cech dla nowej wymiarowosci
        m, n = shape3.shape
        z = np.zeros((m, self.m_))
        
        for i in range(len(z)):
            for j in range(len(z[i])):
                z[i, j] = self.dist2(shape3[i], self.c_[j])  # dla i-tego pkt odleglosc do j-tego centrum
                
        # z = np.c_[np.ones(self.m_ ** 2), z]
        
        return z