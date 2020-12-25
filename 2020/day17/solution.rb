require "set"

Coord = Struct.new(:x,:y,:z,:w)

def parse_line(line)
  return line.gsub("\n", "")
end

def read_input(filename)
  active = Set.new()
  file = File.open(filename).read
  x = 0
  z = 0
  w = 0
  file.each_line do |line|
    parse_line(line).chars.each_with_index do |val, y|
      if val == '#'
        active.add(Coord.new(x,y,z,w))
      end
    end
    x += 1
  end
  return active
end

def count_nearby(active, coord, p1)
  range = -1..1
  wrange = p1 ? 0..0 : -1..1
  nearby = 0
  empty_nearby = Set.new()
  for x in range
    for y in range
      for z in range
        for w in wrange
          if x == 0 && y == 0 && z == 0 && w == 0
            next
          end
          nearby_coord = Coord.new(coord.x + x, coord.y + y, coord.z + z, coord.w + w)
          if active.include?(nearby_coord)
            nearby += 1
          else
            empty_nearby.add(nearby_coord)
          end
        end
      end
    end
  end
  return nearby, empty_nearby
end

def cycle(active, p1)
  new_active = Set.new()
  all_nearby_inactive = Set.new()
  active.each do |coord|
    nearby, nearby_inactive = count_nearby(active, coord, p1)
    if [2, 3].include?(nearby)
      new_active.add(coord)
    end
    if nearby_inactive
      all_nearby_inactive.merge(nearby_inactive)
    end
  end
  all_nearby_inactive.each do |coord|
    nearby, _ = count_nearby(active, coord, p1)
    if nearby == 3
      new_active.add(coord)
    end
  end
  return new_active
end

def solve(state, p1)
  for i in 1..6
    state = cycle(state, p1)
  end
  return state.size
end

inp = read_input("data.txt")
puts solve(inp, true)
puts solve(inp, false)
