# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 14:38:45 2020

@author: Czarny
"""

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin

class DiscreteNBC(BaseEstimator, ClassifierMixin):
    def __init__(self, domain_sizes=None, laplace=False):
        self.class_labels_ = None  # etykietki klas
        self.PY_ = None  # wektor numpy z prawdopodobienstwami (a priori - jak czesto jest jedna, druga, trzecia klasa) klas
        self.P_ = None  # struktura 3-wymiarowa z wszystkimi rozkladami warunkowymi; P[2, 7][1] = Pr(X_7 = 1 | Y = 2) (X_7 - zmienna siodma)
        self.domain_sizes_ = domain_sizes
        self.laplace_ = laplace
    
    def fit(self, X, y):
        m, n = X.shape  # rozmiar danych uczacych m wierszy i n kolumn
        self.class_labels_ = np.unique(y)  # rejestracja unikalnych etykiet klas - 'K' 'M'; tutaj z winem sa etykietki 1, 2, 3
        y_normalized = np.zeros(m, dtype="int8")  # uniezaleznienie od postaci etykiet, kiedy przyjda w postaci tekstowej
        
        for yy, label in enumerate(self.class_labels_):
            # y == label # zaglada do y i sprawdza, gdzie one sa rowne label; zwraca rownoliczny wektor z wartosciami True/False
            y_normalized[y == label] = yy  # tam gdzie w y jest label, to w tym samym miejscu w y_normalized wpisz yy; y oraz y_normalized musza miec taka sama dlugosc !!
            
        self.PY_ = np.zeros(self.class_labels_.size)
        
        for yy, label in enumerate(self.class_labels_):
            # np.sum(y == label)  # zwroci liczbe wystapien klasy o etykiecie label
            self.PY_[yy] = np.sum(y == label) / m
        
        # rejestracja rozkladow warunkowych
        self.P_ = np.empty((self.class_labels_.size, n), dtype="object")  # utworzenie pustej macierzy
        for yy, label in enumerate(self.class_labels_):
            for j in range(n):
                self.P_[yy, j] = np.zeros(self.domain_sizes_[j])  # liczba klas * liczba atrybutow i wstepna rezerwacja pamieci
    
        # wlasciwe uczenie - rejestrowanie prawdopodobienstw
        for i in range(m):  # petla po przykladach uczacych
            for j in range(n):  # petla po kolumnach
                # pierwszy przyklad uczacy jest w klasie pierwszej. przyklad: wino ma kolor czerwony, jest z klasy 1. zwiekszamy licznik dla wina czerwonego klasy 1
                v = X[i, j]
                self.P_[y_normalized[i], j][v] += 1  # licznik wystapien poszczegolnych wydarzen
        
        # sa 3 plastry. w ramach kazdej klasy win rozklad kazdego atrybutu. my to podzielilismy na 5 klas: klasa 0, 1, 2, 3, 4. liczba w odpowiednim indeksie oznacza liczbe wystapien wybranej klasy pod warunkiem klasy odgornej. np. pierwszy plaster; pierwsza tablica, 5 wartosci, wiec 5 klas. wartosc w indeksie 2, czyli srodkowa, bo liczymy od 0 oznacza, ze tyle razy wystapila etykieta klasy 2 pod warunkiem ogolnej klasy wyzszej, czyli tutaj tego pierwszego plastra. czyli dla win: wino klasy 2 wystapilo iles razy pod warunkiem bycia winem czerwonym
        # w pierwszym plastrze w kazdym wierszu sumy sa takie same, bo dotyczy to win klasy pierwszej
       # print(self.P_)
        
        if not self.laplace_:       
            for yy, label in enumerate(self.class_labels_):
                y_sum = self.PY_[yy] * m  # liczba przykladow klasy y
                for j in range(n):
                    self.P_[yy, j] /= y_sum
        else:
            for yy, label in enumerate(self.class_labels_):
                y_sum = self.PY_[yy] * m  # liczba przykladow klasy y
                for j in range(n):
                    self.P_[yy, j] = (self.P_[yy, j] + 1) / (y_sum + self.domain_sizes_[j])
                
    
    # zwraca dla kazdego x w X etykiete klasy; zwraca zestaw przewidywanych klas dla danych obiektow testowych
    def predict(self, X):
        return self.class_labels_[np.argmax(self.predict_proba(X), axis=1)]
    
    # zwraca dla kazdego x w X wektor pradwdopodobienstw: P(Y -1 | x), P(Y - 2 | x), P(Y - 3 | x)
    def predict_proba(self, X):
        # y* = arg max_y prod_(j = 1)^n P(X_j = x_j | Y = y) P(Y = y)
        
        m, n = X.shape
        scores = np.ones((m, self.class_labels_.size))  # macierz na wyniki; kolumn ma byc tyle co klas
        
        for i in range(m):  # musimy przerobic m przykladow
            # x = X[i, :] -> x = [3, 1, 1, 2, 0, 4, ...]
            x = X[i]
            
            for yy in range(self.class_labels_.size):  # petla po klasach
                for j in range(n):  # jest n cech, j iteruje po kolumnach
                    # x = [3, 1, 2, ...]. zakladamy, ze testujemy wino klasy 0. jest iles tam atrybutow. patrzy w atrybut pierwszy ma wartosc 3, w pierwszym wierszu/rozkladzie patrzy co jest na trzeciej pozycji
                    # tutaj zamiast mnozenia dodawania logarytmow
                    scores[i, yy] += np.log2(self.P_[yy, j][x[j]])  # testujemy klase o etykietce yy, patrzymy na j-ty atrybut
                    
                scores[i, yy] += np.log2(self.PY_[yy])
                
            # s = scores[i].sum()
            # if s > 0.0:
            #     scores[i] /= s
        
        return scores
        