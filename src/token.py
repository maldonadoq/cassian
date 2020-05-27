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
	tpow = 10
	tident = 11
	tkeyword = 12
	teq = 13
	tee = 14
	tneq = 15
	tlt = 16
	tgt = 17
	tlte = 18
	tgte = 19


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

	def matches(self, _type, _value):
		return self.type == _type and self.value == _value

	def __repr__(self):
		if(self.value):
			return '{}:{}'.format(self.type, self.value)

		return '{}'.format(self.type)
