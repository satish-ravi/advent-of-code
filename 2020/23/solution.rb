Cup = Struct.new(:val, :right)

def part1_brute_force(inp)
  cups = inp.chars.map {|x| x.to_i }
  final = 9

  for x in 1..100
    pickup = cups[1..3]
    dest = cups[0] - 1
    if dest == 0
      dest = final
    end
    while pickup.include?(dest)
      dest -= 1
      if dest == 0
        dest = final
      end
    end

    # puts "Pickup:#{pickup}"
    # puts "Dest:#{dest}"
    newcups = [nil] * final
    ni = 0
    idx = 4
    # puts cups.include?(dest)
    while cups[idx] != dest
      newcups[ni] = cups[idx]
      idx += 1
      ni += 1
      if idx >= cups.size
        raise
      end
      # idx %= cups.size
    end
    # puts "1 new:#{newcups}"
    newcups[ni] = cups[idx]
    newcups[ni + 1] = pickup[0]
    newcups[ni + 2] = pickup[1]
    newcups[ni + 3] = pickup[2]
    # puts "2 new:#{newcups}"
    ni += 4
    while ni != final
      idx += 1
      idx %= cups.size
      newcups[ni] = cups[idx]
      ni += 1
    end
    # puts "Final new:#{newcups}" 

    cups = newcups
  end

  return cups.join()
end

def part1(inp)
  cups = {}
  input_cups = inp.chars.map {|x| x.to_i }
  prev = nil
  input_cups.each do |inp_cup|
    cup = Cup.new(inp_cup, prev)
    if prev
      prev.right = cup
    end
    prev = cup
    cups[inp_cup] = cup
  end
  prev.right = cups[input_cups[0]]
  do_moves(cups, input_cups[0], 9, 100)
  res = ''
  current = cups[1].right
  while current.val != 1
    res += current.val.to_s
    current = current.right
  end
  return res
end

def part2(inp)
  cups = {}
  input_cups = inp.chars.map {|x| x.to_i }
  prev = nil
  input_cups.each do |inp_cup|
    cup = Cup.new(inp_cup, prev)
    if prev
      prev.right = cup
    end
    prev = cup
    cups[inp_cup] = cup
  end
  for i in 10..1000000
    cup = Cup.new(i)
    prev.right = cup
    prev = cup
    cups[i] = cup
  end
  prev.right = cups[input_cups[0]]
  do_moves(cups, input_cups[0], 1000000, 10000000)
  return cups[1].right.val * cups[1].right.right.val
end

def do_moves(cups, start, max, moves)
  current = cups[start]

  for i in 1..moves
    current_val = current.val
    pick1 = current.right
    pick2 = pick1.right
    pick3 = pick2.right

    dest_val = current_val - 1
    if dest_val == 0
      dest_val = max
    end
    while [pick1.val, pick2.val, pick3.val].include?(dest_val)
      dest_val -= 1
      if dest_val == 0
        dest_val = max
      end
    end

    dest = cups[dest_val]

    current.right = pick3.right
    pick3.right = dest.right
    dest.right = pick1
    current = current.right
  end
  return
end

inp = "219347865"
# test
# inp = "389125467"
puts part1(inp)
puts part2(inp)
