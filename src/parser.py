from .token import Type
from .nodes import NumberNode, BinOpNode, UnaryOpNode, VarAssignNode, VarAccessNode, IfNode, ForNode, WhileNode, CallNode, FunctionNode, StringNode, ListNode
from .errors import InvalidSyntaxError
from .results import ParseResult

class Parser:
	def __init__(self):
		pass
	
	def clear(self, tokens):
		self.tokens = tokens
		self.token_idx = -1
		self.advance()

	def advance(self):
		self.token_idx += 1
		self.update_current_token()
		
		return self.current_token

	def reverse(self, amount=1):
		self.token_idx -= amount
		self.update_current_token()

		return self.current_token

	def update_current_token(self):
		if(self.token_idx >= 0 and self.token_idx < len(self.tokens)):
			self.current_token = self.tokens[self.token_idx]

	def statements(self):
		res = ParseResult()
		statements = []
		pos_start = self.current_token.pos_start.copy()

		while self.current_token.type == Type.tnewline.name:
			res.register_advancement()
			self.advance()

		statement = res.register(self.expr())
		if res.error:
			return res
		statements.append(statement)

		more_statements = True

		while True:
			newline_count = 0
			while self.current_token.type == Type.tnewline.name:
				res.register_advancement()
				self.advance()
				newline_count += 1
			if newline_count == 0:
				more_statements = False

			if not more_statements: break
			statement = res.try_register(self.expr())
			if not statement:
				self.reverse(res.to_reverse_count)
				more_statements = False
				continue
			statements.append(statement)

		return res.success(ListNode(
			statements,
			pos_start,
			self.current_token.pos_end.copy()
		))

	def list_expr(self):
		res = ParseResult()
		element_nodes = []
		pos_start = self.current_token.pos_start.copy()

		if(self.current_token.type != Type.tlsqu.name):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected '['"
			))
		
		res.register_advancement()
		self.advance()

		if(self.current_token.type == Type.trsqu.name):
			res.register_advancement()
			self.advance()
		else:
			element_nodes.append(res.register(self.expr()))
			if(res.error):
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected ']', 'var', 'if', 'for', 'while', 'fun', int, float, ident, '+', '-', '(', '[' or 'not'"
				))
			
			while(self.current_token.type == Type.tcomma.name):
				res.register_advancement()
				self.advance()

				element_nodes.append(res.register(self.expr()))

				if(res.error):
					return res
				
			if(self.current_token.type != Type.trsqu.name):
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected ',' or ']'"
				))

			res.register_advancement()
			self.advance()
		
		return res.success(ListNode(
			element_nodes,
			pos_start,
			self.current_token.pos_end.copy()
		))

	def if_expr(self):
		res = ParseResult()
		cases = []
		else_case = None

		if(not self.current_token.matches(Type.tkeyword.name, 'if')):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'if'"
			))
		res.register_advancement()
		self.advance()

		condition = res.register(self.expr())
		if(res.error):
			return res

		if(not self.current_token.matches(Type.tkeyword.name, 'then')):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'then'"
			))

		res.register_advancement()
		self.advance()

		expr = res.register(self.expr())

		if(res.error):
			return res
		
		cases.append((condition, expr))

		while(self.current_token.matches(Type.tkeyword.name, 'elif')):
			res.register_advancement()
			self.advance()

			condition = res.register(self.expr())

			if(res.error):
				return res

			if(not self.current_token.matches(Type.tkeyword.name, 'then')):
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected 'then'"
				))

			res.register_advancement()
			self.advance()

			expr = res.register(self.expr())

			if(res.error):
				return res

			cases.append((condition, expr))

		if(self.current_token.matches(Type.tkeyword.name, 'else')):
			res.register_advancement()
			self.advance()

			else_case = res.register(self.expr())
			if(res.error):
				return res

		return res.success(IfNode(cases, else_case))

	def for_expr(self):
		res = ParseResult()

		if(not self.current_token.matches(Type.tkeyword.name, 'for')):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'for'"
			))

		res.register_advancement()
		self.advance()

		if(self.current_token.type != Type.tident.name):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected identifier"
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

		start_value = res.register(self.expr())

		if(res.error):
			return res

		if(not self.current_token.matches(Type.tkeyword.name, 'to')):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'to'"
			))

		res.register_advancement()
		self.advance()

		end_value = res.register(self.expr())

		if(res.error):
			return res

		if(self.current_token.matches(Type.tkeyword.name, 'step')):
			res.register_advancement()
			self.advance()

			step_value = res.register(self.expr())
			if(res.error):
				return res
		else:
			step_value = None

		if(not self.current_token.matches(Type.tkeyword.name, 'then')):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'then'"
			))

		res.register_advancement()
		self.advance()

		body = res.register(self.expr())

		if(res.error):
			return res

		return res.success(ForNode(var_name, start_value, end_value, step_value, body))

	def while_expr(self):
		res = ParseResult()

		if(not self.current_token.matches(Type.tkeyword.name, 'while')):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'while'"
			))

		res.register_advancement()
		self.advance()

		condition = res.register(self.expr())

		if(res.error):
			return res

		if(not self.current_token.matches(Type.tkeyword.name, 'then')):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'then'"
			))
		
		
		res.register_advancement()
		self.advance()

		body = res.register(self.expr())

		if(res.error):
			return res

		return res.success(WhileNode(condition, body))

	def fun_def(self):
		res = ParseResult()

		if(not self.current_token.matches(Type.tkeyword.name, 'fun')):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'fun'"
			))

		res.register_advancement()
		self.advance()

		if(self.current_token.type == Type.tident.name):
			var_name_token = self.current_token
			
			res.register_advancement()
			self.advance()

			if(self.current_token.type != Type.tlpar.name):
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected '('"
				))
		else:
			var_name_token = None

			if(self.current_token.type != Type.tlpar.name):
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected '('"
				))

		res.register_advancement()
		self.advance()

		arg_name_tokens = []

		if(self.current_token.type == Type.tident.name):
			arg_name_tokens.append(self.current_token)
			res.register_advancement()
			self.advance()

			while(self.current_token.type == Type.tcomma.name):
				res.register_advancement()
				self.advance()

				if(self.current_token.type != Type.tident.name):
					return res.failure(InvalidSyntaxError(
						self.current_token.pos_start, self.current_token.pos_end,
						'Expected identifier'
					))

				arg_name_tokens.append(self.current_token)
				res.register_advancement()
				self.advance()
			
			if(self.current_token.type != Type.trpar.name):
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected ',' or ')'"
				))
		else:
			if(self.current_token.type != Type.trpar.name):
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected identifier or ')'"
				))

		res.register_advancement()
		self.advance()

		if(self.current_token.type != Type.tarrow.name):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected  '->'"
			))

		res.register_advancement()
		self.advance()

		node_return = res.register(self.expr())

		if(res.error):
			return res
		
		return res.success(FunctionNode(
			var_name_token,
			arg_name_tokens,
			node_return
		))


	def call(self):
		res = ParseResult()
		atom = res.register(self.atom())

		if(res.error):
			return res
		
		if(self.current_token.type == Type.tlpar.name):
			res.register_advancement()
			self.advance()

			arg_nodes = []

			if(self.current_token.type == Type.trpar.name):
				res.register_advancement()
				self.advance()
			else:
				arg_nodes.append(res.register(self.expr()))
				if(res.error):
					return res.failure(InvalidSyntaxError(
						self.current_token.pos_start, self.current_token.pos_end,
						"Expected ')', 'var', 'if', 'for', 'while', 'fun', int, float, ident, '+', '-', '(', '[',] or 'not'"
					))
				
				while(self.current_token.type == Type.tcomma.name):
					res.register_advancement()
					self.advance()

					arg_nodes.append(res.register(self.expr()))

					if(res.error):
						return res
					
				if(self.current_token.type != Type.trpar.name):
					return res.failure(InvalidSyntaxError(
						self.current_token.pos_start, self.current_token.pos_end,
						"Expected ',' or ')'"
					))

				res.register_advancement()
				self.advance()
			
			return res.success(CallNode(atom, arg_nodes))
		
		return res.success(atom)				

	def atom(self):
		res = ParseResult()
		token = self.current_token

		if(token.type in (Type.tint.name, Type.tfloat.name)):
			res.register_advancement()
			self.advance()
			return res.success(NumberNode(token))
		elif(token.type == Type.tstring.name):
			res.register_advancement()
			self.advance()
			return res.success(StringNode(token))
		elif(token.type == Type.tident.name):
			res.register_advancement()
			self.advance()
			return res.success(VarAccessNode(token))
		elif(token.type == Type.tlpar.name):
			res.register_advancement()
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
		
		elif(token.type == Type.tlsqu.name):
			list_expr = res.register(self.list_expr())

			if(res.error):
				return res

			return res.success(list_expr)

		elif(token.matches(Type.tkeyword.name, 'if')):
			if_expr = res.register(self.if_expr())

			if(res.error):
				return res
			
			return res.success(if_expr)

		elif(token.matches(Type.tkeyword.name, 'for')):
			for_expr = res.register(self.for_expr())

			if(res.error):
				return res
			
			return res.success(for_expr)

		elif(token.matches(Type.tkeyword.name, 'while')):
			while_expr = res.register(self.while_expr())

			if(res.error):
				return res
			
			return res.success(while_expr)

		elif(token.matches(Type.tkeyword.name, 'fun')):
			fun_def = res.register(self.fun_def())

			if(res.error):
				return res
			
			return res.success(fun_def)
		
		return res.failure(InvalidSyntaxError(
			token.pos_start, token.pos_end,
			"Expected Int, Float, Identifier, 'var', '+', '-' or '(', '[', 'if', 'for','while' or 'fun'"
		))
	
	def power(self):
		return self.bin_op(self.call, (Type.tpow.name, ), self.factor)

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
				"Expected Int, Float, Identifier, 'var', '+', '-', '(', '[' or 'not'"
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
		
		node = res.register(self.bin_op(self.comp_expr, ((Type.tkeyword.name, 'and'), (Type.tkeyword.name, 'or'))))

		if(res.error):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'var', int, float, identifier, '+', '-', '(', '[' or 'not'"
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

	def parse(self, tokens):

		self.clear(tokens)

		res = self.statements()
		if(not res.error and self.current_token.type != Type.teof.name):
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'and' or 'or'"
			))

		return res

# fun add(a, b) -> a + b