from .token import Type
from .node import NumberNode, BinOpNode

class Parser:
	def __init__(self):
		pass
	
	def clear(self, _tokens):
		self.tokens = _tokens
		self.token_idx = -1
		self.advance()

	def advance(self):
		self.token_idx += 1

		if(self.token_idx < len(self.tokens)):
			self.current_token = self.tokens[self.token_idx]
		
		return self.current_token
	
	def factor(self):
		token = self.current_token

		if(token.type in (Type.tint.name, Type.tfloat.name)):
			self.advance()
			return NumberNode(token)

	def term(self):
		return self.bin_op(self.factor, (Type.tmul.name, Type.tdiv.name))

	def expr(self):
		return self.bin_op(self.term, (Type.tplus.name, Type.tminus.name))

	def bin_op(self, func, ops):
		left = func()

		while(self.current_token.type in ops):
			op_token = self.current_token
			self.advance()
			right = func()
			left = BinOpNode(left, op_token, right)

		return left

	def parse(self, _tokens):

		self.clear(_tokens)
		res = self.expr()

		return res