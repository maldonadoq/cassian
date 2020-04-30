#include <iostream>
#include <string>

using std::getline;
using std::string;
using std::cout;
using std::endl;
using std::cin;

int main(int argc, char const *argv[]){
    
    string line;
    do{
        cout << "cassian: ";
        getline(cin, line);

        cout << " " << line << endl;
    } while (line != ":q");

    return 0;
}
