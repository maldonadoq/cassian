class NumberNode:
	def __init__(self, _token):
		self.token = _token
	
	def __repr__(self):
		return '{}'.format(self.token)

class BinOpNode:
	def __init__(self, _left_node, _op_token, _right_node):
		self.left_node = _left_node
		self.op_token = _op_token
		self.right_node = _right_node

	def __repr__(self):
		return '({},{},{})'.format(self.left_node, self.op_token, self.right_node)