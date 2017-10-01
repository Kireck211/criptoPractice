from math import ceil
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
        self.text_length = len(text)
        self.known = known
        self.fitness = self.fitness()

    def __str__(self):
        return "hi"

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
        text_length = len(text)
        for i in range(0, text_length - 1):
            sub = text[i:i+2]
            if sub in bigram:
                fitness += bigram[sub]
        return fitness

    def trigram_fitness(self):
        fitness = 0
        text_length = len(text)
        for i in range(0, text_length - 2):
            sub = text[i:i+3]
            if sub in trigram:
                fitness += trigram[sub]
        return fitness

    def fitness(self):
        fitness = 0
        fitness += self.bigram_fitness()
        fitness += self.trigram_fitness()
        if self.known != None and self.known in text:
            fitness += 3
        return fitness

class Pop:
    def __init__(self, text, key_length, pop_length=100, known=None, mutation=0.01):
        self.text = text
        self.key_length = key_length
        self.pop_length = pop_length
        self.mutation = mutation
        self.pop = [ Individual(key_length, text, known) for i in range(pop_length) ]
        self.mating_pool = []
        self.answer = ""

    def normalize(self, value, max_num):
        print(value)
        print(max_num)
        input()
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
        while len(child) < partner_a:
            for value in partner_b:
                if value not in child:
                    child.append(value)
        return child

    def mutate(self, child):
        if random() <= mutation:
            first_i = randint(0, len(child)-1)
            second_i = randint(0, len(child)-1)
            child[first_i], child[second_i] = child[second_i], child[first_i]
        return child

    def new_generation(self):
        for i in range(0, pop_length):
            a_index = int(randint(0, len(self.mating_pool) - 1))
            b_index = int(randint(0, len(self.mating_pool) - 1))
            while a_index == b_index:
                b_index = int(randint(0, len(self.mating_pool) - 1))
            partner_a = self.mating_pool[a_index]
            partner_b = self.mating_pool[b_index]
            child = self.crossover(partner_a, partner_b)
            child = self.mutate(child)
            self.pop[i] = child

    def evolve(self):
        pop_length = len(self.pop)
        self.selection()
        self.new_generation()

    def is_done(self):
        for individual in pop:
            if "ENANO" in individual.text:
                self.answer = individual
                return True
        return False


def main():
    global theBestOfEver
    global text
    n_keys = []
    with open('text2.txt') as f:
        list_lines = []
        for line in f:
            list_lines.append(line)
        text = "".join(list_lines)
    with open('keys2.txt') as f:
        for line in f:
            for key_length in line.split(","):
                n_keys.append(int(key_length))
    for key_length in n_keys:
        pop = Pop(text, key_length)
        count = 0
        found = False
        while(not found and count < 10000):
            pop.evolve()
            found = pop.is_done()
            if found:
                print(pop.answer)
                exit(0)
            count += 1
            if count % 100 == 0:
                print(count)

main()
"""print(decrypt([0,1,2]))
keys = []
popu_l = 50
for key in n_keys:
    keys.append([key, population(popu_l, key)])
fo = open("textout2.txt", "w")
foundWord = False
count = 1
while (True):
    popu_l = 50
    keys_l = len(keys)
    for i in range(0, keys_l):
        key_length = keys[i][0]
        keys[i][1] = evolve(keys[i][1], key_length)
        for val in best_fit:
            decrypted_text = decrypt(list(val[1]))
            if ("TEXTO" in decrypted_text):
                fo.write("key: " + str(key_length) + "\n")
                fo.write(decrypted_text+"\n\n")
                exit(0)
    if (count % 10 == 0):
        for key in keys:
            print(key[0])
            for val in best_fit:
                print(decrypt(list(val[1])))
            input()
    if (count % 100 == 0):
        print(count)
    count += 1

main()

text = ""

def parseText(text, key_length):
chunks = len(text)
return [ text[i:i+key_length] for i in range(0, chunks, key_length) ]

def generate_matrix(key):
new_matrix = []
for i in range(0, len(basic_matrix)):
    aux = []
    for j in range(0,len(key)):
        aux.append(0)
    new_matrix.append(aux)
for i in range(0, len(basic_matrix)):
    for j in range(0,len(key)):
        new_matrix[i][j] = basic_matrix[i][key[j]]
return new_matrix


def individual(key_length):
key = []
while(len(key) < key_length):
    rand_value = randint(0,key_length-1)
    if (rand_value not in key):
        key.append(rand_value)
return tuple(key)

def population(count, key_length):
return [ individual(key_length) for x in range(count) ]

def fitness(key):
sum = 0
new_text = decrypt(key)
for i in range(0, len(new_text) - 1):
    sub = new_text[i:i+2].upper()
    if sub in bigram:
        sum += bigram[sub]

for i in range(0, len(new_text) -2):
    sub = new_text[i:i+3].upper()
    if sub in trigram:
        sum += trigram[sub]

if ("ESTE" in new_text):
    sum += 3

return sum

def evolve(pop, key, retain=0.2, random_select=0.05, mutate=0.01):
global best_fit
global best_ind
graded = []
for ind in pop:
    fitness_list = (fitness(ind), ind)
    graded.append(fitness_list)
graded = sorted(graded)
new_graded = list(set(graded))
best_fit.extend(new_graded)
best_fit = sorted(best_fit)[-21:]
graded = [ x[1] for x in sorted(graded)]
retain_length = int(len(graded)*retain)
parents = graded[:retain_length]
# randomly add other individuals to
# promote genetic diversity
for individual in graded[retain_length:]:
    if random_select > random():
        parents.append(individual)
# mutate some individuals
for i in range(0, len(parents)):
    if mutate > random():
        new_individual = list(parents[i])
        first_i = randint(0, len(parents[i])-1)
        second_i = randint(0, len(parents[i])-1)
        while first_i == second_i:
            second_i = randint(0, len(parents[i])-1)
        new_individual[first_i], new_individual[second_i] = new_individual[second_i], new_individual[first_i]
        parents[i] = tuple(new_individual)
# crossover parents to create children
parents_length = len(parents)
desired_length = len(pop) - parents_length
children = []
while len(children) < desired_length:
    male = randint(0, parents_length-1)
    female = randint(0, parents_length-1)
    if male != female:
        male = list(parents[male])
        female = list(parents[female])
        half = int(len(male) / 2)
        child = male[:half]
        for i in female:
            if not i in child:
                child.append(i)
        children.append(child)
parents.extend(children)
for i in range(0, len(parents)):
    if (type(parents[i]) != 'tuple'):
        parents[i] = tuple(parents[i])
return parents

def decrypt(key):
new_matrix = []
key_length = len(key)
rows = ceil(float(len(text)) / key_length)
for i in range(0, rows):
    aux = []
    for j in range(0, len(key)):
        aux.append(0)
    new_matrix.append(aux)
for i in range(0, key_length):
    index = i * rows
    sub = text[index:index +rows]
    for j in range(0, len(sub)):
        new_matrix[j][key[i]] = sub[j]
rows = []
for row in new_matrix:
    rows.extend(row)
return "".join(rows)
"""