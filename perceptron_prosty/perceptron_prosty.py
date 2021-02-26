import numpy as np
import matplotlib.pyplot as plt
import random
import math

#rozmiar ukladu wspolrzednych
x_start = -1
x_stop = 1
y_start = -1
y_stop = 1

#funkcja okreslajaca odleglosc miedzy 2 punktami przy podaniu ich wspolrzednych
def distance(x1_1, x1_2, x2_1, x2_2):
    return math.sqrt((x1_1 - x1_2)**2 + (x2_1 - x2_2)**2)

#funkcja generujaca macierz punktow i ich klas
#jako argumenty podajemy liczbe punktow (lliczba wierszy) oraz minimalna odleglosc miedzy klasami
def generate_matrix(m, min_distance):
    A = np.zeros((m,4))
    #x1 = np.random.uniform(-1, 1, m)
    #x2 = np.random.uniform(-1, 1, m)
    x1 = []
    x2 = []
    labels = []

    x1.append(np.random.uniform(x_start, x_stop))
    x2.append(np.random.uniform(y_start, y_stop))
    if(x1[0] > x2[0]):
        labels.append(1)
    else:
        labels.append(-1)

    while(1):

        #warunek stopu
        if(len(x1) == m):
            break;

        label_wanna_be = 0
        x1_wanna_be = np.random.uniform(x_start, x_stop)
        x2_wanna_be = np.random.uniform(y_start, y_stop)

        if(x1_wanna_be > x2_wanna_be):
            label_wanna_be = 1
        else:
            label_wanna_be = -1

        
        cnt_differents = 0;
        cnt_propers = 0;

        for i in range(len(x1)):
            if(label_wanna_be != labels[i]):
                cnt_differents+=1
                if(distance(x1[i], x1_wanna_be, x2[i], x2_wanna_be) > min_distance):
                    cnt_propers+=1

        if(cnt_differents == cnt_propers):
            x1.append(x1_wanna_be)
            x2.append(x2_wanna_be)
            labels.append(label_wanna_be)

    #labels = []

    #inicjowanie macierzy
    for i in range(m):
        A[i][0] = 1
        A[i][1] = x1[i] 
        A[i][2] = x2[i]
        A[i][3] = labels[i]
        #if(x1[i] > x2[i]):
        #    A[i][3] = 1
        #else:
        #    A[i][3] = -1
        #labels.append(A[i][3])

    return A;



#funkcja obliczajaca iloczyn skalarny wektora wag i wektora cech
def scalar_product(row, weights):
    sum = 0
    for i in range(len(weights)):
        sum+=row[i]*weights[i]

    return sum

#funkcja okreslajaca klase dla podanego wektora
def activation(scalar_product):
    if(scalar_product > 0):
        return 1
    if (scalar_product <= 0):
        return -1

def wrong_classified(data, classes):
    m = len(data)
    E = [] 
    for i in range(m):
        if(data[i][-1] != classes[i]):
            E.append(data[i])
    return E

#algorytm uczenia perceptronu prostego
#jako argumenty podajemy zbior danych oraz wspolczynnik uczenia
#wspolczynnik uczenia (n) to liczba z przedzialu (0,1]
def perceptron(data, n):

    m = len(data)

    weights=np.zeros(len(data[0])-1); #wagi
    k = 0 #licznik krokow

    classes = np.zeros(m) #zbior klas/etykiet, ktore okreslila funkcja activation()

    errors = 1

    while(1):
        #definiowanie 'odgadnietych' klas
        for i in range(m):
            product = scalar_product(data[i], weights)
            classes[i] = activation(product)

        #definiowanie blednie sklasyfikowanych punktow
        E = wrong_classified(data, classes)

        #warunek stopu
        if(len(E) == 0):
            return weights, k

        #wybieranie losowego punktu
        random_position = random.randrange(len(E)) 
        random_point = E[random_position]

        error = random_point[-1] - activation(scalar_product(random_point, weights))
        weights += error * n * random_point[:-1]

        #for i in range (len(weights)):
        #    weights[i] += error * n * random_point[i]

        k += 1


    return weights, k

def draw_plot(matrix, weights):

    #if(weights[0] == 0):
    #    weights[0] = 0.00001
    x1 = matrix[:,1]
    x2 = matrix[:,2]
    labels = matrix[:,3]

    plt.scatter(x1, x2, marker = 'o', c = labels)

    _x = []
    _y = []
    #for i in np.linspace(np.amin(x1), np.amax(x1)):
    #    slope = -(weights[0]/weights[2])/(weights[0]/weights[1])  
    #    intercept = -weights[0]/weights[2]
    #    y = (slope*i) + intercept
    #    _x.append(i)
    #    _y.append(y)

    x1_min = np.amin(x1)
    x1_max = np.amax(x1)
    x2_min =(-weights[1]*x1_min-weights[0])/weights[2]
    x2_max =(-weights[1]*x1_max-weights[0])/weights[2]
    #ax + by + c = 0
        
    plt.plot([x1_min, x1_max], [x2_min, x2_max])
    plt.show()

    

m = [10, 100, 1000]
eta = [0.01, 0.1, 0.99]
margines = [1, 0.01, 0.1]

for i in range(len(margines)):
    print("---------------------------------------")
    print("Odstep miedzy klasami: ", margines[i])
    for j in range(len(m)):
        print("Liczba probek: ", m[j])
        A = generate_matrix(m[j], margines[i])
        for k in range(len(eta)):
            wynik = perceptron(A, eta[k])

            print("Eta: ", eta[k], ", k =", wynik[1])
            print(wynik[0])
            draw_plot(A, wynik[0])

#statystyczne wyniki
for i in range(len(margines)):
    print("---------------------------------------")
    print("Odstep miedzy klasami: ", margines[i])
    for j in range(len(m)):
        print("Liczba probek: ", m[j])
        A = generate_matrix(m[j], margines[i])
        counts = np.zeros(len(eta))
        for k in range(len(eta)):
            for n in range(100):
                counts[k] += perceptron(A, eta[k])[1]
            counts[k] /= 100
            print("Eta: ", eta[k], ", k =", counts[k])
