#ifndef _LEXER_H_
#define _LEXER_H_

#include <iostream>
#include <cstring>
#include "token.h"

using std::cout;
using std::endl;
using std::stoi;
using std::stof;

class Lexer{
private:
    string text;
    int pos;
    char current;

    vector<Token> tokens;
public:
    Lexer();
    Lexer(string);
    ~Lexer();
    
    void scanner();

    void setText(string);
    
    void advance();
    void back();

    void printError(int);
    void printTokens();

    bool isAlpha(char);
    bool isAlphaNum(char);

    Token getNum();

};

#endif