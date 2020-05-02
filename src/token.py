import enum


class Type(enum.Enum):
	tint = 1
	tfloat = 2
	tplus = 3
	tminus = 4
	tmul = 5
	tdiv = 6
	tlpar = 7
	trpar = 8
	teof = 9


class Token:
	def __init__(self, _type, _value=None, _pos_start=None, _pos_end=None):
		self.type = _type
		self.value = _value

		if(_pos_start):
			self.pos_start = _pos_start.copy()
			self.pos_end =_pos_start.copy()
			self.pos_end.advance()

		if(_pos_end):
			self.pos_end = _pos_end

	def __repr__(self):
		if(self.value):
			return '{}:{}'.format(self.type, self.value)

		return '{}'.format(self.type)
