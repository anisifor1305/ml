from collections import Counter, defaultdict

# 1
numbers = [-1, 1, 2, -2, -5, 2, 3]

result = [number**2 for number in numbers if number > 0]
print(result)

# 2
print("_________________")
losses = [-1, 1, 2, -2, -5, 2, 3]
for index, loss in enumerate(losses, start=1):
    print(index, loss)

# 3
print("_________________")
names = [-5, 3, 4, -6, 9, 3, 3]
scores = [-1, 1, 2, -2, -5, 2, 3]
for name, score in zip(names, scores):
    print(name, score)

# 4
print("_________________")

labels = [-1, 1, 2, -2, -5, 2, 3]
label_counts = Counter(labels)

print(label_counts)

# 5

events = [(1, 1), (1, 2), (2, 3)]
print("_________________")
groups = defaultdict(list)
for user_id, event in events:
    groups[user_id].append(event)

print(groups)

# 6
print("_________________")
values = [-1, 1, 2, -2, -5, 2, 3]
unique_values = list(dict.fromkeys(values))
print(unique_values)

# 7
models = [{"accuracy": 75, "a": 4}, {"accuracy": 25, "a": 3}, {"accuracy": 50, "a": 5}]

models.sort(key=lambda model: model["accuracy"], reverse=True)

print(models)

# 8
epoch = "myepoch"
loss = "myloss"
accuracy = "myaccuracy"
message = f"epoch: {epoch} \n loss: {loss} \n accuracy: {accuracy}"
print(message)

# 9
squares = {number: number**2 for number in range(10)}

print(squares)

# 10
first = values[0]
last = values[-1]

# 11
lst1 = [1, 2, 3]
lst2 = [2, 3, 4]
lst2_set = set(lst2)
res = list(dict.fromkeys(x for x in lst1 if x in lst2_set))

# 12
base_config = {"accuracy": 75, "a": 4}
config = {**base_config, "seed": 42}
print(config)

# 13
scores = {
    "model_a": 0.81,
    "model_b": 0.93,
    "model_c": 0.77,
}

best_name = max(scores, key=scores.get)
print(best_name, scores[best_name])


# 14

values = [1, 2, None, 3]
print(None in values)

# 15

raw_values = ["1.2", "2.2", "3.3"]
numbers = [float(i) for i in raw_values]
print(numbers)
