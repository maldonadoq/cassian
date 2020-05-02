from src.lexer import Lexer
from src.parser import Parser

if __name__ == "__main__":
	lex = Lexer()
	par = Parser()
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
				print(ast.node)