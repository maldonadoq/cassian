class Number:
	def __init__(self, _value):
		self.value = _value
		self.set_pos()

	def set_pos(self, _pos_start=None, _pos_end=None):
		self.pos_start = _pos_start
		self.pos_end = _pos_end

		return self

	def added_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(self.value + _other.value)

	def subbed_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(self.value - _other.value)

	def multed_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(self.value * _other.value)

	def dived_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(self.value / _other.value)

	def __repr__(self):
		return str(self.value)