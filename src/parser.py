from .token import Type
from .node import NumberNode, BinOpNode
from .error import InvalidSyntaxError

class ParseResult:
	def __init__(self):
		self.error = None
		self.node = Nones

	def register(self, _res):
		if(isinstance(res, ParseResult)):
			if(res.error):
				self.error = _res.error
			
			return _res.node
		
		return _res


	def success(self, _node):
		self.node = _node
		return self

	def failure(self, _error):
		self.error = _error
		return self

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
		res = ParseResult()
		token = self.current_token

		if(token.type in (Type.tint.name, Type.tfloat.name)):
			res.register(self.advance())
			return res.success(NumberNode(token))

		return res.failure(InvalidSyntaxError(
			token.pos_start, token.pos_end,
			"Expected Int or Float"
		))

	def term(self):
		return self.bin_op(self.factor, (Type.tmul.name, Type.tdiv.name))

	def expr(self):
		return self.bin_op(self.term, (Type.tplus.name, Type.tminus.name))

	def bin_op(self, func, ops):
		res = ParseResult()
		left = res.register(func())

		if(res.error):
			return res

		while(self.current_token.type in ops):
			op_token = self.current_token
			res.register(self.advance())

			right = res.register(func())

			if(res.error):
				return res

			left = BinOpNode(left, op_token, right)

		return res.success(left)

	def parse(self, _tokens):

		self.clear(_tokens)
		res = self.expr()

		return res