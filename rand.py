import random as r

l = [10, 20, 30, 40, 50]

print("random():", r.random())
print("randint():", r.randint(1, 100))
print("randrange():", r.randrange(10, 50, 5))
print("choice():", r.choice(l))
print("uniform():", r.uniform(1, 10))
print("sample():", r.sample(l, 4))

r.shuffle(l)
print("shuffle():", l)
