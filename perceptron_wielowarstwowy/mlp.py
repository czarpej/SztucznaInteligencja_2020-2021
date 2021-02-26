# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 14:23:03 2021

@author: Czarny
"""

from sklearn.base import BaseEstimator, RegressorMixin
import numpy as np
import copy


class MLP(BaseEstimator, RegressorMixin):
    def __init__(self, K:int = 1, T:int = 10**3, eta:float = 0.01, mu:float = 0.9, random_state:float = 0, batch_size:int = 1, method:str = "backprop"):
        self.K_ = K  # liczba neuronow
        self.T_ = T  # liczba iteracji uczacych
        self.eta_ = eta  # wspolczynnik uczenia
        self.random_state_ = random_state  # random seed
        self.V_ = None  # K x (n + 1); sygnaly pochodzace od n zmiennych
        self.W_ = None  # K + 1
        self.V_scale_ = 10**(-3)  # z jak szerokiego przedzialu sa te przedzialy wagowe wylosowane
        self.batch_size_ = batch_size  # ile probek chce przeliczyc przed wstawieniem poprawki
        self.method_ = method
        self.mu_ = mu  # wspolczynnik rozpedu
        
    def fit(self, X, y):
        if self.method_ == "backprop":
            self.fit_backprop(X, y)
        elif self.method_ == "momentum":
            self.fit_momentum(X, y)
        else:
            self.fit_rprop(X, y)
        
    def fit_backprop(self, X, y):
        np.random.seed(self.random_state_)  # ustawienie seeda losowania
        
        m, n = X.shape
        
        self.V_ = (np.random.rand(self.K_, n + 1) * 2 - 1) * self.V_scale_  # mnozenie przez 2 i odjecie -1 sprawia, ze beda na chwile w przedziale <-1; 1>; po pomnozeniu przez V_scale sa one z przedzialu 0.001 do ...; to pomoga duzo w uczeniu
        self.W_ = np.random.rand(1, self.K_ + 1)  # wymuszenie, aby to byl wiersz
        
        for t in range(self.T_):
            dV = np.zeros(self.V_.shape)
            dW = np.zeros(self.W_.shape)
            
            # unikalne liczby z m i wzieta pewna liczba pierwszych wyrazow
            indexes = np.random.permutation(m)[:self.batch_size_]
            
            # kumulowanie gradientow
            for i in indexes: 
                x = (np.c_[1.0, np.array([X[i]])]).T  # wyciaga pkt, dokleja 1 z przodu i robi z niego kolumne za pomoca T;
                
                s = self.V_.dot(x)  # K sum wazonych
                phi = 1.0 / (1.0 + np.exp(-s))
                one_phi = np.r_[np.array([[1.0]]), phi]
                
                # przeksztalcenie wag W
                y_MLP = self.W_.dot(one_phi)[0, 0]
                
                # dokladanie macierzy poprawek
                dV += np.dot((y_MLP - y[i]) * np.array([self.W_[0, 1:]]).T * phi * (1.0 - phi), x.T)  # (y_MLP - y[i]) * w_k * phi_k * (1 - phi_k) * x_j; y_MLP to jest skalar; pozniej mnozenie przez wagi W bez pierwszej kolumny 
                dW += ((y_MLP - y[i]) * one_phi).T #  (Y_MLP - y[i]) * one_phi
            
            # poprawki
            self.V_ = self.V_ - self.eta_ * dV  # np.sign(dV); zamiast self.eta_ bedzie cala macierz wspolczynnikow uczenia, nie bedzie self.eta_; zrobic wektor etaV, etaW; dobrze uzyc funkcji np.clip(macierz, min, max) ktora obcina wartosci w macierzy do zadanych widelek; jezeli iloczyn dwoch gradientow jest tego samego znaku to idziemy w tym samym kierunku; macierzowo modyfikowac macierz wspolczynnikow mnozenia
            self.W_ = self.W_ - self.eta_ * dW  # np.sign(dW) - miec zapamietane takie samo cos z poprzedniej iteracji dV_sign_prev; jak sie pomnozy przez siebie te dwie macierze np.sign(dV) * dV_sign_prev > 0 || < 0 = 0.5
            
    def fit_momentum(self, X, y):
        np.random.seed(self.random_state_)  # ustawienie seeda losowania
        
        m, n = X.shape
        
        self.V_ = (np.random.rand(self.K_, n + 1) * 2 - 1) * self.V_scale_  # mnozenie przez 2 i odjecie -1 sprawia, ze beda na chwile w przedziale <-1; 1>; po pomnozeniu przez V_scale sa one z przedzialu 0.001 do ...; to pomoga duzo w uczeniu
        self.W_ = np.random.rand(1, self.K_ + 1)  # wymuszenie, aby to byl wiersz
        
        for t in range(self.T_):
            dV = np.zeros(self.V_.shape)
            dW = np.zeros(self.W_.shape)
            
            deltaV = np.zeros(self.V_.shape)
            deltaW = np.zeros(self.W_.shape)
            
            # unikalne liczby z m i wzieta pewna liczba pierwszych wyrazow
            indexes = np.random.permutation(m)[:self.batch_size_]
            
            # kumulowanie gradientow
            for i in indexes: 
                x = (np.c_[1.0, np.array([X[i]])]).T  # wyciaga pkt, dokleja 1 z przodu i robi z niego kolumne za pomoca T;
                
                s = self.V_.dot(x)  # K sum wazonych
                phi = 1.0 / (1.0 + np.exp(-s))
                one_phi = np.r_[np.array([[1.0]]), phi]
                
                # przeksztalcenie wag W
                y_MLP = self.W_.dot(one_phi)[0, 0]
                
                # dokladanie macierzy poprawek
                dV += np.dot((y_MLP - y[i]) * np.array([self.W_[0, 1:]]).T * phi * (1.0 - phi), x.T)  # (y_MLP - y[i]) * w_k * phi_k * (1 - phi_k) * x_j; y_MLP to jest skalar; pozniej mnozenie przez wagi W bez pierwszej kolumny 
                dW += ((y_MLP - y[i]) * one_phi).T #  (Y_MLP - y[i]) * one_phi
               
            # w kazdym kroku wylicza poprawke na podstawie poprzedniej
            deltaV = - self.eta_ * dV + self.mu_ * deltaV
            deltaW = - self.eta_ * dW + self.mu_ * deltaW   
            
            # poprawki - do starych poprawek dodaje nowe
            self.V_ = self.V_ + deltaV
            self.W_ = self.W_ + deltaW
            
    def fit_rprop(self, X, y):
        np.random.seed(self.random_state_)  # ustawienie seeda losowania
        
        m, n = X.shape
        
        self.V_ = (np.random.rand(self.K_, n + 1) * 2 - 1) * self.V_scale_  # mnozenie przez 2 i odjecie -1 sprawia, ze beda na chwile w przedziale <-1; 1>; po pomnozeniu przez V_scale sa one z przedzialu 0.001 do ...; to pomoga duzo w uczeniu
        self.W_ = np.random.rand(1, self.K_ + 1)  # wymuszenie, aby to byl wiersz
        
        # stale do metody
        eta_0 = 0.01
        eta_min = 10**-3
        eta_max = 50
        eta_increase = 1.2
        eta_decrease = 0.5
        
        etaV_prev = np.ones(self.V_.shape) * eta_0
        etaW_prev = np.ones(self.W_.shape) * eta_0
        
        
        for t in range(self.T_):
            dV = np.zeros(self.V_.shape)
            dW = np.zeros(self.W_.shape)
            
            # od poprzednich iteracji
            dV_prev = np.zeros(self.V_.shape)
            dW_prev = np.zeros(self.W_.shape)
            
            # unikalne liczby z m i wzieta pewna liczba pierwszych wyrazow
            indexes = np.random.permutation(m)[:self.batch_size_]
            
            # kumulowanie gradientow
            for lp, i in enumerate(indexes): 
                x = (np.c_[1.0, np.array([X[i]])]).T  # wyciaga pkt, dokleja 1 z przodu i robi z niego kolumne za pomoca T;
                
                s = self.V_.dot(x)  # K sum wazonych
                phi = 1.0 / (1.0 + np.exp(-s))
                one_phi = np.r_[np.array([[1.0]]), phi]
                
                # przeksztalcenie wag W
                y_MLP = self.W_.dot(one_phi)[0, 0]
                
                # dokladanie macierzy poprawek
                dV += np.dot((y_MLP - y[i]) * np.array([self.W_[0, 1:]]).T * phi * (1.0 - phi), x.T)  # (y_MLP - y[i]) * w_k * phi_k * (1 - phi_k) * x_j; y_MLP to jest skalar; pozniej mnozenie przez wagi W bez pierwszej kolumny 
                dW += ((y_MLP - y[i]) * one_phi).T #  (Y_MLP - y[i]) * one_phi
            
            if t == 0:
                dV_prev = copy.copy(dV)
                dW_prev = copy.copy(dW)
            
            etaV = copy.deepcopy(etaV_prev)
            etaW = copy.deepcopy(etaW_prev)
            
            productDerivativesDV = dV * dV_prev
            etaV[productDerivativesDV > 0] = np.minimum(eta_increase * etaV[productDerivativesDV > 0], eta_max)
            etaV[productDerivativesDV < 0] = np.maximum(eta_decrease * etaV[productDerivativesDV < 0], eta_min)
                
            productDerivativesDW = dW * dW_prev
            etaW[productDerivativesDW > 0] = np.minimum(eta_increase * etaW[productDerivativesDW > 0], eta_max)
            etaW[productDerivativesDW < 0] = np.maximum(eta_decrease * etaW[productDerivativesDW < 0], eta_min)
            
            etaW_prev = copy.deepcopy(etaW)
            etaV_prev = copy.deepcopy(etaV)
                
            
            # poprawki
            self.V_ = self.V_ - etaV * np.sign(dV)  # np.sign(dV); zamiast self.eta_ bedzie cala macierz wspolczynnikow uczenia, nie bedzie self.eta_; zrobic wektor etaV, etaW; dobrze uzyc funkcji np.clip(macierz, min, max) ktora obcina wartosci w macierzy do zadanych widelek; jezeli iloczyn dwoch gradientow jest tego samego znaku to idziemy w tym samym kierunku; macierzowo modyfikowac macierz wspolczynnikow mnozenia
            self.W_ = self.W_ - etaW * np.sign(dW)  # np.sign(dW) - miec zapamietane takie samo cos z poprzedniej iteracji dV_sign_prev; jak sie pomnozy przez siebie te dwie macierze np.sign(dV) * dV_sign_prev > 0 || < 0 = 0.5
            
            dV_prev = copy.copy(dV)
            dW_prev = copy.copy(dW)
            
    # chcemy zrobic przegieg sieci w przod dla calej tabelki; dostaje zestaw X w formie macierzy
    def predict(self, X):
        m = X.shape[0]  # ile wierszy jest w tej tabelce
        
        X = np.c_[np.ones((m, 1)), X].T  # rozszerzenie o kolumne jedynek i transpozycja; otrzymujemy (n + 1) x m 
        s = self.V_.dot(X)  # K x m
        
        phi = 1.0 / (1.0 + np.exp(-s))
        one_phi = np.r_[np.ones((1, m)), phi]
        
        y_MLP = self.W_.dot(one_phi)
        
        return y_MLP[0]
        