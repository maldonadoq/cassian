from .token import Type
from .values import Number

class Interpreter:
	def visit(self, _node):
		method_name = 'visit_{}'.format(type(_node).__name__)
		method = getattr(self, method_name, self.no_visit)

		return method(_node)

	def no_visit(self, _node):
		raise Exception('No visit_{} method difined'.format(type(_node).__name__))

	def visit_NumberNode(self, _node):
		return Number(_node.token.value).set_pos(_node.pos_start, _node.pos_end)

	def visit_BinOpNode(self, _node):
		left = self.visit(_node.left_node)		
		right = self.visit(_node.right_node)

		if(_node.op_token.type == Type.tplus.name):
			res = left.added_by(right)
		elif(_node.op_token.type == Type.tminus.name):
			res = left.subbed_by(right)
		elif(_node.op_token.type == Type.tmul.name):
			res = left.multed_by(right)
		elif(_node.op_token.type == Type.tdiv.name):
			res = left.dived_by(right)

		return res.set_pos(_node.pos_start, _node.pos_end)

	def visit_UnaryOpNode(self, _node):		
		number = self.visit(_node.node)

		if(_node.op_token.type == Type.tminus.name):
			number = number.multed_by(Number(-1))

		return number.set_pos(_node.pos_start, _node.pos_end)