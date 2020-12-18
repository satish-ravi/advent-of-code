require "set"

Coord = Struct.new(:x,:y,:z,:w)

def parse_line(line)
  return line.gsub("\n", "").gsub(" ","")
end

def read_input(filename)
  expr = []
  file = File.open(filename).read
  file.each_line do |line|
    expr.append(parse_line(line).chars)
  end
  return expr
end

def part1_brute_force(expr)
  res = nil
  i = 0
  op = nil
  while i < expr.size
    new_val = nil
    if expr[i] == '('
      sub_expr = []
      cnt_prn = 0
      i += 1
      while expr[i] != ')' || cnt_prn > 0
        sub_expr.append(expr[i])
        if expr[i] == '('
          cnt_prn += 1
        elsif expr[i] == ')'
          cnt_prn -= 1
        end
        i += 1
      end
      i += 1
      new_val = part1_brute_force(sub_expr)
    elsif expr[i] == '*' || expr[i] == '+'
      op = expr[i]
      i += 1
      next
    else
      new_val = expr[i].to_i
      i += 1
    end
    if res == nil
      res = new_val
    elsif op == '+'
      res += new_val
    elsif op == '*'
      res *= new_val
    end
  end
  return res
end

def apply(val1, val2, op)
  if op == '+'
    return val1 + val2
  else
    return val1 * val2
  end
end

def precedence_p1(op)
  return 1
end

def precedence_p2(op)
  return op == '*' ? 1 : 2
end

def evaluate(expr, precendence_fn)
  values = []
  ops = []
  i = 0
  while i < expr.size
    if ['+', '*'].include?(expr[i])
      while (ops.size != 0 && ops[-1] != '(' && precendence_fn.call(ops[-1]) >= precendence_fn.call(expr[i]))
        op = ops.pop
        val2 = values.pop
        val1 = values.pop
        values.append(apply(val1, val2, op))
      end
      ops.append(expr[i])
    elsif expr[i] == '('
      ops.append(expr[i])
    elsif expr[i] == ')'
      while ops[-1] != '('
        op = ops.pop
        val2 = values.pop
        val1 = values.pop
        values.append(apply(val1, val2, op))
      end
      ops.pop
    else
      values.append(expr[i].to_i)
    end
    i += 1
  end

  while ops.size != 0
    op = ops.pop
    val2 = values.pop
    val1 = values.pop
    values.append(apply(val1, val2, op))
  end
  return values[0]
end

def solve(inp, precedence_fn)
  sum = 0
  inp.each do |expr|
    sum += evaluate(expr, precedence_fn)
  end
  return sum
end

inp = read_input("data.txt")
puts solve(inp, method(:precedence_p1))
puts solve(inp, method(:precedence_p2))
