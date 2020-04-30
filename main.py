from src.lexer import Lexer

if __name__ == "__main__":
	lex = Lexer()
	while(True):
		line = input('cassian: ')

		if(line == ':q'):
			break

		tokens, error = lex.scanner('<stdin>', line)

		if(error):
			print(error)
		else:
			print(tokens)