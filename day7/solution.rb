require "set"

def parse(entry)
  if entry == "no other bags"
    return nil, nil
  end
  count = entry[0].to_i
  color = entry.gsub(/ bags?/, "")[2..]
  return color, count
end

def read_input(filename)
  colors = {}
  file = File.open(filename).read
  cur_line = ""
  file.each_line do |line|
    line = line.gsub(".\n", "")
    color = line.match(/^(.+?) bags/i).captures[0]
    suffix = line.gsub("#{color} bags contain ", "").split(", ")
    contains = {}
    suffix.each do |entry|
      col, count = parse(entry)
      if col
        contains[col] = count
      end
    end
    colors[color] = contains
  end
  return colors
end

def has_gold(color, colors)
  if !colors.key?(color)
    colors[color] = {}
  end
  if colors[color].key?("has_gold")
    return colors[color]["has_gold"]
  elsif colors[color]["shiny gold"]
    colors[color]["has_gold"] = true
    return true
  end
  val = false
  colors[color].each do |col, contains|
    if has_gold(col, colors)
      val = true
      break
    end
  end
  colors[color]["has_gold"] = val
  return val
end

def build_has_gold(colors)
  colors2 = Marshal.load(Marshal.dump(colors))
  colors.each do |color, contains|
    has_gold(color, colors2)
  end
  return colors2
end

def part1(colors)
  colors_with_gold = build_has_gold(colors)
  return colors_with_gold.keys.count {|color| colors_with_gold[color]["has_gold"]}
end

def count_bags(colors, color)
  if !colors.key?(color)
    colors[color] = {}
  end
  if colors[color]["count"]
    return colors[color]["count"]
  end
  total = 0
  colors[color].each do |col, val|
    total += val + val * count_bags(colors, col)
  end
  colors[color]["count"] = total
  return total
end

def part2(colors)
  return count_bags(colors, "shiny gold")
end

entries = read_input("data.txt")
puts part1(entries)
puts part2(entries)
