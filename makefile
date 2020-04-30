CC		= g++ -std=c++11
SRCS	= 	main.cpp \
			src/lexer/token.cpp \
			src/lexer/lexer.cpp

OBJS	= $(SRCS:.cpp=.o)

all: main

main: $(OBJS)
	$(CC) -o main.out $(OBJS)

%.o: %.cpp
	$(CC) -c $< -o $@

# delete lib with clean 
clean:
	rm -f src/lexer/*.o src/parser/*.o *.o *.out