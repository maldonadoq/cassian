class SymbolTable:
	def __init__(self):
		self.symbols = {}
		self.parent = None

	def get(self, _name):
		value = self.symbols.get(_name, None)

		if(value == None and self.parent):
			return self.parent.get(_name)

		return value

	def set(self, _name, _value):
		self.symbols[_name] = _value

	def remove(self, _name):
		del self.symbols[_name]