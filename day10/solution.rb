require "set"

def read_input(filename)
  numbers = []
  file = File.open(filename).read
  cur_line = ""
  file.each_line do |line|
    numbers.append(line.gsub(".\n", "").to_i)
  end
  return numbers.sort
end

def build(counts, numbers, i)
  if counts[i]
    return counts[i]
  end
  if i == numbers.count - 1
    return 1
  end
  count = 0
  if numbers[i+1] - numbers[i] <= 3
    count += build(counts, numbers, i+1)
  end
  if i < numbers.count - 2 and numbers[i+2] - numbers[i] <= 3
    count += build(counts, numbers, i+2)
  end
  if i < numbers.count - 3 and numbers[i+3] - numbers[i] <= 3
    count += build(counts, numbers, i+3)
  end
  counts[i] = count
  return count
end

def count(numbers)
  cnt3 = 0
  cnt1 = 0
  for i in 0..numbers.count-2
    if numbers[i+1] - numbers[i] == 1
      cnt1 += 1
    elsif numbers[i+1] - numbers[i] == 3
      cnt3 += 1
    end
  end
  return cnt1, cnt3
end


num_list = read_input("data.txt")
num_list = [0] + num_list + [num_list.max + 3]
puts count(num_list)
puts build({}, num_list, 0)
