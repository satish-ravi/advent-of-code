require "set"

Instruction = Struct.new(:command, :val)

def read_input(filename)
  program = []
  file = File.open(filename).read
  cur_line = ""
  file.each_line do |line|
    line = line.gsub(".\n", "")
    cmd, val = line.match(/^(acc|jmp|nop) ([+-]\d+)/).captures
    program.append(Instruction.new(cmd, val.to_i))
  end
  return program
end

def execute(program)
  acc = 0
  cur = 0
  visited = Set[]
  while true
    if cur == program.count
      return "success", acc
    elsif visited.include?(cur)
      return "loop", acc
    end
    visited.add(cur)
    case program[cur].command
    when "jmp"
      cur += program[cur].val
    when "acc"
      acc += program[cur].val
      cur += 1
    when "nop"
      cur += 1
    end
  end
end

program = read_input("data.txt")
puts execute(program)

program.each_with_index do |instruction, idx|
  if instruction.command == "nop"
    cpy = Marshal.load(Marshal.dump(program))
    cpy[idx].command = "jmp"
    res, val = execute(cpy)
  elsif instruction.command == "jmp"
    cpy = Marshal.load(Marshal.dump(program))
    cpy[idx].command = "nop"
    res, val = execute(cpy)
  end
  if res == "success"
    puts "#{val}, #{instruction}, #{idx}"
  end
end
