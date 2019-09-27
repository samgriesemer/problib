from probability import bernoulli

lotteries = [[[0.8,0.2], [3500,0]], [[0.75,0.25], [4000,0]]]
players = {'a':0, 'b':1, 'c':0}
results = {key:[] for key in players.keys()}

n = 10000
for _ in range(n):
  for (player, choice) in players.items():
    lottery = lotteries[choice]
    p = lottery[0][0]
    b = bernoulli.Bernoulli(p)
    res = next(b.sample())
    results[player].append(lottery[1][1-res])

print({k:sum(v)/n for (k,v) in results.items()})