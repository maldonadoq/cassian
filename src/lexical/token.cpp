#include "token.h"

Token::Token(){

}

string Token::getTokenString(){
    string line;
    if(value.id != nullptr){
        line = to_string(type) + ":" + value.id;
        return line;
    }

    return to_string(type);
}