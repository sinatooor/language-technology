from collections import defaultdict
d = defaultdict(lambda: defaultdict(int))

d["fruit"]["apple"] += 1   # creates "fruit" (inner defaultdict) and "apple" (0 -> 1)
d["veg"]["carrot"]  += 3   # creates "veg" and "carrot" (0 -> 3)


print(d)
#defaultdict(<function <lambda> at 0x1032e6340>, {'fruit': defaultdict(<class 'int'>, {'apple': 1}), 'veg': defaultdict(<class 'int'>, {'carrot': 3})})