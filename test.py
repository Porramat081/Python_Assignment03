import random

doors = {"east": 1, "west": 2, "north": 3, "south": None}

vals = list(doors.values())


random.shuffle(vals)

reassigned = dict(zip(doors.keys(), vals))

print(reassigned)