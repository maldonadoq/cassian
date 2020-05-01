class Position:
	def __init__(self, _idx, _ln, _col, _fn, _ftxt):
		self.idx = _idx
		self.ln = _ln
		self.col = _col
		self.fn = _fn
		self.ftxt = _ftxt

	def advance(self, _current):
		self.idx += 1
		self.col += 1

		if(_current == '\n'):
			self.ln += 1
			self.col = 0

		return self

	def copy(self):
		return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
