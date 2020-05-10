from .utils import string_with_arrows

class Error:
	def __init__(self, _pos_start, _pos_end, _name, _details):
		self.name = _name
		self.pos_start = _pos_start
		self.pos_end = _pos_end
		self.details = _details

	def __repr__(self):
		result = ' {}:{}\n'.format(self.name, self.details)
		result += ' File {}, line{}\n\n'.format(self.pos_start.fn, self.pos_start.ln + 1)
		result += ' {}'.format(string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end))

		return result


class IllegalCharError(Error):
	def __init__(self, _pos_start, _pos_end, _details):
		super().__init__(_pos_start, _pos_end, 'Illegal Character', _details)


class InvalidSyntaxError(Error):
	def __init__(self, _pos_start, _pos_end, _details):
		super().__init__(_pos_start, _pos_end, 'Invalid Syntax', _details)

class RunTimeError(Error):
	def __init__(self, _pos_start, _pos_end, _details, _context):
		super().__init__(_pos_start, _pos_end, 'Runtime Error', _details)
		self.context = _context

	def __repr__(self):

		result = self.generate_traceback()
		result += ' {}: {}\n\n'.format(self.name, self.details)
		result += ' {}'.format(string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end))

		return result
	
	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while(ctx):
			result = ' File {}, line {}, in {}\n'.format(pos.fn, str(pos.ln + 1), ctx.display_name) + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent
		
		return ' Traceback (most recent call last):\n{}'.format(result)