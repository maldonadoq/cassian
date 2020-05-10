class NumberNode:
	def __init__(self, _token):
		self.token = _token

		self.pos_start = self.token.pos_start
		self.pos_end = self.token.pos_end
	
	def __repr__(self):
		return '{}'.format(self.token)

class BinOpNode:
	def __init__(self, _left_node, _op_token, _right_node):
		self.left_node = _left_node
		self.op_token = _op_token
		self.right_node = _right_node

		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end

	def __repr__(self):
		return '({},{},{})'.format(self.left_node, self.op_token, self.right_node)

class UnaryOpNode:
	def __init__(self, _op_token, _node):
		self.op_token = _op_token
		self.node = _node

		self.pos_start = self.op_token.pos_start
		self.pos_end = _node.pos_end

	def __repr__(self):
		return '({},{})'.format(self.op_token, self.node)