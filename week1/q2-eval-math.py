# Extend this basic solution that was introduced in class.
import sys
from dataclasses import dataclass
import math
import string 
@dataclass
class Operator:
  priority: int
  executor: callable

operators = { # Map of operators allows quick retrieval
  '+': Operator(1, lambda a, b: a + b),
  '-': Operator(1, lambda a, b: a - b),
  '*': Operator(2, lambda a, b: a * b),
  '/': Operator(2, lambda a, b: float(a) / b),
  '^': Operator(3, lambda a, b: math.pow(a, b))
}

functions = {
  'sin': Operator(3, lambda a: math.sin(a)),
  'cos': Operator(3, lambda a: math.cos(a)),
  'tan': Operator(3, lambda a: math.tan(a))
}

def parse_lexemes(string_input):
  result = []
  digit_buffer = []
  function_buffer = []
  for c in string_input:
    if not c.isspace():
      if c in operators or c in [')', '(']:
        if len(digit_buffer) > 0:      
          result.append(drain_digit_buffer(digit_buffer))
          digit_buffer = []
        elif len(function_buffer) > 0:
          result.append(drain_function_buffer(function_buffer))
          function_buffer = []
        result.append(c)
      elif c in list(map(str, range(10))) or c == '.':
        digit_buffer.append(c)
      else:
        function_buffer.append(c)
  if len(digit_buffer) > 0:
    result.append(drain_digit_buffer(digit_buffer))
  if len(function_buffer) > 0:
    raise ValueError(f"Malformed string, not a valid expression")
  return result

def drain_digit_buffer(buffer: list) -> str:
  return float(''.join(buffer))

def drain_function_buffer(buffer: list) -> str:
  function_name = ''.join(buffer)
  if function_name not in functions:
    raise ValueError(f"Unknown function {function_name} used!")
  return function_name

def execute_ops(ops, args, funcs, condition):
  if len(funcs) > 0:
    val = args.pop()
    func = funcs.pop()
    args.append(functions[func].executor(val))
  else:
    while ops and condition():
      val2, val1 = args.pop(), args.pop()
      args.append(operators[ops.pop()].executor(val1, val2))

def evaluate_expression(string_input):
  lexemes = parse_lexemes(string_input)
  ops = []
  args = []
  funcs = []
  for l in lexemes:
    if isinstance(l, float):
      args.append(l)
    elif l == '(':
      ops.append(l)
    elif l == ')':
      execute_ops(ops, args, funcs, lambda: ops[-1] != '(')
      ops.pop()
    elif l in operators:
      priority = operators[l].priority
      execute_ops(ops, args, funcs, lambda: ops[-1] != '(' and operators[ops[-1]].priority >= priority)
      ops.append(l)
    elif l in functions:
      funcs.append(l)
  execute_ops(ops, args, funcs, lambda: True)
  return args[-1] if len(args) == 1 else None

res = evaluate_expression(sys.stdin.readline())
print(f"{res:.2f}")