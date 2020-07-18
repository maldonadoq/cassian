class SymbolTable:
	def __init__(self, parent=None):
		self.symbols = dict()
		self.parent = parent

	def get(self, name):
		value = self.symbols.get(name, None)

		if(value == None and self.parent):
			return self.parent.get(name)

		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]

	def __repr__(self):
		st = ''

		for i, s in enumerate(self.symbols):
			if(i == len(self.symbols) - 1):
				st += '  {:10} : {}'.format(s, self.symbols[s])
			else:
				st += '  {:10} : {}\n'.format(s, self.symbols[s])

		return st