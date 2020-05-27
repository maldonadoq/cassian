from .errors import RunTimeError

class Number:
	def __init__(self, _value):
		self.value = _value
		self.set_pos()
		self.set_context()

	def set_pos(self, _pos_start=None, _pos_end=None):
		self.pos_start = _pos_start
		self.pos_end = _pos_end

		return self

	def set_context(self, _context=None):
		self.context = _context
		return self

	def added_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(self.value + _other.value).set_context(self.context), None

	def subbed_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(self.value - _other.value).set_context(self.context), None

	def multed_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(self.value * _other.value).set_context(self.context), None

	def dived_by(self, _other):
		if(isinstance(_other, Number)):
			if(_other.value == 0):
				return None, RunTimeError(
					_other.pos_start, _other.pos_end,
					'Division by Zero',
					self.context
				)

			return Number(self.value / _other.value).set_context(self.context), None

	def powed_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(self.value ** _other.value).set_context(self.context), None

	def getComparisonEq(self, _other):
		if(isinstance(_other, Number)):
			return Number(int(self.value == _other.value)).set_context(self.context), None

	def getComparisonNeq(self, _other):
		if(isinstance(_other, Number)):
			return Number(int(self.value != _other.value)).set_context(self.context), None

	def getComparisonLt(self, _other):
		if(isinstance(_other, Number)):
			return Number(int(self.value < _other.value)).set_context(self.context), None

	def getComparisonGt(self, _other):
		if(isinstance(_other, Number)):
			return Number(int(self.value > _other.value)).set_context(self.context), None

	def getComparisonLte(self, _other):
		if(isinstance(_other, Number)):
			return Number(int(self.value <= _other.value)).set_context(self.context), None

	def getComparisonGte(self, _other):
		if(isinstance(_other, Number)):
			return Number(int(self.value >= _other.value)).set_context(self.context), None

	def anded_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(int(self.value and _other.value)).set_context(self.context), None

	def ored_by(self, _other):
		if(isinstance(_other, Number)):
			return Number(int(self.value or _other.value)).set_context(self.context), None

	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None

	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)

		return copy

	def __repr__(self):
		return str(self.value)