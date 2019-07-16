import random

def single_point(parent1, parent2):
  child = list(parent1)
  begin = random.randint(0, len(parent1) - 1)
  end = random.randint(0, len(parent1) - 1)
  start, stop = min(begin, end), max(begin, end)
  child[start:stop] = list(parent2)[start:stop]

  pos = random.randint(0, len(child) - 1)
  child[pos] = chr(ord(child[pos]) + random.randint(-1, 1))
