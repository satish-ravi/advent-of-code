require "set"

def parse_line(line)
  return line.gsub("\n", "")
end

def read_input(filename)
  rules = {}
  msgs = []
  file = File.open(filename).read
  is_msg = false
  file.each_line do |line|
    l = parse_line(line)
    if l == ''
      next
    elsif l.include?(":")
      k, val = l.split(": ")
      rules[k] = val.gsub("\"", "")
    else
      msgs.append(l)
    end
  end
  return rules, msgs
end

def build_rules(rules, key, final)
  if final[key]
    return final[key]
  end
  if rules[key] == 'a' || rules[key] == 'b'
    return Set.new([rules[key]])
  end
  matches = Set.new()
  rules[key].split(" | ").each do |rule|
    valid = Set.new([""])
    rule.split(" ").each do |subrule|
      subv = build_rules(rules, subrule, final)
      new_valid = Set.new()
      valid.each do |v|
        subv.each do |sv|
          new_valid.add(v + sv)
        end
      end
      valid = new_valid
    end
    matches += valid
  end
  final[key] = matches
  return matches
end

def solve(rules, msgs)
  final = {}
  build_rules(rules, "0", final)
  s = final["42"].to_a[0].size
  p2 = p1 = 0
  msgs.each do |msg|
    if final["0"].include?(msg)
      p1 += 1
      p2 += 1
      next
    end
    if msg.size % s != 0 || msg.size <= s * 3 || !final["42"].include?(msg[0..s-1]) || !final["31"].include?(msg[-s..-1])
      next
    end
    submsg = msg[s..]
    while submsg != '' && final["42"].include?(submsg[0..s-1]) && final["31"].include?(submsg[-s..-1])
      submsg = submsg[s..-(s+1)]
    end
    while submsg != '' && final["42"].include?(submsg[0..s-1])
      submsg = submsg[s..]
    end
    if submsg == ''
      p2 += 1
    end
  end
  return p1, p2
end

def build_regex(rules, key, final, p2)
  if p2 && key == '8'
    rule42 = build_regex(rules, "42", final, p2)
    return "(#{rule42})+"
  elsif p2 && key == '11'
    rule42 = build_regex(rules, "42", final, p2)
    rule31 = build_regex(rules, "31", final, p2)
    comp = []
    for i in 1..6
      comp.append(rule42 * i + rule31 * i)
    end
    return "(#{comp.join('|')})"
  elsif final[key]
    return final[key]
  elsif rules[key] == 'a' || rules[key] == 'b'
    return rules[key]
  else
    res = []
    rules[key].split('|').each do |rule|
      res.append((rule.split(' ').map {|subkey| build_regex(rules, subkey, final, p2)}).join(''))
    end
    result = nil
    if res.size == 1
      result = res[0]
    else
      result = "(#{res.join('|')})"
    end
    final[key] = result
    return result
  end
end

def solve_regex(rules, msgs, p2)
  regex = "^" + build_regex(rules, "0", {}, p2) + "$"
  puts regex
  return msgs.count {|msg| msg =~ Regexp.new(regex)}
end

rules, msgs = read_input("data.txt")
puts solve(rules, msgs)
puts solve_regex(rules, msgs, false)
puts solve_regex(rules, msgs, true)
