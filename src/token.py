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
	tcomma = 20
	tarrow = 21
	tstring = 22
	tlsqu = 23
	trsqu = 24
	tnewline = 25

class Token:
	def __init__(self, _type, value=None, pos_start=None, pos_end=None):
		self.type = _type
		self.value = value

		if(pos_start):
			self.pos_start = pos_start.copy()
			self.pos_end =pos_start.copy()
			self.pos_end.advance()

		if(pos_end):
			self.pos_end = pos_end.copy()

	def matches(self, _type, value):
		return self.type == _type and self.value == value

	def __repr__(self):
		if(self.value):
			return '{}:{}'.format(self.type, self.value)

		return '{}'.format(self.type)
