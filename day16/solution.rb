require "set"

def parse_line(line)
  return line.gsub("\n", "")
end

def solve(filename)
  rules = Set.new()
  rules_by_name = {}
  my_ticket = nil
  nearby_tickets = []
  invalid_sum = 0
  file = File.open(filename).read
  nearby = false
  your = false
  file.each_line do |line|
    l = parse_line(line)
    if l == ''
      next
    elsif l.include?('or')
      name = l.split(": ")[0]
      rules_by_name[name] = Set.new()
      l1, h1, l2, h2 = line.scan(/(\d+)/).map {|x| x[0].to_i}
      for i in l1..h1
        rules.add(i)
        rules_by_name[name].add(i)
      end
      for i in l2..h2
        rules.add(i)
        rules_by_name[name].add(i)
      end
    elsif l.include?('your ticket')
      your = true
    elsif l.include?('nearby')
      your = false
      nearby = true
    elsif your
      my_ticket = l.split(",").map {|n| n.to_i}
    elsif nearby
      nums = l.split(",").map {|n| n.to_i}
      valid = true
      nums.each do |n|
        if !rules.include?(n)
          invalid_sum += n
          valid = false
        end
      end
      if valid
        nearby_tickets.append(nums)
      end
    end
  end
  by_cols = Array.new(nearby_tickets[0].size) {|i| Set.new()}
  nearby_tickets.each do |nt|
    nt.each_with_index do |n,i|
      by_cols[i].add(n)
    end
  end
  cols = []
  by_cols.each do |col|
    possible_cols = Set.new()
    rules_by_name.each do |name, rule|
      diff = col - rule
      if diff.empty?
        possible_cols.add(name)
      end
    end
    cols.append(possible_cols)
  end
  done = Set.new()
  while cols.count {|col| col.size > 1} > 0
    size1 = cols.select {|col| col.size == 1 && !done.include?(col.to_a[0])}[0]
    col_name = size1.to_a[0]
    done.add(col_name)
    cols.each do |col|
      if col.include?(col_name) && col.size > 1
        col.delete(col_name)
      end
    end
  end
  result = 1
  cols.each_with_index do |col, i|
    if col.to_a[0].include?('departure')
      result *= my_ticket[i]
    end
  end
  return invalid_sum, result
end

puts solve("data.txt")
