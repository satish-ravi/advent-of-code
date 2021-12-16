require "set"

def report_repair1(filename)
  elements = Set[]
  file = File.open(filename).read
  file.each_line do |line|
    element = line.to_i
    if elements.include?(2020 - element)
      return element * (2020 - element)
    else
      elements.add(element)
    end
  end
end

def report_repair2(filename)
  elements = []
  file = File.open(filename).read
  file.each_line do |line|
    elements.append(line.to_i)
  end
  elementset = Set.new(elements)
  elements.each_with_index do |element1, index|
    elements[index+1..-1].each do |element2|
      if elementset.include?(2020 - element1 - element2)
        return element1 * element2 * (2020 - element1 - element2)
      end
    end
  end
end

inputfile = "data.txt"
puts report_repair1(inputfile)
puts report_repair2(inputfile)
