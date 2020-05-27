import readline

from src.lexer import Lexer
from src.parser import Parser
from src.values import Number
from src.interpreter import Interpreter, Context
from src.symbol_table import SymbolTable

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))
global_symbol_table.set("false", Number(0))
global_symbol_table.set("true", Number(1))

if __name__ == "__main__":
	lex = Lexer()
	par = Parser()
	inter = Interpreter()
	ctx = Context('<program>')
	ctx.symbol_table = global_symbol_table

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
				elif(res.value):
					print(res.value)