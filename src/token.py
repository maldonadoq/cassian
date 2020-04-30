import enum

class Type(enum.Enum):
	tint	= 1
	tfloat	= 2
	tplus	= 3
	tminus	= 4
	tmul	= 5
	tdiv	= 6
	tlpar	= 7
	trpar	= 8

class Token:
	def __init__(self, _type, _value=None):
		self.type = _type
		self.value = _value

	def __repr__(self):
		if(self.value):
			return '{}:{}'.format(self.type,self.value)
		
		return '{}'.format(self.type)