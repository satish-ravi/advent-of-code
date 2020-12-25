require "set"

def read_input(filename)
  numbers = []
  file = File.open(filename).read
  cur_line = ""
  file.each_line do |line|
    numbers.append(line.gsub(".\n", "").to_i)
  end
  return numbers
end

def validate(preamble, num)
  l = preamble.count - 1
  for i in 0..l
    for j in (i+1)..l
      if num == preamble[i] + preamble[j]
        return true
      end
    end
  end
  return false
end

def find_offending(num_list, preamble_len)
  l = num_list.count - preamble_len - 1
  for i in 0..l
    if not validate(num_list[i..i+preamble_len-1], num_list[i+preamble_len])
      return num_list[i+preamble_len]
    end
  end
end

def count_continuous(num_list, num, len)
  for i in 0..num_list.count-len-1
    sum = num_list[i..i+len-1].inject(0){|sum, x| sum + x}
    if sum == num
      return num_list[i..i+len-1]
    end
  end
  return nil
end

def find_continuous(num_list, num)
  for i in 2..num_list.count
    list = count_continuous(num_list, num, i)
    if list
      return list
    end
  end
end


num_list = read_input("data.txt")
part1 = find_offending(num_list, 25)
puts part1
l = find_continuous(num_list, part1)
puts l.max + l.min
