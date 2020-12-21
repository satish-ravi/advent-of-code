require "set"

def gen_empty_2d(size)
  res = []
  for _ in 0..size-1
    res.append([nil] * size)
  end
  return res
end

class Tile
  attr_accessor :num, :data, :top, :bottom, :left, :right

  def initialize(num, data)
    @num = num
    @data = data
    @top = data[0].join('').to_i(2)
    @bottom = data[-1].join('').to_i(2)
    @left = data.map {|row| row[0]}.join('').to_i(2)
    @right = data.map {|row| row[-1]}.join('').to_i(2)
  end

  def rotate()
    new_data = gen_empty_2d(@data.size)
    for i in 0..@data.size-1
      for j in 0..@data.size-1
        new_data[j][@data.size - 1 - i] = @data[i][j]
      end
    end
    return Tile.new(@num, new_data)
  end

  def flip_horizontal()
    new_data = gen_empty_2d(@data.size)
    for i in 0..@data.size-1
      for j in 0..@data.size-1
        new_data[i][@data.size - j - 1] = @data[i][j]
      end
    end
    return Tile.new(@num, new_data)
  end

  def flip_vertical()
    new_data = gen_empty_2d(@data.size)
    for i in 0..@data.size-1
      for j in 0..@data.size-1
        new_data[@data.size - i - 1][j] = @data[i][j]
      end
    end
    return Tile.new(@num, new_data)
  end

  def get_all_combinations()
    r1 = self.rotate
    r2 = r1.rotate
    r3 = r2.rotate
    return [self, self.flip_horizontal, self.flip_vertical, r1, r1.flip_horizontal, r1.flip_vertical, r2, r3]
  end

  def strip_borders()
    return @data[1..-2].map {|row| row[1..-2]}
  end

  def total_hash()
    return @data.flatten.join("").scan(/1/).length
  end
end

def parse_line(line)
  return line.gsub("\n", "")
end

def read_input(filename)
  tiles = []
  file = File.open(filename).read
  tile = nil
  data = nil
  file.each_line do |line|
    l = parse_line(line)
    if l == ''
      tiles.append(Tile.new(tile, data))
    elsif l.include?("Tile")
      tile = l.split(" ")[1].to_i
      data = []
    else
      data.append(l.gsub("#", "1").gsub(".", "0").chars)
    end
  end
  return tiles
end

def find_tile(i, j, n, visited, candidates, tiling)
  if i == n
    return true
  end
  ni = i
  nj = j + 1
  if nj == n
    ni = i + 1
    nj = 0
  end
  candidates.each do |num, all_tiles|
    if visited.include?(num)
      next
    end
    visited.add(num)
    all_tiles.each do |tile|
      if (i > 0 && tiling[i-1][j].bottom != tile.top) || (j > 0 && tiling[i][j-1].right != tile.left)
        next
      end
      tiling[i][j] = tile
      next_ = find_tile(ni, nj, n, visited, candidates, tiling)
      if next_
        return next_
      end
    end
    visited.delete(num)
  end
  tiling[i][j] = nil
  return false
end

def generate_tiling(tiles)
  n = Math.sqrt(tiles.size)
  tiling = gen_empty_2d(n)
  candidates = {}
  tiles.each do |tile|
    candidates[tile.num] = tile.get_all_combinations
  end
  find_tile(0, 0, n, Set.new(), candidates, tiling)
  return tiling
end

def part1(inp)
  tiling = generate_tiling(inp)
  return tiling[0][0].num * tiling[0][-1].num * tiling[-1][0].num * tiling[-1][-1].num
end

def get_image_tile(tiling)
  image = []
  tiling.each do |row|
    current_row = []
    for i in 0..row[0].data.size-3
      current_row.append([])
    end
    row.each do |tile|
      striped = tile.strip_borders
      for i in 0..current_row.size-1
        current_row[i] += striped[i]
      end
    end
    image += current_row
  end
  image_tile = Tile.new(0, image)
  return image_tile
end

def is_monster(monster, tile)
  for i in 0..monster.size-1
    if monster[i] & tile[i] != monster[i]
      return false
    end
  end
  return true
end

def part2(inp)
  tiling = generate_tiling(inp)
  image_tile = get_image_tile(tiling)
  monster = ['                  # ', '#    ##    ##    ###', ' #  #  #  #  #  #   '].map {|row| row.gsub(" ", "0").gsub("#", "1")}
  monster_size = monster.join("").scan(/1/).length
  cols = monster[0].size
  rows = monster.size
  monster = monster.map {|row| row.to_i(2)}
  image_tile.get_all_combinations.each do |combo|
    monster_count = 0
    for i in 0..combo.data.size-1-rows
      for j in 0..combo.data.size-1-cols
        pos_to_check = combo.data[i..i+rows-1].map {|row| row[j..j+cols-1].join("").to_i(2)}
        if is_monster(monster, pos_to_check)
          monster_count += 1
        end
      end
    end
    if monster_count > 0
      return combo.total_hash - monster_count * monster_size
    end
  end
  return 0
end

inp = read_input("data.txt")
puts part1(inp)
puts part2(inp)
