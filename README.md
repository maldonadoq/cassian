# Cassian
Interpreter Code

[Content](#cassian)
- [Code](#code)
- [How to run](#how-to-run)

## Code
### Inspired by
- [Let’s Build A Simple Interpreter. Part 1.](https://ruslanspivak.com/lsbasi-part1/)

### Classes

#### Token
```python
class Token:
  def __init__(self, _type, value=None, pos_start=None, pos_end=None):
    self.type = _type
    self.value = value
```

#### Lexer
```python
class Lexer:
  def scanner(self, fn, text):
    self.clear(fn, text)

    tokens = []
    while(self.current_char != None):
      if(self.current_char in ' \t'):
        self.advance()
      elif(self.current_char in digits):
        tokens.append(self.getNumber())
      elif(self.current_char in letters):
        tokens.append(self.getIdentifier())
      elif(_):
        pass
      else:
        pos_start = self.pos.copy()
        ch = self.current_char
        self.advance()
        return [], IllegalCharError(pos_start, self.pos, "'" + ch + "'")

    tokens.append(Token(Type.teof.name, pos_start=self.pos))
    return tokens, None
```

#### Parser
```python
class Parser:
  def clear(self, tokens):
    self.tokens = tokens
    self.token_idx = -1
    self.advance()

  def parse(self, tokens):
    self.clear(tokens)

    res = self.expr()

    if(not res.error and self.current_token.type != Type.teof.name):
      return res.failure(InvalidSyntaxError(
        self.current_token.pos_start, self.current_token.pos_end,
        "Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'and' or 'or'"
      ))

    return res
```

#### Interpreter
```python
class Interpreter:
  def visit(self, node, context):
    method_name = 'visit_{}'.format(type(node).__name__)
    method = getattr(self, method_name, self.no_visit)

    return method(node, context)
```

#### Main
```python
if __name__ == "__main__":
  lex = Lexer()
  par = Parser()
  inter = Interpreter()
  ctx = Context('<program>')
  ctx.symbol_table = symb_table

  while(True):
    line = input('cassian: ')

    if(line == ':q'):
      break

    tokens, error = lex.scanner('<stdin>', line)

    if(error):
      print(error)
    else:
      # print(tokens)
      ast = par.parse(tokens)
      if(ast.error):
        print(ast.error)
      else:
        res = inter.visit(ast.node, ctx)

        if(res.error):
          print(res.error)
        elif(res.value):
          print(res.value)
```

## How to run

```bash
$ cd folder name
$ python main.py
```
