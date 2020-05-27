from .token import Type
from .nodes import NumberNode, BinOpNode, UnaryOpNode, VarAssignNode, VarAccessNode
from .errors import InvalidSyntaxError
from .results import ParseResult

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
	
	def atom(self):
		res = ParseResult()
		token = self.current_token

		if(token.type in (Type.tint.name, Type.tfloat.name)):
			res.register_advancement()
			self.advance()
			return res.success(NumberNode(token))
		elif(token.type == Type.tident.name):
			res.register_advancement()
			self.advance()
			return res.success(VarAccessNode(token))
		elif(token.type == Type.tlpar.name):
			res.register(self.advance())
			self.advance()

			expr = res.register(self.expr())

			if(res.error):
				return res
			
			if(self.current_token.type == Type.trpar.name):
				res.register_advancement()
				self.advance()
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected ')'"
				))
		
		return res.failure(InvalidSyntaxError(
			token.pos_start, token.pos_end,
			"Expected Int, Float, Identifier, 'var', '+', '-' or '('"
		))
	
	def power(self):
		return self.bin_op(self.atom, (Type.tpow.name, ), self.factor)

	def factor(self):
		res = ParseResult()
		token = self.current_token

		if(token.type in (Type.tplus.name, Type.tminus.name)):
			res.register_advancement()
			self.advance()
			factor = res.register(self.factor())

			if(res.error):
				return res
			
			return res.success(UnaryOpNode(token, factor))

		return self.power()

	def term(self):
		return self.bin_op(self.factor, (Type.tmul.name, Type.tdiv.name))

	def arith_expr(self):
		return self.bin_op(self.term, (Type.tplus.name, Type.tminus.name))

	def comp_expr(self):
		res = ParseResult()

		if(self.current_token.matches(Type.tkeyword.name, 'not')):
			op_token = self.current_token
			res.register_advancement()
			self.advance()

			node = res.register(self.comp_expr())

			if(res.error):
				return res

			return res.success(UnaryOpNode(op_token, node))

		node = res.register(self.bin_op(self.arith_expr, (Type.tee.name, Type.tneq.name, Type.tlt.name, Type.tgt.name, Type.tlte.name, Type.tgte.name)))

		if(res.error):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected Int, Float, Identifier, 'var', '+', '-', '(', 'not'"
			))

		return res.success(node)

	def expr(self):
		res = ParseResult()
		if(self.current_token.matches(Type.tkeyword.name, 'var')):
			res.register_advancement()
			self.advance()

			if(self.current_token.type != Type.tident.name):
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					'Expected Identifier'
				))

			var_name = self.current_token
			res.register_advancement()
			self.advance()

			if(self.current_token.type != Type.teq.name):
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected '='"
				))

			res.register_advancement()
			self.advance()
			expr = res.register(self.expr())

			if(res.error):
				return res

			return res.success(VarAssignNode(var_name, expr))
		
		node = res.register(self.bin_op(self.comp_expr, ((Type.tkeyword, 'and'), (Type.tkeyword, 'or'))))

		if(res.error):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'var', int, float, identifier, '+', '-' or '(' or 'not'"
			))

		return res.success(node)

	def bin_op(self, func_a, ops, func_b=None):
		if(func_b == None):
			func_b = func_a

		res = ParseResult()
		left = res.register(func_a())

		if(res.error):
			return res

		while(self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops):
			op_token = self.current_token
			res.register_advancement()
			self.advance()

			right = res.register(func_b())

			if(res.error):
				return res

			left = BinOpNode(left, op_token, right)

		return res.success(left)

	def parse(self, _tokens):

		self.clear(_tokens)

		res = self.expr()
		if(not res.error and self.current_token.type != Type.teof.name):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'and' or 'or'"
			))

		return res