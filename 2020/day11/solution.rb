require "set"

def read_input(filename)
  seats = []
  file = File.open(filename).read
  cur_line = ""
  file.each_line do |line|
    seats.append(line.gsub("\n", "").chars)
  end
  return seats
end

def p1_rule(seats, i, j, di, dj)
  ni = i + di
  nj = j + dj
  return (ni >= 0 and ni < seats.count and nj >= 0 and nj < seats[0].count and seats[ni][nj] == '#')
end

def p2_rule(seats, i, j, di, dj)
  ni = i + di
  nj = j + dj
  while ni >= 0 and ni < seats.count and nj >= 0 and nj < seats[0].count and seats[ni][nj] == '.'
    ni+=di
    nj+=dj
  end
  return (ni >= 0 and ni < seats.count and nj >= 0 and nj < seats[0].count and seats[ni][nj] == '#')
end

def check_adjacent(seats, i, j, rule_fn)
  c = 0
  for di in -1..1
    for dj in -1..1
      if di == 0 and dj == 0
        next
      end
      if rule_fn.call(seats, i, j, di, dj)
        c+=1
      end
    end
  end
  return c
end

def occupy(seats, rule_fn, thresh)
  newseats = Marshal.load(Marshal.dump(seats))
  changed = false
  for i in 0..seats.count-1
    for j in 0..seats[0].count-1
      adj = check_adjacent(seats, i, j, rule_fn)
      case seats[i][j]
      when 'L'
        if adj == 0
          changed = true
          newseats[i][j] = '#'
        end
      when '#'
        if adj >= thresh
          changed = true
          newseats[i][j] = 'L'
        end
      end
    end
  end
  return newseats, changed
end

def converge(s, rule_fn, thresh)
  while true
    n, changed = occupy(s, rule_fn, thresh)
    if !changed
      return n
    end
    s = n
  end
end

def cntseats(s)
  c = 0
  s.each do |row|
    c += row.count {|c| c == '#'}
  end
  return c
end

def pr(s)
  s.each do |row|
    puts "#{row.join('')}"
  end
end


seats = read_input("data.txt")

cnv = converge(seats, method(:p1_rule), 4)
puts cntseats(cnv)
cnv2 = converge(seats, method(:p2_rule), 5)
puts cntseats(cnv2)
