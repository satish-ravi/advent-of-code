require "set"

def read_input(filename)
  entries = []
  file = File.open(filename).read
  cur_line = ""
  file.each_line do |line|
    if line == "\n"
      entries.append(cur_line)
      cur_line = ""
    else
      cur_line += line
    end
  end
  entries.append(cur_line)
  return entries
end

def count_answers1(entry)
  return Set.new(entry.chars).difference(Set["\n"]).to_a.count
end

def count_answers2(entry)
  answers = entry.split("\n")
  x = Set.new(answers[0].chars)
  answers.each do |answer|
    before = x
    x = x.intersection(Set.new(answer.chars))
  end
  return x.to_a.count
end

def puzzle(entries, count_method)
  sum = 0
  entries.each do |entry|
    sum += count_method.call(entry)
  end
  return sum
end

entries = read_input("data.txt")
puts puzzle(entries, method(:count_answers1))
puts puzzle(entries, method(:count_answers2))
