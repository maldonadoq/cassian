#include <iostream>
#include "token.h"

using std::cout;
using std::endl;

class Lexer{
private:
    string text;
    int pos;
    char current;    
public:
    Lexer();
    Lexer(string);

    Token scanner();
    
    void advance();
    void isError(int);
    int isAlpha(char);
    int isAlphaNum(char);

    int getNum(char);

};