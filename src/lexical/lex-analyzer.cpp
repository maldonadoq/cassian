#include <cstring>
#include <iostream>

#define NO_KEYWORDS 7
#define ID_SIZE 12

using std::cout;
using std::endl;

enum tSymbol {
    tnull = -1,
    tnot, tnoteq, tident, tnumber, tand, tlparen,
    trparen, tmul, tplus, tcomma, tminus, tdiv,
    tsemicolon, tless, tlesse, tassign, tequal, tgreat,
    tgreate, tlbracket, trbracket, teof, tconst, telse,
    tif, tint, treturn, tvoid, twhile, tlbrace,
    tor, trbrace
};

const char * symbol_token[] = {
    "!", "!=", "NULL", "NULL", "&&", "(",
    ")", "*", "+", ",", "-", "/",
    ";", "<", "<=", "=", "==", ">",
    ">=", "[", "]", "", "const", "else",
    "if", "int", "return", "void", "while", "{",
    "||", "}"
};

const char *keyword[NO_KEYWORDS] = {
    "const", "else", "if", "int", "return", "void", "while"
};

enum tSymbol tnum[NO_KEYWORDS] = {
    tconst, telse, tif, tint, treturn, tvoid, twhile
};

int isWord(char ch){
    if(isalpha(ch) || ch == '_')
        return 1;
    
    return 0;
}

int isWordOrDigit(char ch){
    if(isalnum(ch) || ch == '_')
        return 1;
    
    return 0;
}

int getIntNum(char firstCh){
    int num = 0;
    char ch;

    if(firstCh != '0'){
        ch = firstCh;

        do{
            num = 10 * num + (int) (ch - '0');
            ch = getchar();
        } while (isdigit(ch));

        ungetc(ch, stdin);
    }

    return num;
}

class TokenType{
public:
    int number;
    union {
        char id[ID_SIZE];
        int num;        
    } value;

    TokenType(){}
};

class LexicalAnalyzer{
public:
    LexicalAnalyzer();

    TokenType scanner();
    void lexError(int);
};

LexicalAnalyzer::LexicalAnalyzer(){

}

void LexicalAnalyzer::lexError(int n){
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

TokenType LexicalAnalyzer::scanner(){
    TokenType token;
    int i;
    int idx;
    char ch;
    char id[ID_SIZE];

    token.number = tnull;
    token.value.num = 0;    

    do{
        // Space
        while(isspace(ch = getchar()));

        //cout << ch << endl;

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
                    cout << id << endl;
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

int main(int argc, char const *argv[]){
    if(argc != 2){
        cout << "Input Error: Must have two parameters\n";
        return -1;
    }

    if(freopen(argv[1], "rb", stdin) == NULL){
        cout << "Read Error: Invalid File Path\n";
        return -1;
    }

    LexicalAnalyzer lex = LexicalAnalyzer();
    TokenType token = lex.scanner();

    while(token.number != teof){
        if(token.number == tident){
            cout << token.value.id << " " << token.number << "\n";
        }
        else if(token.number == tnumber){
            cout << token.value.num << " " << token.number << "\n";
        }
        else{
            cout << symbol_token[token.number] << " " << token.number << " " << token.value.num << "\n";
        }

        token = lex.scanner();
    }
    
    return 0;
}
