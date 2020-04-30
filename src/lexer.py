from .error import IllegalCharError
from .position import Position
from .token import Token, Type

digits = "0123456789"

class Lexer:
	def __init__(self):
		pass

	def clear(self, _fn, _text):
		self.fn = _fn
		self.text = _text		
		self.pos = Position(-1, 0, -1, _fn, _text)
		self.current = None
		self.advance()

	def advance(self):
		self.pos.advance(self.current)

		if(self.pos.idx < len(self.text)):
			self.current = self.text[self.pos.idx]
		else:
			self.current = None
	
	def getNumber(self):
		num = ''
		dot = 0

		while(self.current != None and self.current in digits+'.'):
			if(self.current == '.'):
				if(dot == 1):
					break

				dot += 1
				num += '.'
			else:
				num += self.current

			self.advance()
		
		if(dot == 0):
			return Token(Type.tint.name, int(num))
		else:
			return Token(Type.tfloat.name, float(num))

	def scanner(self, _fn, _text):
		self.clear(_fn, _text)

		tokens = []
		while(self.current != None):
			if(self.current in ' \t'):
				self.advance()
			elif(self.current in digits):
				tokens.append(self.getNumber())
			elif(self.current == '+'):
				tokens.append(Token(Type.tplus.name))
				self.advance()
			elif(self.current == '-'):
				tokens.append(Token(Type.tminus.name))
				self.advance()
			elif(self.current == '*'):
				tokens.append(Token(Type.tmul.name))
				self.advance()
			elif(self.current == '/'):
				tokens.append(Token(Type.tdiv.name))
				self.advance()
			elif(self.current == '('):
				tokens.append(Token(Type.tlpar.name))
				self.advance()
			elif(self.current == ')'):
				tokens.append(Token(Type.trpar.name))
				self.advance()
			else:
				pos_start = self.pos.copy()
				ch = self.current
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + ch + "'")
	
		return tokens, None