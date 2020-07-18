from .token import Type
from .values import Value, Number, String
from .results import RunTimeResult
from .errors import RunTimeError
from .symbol_table import SymbolTable

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None

	def restart(self, initials):
		symb_remove = []
		
		for symb in self.symbol_table.symbols:
			if(symb not in initials):
				symb_remove.append(symb)
		
		for symb in symb_remove:
			self.symbol_table.remove(symb)

class List(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements

	def added_by(self, other):
		new_list = self.copy()
		new_list.elements.append(other)

		return new_list, None
	
	def subbed_by(self, other):
		if(isinstance(other, Number)):
			new_list = self.copy()
			try:
				new_list.elements.pop(other.value)
				return new_list, None
			except:
				return None, RunTimeError(
					other.pos_start, other.pos_end,
					'Element at this index could not remove because index is out of bounds',
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if(isinstance(other, List)):
			print(self.elements)
			new_list = self.copy()
			new_list.elements.extend(other.elements)
			return new_list, None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if(isinstance(other, Number)):
			try:
				return self.elements[other.value], None
			except:
				return None, RunTimeError(
					other.pos_start, other.pos_end,
					'Element at this index could not remove because index is out of bounds',
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def copy(self):
		copy = List(self.elements)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)

		return copy

	def __repr__(self):
		return '[{}]'.format(", ".join([str(x) for x in self.elements]))

class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name or '<anonymous>'

	def generate_context(self):
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

		return new_context
	
	def check_args(self, arg_names, args):
		res = RunTimeResult()
		if(len(args) > len(arg_names)):
			return res.failure(RunTimeError(
				self.pos_start, self.pos_end,
				"'{}' too many args passed into '{}'".format(len(args) - len(arg_names), self.name),
				self.context
			))
		
		if(len(args) < len(arg_names)):
			return res.failure(RunTimeError(
				self.pos_start, self.pos_end,
				"{} too few args passed into '{}'".format(len(arg_names) - len(args), self.name),
				self.context
			))

		return res.success(None)

	def populate_args(self, arg_names, args, exec_ctx):
		for i in range(len(args)):
			arg_name = arg_names[i]
			arg_value = args[i]
			arg_value.set_context(exec_ctx)
			exec_ctx.symbol_table.set(arg_name, arg_value)

	def check_and_populate_args(self, arg_names, args, exec_ctx):
		res = RunTimeResult()
		res.register(self.check_args(arg_names, args))

		if(res.error):
			return res
		
		self.populate_args(arg_names, args, exec_ctx)
		return res.success(None)

class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names

	def execute(self, args):
		res = RunTimeResult()

		interpreter = Interpreter()
		exec_ctx = self.generate_context()

		res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
		
		if(res.error):
			return res

		value = res.register(interpreter.visit(self.body_node, exec_ctx))

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

class BuiltInFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RunTimeResult()
		exec_ctx = self.generate_context()

		method_name = 'execute_{}'.format(self.name)
		method = getattr(self, method_name, self.no_visit_method)

		res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
		if(res.error):
			return res

		return_value = res.register(method(exec_ctx))

		if(res.error):
			return res

		return res.success(return_value)
	
	def no_visit_method(self, node, context):
		raise Exception('No execute_{} method defined'.format(self.name))

	def copy(self):
		copy = BuiltInFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return '<build-in function {}>'.format(self.name)

	def execute_print(self, exec_ctx):
		print(str(exec_ctx.symbol_table.get('value')))
		return RunTimeResult().success(Number.null)
	execute_print.arg_names = ['value']

	def execute_print_ret(self, exec_ctx):
		return RunTimeResult().success(String(str(exec_ctx.symbol_table.get('value'))))
	execute_print_ret.arg_names = ['value']
  
	def execute_input(self, exec_ctx):
		text = input()
		return RunTimeResult().success(String(text))
	execute_input.arg_names = []

	def execute_input_int(self, exec_ctx):
		while True:
			text = input()
			try:
				number = int(text)
				break
			except ValueError:
				print(f"'{text}' must be an integer. Try again!")
		return RunTimeResult().success(Number(number))
	execute_input_int.arg_names = []

	def execute_is_number(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
		return RunTimeResult().success(Number.true if is_number else Number.false)
	execute_is_number.arg_names = ["value"]

	def execute_is_string(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
		return RunTimeResult().success(Number.true if is_number else Number.false)
	execute_is_string.arg_names = ["value"]

	def execute_is_list(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
		return RunTimeResult().success(Number.true if is_number else Number.false)
	execute_is_list.arg_names = ["value"]

	def execute_is_function(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
		return RunTimeResult().success(Number.true if is_number else Number.false)
	execute_is_function.arg_names = ["value"]

	def execute_append(self, exec_ctx):
		list_ = exec_ctx.symbol_table.get("list")
		value = exec_ctx.symbol_table.get("value")

		if not isinstance(list_, List):
			return RunTimeResult().failure(RunTimeError(
				self.pos_start, self.pos_end,
				'First argument must be list',
				exec_ctx
			))

		list_.elements.append(value)
		return RunTimeResult().success(Number.null)
	execute_append.arg_names = ["list", "value"]

	def execute_pop(self, exec_ctx):
		list_ = exec_ctx.symbol_table.get("list")
		index = exec_ctx.symbol_table.get("index")

		if not isinstance(list_, List):
			return RunTimeResult().failure(RunTimeError(
				self.pos_start, self.pos_end,
				"First argument must be list",
				exec_ctx
			))

		if not isinstance(index, Number):
			return RunTimeResult().failure(RunTimeError(
				self.pos_start, self.pos_end,
				'Second argument must be number',
				exec_ctx
			))

		try:
			element = list_.elements.pop(index.value)
		except:
			return RunTimeResult().failure(RunTimeError(
				self.pos_start, self.pos_end,
				'Element at this index could not be removed from list because index is out of bounds',
				exec_ctx
			))
		return RunTimeResult().success(element)
	execute_pop.arg_names = ["list", "index"]

	def execute_extend(self, exec_ctx):
		listA = exec_ctx.symbol_table.get("listA")
		listB = exec_ctx.symbol_table.get("listB")

		if not isinstance(listA, List):
			return RunTimeResult().failure(RunTimeError(
				self.pos_start, self.pos_end,
				'First argument must be list',
				exec_ctx
			))

		if not isinstance(listB, List):
			return RunTimeResult().failure(RunTimeError(
				self.pos_start, self.pos_end,
				'Second argument must be list',
				exec_ctx
			))

		listA.elements.extend(listB.elements)
		return RunTimeResult().success(Number.null)
	execute_extend.arg_names = ["listA", "listB"]
	

BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.print_ret   = BuiltInFunction("print_ret")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.input_int   = BuiltInFunction("input_int")
BuiltInFunction.is_number   = BuiltInFunction("is_number")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append      = BuiltInFunction("append")
BuiltInFunction.pop         = BuiltInFunction("pop")
BuiltInFunction.extend      = BuiltInFunction("extend")


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

	def visit_StringNode(self, node, context):
		return RunTimeResult().success(
			String(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_ListNode(self, node, context):
		res = RunTimeResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.visit(element_node, context)))
			if(res.error):
				return res

		return res.success(
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
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

		value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
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
		elements = []

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

			elements.append(res.register(self.visit(node.body_node, context)))

			if(res.error):
				return res
	
		return res.success(
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_WhileNode(self, node, context):
		res = RunTimeResult()
		elements = []

		while(True):
			condition = res.register(self.visit(node.condition_node, context))

			if(res.error):
				return res

			if(not condition.is_true()):
				break

			elements.append(res.register(self.visit(node.body_node, context)))

			if(res.error):
				return res

		return res.success(
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)
	
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
		return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(return_value)
