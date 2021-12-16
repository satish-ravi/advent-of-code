def parse_line(line)
  return line.gsub("\n", "")
end

def read_input(filename)
  inp = []
  file = File.open(filename).read
  file.each_line do |line|
    return parse_line(line).split(",").map {|x| x.to_i}
  end
end

def solve(inp, final_turn)
  turn = 1
  last_spoken = Array.new(final_turn)
  last = nil
  inp.each do |i|
    last_spoken[i] = turn
    last = i
    turn += 1
  end
  last_spoken[inp[-1]] = nil
  while turn <= final_turn
    new_last = 0
    if last_spoken[last] != nil
      new_last = turn - 1 - last_spoken[last]
    end
    last_spoken[last] = turn - 1
    last = new_last
    turn += 1
  end
  return last
end

inp = read_input("data.txt")
puts solve(inp, 2020)
puts solve(inp, 30000000)
