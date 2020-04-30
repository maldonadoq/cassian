#include "lexer.h"

const char * symbolToken[] = {
    "!", "!=", "NULL", "NULL", "NULL", "&&",
    "(", ")", "*", "+", "-", "/",
    "<", "<=", "=", "==", ">", ">=",
    "[", "]", "", "else", "if", "while",
    "{", "||", "}"
};

const char *keyword[NO_KEYWORDS] = {
    "if", "else", "while", "int", "float"
};

enum symbolTable tnum[NO_KEYWORDS] = {
    tif, telse, twhile, tint, tfloat
};

Lexer::Lexer(){

}

Lexer::Lexer(string text){
    this->text = text;
    this->pos = tnull;
    
    advance();

}

Lexer::~Lexer(){

}

void Lexer::setText(string text){
    this->text = text;
    this->pos = tnull;

    advance();
}

void Lexer::advance(){
    pos++;

    if(pos < text.size()){
        current = text[pos];
    }
    else{
        current = tnull;
    }
    
}

void Lexer::back(){
    pos--;

    if(pos < 0){
        current = tnull;
    }
    else{
        current = text[pos];
    }
    
}

void Lexer::printError(int n){
    cout << "Lexical Error: ";

    switch (n){
        case 1:
            cout << "An identifiers size must be less that " << ID_SIZE << endl;
            break;
        case 2:
            cout << "Next character must be &\n";
            break;
        case 3:
            cout << "Next character must be |\n";
            break;
        case 4:
            cout << "Invalid character\n";
            break;
        default:
            break;
    }
}

void Lexer::printTokens(){
    for(int i=0; i<tokens.size(); i++){
        cout << tokens[i].toString() << endl;
    }    
}


bool Lexer::isAlpha(char ch){
    if(isalpha(ch))
        return true;
    
    return false;
}

bool Lexer::isAlphaNum(char ch){
    if(isalnum(ch) || ch == '_')
        return true;
    
    return false;
}

Token Lexer::getNum(){
    string num = "";
    int dot = 0;

    while (isdigit(current) or current == '.'){
        if(current == '.'){
            if(dot == 1){
                break;
            }

            dot++;
            num += current;
        }
        else{
            num += current;
        }
        advance();
    }

    Token token;

    if(dot == 0){
        token.type = tint;
        token.value._int = stoi(num);
        token.idx = 1;
        //cout << "tok int: " << token.value._int << endl;
    }
    else{
        token.type = tfloat;
        cout<<"ls: " << num << "\n";
        cout<<"lf: " << stof(num) << "\n";
        token.value._float = stof(num);
        token.idx = 2;
        //cout << "tok float: " << token.value._float << endl;
    }

    return token;
    
}

void Lexer::scanner(){
    tokens.clear();
    Token token;
    token.type = 0;

    int i, idx;
    char id[ID_SIZE];    

    while(pos < text.size() and token.type != tnull){
        token.clear();

        // Space        
        while(isspace(current)){
            advance();
        }

        // Identifier or Keyword
        if(isAlpha(current)){
            i = 0;
            do{
                if(i < ID_SIZE)
                    id[i++] = current;
                advance();
            } while(isAlphaNum(current));

            //if(i >= ID_SIZE){
            //    printError(1);
            //}

            id[i] = '\0';
            
            for(idx = 0; idx<NO_KEYWORDS; idx++){
                if(!strcmp(id, keyword[idx])){
                    break;
                }
            }

            if(idx < NO_KEYWORDS){
                token.type = tnum[idx];
                tokens.push_back(token);
            }
            else{
                token.type = tident;
                token.idx = 0;
                strcpy(token.value._id, "");
                tokens.push_back(token);
            }
        }
        // Integer const
        else if(isdigit(current)){
            token = getNum();
            tokens.push_back(token);
        }
        else{
            switch (current){
                case '!':
                    advance();
                    if(current == '='){
                        token.type = tnoteq;
                        tokens.push_back(token);
                    }
                    else{
                        token.type = tnot;
                        tokens.push_back(token);
                        back();
                    }
                    break;  
                case '&':
                    advance();
                    if (current == '&'){
                        token.type = tand;
                        tokens.push_back(token);
                    }
                    else {
                        // lexError(2);
                        back();
                    }
                    break;                
                case '<':
                    advance();
                    if (current == '='){
                        token.type = tlesse;
                        tokens.push_back(token);
                    }
                    else {
                        token.type = tless;
                        tokens.push_back(token);
                        back();
                    }
                    break;
                case '=':
                    advance();
                    if (current == '='){
                        token.type = tequal;
                        tokens.push_back(token);
                    }
                    else {
                        token.type = tassign;
                        tokens.push_back(token);
                        back();
                    }
                    break;
                case '>':
                    advance();
                    if (current == '='){
                        token.type = tgreate;
                        tokens.push_back(token);
                    }
                    else {
                        token.type = tgreat;
                        tokens.push_back(token);
                        back();
                    }
                    break;
                case '|':
                    advance();
                    if (current == '='){
                        token.type = tor;
                        tokens.push_back(token);
                    }
                    else {
                        // lexError(3);
                        back();
                    }
                    break;
                case '/':   token.type = tdiv;      tokens.push_back(token);    advance();  break;
                case '*':   token.type = tmul;      tokens.push_back(token);    advance();  break;
                case '+':   token.type = tplus;     tokens.push_back(token);    advance();  break;
                case '-':   token.type = tminus;    tokens.push_back(token);    advance();  break;
                case '(':   token.type = tlparen;   tokens.push_back(token);    advance();  break;
                case ')':   token.type = trparen;   tokens.push_back(token);    advance();  break;
                case '[':   token.type = tlbracket; tokens.push_back(token);    advance();  break;
                case ']':   token.type = trbracket; tokens.push_back(token);    advance();  break;
                case '{':   token.type = tlbrace;   tokens.push_back(token);    advance();  break;
                case '}':   token.type = trbrace;   tokens.push_back(token);    advance();  break;
                case EOF:   token.type = teof;      tokens.push_back(token);    advance();  break;
                default:
                    break;
            }
        }
    }
}