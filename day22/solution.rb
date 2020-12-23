require "set"

def parse_line(line)
  return line.gsub("\n", "")
end

def read_input(filename)
  p1 = []
  p2 = []
  is2 = false
  file = File.open(filename).read
  file.each_line do |line|
    l = parse_line(line)
    if l.include?("Player")
      if l.include?("2")
        is2 = true
      end
    elsif l != ''
      is2 ? p2.append(l.to_i) : p1.append(l.to_i)
    end
  end
  return p1, p2
end

def part1(p1, p2)
  while p1.size > 0 && p2.size > 0
    c1 = p1[0]
    c2 = p2[0]
    p1 = p1[1..]
    p2 = p2[1..]
    if c1 > c2
      p1.append(c1)
      p1.append(c2)
    else
      p2.append(c2)
      p2.append(c1)
    end
  end
  winner = p1.size > 0 ? p1 : p2
  score = 0
  for i in 0..winner.size-1
    score += winner[i] * (winner.size-i)
  end
  return score
end

def get_mem(mem, c1, c2)
  c1 = c1.join(',')
  c2 = c2.join(',')
  if mem[c1 + '|' + c2]
    return mem[c1 + '|' + c2]
  end
  return nil, nil
end

def rec_combat(p1, p2, mem)
  m_winner, score = get_mem(mem, p1, p2)
  key = p1.join(',') + '|' + p2.join(',')
  hist = Set.new()
  if m_winner
    return m_winner, score
  end
  while p1.size > 0 && p2.size > 0
    ckey = p1.join(',') + '|' + p2.join(',')
    if hist.include?(ckey)
      mem[key] = 1
      return 1, 0
    end
    hist.add(ckey)
    c1 = p1[0]
    c2 = p2[0]
    p1 = p1[1..]
    p2 = p2[1..]
    if c1 < p1.size + 1 && c2 < p2.size + 1
      c_winner, _ = rec_combat(p1[0..c1-1], p2[0..c2-1], mem)
    else
      c_winner = c1 > c2 ? 1 : 2
    end
    if c_winner == 1
      p1.append(c1)
      p1.append(c2)
    else
      p2.append(c2)
      p2.append(c1)
    end
  end
  n_winner = p1.size > 0 ? 1 : 2
  winner = p1.size > 0 ? p1 : p2
  score = 0
  for i in 0..winner.size-1
    score += winner[i] * (winner.size-i)
  end
  mem[key] = n_winner, score
  return n_winner, score
end

def part2(p1, p2)
  mem = {}
  w, score = rec_combat(p1, p2, mem)
  return score
end

p1, p2 = read_input("data.txt")
puts part1(p1, p2)
puts part2(p1, p2)
