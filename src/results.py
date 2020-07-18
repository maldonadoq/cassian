class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.last_registered_advance_count = 0
		self.advance_count = 0
		self.to_reverse_count = 0

	def register_advancement(self):
		self.last_registered_advance_count = 1
		self.advance_count += 1

	def register(self, _res):
		self.last_registered_advance_count = _res.advance_count
		self.advance_count += _res.advance_count

		if(_res.error):
			self.error = _res.error
			
		return _res.node

	def try_register(self, res):
		if(res.error):
			self.to_reverse_count = res.advance_count
			return None

		return self.register(res)

	def success(self, node):
		self.node = node
		return self

	def failure(self, _error):
		if(not self.error or self.last_registered_advance_count == 0):
			self.error = _error
			
		return self

class RunTimeResult:
	def __init__(self):
		self.value = None
		self.error = None

	def register(self, _res):
		self.error = _res.error
		return _res.value

	def success(self, value):
		self.value = value
		return self

	def failure(self, _error):
		self.error = _error
		return self