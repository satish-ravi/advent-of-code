require "set"

REQUIRED_FIELDS = Set['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def read_input(filename)
  passports = []
  file = File.open(filename).read
  current = []
  file.each_line do |line|
    if line == "\n"
      passports.append(current)
      current = []
    else
      current.push(*line.scan(/(\w{3}):(#?\w+)/))
    end
  end
  passports.append(current)
end

def valid1(passport)
  fields = passport.map {|field, val| field}
  return REQUIRED_FIELDS.subset?(Set.new(fields))
end

def is_field_valid(field, val)
  case field
  when "byr"
    return (val =~ /^\d{4}+$/ and val.to_i >= 1920 and val.to_i <= 2002)
  when "iyr"
    return (val =~ /^\d{4}+$/ and val.to_i >= 2010 and val.to_i <= 2020)
  when "eyr"
    return (val =~ /^\d{4}+$/ and val.to_i >= 2020 and val.to_i <= 2030)
  when "hgt"
    match = val.match(/^(\d+)(in|cm)$/)
    if not match
      return false
    end
    hgt, unit = match.captures
    hgt = hgt.to_i
    case unit
    when "in"
      return (hgt >= 59 and hgt <= 76)
    when "cm"
      return (hgt >= 150 and hgt <= 193)
    end
  when "hcl"
    return val =~ /^#[a-f0-9]{6}$/
  when "ecl"
    return Set["amb", "blu", "brn", "gry", "grn", "hzl", "oth"].include?(val)
  when "pid"
    return val =~ /^\d{9}+$/
  else
    return true
  end
end

def valid2(passport)
  if not valid1(passport)
    return false
  end
  passport.each do |field, val|
    if not is_field_valid(field, val)
      return false
    end
  end
  return true
end

def count_valid(passports, fn)
  return passports.count {|passport| fn.call(passport)}
end

inputfile = "data.txt"
passports = read_input(inputfile)
puts count_valid(passports, method(:valid1))
puts count_valid(passports, method(:valid2))
