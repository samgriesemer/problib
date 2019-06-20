from combinatorics import counting

# define options
dinner  = ['Salt+Smoke', 'Hopcat', 'J Smuggs', 'Hi-pointe', 'Canes']
dessert = ['Andy\'s']
grocery = ['Schnucks']

# sample a product
p = counting.Product(dinner,dessert,grocery)
print(next(p.sample()))