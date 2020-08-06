import hashlib

items = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "X"]

for item in items:
       hashVal = hashlib.sha256(item.encode()).hexdigest()
       print()
       print(item)
       print(hashVal)