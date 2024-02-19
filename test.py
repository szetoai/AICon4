temp = [[0, 0], [1, 1], [2,2]]
try:
    x = temp.index([0, 0])
except ValueError:
    x = 2
print(f"{x}")