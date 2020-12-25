card_public = 11349501
door_public = 5107328
# door_public = 17807724
# card_public = 5764801


def get_loop_from_public(num)
  res = 1
  i = 0
  while true
    res *= 7
    res %= 20201227
    i += 1
    if res == num
      return i
    end
  end
end

def apply(num, loop)
  res = 1
  for i in 0..loop-1
    res *= num
    res %= 20201227
  end
  return res
end

door_loop = get_loop_from_public(door_public)
card_loop = get_loop_from_public(card_public)
puts apply(door_public, card_loop)
puts apply(card_public, door_loop)
