#include <iostream>
#include <string>

#include "src/lexer/lexer.h"

using std::getline;
using std::string;
using std::cout;
using std::endl;
using std::cin;

int main(int argc, char const *argv[]){
    
    Lexer *lex = new Lexer();

    string line = "";

    while(line != ":q"){
        cout << "cassian: ";
        getline(cin, line);

        if(line == ":q"){
            break;
        }

        lex->setText(line);
        lex->scanner();

        lex->printTokens();
    }

    delete lex;
    return 0;
}
