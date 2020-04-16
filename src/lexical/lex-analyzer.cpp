#include <iostream>

#define NO_KEYWORDS 7
#define ID_SIZE 12


enum tSymbol {
    tnull = -1,
    tnot, tnoteq, tmod, tmodAssign, tident, tnumber, tand, tlparen, trparen, tmul,
    tmulAssign, tplus, tinc, taddAssign, tcomma, tminus, tdec, tsubAssign, tequal,
    tgreat, tgreate, tlbracket, trbracket, teof, tconst, telse, tif, tint, treturn,
    tvoid, twhile, tlbrace, tor, trbrace
};

char * symbol_token[] = {
    "!", "!=", "%", "%=", "NULL", "NULL", "&&", "(", ")", "*",
    "*=", "+", "++", "+=", ",", "-", "--", "-=", "==",
    ">", ">=", "[", "]", "", "const", "else", "if", "int", "return",
    "void", "while", "{", "||", ")"
};