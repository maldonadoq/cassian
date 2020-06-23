from .token import Type
from .values import Number
from .results import RunTimeResult
from .errors import RunTimeError

class Context:
	def __init__(self, _display_name, _parent=None, _parent_entry_pos=None):
		self.display_name = _display_name
		self.parent = _parent
		self.parent_entry_pos = _parent_entry_pos
		self.symbol_table = None

class Interpreter:
	def visit(self, _node, _context):
		method_name = 'visit_{}'.format(type(_node).__name__)
		method = getattr(self, method_name, self.no_visit)

		return method(_node, _context)

	def no_visit(self, _node, _context):
		raise Exception('No visit_{} method difined'.format(type(_node).__name__))

	def visit_NumberNode(self, _node, _context):
		return RunTimeResult().success(
			Number(_node.token.value).set_context(_context).set_pos(_node.pos_start, _node.pos_end)
		)

	def visit_VarAccessNode(self, _node, _context):
		res = RunTimeResult()

		var_name = _node.var_name_token.value
		value = _context.symbol_table.get(var_name)

		if(not value):
			return res.failure(RunTimeError(
				_node.pos_start, _node.pos_end,
				"'{}' is not defined".format(var_name),
				_context
			))

		value = value.copy().set_pos(_node.pos_start, _node.pos_end)
		return res.success(value)

	def visit_VarAssignNode(self, _node, _context):
		res = RunTimeResult()
		var_name = _node.var_name_token.value
		value = res.register(self.visit(_node.value_node, _context))

		if(res.error):
			return res

		_context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_BinOpNode(self, _node, _context):
		res = RunTimeResult()

		left = res.register(self.visit(_node.left_node, _context))
		if(res.error):
			return res

		right = res.register(self.visit(_node.right_node, _context))
		if(res.error):
			return res

		if(_node.op_token.type == Type.tplus.name):
			result, error = left.added_by(right)
		elif(_node.op_token.type == Type.tminus.name):
			result, error = left.subbed_by(right)
		elif(_node.op_token.type == Type.tmul.name):
			result, error = left.multed_by(right)
		elif(_node.op_token.type == Type.tdiv.name):
			result, error = left.dived_by(right)
		elif(_node.op_token.type == Type.tpow.name):
			result, error = left.powed_by(right)

		elif(_node.op_token.type == Type.tee.name):
			result, error = left.getComparisonEq(right)
		elif(_node.op_token.type == Type.tneq.name):
			result, error = left.getComparisonNeq(right)
		elif(_node.op_token.type == Type.tlt.name):
			result, error = left.getComparisonLt(right)
		elif(_node.op_token.type == Type.tgt.name):
			result, error = left.getComparisonGt(right)
		elif(_node.op_token.type == Type.tlte.name):
			result, error = left.getComparisonLte(right)
		elif(_node.op_token.type == Type.tgte.name):
			result, error = left.getComparisonGte(right)
		elif(_node.op_token.matches(Type.tkeyword.name, 'and')):
			result, error = left.anded_by(right)
		elif(_node.op_token.matches(Type.tkeyword.name, 'or')):
			result, error = left.ored_by(right)

		if(error):
			return res.failure(error)
		else:
			return res.success(result.set_pos(_node.pos_start, _node.pos_end))

	def visit_UnaryOpNode(self, _node, _context):	
		res = RunTimeResult()
		number = res.register(self.visit(_node.node, _context))

		if(res.error):
			return res
		
		error = None

		if(_node.op_token.type == Type.tminus.name):
			number, error = number.multed_by(Number(-1))
		elif(_node.op_token.matches(Type.tkeyword.name, 'not')):
			number, error = number.notted()

		if(error):
			return res.failure(error)
		else:
			return res.success(number.set_pos(_node.pos_start, _node.pos_end))

	def visit_IfNode(self, _node, _context):
		res = RunTimeResult()

		for condition, expr in _node.cases:
			condition_value = res.register(self.visit(condition, _context))
			if(res.error):
				return res
			
			if(condition_value.is_true()):
				expr_value = res.register(self.visit(expr, _context))

				if(res.error):
					return res

				return res.success(expr_value)
		
		if(_node.else_case):
			else_value = res.register(self.visit(_node.else_case, _context))

			if(res.error):
				return res
			
			return res.success(else_value)
		
		return res.success(None) 
	
	def visit_ForNode(self, _node, _context):
		res = RunTimeResult()

		start_value = res.register(self.visit(_node.start_value_node, _context))
		if(res.error):
			return res

		end_value = res.register(self.visit(_node.end_value_node, _context))
		if(res.error):
			return res

		if(_node.step_value_node):
			step_value = res.register(self.visit(_node.step_value_node, _context))
			if(res.error):
				return res
		else:
			step_value = Number(1)

		i = start_value.value

		if(step_value.value >= 0):
			condition = lambda: i < end_value.value
		else:
			condition = lambda: i > end_value.value

		while(condition()):
			_context.symbol_table.set(_node.var_name_token.value, Number(i))
			i += step_value.value

			res.register(self.visit(_node.body_node, _context))

			if(res.error):
				return res
	
		return res.success(None)

	def visit_WhileNode(self, _node, _context):
		res = RunTimeResult()

		while(True):
			condition = res.register(self.visit(_node.condition_node, _context))

			if(res.error):
				return res

			if(not condition.is_true()):
				break

			res.register(self.visit(_node.body_node, _context))

			if(res.error):
				return res

		return res.success(None)
	
	def visit_FunctionNode(self, node, context):
		res = RunTimeResult()

		func_name = node.var_name_tok.value if node.var_name_tok else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_toks]
		func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)
		
		if node.var_name_tok:
			context.symbol_table.set(func_name, func_value)

		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RunTimeResult()
		args = []

		value_to_call = res.register(self.visit(node.node_to_call, context))
		if res.error: return res
		value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

		for arg_node in node.arg_nodes:
			args.append(res.register(self.visit(arg_node, context)))
			if res.error: return res

		return_value = res.register(value_to_call.execute(args))
		if res.error: return res
		return res.success(return_value)
