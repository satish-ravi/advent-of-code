def gen_empty_2d(size)
  res = []
  for _ in 0..size-1
    res.append([nil] * size)
  end
  return res
end

def parse_line(line)
  return line.gsub("\n", "")
end

def read_input(filename)
  inp = []
  file = File.open(filename).read
  file.each_line do |line|
    l = parse_line(line)
    cur = []
    i = 0
    while i < l.size
      if l[i] == 'e' || l[i] == 'w'
        cur.append(l[i])
        i += 1
      else
        cur.append(l[i..i+1])
        i += 2
      end
    end
    inp.append(cur)
  end
  return inp
end

def part1(inp, size)
  dirs = {
    'e' => [0, 2],
    'w' => [0, -2],
    'ne' => [1, 1],
    'nw' => [1, -1],
    'se' => [-1, 1],
    'sw' => [-1, -1]
  }
  grid = gen_empty_2d(size)
  for i in 0..size-1
    for j in 0..size-1
      if (i + j) % 2 == 0
        grid[i][j] = 0
      end
    end
  end
  inp.each do |ins|
    i = size / 2
    j = size / 2
    ins.each do |dir|
      di, dj = dirs[dir]
      i += di
      j += dj
    end
    grid[i][j] = grid[i][j] ^ 1
  end
  return count_black(grid), grid
end

def get_adjacent_black(grid, i, j)
  dirs = [[0,2], [0,-2], [1,-1], [-1,1], [1,1], [-1,-1]]
  sum = 0
  dirs.each do |di, dj|
    ai = i + di
    aj = j + dj
    if ai >= 0 && ai < grid.size && aj >= 0 && aj < grid.size
      sum += grid[ai][aj]
    end
  end
  return sum
end

def count_black(grid)
  nb = 0
  for i in 0..grid.size-1
    for j in 0..grid.size-1
      if (i + j) % 2 == 0
        nb += grid[i][j]
      end
    end
  end
  return nb
end

def part2(grid)
  for x in 1..100
    to_flip = []
    for i in 0..grid.size-1
      for j in 0..grid.size-1
        if (i + j) % 2 == 0
          blacks = get_adjacent_black(grid, i, j)
          if grid[i][j] == 1 && (blacks == 0 || blacks > 2)
            to_flip.append([i, j])
          elsif grid[i][j] == 0 && blacks == 2
            to_flip.append([i, j])
          end
        end
      end
    end
    to_flip.each do |i, j|
      grid[i][j] = grid[i][j] ^ 1
    end
  end
  return count_black(grid)
end

inp = read_input("data.txt")
sum, grid = part1(inp, 250)
puts sum
puts part2(grid)
