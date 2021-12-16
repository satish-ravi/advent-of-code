def read_input(filename)
  area = []
  file = File.open(filename).read
  file.each_line do |line|
    area.append(line.chars[0..-2])
  end
  return area
end

def count_trees(area, right, down)
  rows = area.count
  cols = area[0].count
  row = 0
  col = 0
  trees = 0
  while row < area.count
    if area[row][col] == '#'
      trees += 1
    end
    row += down
    col = (col + right) % cols
  end
  return trees
end

def toboggan1(area)
  return count_trees(area, 3, 1)
end

def toboggan2(area)
  slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
  result = 1
  slopes.each do |right, down|
    result *= count_trees(area, right, down)
  end
  return result
end

inputfile = "data.txt"
area = read_input(inputfile)
puts toboggan1(area)
puts toboggan2(area)
