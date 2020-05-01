class Error:
	def __init__(self, _pos_start, _pos_end, _name, _details):
		self.name = _name
		self.pos_start = _pos_start
		self.pos_end = _pos_end
		self.details = _details

	def __repr__(self):
		return '{}:{}\nFile{},line{}'.format(self.name, self.details, self.pos_start.fn, self.pos_start.ln + 1)


class IllegalCharError(Error):
	def __init__(self, _pos_start, _pos_end, details):
		super().__init__(_pos_start, _pos_end, 'Illegal Character', details)


class InvalidSyntaxError(Error):
	def __init__(self, _pos_start, _pos_end, details):
		super().__init__(_pos_start, _pos_end, 'Invalid Syntax', details)
