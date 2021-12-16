import sys

inp = list(l.strip() for l in sys.stdin.readlines())


def count_bits(inp):
    zeros = [0] * len(inp[0])
    ones = [0] * len(inp[0])
    for l in inp:
        for (i, bit) in enumerate(l.strip()):
            if bit == "0":
                zeros[i] += 1
            else:
                ones[i] += 1
    return zeros, ones


def part1(inp):
    zeros, ones = count_bits(inp)

    gamma_rate = ""
    epsilon_rate = ""
    for (z, o) in zip(zeros, ones):
        if z > o:
            gamma_rate += "0"
            epsilon_rate += "1"
        else:
            gamma_rate += "1"
            epsilon_rate += "0"

    return int(gamma_rate, 2) * int(epsilon_rate, 2)


def part2(inp):
    o2_gen_rating = list(inp)
    co2_gen_rating = list(inp)
    for i in range(len(inp[0])):
        if len(o2_gen_rating) > 1:
            zeroes, ones = count_bits(o2_gen_rating)
            current_bit = "1" if ones[i] >= zeroes[i] else "0"
            o2_gen_rating = [n for n in o2_gen_rating if n[i] == current_bit]
        if len(co2_gen_rating) > 1:
            zeroes, ones = count_bits(co2_gen_rating)
            current_bit = "0" if zeroes[i] <= ones[i] else "1"
            co2_gen_rating = [n for n in co2_gen_rating if n[i] == current_bit]

    return int(o2_gen_rating[0], 2) * int(co2_gen_rating[0], 2)


print("part1:", part1(inp))
print("part2:", part2(inp))
