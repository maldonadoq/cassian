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

## How to run

```bash
$ cd folder name
$ python main.py
```
