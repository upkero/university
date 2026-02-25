#include <iostream>
using namespace std;

int slen(char*);
int sravn(char*, char*);

int main() {
    char str1[200] = {};
    char str2[200] = {};

    cout << "Enter first string: ";
    cin >> str1;
    cout << "Enter second string: ";
    cin >> str2;

    /*for (int j = 0; j < slen(str2); j++) {
      cout << (int)*(str1+j) << "\t" << (int)*(str2+j) << endl;
    }*/

    cout << sravn(str1, str2) << endl;
}

int slen(char* string) {
    int lenth = 0;
    while (string[lenth]) lenth++;
    return lenth;
}

int sravn(char* string1, char* string2) {
    int i = 0;

    while (true) {
        if (string1[i] == string2[i]) i++;
        else break;
    }

    return string1[i] - string2[i];
}
