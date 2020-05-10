import readline

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter, Context

if __name__ == "__main__":
	lex = Lexer()
	par = Parser()
	inter = Interpreter()
	ctx = Context('<program>')

	while(True):
		line = input('cassian: ')

		if(line == ':q'):
			break

		tokens, error = lex.scanner('<stdin>', line)		

		if(error):
			print(error)
		else:
			#print(tokens)
			ast = par.parse(tokens)
			if(ast.error):
				print(ast.error)
			else:
				#print(type(ast.node).__name__)
				res = inter.visit(ast.node, ctx)

				if(res.error):
					print(res.error)
				else:
					print(res.value)