import numpy as np

class GeneticAlgorithm(object):

    def __init__(self, n=None, m=1000, T=100, prob_cross_over=0.9, prob_mutation=10.0**(-3), selection="selection_rank", crossover="crossover_twopoint", fitness=None, fitness_params=None, seed=0, history=False):
        self.n_ = n
        self.m_ = m
        self.T_ = T
        self.prob_cross_over_ = prob_cross_over
        self.prob_mutation_ = prob_mutation
        self.selection_ = getattr(self, selection)
        self.crossover_ = getattr(self, crossover)
        self.mutation_ = getattr(self, "mutation_ordinary")
        self.fitness_ = fitness
        self.fitness_params_ = fitness_params
        self.seed_ = seed 
        self.history_ = history
        if self.n_ is None or self.n_ <= 0:
            raise RuntimeError("Number of bits n (chromosome length) must be a positive integer.")        
        if self.fitness_ is None:
            raise RuntimeError("Pointer to fitness function must not be none.")
        self.solution = None        
        self.randomizer_ = np.random.RandomState(self.seed_)  
    
    def selection_roulette(self, population, f):
        prob = f / f.sum()
        #prob_cum = np.cumsum(prob)
        indexes = self.randomizer_.choice(self.m_, self.m_, p=prob)
        return population[indexes]  
    
    def selection_rank(self, population, f):                
        rank = f.argsort().argsort() + 1
        prob = rank / rank.sum()
        #prob_cum = np.cumsum(prob)
        indexes = self.randomizer_.choice(self.m_, self.m_, p=prob)
        return population[indexes]        
    
    def crossover_onepoint(self, population):
        indexes = self.randomizer_.permutation(self.m_)
        population_new = np.zeros((self.m_, self.n_), dtype="int8")
        for i in range(int(self.m_ / 2)):
            l = 2 * i
            r = l + 1
            if self.randomizer_.rand() < self.prob_cross_over_:
                point = 1 + self.randomizer_.randint(self.n_ - 1)            
                population_new[l] = np.r_[population[indexes[l], :point], population[indexes[r], point:]]
                population_new[r] = np.r_[population[indexes[r], :point], population[indexes[l], point:]]
            else:
                population_new[l] = population[indexes[l]]
                population_new[r] = population[indexes[r]]
        return population_new  

    def crossover_twopoint(self, population):
        indexes = self.randomizer_.permutation(self.m_)
        population_new = np.zeros((self.m_, self.n_), dtype="int8")
        for i in range(int(self.m_ / 2)):
            l = 2 * i
            r = l + 1            
            if self.randomizer_.rand() < self.prob_cross_over_:
                points = np.sort((self.randomizer_.permutation(self.n_ - 1) + 1)[:2])
                population_new[l] = np.r_[population[indexes[l], :points[0]], population[indexes[r], points[0]:points[1]], population[indexes[l], points[1]:]]
                population_new[r] = np.r_[population[indexes[r], :points[0]], population[indexes[l], points[0]:points[1]], population[indexes[r], points[1]:]]                
            else:
                population_new[l] = population[indexes[l]]
                population_new[r] = population[indexes[r]]
        return population_new 
    
    def mutation_ordinary(self, population):
        indexes = self.randomizer_.rand(self.m_, self.n_) < self.prob_mutation_
        mutation_matrix = np.zeros((self.m_, self.n_), dtype="int8")
        mutation_matrix[indexes] = 1;
        population_new = (np.logical_xor(population, mutation_matrix) * 1).astype("int8")
        return population_new
    
    def execute(self):
        best_f = -np.inf
        solution = None
        history_f_mean = []
        history_f_best = []
        if self.seed_ is not None:
            np.random.seed(self.seed_)
        population = np.round(np.random.rand(self.m_, self.n_)).astype("int8")
        f = np.zeros(self.m_)            
        for t in range(self.T_):
            for i in range(self.m_):
                f[i] = self.fitness_(population[i], **self.fitness_params_)
            index = f.argmax()
            if f[index] > best_f:
                best_f = f[index]
                solution = population[index]
            if self.history_:
                history_f_mean.append(np.mean(f))
                history_f_best.append(best_f)
            population = self.selection_(population, f)
            population = self.crossover_(population)
            population = self.mutation_(population)
        for i in range(self.m_):        
            f[i] = self.fitness_(population[i], **self.fitness_params_)
        index = f.argmax()
        if f[index] > best_f:
            best_f = f[index]
            solution = population[index]
        if self.history_:
            history_f_mean.append(np.mean(f))
            history_f_best.append(best_f)                            
        return best_f, solution, history_f_mean, history_f_best