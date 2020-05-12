from .errors import IllegalCharError
from .position import Position
from .token import Token, Type

import string

digits = "0123456789"
letters = string.ascii_letters
letters_digits = letters + digits

keywords = [
	'var'
]

class Lexer:
	def __init__(self):
		pass

	def clear(self, _fn, _text):
		self.fn = _fn
		self.text = _text
		self.pos = Position(-1, 0, -1, _fn, _text)
		self.current_char = None
		self.advance()

	def advance(self):
		self.pos.advance(self.current_char)

		if(self.pos.idx < len(self.text)):
			self.current_char = self.text[self.pos.idx]
		else:
			self.current_char = None

	def getNumber(self):
		num = ''
		dot = 0
		pos_start = self.pos.copy()

		while(self.current_char != None and self.current_char in digits+'.'):
			if(self.current_char == '.'):
				if(dot == 1):
					break

				dot += 1
				num += '.'
			else:
				num += self.current_char

			self.advance()

		if(dot == 0):
			return Token(Type.tint.name, int(num), pos_start, self.pos)
		else:
			return Token(Type.tfloat.name, float(num), pos_start, self.pos)

	def getIdentifier(self):
		ident = ''
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in letters_digits + '_':
			ident += self.current_char
			self.advance()

		if(ident in keywords):
			token_type = Type.tkeyword.name
		else:
			token_type = Type.tident.name

		return Token(token_type, ident, pos_start, self.pos)

	def scanner(self, _fn, _text):
		self.clear(_fn, _text)

		tokens = []
		while(self.current_char != None):
			if(self.current_char in ' \t'):
				self.advance()
			elif(self.current_char in digits):
				tokens.append(self.getNumber())
			elif(self.current_char in letters):
				tokens.append(self.getIdentifier())
			elif(self.current_char == '+'):
				tokens.append(Token(Type.tplus.name, _pos_start=self.pos))
				self.advance()
			elif(self.current_char == '-'):
				tokens.append(Token(Type.tminus.name, _pos_start=self.pos))
				self.advance()
			elif(self.current_char == '*'):
				tokens.append(Token(Type.tmul.name, _pos_start=self.pos))
				self.advance()
			elif(self.current_char == '/'):
				tokens.append(Token(Type.tdiv.name, _pos_start=self.pos))
				self.advance()
			elif(self.current_char == '^'):
				tokens.append(Token(Type.tpow.name, _pos_start=self.pos))
				self.advance()
			elif(self.current_char == '='):
				tokens.append(Token(Type.teq.name, _pos_start=self.pos))
				self.advance()
			elif(self.current_char == '('):
				tokens.append(Token(Type.tlpar.name, _pos_start=self.pos))
				self.advance()
			elif(self.current_char == ')'):
				tokens.append(Token(Type.trpar.name, _pos_start=self.pos))
				self.advance()
			else:
				pos_start = self.pos.copy()
				ch = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + ch + "'")

		tokens.append(Token(Type.teof.name, _pos_start=self.pos))
		return tokens, None
