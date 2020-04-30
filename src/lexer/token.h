#ifndef _TOKEN_H_
#define _TOKEN_H_

#include <string>
#include <iostream>
#include <vector>
#include <cstring>

using std::string;
using std::to_string;
using std::ostream;
using std::vector;
using std::cout;
using std::strcpy;

#define NO_KEYWORDS 5
#define ID_SIZE 12

enum symbolTable {
    tnull = -1,
    tnot, tnoteq, tident, tint, tfloat, tand,
    tlparen, trparen, tmul, tplus, tminus, tdiv,
    tless, tlesse, tassign, tequal, tgreat, tgreate,
    tlbracket, trbracket, teof, telse, tif, twhile,
    tlbrace, tor, trbrace
};

class Token{
public:
    int type;
    int idx;
    union {
        char _id[ID_SIZE];
        int _int;
        int _float;
    } value;

    Token();

    void clear();
    string toString();

    friend ostream& operator<< (ostream & out, Token &token){
       out << token.toString();
       return out;
   	}
};

#endif