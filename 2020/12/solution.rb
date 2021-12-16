require "set"

Ins = Struct.new(:dir, :len)

def read_input(filename)
  inp = []
  file = File.open(filename).read
  cur_line = ""
  file.each_line do |line|
    dir = line[0]
    len = line.gsub("\n", "")[1..-1].to_i
    inp.append(Ins.new(dir, len))
  end
  return inp
end

def part2(inp)
  wayX = 10
  wayY = 1
  posX = 0
  posY = 0
  inp.each do |ins|
    if ins.dir == 'L' or ins.dir == 'R'
      wayX, wayY = change2(ins, wayX, wayY)
      next
    end
    dir = ins.dir
    if ins.dir == 'F'
      posX += ins.len * wayX
      posY += ins.len * wayY
    end
    case dir
    when 'N'
      wayY += ins.len
    when 'E'
      wayX += ins.len
    when 'S'
      wayY -= ins.len
    when 'W'
      wayX -= ins.len
    end
  end

  return posX.abs + posY.abs
end

def change2(ins, pX, pY)
  if ins.len == 180
    return -pX, -pY
  end
  dir = "#{ins.dir}#{ins.len}"
  if dir == 'R90' or dir == 'L270'
    return pY, -pX
  elsif dir == 'L90' or dir == 'R270'
    return -pY, pX
  end
  return pX, pY
end


def change(cur, ins)
  dir = {
    'R90' => {'E'=> 'S', 'W'=> 'N', 'S'=> 'W', 'N'=> 'E'},
    'L90'=> {'E'=> 'N', 'W'=> 'S', 'S'=> 'E', 'N'=> 'W'},
    'L180'=> {'E'=> 'W', 'W'=> 'E', 'S'=> 'N', 'N'=> 'S'}
  }
  dir['R180'] = dir['L180']
  dir['R270'] = dir['L90']
  dir['L270'] = dir['R90']
  return dir["#{ins.dir}#{ins.len}"][cur]
end

def part1(inp)
  posX = 0
  posY = 0
  cur = 'E'
  inp.each do |ins|
    if ins.dir == 'L' or ins.dir == 'R'
      cur = change(cur, ins)
      next
    end
    dir = ins.dir
    if ins.dir == 'F'
      dir = cur
    end
    case dir
    when 'N'
      posY += ins.len
    when 'E'
      posX += ins.len
    when 'S'
      posY -= ins.len
    when 'W'
      posX -= ins.len
    end
  end
  return posX.abs + posY.abs
end

inp = read_input("data.txt")
puts part1(inp)
puts part2(inp)
