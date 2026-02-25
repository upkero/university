#include <iostream>
#include <cmath>
using namespace std;

double fbRecursion(int);
double fbNormal(int);
double rtRecursion(int, int);
double rtNormal(int);
void convertNormal(int, int);
void convertRecursion(int, int);

int main() {
	int n;
	cout << "Enter n: "; cin >> n;
	cout << "convertNormal: " << endl;
	for (int i = 2; i <= 16; i++) { 
		cout << i << ": "; 
		convertNormal(n, i); 
	}
	cout << "convertRecursion: " << endl;
	for (int i = 2; i <= 16; i++) {
		cout << i << ": ";
		convertRecursion(n, i);
		cout << endl;
	}
	/*cout << "===============================" << endl;
	cout << "FbRecursion(n) = " << fbRecursion(n) << endl << "FbNormal(n) = " << fbNormal(n) << endl;
	cout << "===============================" << endl;
	cout << "RtRecursion(n) = " << rtRecursion(n, 1) << endl << "RtNormal(n) = " << rtNormal(n) << endl;*/
	return 0;
}

double fbRecursion(int n) {
	if (n <= 0) return 0;
	if (n == 1) return 1;
	return fbRecursion(n - 1) + fbRecursion(n - 2);
}
double fbNormal(int n) {
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

double rtRecursion(int n, int counter) {
	if (n < 0) { return 0; }
	if (n <= counter) { return sqrt(n); }
	return sqrt(counter + rtRecursion(n, counter + 1));
}
double rtNormal(int n) {
	if (n < 0) { return 0; }
	double result = sqrt(n);
	for (int i = n - 1; i > 0; i--) {
		result = sqrt(i + result);
	}
	return result;
}

void convertRecursion(int n, int p) {
	if (n <= 0) { return; }
	convertRecursion(n/p, p);
	cout << ((n % p < 10) ? char(n % p + '0') : char(n % p - 10 + 'A'));
}

void convertNormal(int n, int p) {
	char result[255] = {};
	int i = 0;
	while(n){
		result[i++] = (n % p < 10) ? (n % p + '0') : (n % p - 10 + 'A');
		n /= p;
	}
	while(i >= 0) { cout << result[i--]; }
	cout << endl;
}