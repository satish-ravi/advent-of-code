from itertools import groupby

def look_and_say(input):
    return ''.join(str(len(list(v))) + k for k, v in groupby(input))

input = "1113222113"

p1 = input
for _ in range(40):
    p1 = look_and_say(p1)
print(len(p1))

p2 = input
for _ in range(50):
    p2 = look_and_say(p2)
print(len(p2))
