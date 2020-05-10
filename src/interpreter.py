from .token import Type
from .values import Number
from .results import RunTimeResult

class Context:
	def __init__(self, _display_name, _parent=None, _parent_entry_pos=None):
		self.display_name = _display_name
		self.parent = _parent
		self.parent_entry_pos = _parent_entry_pos

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

		if(error):
			return res.failure(error)
		else:
			return res.success(number.set_pos(_node.pos_start, _node.pos_end))