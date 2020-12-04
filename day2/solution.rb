Entry = Struct.new(:lower, :upper, :letter, :password)

def read_input(filename)
  entries = []
  file = File.open(filename).read
  file.each_line do |line|
    l, u, ltr, pwd = line.match(/^(\d+)-(\d+) (\w): (\w+)$/).captures
    entries.append(Entry.new(l.to_i, u.to_i, ltr, pwd))
  end
  return entries
end

def password1(entry)
  occurences = entry.password.chars.count {|l| l == entry.letter}
  return (occurences >= entry.lower and occurences <= entry.upper)
end

def password2(entry)
  return (entry.password[entry.lower - 1] == entry.letter) != (entry.password[entry.upper - 1] == entry.letter)
end

def validate(entries, fn)
  return entries.count {|entry| fn.call(entry)}
end

inputfile = "data.txt"
entries = read_input(inputfile)
puts validate(entries, method(:password1))
puts validate(entries, method(:password2))
