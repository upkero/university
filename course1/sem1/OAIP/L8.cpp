#include <iostream>
using namespace std;

double fnRecursion(double);
double fnNormal(double);

int main() {
 double n;
 cout << "Enter n: "; cin >> n;
 cout << "FnRecursion(n) = " << /*fnRecursion(n) <<*/ endl << "FnNormal(n) = " << fnNormal(n) << endl;
 return 0;
}

double fnRecursion(double n) {
 if (n == 0) return 0;
 if (n == 1) return 1;
 return fnRecursion(n - 1) + fnRecursion(n - 2);
}
double fnNormal(double n) {
 double firstItem = 0; 
 double secondItem = 1;
 double temp;
 for (int i = 0; i < n; i++) {
  temp = firstItem;
  firstItem = secondItem;
  secondItem += temp;
 }
 return firstItem;
}
