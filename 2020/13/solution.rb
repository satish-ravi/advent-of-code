require "set"

Bus = Struct.new(:id, :idx)

def parse_line(line)
  return line.gsub("\n", "")
end

def read_input(filename)
  file = File.foreach(filename).first(2)
  time = parse_line(file[0]).to_i
  buses = []
  parse_line(file[1]).split(',').each_with_index do |bus, idx|
    if bus == 'x'
      next
    end
    buses.append(Bus.new(bus.to_i, idx))
  end
  return time, buses
end

def part1(time, buses)
  minwait = 1000000000000
  minbus = 0
  buses.each do |bus|
    cur_min = bus.id - (time % bus.id)
    if cur_min < minwait
      minwait = cur_min
      minbus = bus
    end
  end
  return minwait * minbus.id
end

def part2(buses)
  runningProd = 1
  time = 0
  buses.each do |bus|
    while (time + bus.idx) % bus.id != 0
      time += runningProd
    end
    runningProd *= bus.id
  end
  return time
end

time, buses = read_input("data.txt")
puts part1(time, buses)
puts part2(buses)
