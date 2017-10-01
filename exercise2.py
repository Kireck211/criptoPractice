from math import ceil
from heapq import heappush
from random import randint, random
from operator import attrgetter

bigram = {
    "DE" :  2.57,"AD" :  1.43,"TA" :  1.09,
    "ES" :  2.31,"AR" :  1.43,"TE" :  1.00,
    "EN" :  2.27,"RE" :  1.42,"OR" :  0.98,
    "EL" :  2.01,"AL" :  1.33,"DO" :  0.98,
    "LA" :  1.80,"AN" :  1.24,"IO" :  0.98,
    "OS" :  1.79,"NT" :  1.22,"AC" :  0.96,
    "ON" :  1.61,"UE" :  1.21,"ST" :  0.95,
    "AS" :  1.56,"CI" :  1.15,"NA" :  0.92,
    "ER" :  1.52,"CO" :  1.13,"RO" :  0.85,
    "RA" :  1.47,"SE" :  1.11,"UN" :  0.84
}

trigram = {
    "DEL":   0.75,"EST":   0.48,"PAR":   0.32,
    "QUE":   0.74,"LOS":   0.47,"DES":   0.31,
    "ENT":   0.67,"ODE":   0.47,"ESE":   0.30,
    "ION":   0.56,"ADO":   0.45,"IEN":   0.30,
    "ELA":   0.55,"RES":   0.40,"ALA":   0.29,
    "CON":   0.54,"STA":   0.38,"POR":   0.29,
    "SDE":   0.52,"ACI":   0.36,"ONE":   0.29,
    "ADE":   0.51,"LAS":   0.35,"NDE":   0.29,
    "CIO":   0.50,"ARA":   0.34,"TRA":   0.28,
    "NTE":   0.49,"ENE":   0.32,"NES":   0.27
}

class Individual:
    def __init__(self, key_length, crypted_text, known=None):
        self.key = []
        self.get_key(key_length)
        self.key_length = key_length
        self.text = self.get_text(crypted_text)
        self.text_length = len(self.text)
        self.known = known
        self.fitness = self.fitness()

    def __str__(self):
        return self.text

    def get_key(self, key_length):
        while (len(self.key) < key_length):
            rand_value = randint(0, key_length - 1)
            if (rand_value not in self.key):
                self.key.append(rand_value)

    def get_text(self, text):
        temp_matrix = []
        rows = ceil(float(len(text)) / self.key_length)
        for i in range(0, rows):
            aux = []
            for j in range(0, self.key_length):
                aux.append(0)
            temp_matrix.append(aux)
        for i in range(0, self.key_length):
            index = i * rows
            sub = text[index : index + rows]
            for j in range(0, len(sub)):
                temp_matrix[j][self.key[i]] = sub[j]
        rows = []
        for row in temp_matrix:
            rows.extend(row)
        return "".join(rows)

    def bigram_fitness(self):
        fitness = 0
        for i in range(0, self.text_length - 1):
            sub = self.text[i:i+2]
            if sub in bigram:
                fitness += bigram[sub]
        return fitness

    def trigram_fitness(self):
        fitness = 0
        for i in range(0, self.text_length - 2):
            sub = self.text[i:i+3]
            if sub in trigram:
                fitness += trigram[sub]
        return fitness

    def fitness(self):
        fitness = 0
        fitness += self.bigram_fitness()
        fitness += self.trigram_fitness()
        #if self.known != None and self.known in self.text:
            #fitness += 3
        return fitness

class Pop:
    def __init__(self, text, key_length, known=None, pop_length=100, mutation=0.01):
        self.text = text
        self.key_length = key_length
        self.pop_length = pop_length
        self.mutation = mutation
        self.pop = [ Individual(key_length, text, known) for i in range(pop_length) ]
        self.mating_pool = []
        self.answer = ""
        self.known = known
        self.max_fit = self.max_fitness()

    def normalize(self, value, max_num):
        return value / max_num

    def max_fitness(self):
        max_fit = -1
        for individual in self.pop:
            if individual.fitness > max_fit:
                max_fit = individual.fitness
        return max_fit

    def selection(self):
        for individual in self.pop:
            fitness = self.normalize(individual.fitness, self.max_fitness())
            for i in range(0, int(fitness * 100)):
                self.mating_pool.append(individual)

    def crossover(self, partner_a, partner_b):
        child = partner_a[:int(randint(0, len(partner_a)-1))]
        while len(child) < len(partner_a):
            for value in partner_b:
                if value not in child:
                    child.append(value)
        return child

    def mutate(self, child):
        if random() <= self.mutation:
            first_i = randint(0, len(child)-1)
            second_i = randint(0, len(child)-1)
            child[first_i], child[second_i] = child[second_i], child[first_i]
        return child

    def new_generation(self):
        for i in range(0, self.pop_length):
            a_index = int(randint(0, len(self.mating_pool) - 1))
            b_index = int(randint(0, len(self.mating_pool) - 1))
            while a_index == b_index:
                b_index = int(randint(0, len(self.mating_pool) - 1))
            partner_a = self.mating_pool[a_index]
            partner_b = self.mating_pool[b_index]
            child = self.crossover(partner_a.key, partner_b.key)
            child = self.mutate(child)
            child = Individual(len(child), self.text, self.known)
            self.pop[i] = child
            self.max_fit = self.max_fitness()

    def evolve(self):
        pop_length = len(self.pop)
        self.selection()
        self.new_generation()

    def get_fittest(self):
        fit = -1
        fittest = None
        for individual in self.pop:
            if individual.fitness > fit:
                fit = individual.fitness
                fittest = individual
        return fittest


    def is_done(self):
        for individual in self.pop:
            if self.known in individual.text:
                self.answer = individual
                return True
        return False


def main():
    global theBestOfEver
    n_keys = []
    text = ""
    with open('text2.txt') as f:
        list_lines = []
        for line in f:
            list_lines.append(line)
        text = "".join(list_lines)
    with open('keys2.txt') as f:
        for line in f:
            for key_length in line.split(","):
                n_keys.append(int(key_length))
    fo = open("textout2.txt", "w")
    for key_length in n_keys:
        pop = Pop(text, key_length, "ELENANO", 200)
        count = 0
        found = False
        founded = []
        last_founded = -1
        while(count < 1000):
            pop.evolve()
            found = pop.is_done()
            if found:
                founded.append((pop.answer.text, pop.answer.fitness))
                founded = list(set(founded))
            count += 1
            if count % 100 == 0:
                print(count)

        for answer in founded:
            fo.write(str(key_length)+"\n")
            fo.write(answer[0] + "\n")
            fo.write(str(answer[1]))
            fo.write("\n")
    with open("textout2.txt") as f:
        i = 0
        max_20 = []
        temp = []
        for line in f:
            temp.append(line.replace("\n",""))
            if i == 2:
                temp[2] = float(temp[2])
                temp[0], temp[2] = temp[2], temp[0]
                heappush(max_20, temp)
                temp = []
            i+=1
            i%=3
    max_20 = max_20[:-40]
    fo = open("textfinal2.txt", "w")
    for value in max_20:
        fo.write(str(value[2])+"\n")
        fo.write(value[1]+"\n")
        fo.write(str(value[0])+"\n")


main()