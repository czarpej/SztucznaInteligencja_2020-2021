# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:37:49 2020

@author: Czarny
"""

from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np

class SimplePerceptron(BaseEstimator, ClassifierMixin):
    def __init__(self, eta=1.0):
        self.class_labels_ = None
        self.w_ = None  # wektor wspolczynnikow
        self.k_ = 0  # liczba krokow algorytmu, jedynie dla informacji
        self.eta_ = eta
    
    def fit(self, X, y):
        m, n = X.shape  # rozmiar danych
        self.class_labels_ = np.unique(y)  # dowiadujemy sie jakie etykietki sa w y
        
        y_normalized = np.ones(m).astype("int8")  # do zamiany etykietek, dla zabezpieczenia - te ktore sa string na liczby 1, -1
        y_normalized[y == self.class_labels_[0]] = -1  # zamiana etykietek ns wlasne
        
        self.w_ = np.zeros(n + 1)  # inicjalizacja wartosci etykietek z kapelusza, losowo, albo jak tutaj 0
        self.k_ = 0  # jakby ktos ponownie uzyl funkcji fit
        
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
                    
            if len(E) == 0:
                break

            # teraz poprawka, trzeba sobie wylosowac jakis pkt sposrod zle sklasyfikowanych
            i = int(np.random.rand() * len(E))

            x = E[i]
            y = E_y[i]

            # wzor na poprawke
            self.w_ = self.w_ + self.eta_ * y * x    
            self.k_ += 1  # zwiekszenie liczinka krokow
            
        return self.w_, self.k_
    
    
    def predict(self, X):
        return self.class_labels_[(self.decision_function(X) > 0) * 1]  # patrzymy gdzie to co otrzymalismy jest wieksze od 0, zamieniamy odpowiedzi True/False na 0/1 przez pomnozenie razy 1; zwracamy odpowiednie etykietki klas; mozna tez zrobic petlami, ale macierzowo tak jak jest teraz dziala szybciej
    
    # nie potrzebna funkcja predict proba, bo klasyfikator jest geometryczny. nie zawiera prawdopodobienstw. zamiast tego jest funkcja decision_function. nie zwracamy wektora prawdopodobienstw poszczegolnych klas, tylko rzeczywiste wartosci
    def decision_function(self, X):
        # w X, ktorzy przychodzi siedzi pewna tabelka
        m, n = X.shape
        return self.w_.dot(np.c_[np.ones((m, 1)), X].T)  # do macierzy dokleilismy jedynke, transponujemy ja i mnozymy przez wektor wag w; w efekcie dostaje wektor rzeczywistych sum wazonych