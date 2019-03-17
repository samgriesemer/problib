from combinatorics import counting

dinner  = ['Salt+Smoke', 'Hopcat', 'J Smuggs', 'Hi-pointe', 'Canes']
dessert = ['Andy\'s']
grocery = ['Schnucks']
results = []

for i in range(420):
  e = random.choice(dinner)
  d = random.choice(dessert)
  g = random.choice(grocery)
  results.append({'e':e,'d':d,'g':g})

print('Dinner: {}, Dessert: {}, Grocery: {}'.format(e,d,g))

from combinatorics import Permutations
prod([dinner,dessert,grocery])

from combinatorics import Product
p = Product(dinner,dessert,grocery)
g = p.generate()
s = p.sample()