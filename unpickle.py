import pickle

with open("data", "rb") as file:
   data = pickle.load(file)

print(data)
