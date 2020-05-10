class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None

	def register(self, _res):
		if(isinstance(_res, ParseResult)):
			if(_res.error):
				self.error = _res.error
			
			return _res.node
		
		return _res


	def success(self, _node):
		self.node = _node
		return self

	def failure(self, _error):
		self.error = _error
		return self

class RunTimeResult:
	def __init__(self):
		self.value = None
		self.error = None

	def register(self, _res):
		if(_res.error):
			self.error = _res.error

		return _res.value

	def success(self, _value):
		self.value = _value
		return self

	def failure(self, _error):
		self.error = _error
		return self