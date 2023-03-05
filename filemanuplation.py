import random
import json

with open("addresses.txt", 'r') as f:
    addresses = f.read().splitlines()

new_data = []
sum = 0
for address in addresses:
    amount = random.randint(3300000000000000000000, 4000000000000000000000)
    sum += amount
    if sum >= 729951959080324788210487:
        break
    new_data.append({
        "bep20": address,
        "amount": amount
    })

with open('usersnew.json', 'w') as f:
    json.dump(new_data, f)

print(new_data)
print(sum)
print(len(new_data))
