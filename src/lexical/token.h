#ifndef _TOKEN_H_
#define _TOKEN_H_

#include <string>
using std::string;
using std::to_string;

#define NO_KEYWORDS 3
#define ID_SIZE 12

class Token{
public:
    int type;
    union {
        char id[ID_SIZE];
        int num;        
    } value;

    Token();
    string getTokenString();
};

enum symbolTable {
    tnull = -1,
    tnot, tnoteq, tident, tnumber, tand, tlparen,
    trparen, tmul, tplus, tminus, tdiv, tless,
    tlesse, tassign, tequal, tgreat, tgreate, tlbracket,
    trbracket, teof, telse, tif, twhile, tlbrace,
    tor, trbrace
};

const char * symbolToken[] = {
    "!", "!=", "NULL", "NULL", "&&", "(",
    ")", "*", "+", "-", "/", "<",
    "<=", "=", "==", ">", ">=", "[",
    "]", "", "else", "if", "while", "{",
    "||", "}"
};

const char *keyword[NO_KEYWORDS] = {
    "if", "else", "while"
};

enum symbolTable tnum[NO_KEYWORDS] = {
    tif, telse, twhile
};

#endif