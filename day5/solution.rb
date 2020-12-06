require "set"

def read_input(filename)
  entries = []
  file = File.open(filename).read
  file.each_line do |line|
    entries.append(line)
  end
  return entries
end

def get_seat(entry)
  row = entry[0..6].gsub("B", "1").gsub("F", "0").to_i(2)
  col = entry[7..].gsub("R", "1").gsub("L", "0").to_i(2)
  return row * 8 + col
end

def find_max(entries)
  max = -1
  entries.each do |entry|
    seat = get_seat(entry)
    if seat > max
      max = seat
    end
  end
  return max
end

def find_missing(entries, max)
  all_taken_seats = Set.new(entries.map {|entry| get_seat(entry)})
  last_row = 127
  all_seats = Set.new([*(0..last_row*8+7)])
  all_first_row = Set.new([*(0..7)])
  all_last_row = Set.new([*(last_row*8..last_row*8+7)])
  missing = all_seats.difference(all_taken_seats).difference(all_first_row).difference(all_last_row)
  return missing
end

entries = read_input("data.txt")
max = find_max(entries)
puts max
puts find_missing(entries, max)
