import random

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
print()