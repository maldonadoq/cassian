#include "lexer.h"


Lexer::Lexer(){

}

Lexer::Lexer(string text){
    this->text = text;
    this->pos = -1;
    
    advance();

}

void Lexer::advance(){
    pos = -1;
    current = 
}

void Lexer::isError(int n){
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

Token Lexer::scanner(){
    Token token;
    int i;
    int idx;
    char ch;
    char id[ID_SIZE];

    token.number = tnull;
    token.value.num = 0;    

    do{
        // Space
        while(isspace(ch = getchar()));

        // Identifier or Keyword
        if(isWord(ch)){
            i = 0;
            do{
                if(i < ID_SIZE)
                    id[i++] = ch;
                ch = getchar();
            } while(isWordOrDigit(ch));

            if(i >= ID_SIZE){
                lexError(1);
            }

            id[i] = '\0';

            ungetc(ch, stdin);
            
            for(idx = 0; idx<NO_KEYWORDS; idx++){
                if(!strcmp(id, keyword[idx])){
                    // cout << id << endl;
                    break;
                }
            }

            if(idx < NO_KEYWORDS){
                token.number = tnum[idx];
            }
            else{
                token.number = tident;
                strcpy(token.value.id, id);
            }
        }
        // Integer const
        else if(isdigit(ch)){
            token.number = tnumber;
            token.value.num = getIntNum(ch);
        }
        else{
            switch (ch){                
                case '!':
                    ch = getchar();
                    if(ch == '='){
                        token.number = tnoteq;
                    }
                    else{
                        token.number = tnot;
                        ungetc(ch, stdin);
                    }
                    break;  
                case '&':
                    ch = getchar();
                    if (ch == '&'){
                        token.number = tand;
                    }
                    else {
                        lexError(2);
                        ungetc(ch, stdin);
                    }
                    break;                
                case '<':
                    ch = getchar();
                    if (ch == '=')
                        token.number = tlesse;
                    else {
                        token.number = tless;
                        ungetc(ch, stdin);
                    }
                    break;
                case '=':
                    ch = getchar();
                    if (ch == '=')
                        token.number = tequal;
                    else {
                        token.number = tassign;
                        ungetc(ch, stdin);
                    }
                    break;
                case '>':
                    ch = getchar();
                    if (ch == '=')
                        token.number = tgreate;
                    else {
                        token.number = tgreat;
                        ungetc(ch, stdin);
                    }
                    break;
                case '|':
                    ch = getchar();
                    if (ch == '=')
                        token.number = tor;
                    else {
                        lexError(3);
                        ungetc(ch, stdin); // retract
                    }
                    break;
                case '/':   token.number = tdiv;        break;
                case '*':   token.number = tmul;        break;
                case '+':   token.number = tplus;       break;
                case '-':   token.number = tminus;      break;
                case '(':   token.number = tlparen;     break;
                case ')':   token.number = trparen;     break;
                case ',':   token.number = tcomma;      break;
                case ';':   token.number = tsemicolon;  break;
                case '[':   token.number = tlbracket;   break;
                case ']':   token.number = trbracket;   break;
                case '{':   token.number = tlbrace;     break;
                case '}':   token.number = trbrace;     break;
                case EOF:   token.number = teof;        break;
                default:
                    break;
            }
        }
    } while (token.number == tnull);

    return token;
}