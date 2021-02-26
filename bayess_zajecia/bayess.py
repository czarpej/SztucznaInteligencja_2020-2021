# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:04:39 2020

@author: Czarny
"""

import numpy as np
from sklearn.model_selection import train_test_split
from nbc import DiscreteNBC


def read_wine_data(path):
    D = np.genfromtxt(path, delimiter=",")

    X = D[:, 1:]
    y = D[:, 0]

    return X, y


# dyskretyzacja wybranej zmiennej - podzial na wybrana liczbe kubelkow
def discretize(X, B: int, X_ref=None):
    # B to liczba kubelkow
    # X_ref to dane referencyjne, sluzy do tego, aby wyciagnac minima i maksima, sluzy do tego, aby szufladki kubelkow sie nie przesuwaly. W ogolnosci jest to po to, aby jak przyjda dane testowe to wybrac min i max na podstawie danych uczacych
    if X_ref is None:
        X_ref = X;

    mins = np.min(X_ref, axis=0)  # wybranie minimow kolumn; jest brane wzdluz wymiaru wierszowego i wyjdzie 13 kolumn
    maxes = np.max(X_ref, axis=0)  # wybranie maksimow kolumn
    X_d = np.floor((X - mins) / (maxes - mins) * B).astype("int8")  # X dyskretne

    return np.clip(X_d, 0, B - 1)  # zwroc przyciete X dyskretne od 0 do B - 1


def train_test_split_mine(X, y, train_ratio = 0.75, seed = 0):
    m = X.shape[0]  # wybranie pierwszego wymiaru

    np.random.seed(seed)
    indexes = np.random.permutation(m)  # losowa permutacja m indeksow

    X = X[indexes]
    y = y[indexes]

    split = round(train_ratio * m)  # indeks progowy
    X_train = X[:split]  # wszystkie do split bez split (split - 1)
    y_train = y[:split].astype("int32")
    X_test = X[split:]  # od indeksu split w gore
    y_test = y[split:].astype("int32")

    return X_train, y_train, X_test, y_test


if __name__ == "__main__":
    X, y = read_wine_data("wine.data")

    # powielenie danych - zepsucie programu
    X = np.tile(X, (1, 100))

    X_train, y_train, X_test, y_test = train_test_split_mine(X, y)
    m, n = X_train.shape

    B = 15  # liczba koszykow dyskretyzacyjnych
    X_train_d = discretize(X_train, B)
    X_test_d = discretize(X_test, B, X_ref=X_train)

    domain_sizes = np.ones(n, dtype="int8") * B  # rozmiary naszych dziedzin
    dnbc = DiscreteNBC(domain_sizes=domain_sizes, laplace=True)
    dnbc.fit(X_train_d, y_train)

    print(X_test_d.shape)  # ilosc przykladow testowych

    # dokladnosc na rzecz danych uczacych
    predictions_train = dnbc.predict(X_train_d)
    accuracy_train = (predictions_train == y_train).mean()
    print("TRAIN ACCURACY: " + str(accuracy_train))
    print("TRAIN ACCURACY2: " + str(dnbc.score(X_train_d, y_train)))  # score wbudowane w nasza klase dzieki dziedziczenu, potrzebne mu tez sa etykietki

    # dokladnosc na rzecz danych testowych
    predictions_test = dnbc.predict(X_test_d)
    accuracy_test = (predictions_test == y_test).mean()
    print("TEST ACCURACY: " + str(accuracy_test))
    print("TEST ACCURACY2: " + str(dnbc.score(X_test_d, y_test)))

    # k / n - 62% prawdopodobienstwa, to logicznie 62/100
    # (k + 1) / (n + 2) - zdarzenia binarne, unika zdarzen skrajnych
    # (k + 1) / (n + domain_sizes[j]) - nie bedzie zer i jedynek
