require "set"

Dish = Struct.new(:ingredients, :allergens)

def parse_line(line)
  return line.gsub("\n", "")
end

def read_input(filename)
  dishes = []
  file = File.open(filename).read
  file.each_line do |line|
    l = parse_line(line)
    ing = l.split(" (")[0].split(" ")
    aller = l.split("contains ")[1][0..-2].split(", ")
    dishes.append(Dish.new(ing, aller))
  end
  return dishes
end

def get_allergen_candidates(dishes)
  allergen_candidates = {}
  dishes.each do |dish|
    dish.allergens.each do |allergen|
      if allergen_candidates[allergen]
        allergen_candidates[allergen] &= Set.new(dish.ingredients)
      else
        allergen_candidates[allergen] = Set.new(dish.ingredients)
      end
    end
  end
  return allergen_candidates
end

def part1(dishes)
  all_ings = Set.new(dishes.map {|dish| dish.ingredients}.flatten())
  allergen_candidates = get_allergen_candidates(dishes)
  allergy_ings = Set.new(allergen_candidates.values.map {|x| x.to_a}.flatten)
  safe = all_ings - allergy_ings
  res = 0
  safe.each do |safe_ing|
    res += dishes.count {|dish| dish.ingredients.include?(safe_ing)}
  end
  return res
end

def part2(dishes)
  allergen_candidates = get_allergen_candidates(dishes)
  done = Set.new()
  while allergen_candidates.keys.count {|allergent| allergen_candidates[allergent].size > 1} > 0 do
    size1 = allergen_candidates.keys.select {|allergent| !done.include?(allergent) && allergen_candidates[allergent].size == 1}[0]
    size1ing = allergen_candidates[size1].to_a[0]
    done.add(size1)
    allergen_candidates.each do |allergent, ing|
      if allergent == size1
        next
      end
      allergen_candidates[allergent].delete(size1ing)
    end
  end
  return allergen_candidates.keys.sort.map {|allergent| allergen_candidates[allergent].to_a[0]}.join(",")
end

dishes = read_input("data.txt")
puts part1(dishes)
puts part2(dishes)
