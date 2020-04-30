#include "token.h"

Token::Token(){
    clear();
}

string Token::toString(){
    string line = to_string(type);

    if(idx == 0){
        line = line + ":" + value._id;
    }
    else if(idx == 1){
        line = line + ":" + to_string(value._int);
    }
    else if(idx == 2){
        cout << to_string(value._float) << "\n";
        cout << value._float << "\n";
        line = line + ":" + to_string(value._float);
    }

    return line;
}

void Token::clear(){
    idx = -1;
    type = tnull;

    strcpy(value._id, "");
    value._int = tnull;
    value._float = tnull;
}