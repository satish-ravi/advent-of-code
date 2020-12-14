Mask = Struct.new(:raw, :orBits, :andBits, :combos)
Mem = Struct.new(:key, :value)

def parse_line(line)
  return line.gsub("\n", "")
end

def read_input(filename)
  instructions = []
  file = File.open(filename).read
  file.each_line do |line|
    split = parse_line(line).split(' = ')
    if split[0] == 'mask'
      orBits = split[1].gsub('X', '0').to_i(2)
      andBits = split[1].gsub('X', '1').to_i(2)
      instructions.append(Mask.new(split[1], orBits, andBits, get_all_combos(split[1])))
    else
      key = split[0].split('[')[1][0..-2].to_i
      value = split[1].to_i
      instructions.append(Mem.new(key, value))
    end
  end
  return instructions
end

def part1_mem_action(mem, mem_inst, mask)
  mem[mem_inst.key] = (mem_inst.value | mask.orBits) & mask.andBits
end

def part2_mem_action(mem, mem_inst, mask)
  nonX = mask.raw.gsub('X', '1').to_i(2)
  intKey = mem_inst.key | nonX
  mask.combos.each do |combo|
    mem[intKey & combo] = mem_inst.value
  end
end

def process(instructions, mem_action)
  mem = {}
  mask = nil
  instructions.each do |inst|
    case inst.class.to_s
    when "Mask"
      mask = inst
    when "Mem"
      mem_action.call(mem, inst, mask)
    end
  end
  res = 0
  mem.each do |k,v|
    res += v
  end
  return res
end

def recursive_gen(raw_mark)
  if raw_mark.size == 0
    return ['']
  else
    combos = []
    start_bits = raw_mark[0] == '1' ? ['1'] : ['0', '1']
    next_combos = recursive_gen(raw_mark[1..])
    start_bits.each do |s|
      next_combos.each do |n|
        combos.append(s + n)
      end
    end
    return combos
  end
end

def get_all_combos(raw_mark)
  return recursive_gen(raw_mark.gsub('0', '1')).map {|combo| combo.to_i(2)}
end

ins = read_input("data.txt")
puts process(ins, method(:part1_mem_action))
puts process(ins, method(:part2_mem_action))
