import time

dinner  = ['Salt+Smoke', 'Hopcat', 'J Smuggs', 'Hi-pointe', 'Canes']
dessert = ['Andy\'s']
grocery = ['Schnucks']

# old way
import random
start = time.time()
e = random.choice(dinner)
d = random.choice(dessert)
g = random.choice(grocery)
print('old time: {}'.format(time.time()-start))
print('Dinner: {}, Dessert: {}, Grocery: {}'.format(e,d,g))

# new way
from combinatorics import counting
start = time.time()
p = counting.Product(dinner,dessert,grocery)
print('new time: {}'.format(time.time()-start))
print(list(p.sample()))