from .token import Type
from .values import Value, Number
from .results import RunTimeResult
from .errors import RunTimeError
from .symbol_table import SymbolTable

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None

class Function(Value):
	def __init__(self, name, body_node, arg_names):
		super().__init__()
		self.name = name or "<anonymous>"
		self.body_node = body_node
		self.arg_names = arg_names

	def execute(self, args):
		res = RunTimeResult()

		interpreter = Interpreter()
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

		if(len(args) > len(self.arg_names)):
			return res.failure(RunTimeError(
				self.pos_start, self.pos_end,
				"'{}' too many args passed into '{}'".format(len(args) - len(self.arg_names), self.name),
				self.context
			))
		
		if(len(args) < len(self.arg_names)):
			return res.failure(RunTimeError(
				self.pos_start, self.pos_end,
				"{} too few args passed into '{}'".format(len(self.arg_names) - len(args), self.name),
				self.context
			))

		for i in range(len(args)):
			arg_name = self.arg_names[i]
			arg_value = args[i]
			arg_value.set_context(new_context)
			new_context.symbol_table.set(arg_name, arg_value)

		value = res.register(interpreter.visit(self.body_node, new_context))

		if(res.error):
			return res

		return res.success(value)

	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return '<function {}>'.format(self.name)

class Interpreter:
	def visit(self, node, context):
		method_name = 'visit_{}'.format(type(node).__name__)
		method = getattr(self, method_name, self.no_visit)

		return method(node, context)

	def no_visit(self, node, context):
		raise Exception('No visit_{} method difined'.format(type(node).__name__))

	def visit_NumberNode(self, node, context):
		return RunTimeResult().success(
			Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_VarAccessNode(self, node, context):
		res = RunTimeResult()

		var_name = node.var_name_token.value
		value = context.symbol_table.get(var_name)

		if(not value):
			return res.failure(RunTimeError(
				node.pos_start, node.pos_end,
				"'{}' is not defined".format(var_name),
				context
			))

		value = value.copy().set_pos(node.pos_start, node.pos_end)
		return res.success(value)

	def visit_VarAssignNode(self, node, context):
		res = RunTimeResult()
		var_name = node.var_name_token.value
		value = res.register(self.visit(node.value_node, context))

		if(res.error):
			return res

		context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_BinOpNode(self, node, context):
		res = RunTimeResult()

		left = res.register(self.visit(node.left_node, context))
		if(res.error):
			return res

		right = res.register(self.visit(node.right_node, context))
		if(res.error):
			return res

		if(node.op_token.type == Type.tplus.name):
			result, error = left.added_by(right)
		elif(node.op_token.type == Type.tminus.name):
			result, error = left.subbed_by(right)
		elif(node.op_token.type == Type.tmul.name):
			result, error = left.multed_by(right)
		elif(node.op_token.type == Type.tdiv.name):
			result, error = left.dived_by(right)
		elif(node.op_token.type == Type.tpow.name):
			result, error = left.powed_by(right)

		elif(node.op_token.type == Type.tee.name):
			result, error = left.getComparisonEq(right)
		elif(node.op_token.type == Type.tneq.name):
			result, error = left.getComparisonNeq(right)
		elif(node.op_token.type == Type.tlt.name):
			result, error = left.getComparisonLt(right)
		elif(node.op_token.type == Type.tgt.name):
			result, error = left.getComparisonGt(right)
		elif(node.op_token.type == Type.tlte.name):
			result, error = left.getComparisonLte(right)
		elif(node.op_token.type == Type.tgte.name):
			result, error = left.getComparisonGte(right)
		elif(node.op_token.matches(Type.tkeyword.name, 'and')):
			result, error = left.anded_by(right)
		elif(node.op_token.matches(Type.tkeyword.name, 'or')):
			result, error = left.ored_by(right)

		if(error):
			return res.failure(error)
		else:
			return res.success(result.set_pos(node.pos_start, node.pos_end))

	def visit_UnaryOpNode(self, node, context):	
		res = RunTimeResult()
		number = res.register(self.visit(node.node, context))

		if(res.error):
			return res
		
		error = None

		if(node.op_token.type == Type.tminus.name):
			number, error = number.multed_by(Number(-1))
		elif(node.op_token.matches(Type.tkeyword.name, 'not')):
			number, error = number.notted()

		if(error):
			return res.failure(error)
		else:
			return res.success(number.set_pos(node.pos_start, node.pos_end))

	def visit_IfNode(self, node, context):
		res = RunTimeResult()

		for condition, expr in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if(res.error):
				return res
			
			if(condition_value.is_true()):
				expr_value = res.register(self.visit(expr, context))

				if(res.error):
					return res

				return res.success(expr_value)
		
		if(node.else_case):
			else_value = res.register(self.visit(node.else_case, context))

			if(res.error):
				return res
			
			return res.success(else_value)
		
		return res.success(None) 
	
	def visit_ForNode(self, node, context):
		res = RunTimeResult()

		start_value = res.register(self.visit(node.start_value_node, context))
		if(res.error):
			return res

		end_value = res.register(self.visit(node.end_value_node, context))
		if(res.error):
			return res

		if(node.step_value_node):
			step_value = res.register(self.visit(node.step_value_node, context))
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
			context.symbol_table.set(node.var_name_token.value, Number(i))
			i += step_value.value

			res.register(self.visit(node.body_node, context))

			if(res.error):
				return res
	
		return res.success(None)

	def visit_WhileNode(self, node, context):
		res = RunTimeResult()

		while(True):
			condition = res.register(self.visit(node.condition_node, context))

			if(res.error):
				return res

			if(not condition.is_true()):
				break

			res.register(self.visit(node.body_node, context))

			if(res.error):
				return res

		return res.success(None)
	
	def visit_FunctionNode(self, node, context):
		res = RunTimeResult()

		func_name = node.var_name_token.value if node.var_name_token else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
		func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)
		
		if node.var_name_token:
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
