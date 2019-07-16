import random
import string

def initPop(strSize, popSize):
  population = []
  for x in range(popSize):
    randStr = ""
    for letter in range(strSize):
      randStr += random.choice(string.printable[:-5])
    population.append(randStr)
  return population

def fitness(candidate, target):
  fitVal = 0
  for x in range(len(candidate)):
    fitVal += (ord(candidate[x]) - ord(target[x])) ** 2
  return fitVal

def crossover(parent1, parent2):
  child = list(parent1)
  begin = random.randint(0, len(parent1) - 1)
  end = random.randint(0, len(parent1) - 1)
  start, stop = min(begin, end), max(begin, end)
  child[start:stop] = list(parent2)[start:stop]

  randex = random.randint(0, len(child) - 1)
  child[randex] = chr(ord(child[randex]) + random.randint(-1, 1))
  return "".join(child)

def randomParent(population):
  randex = random.random() * random.random() * (len(population))
  randex = int(randex)
  return population[randex]

x = 1
target = raw_input("Enter target string: ")
population = initPop(len(target), int(raw_input("Enter population size: ")))
while True:
  population.sort(key = lambda x: fitness(x, target))

  if fitness(population[0], target) == 0: break

  parent1 = randomParent(population)
  parent2 = randomParent(population)
  child = crossover(parent1, parent2)

  if fitness(child, target) < fitness(population[-1], target):
    population[-1] = child

  for candidate in population:
    print x, " : ", candidate, " - ", fitness(candidate, target)

  x += 1