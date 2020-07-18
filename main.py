import readline

from src.lexer import Lexer
from src.parser import Parser
from src.values import Number
from src.interpreter import Interpreter, Context, BuiltInFunction
from src.symbol_table import SymbolTable

symb_table = SymbolTable()
symb_table.set('null', Number.null)
symb_table.set('false', Number.false)
symb_table.set('true', Number.true)
symb_table.set('math_pi', Number.math_PI)
symb_table.set('print', BuiltInFunction.print)
symb_table.set('print_ret', BuiltInFunction.print_ret)
symb_table.set('input', BuiltInFunction.input)
symb_table.set('input_int', BuiltInFunction.input_int)
symb_table.set('is_num', BuiltInFunction.is_number)
symb_table.set('is_str', BuiltInFunction.is_string)
symb_table.set('is_list', BuiltInFunction.is_list)
symb_table.set('is_fun', BuiltInFunction.is_function)
symb_table.set('append', BuiltInFunction.append)
symb_table.set('pop', BuiltInFunction.pop)
symb_table.set('extend', BuiltInFunction.extend)

if __name__ == "__main__":
	lex = Lexer()
	par = Parser()
	inter = Interpreter()
	ctx = Context('<program>')
	ctx.symbol_table = symb_table

	while(True):
		line = input('cassian: ')

		if(line == ':q'):
			break
		elif(line == 'st'):
			print(ctx.symbol_table)
			continue
		elif(line == 'cls'):
			ctx.restart(['null', 'false', 'true'])
			continue

		tokens, error = lex.scanner('<stdin>', line)

		if(error):
			print(error)
		else:
			# print(tokens)
			ast = par.parse(tokens)
			if(ast.error):
				print(ast.error)
			else:
				# print(type(ast.node).__name__)
				res = inter.visit(ast.node, ctx)

				if(res.error):
					print(res.error)
				elif(res.value):
					print(res.value)