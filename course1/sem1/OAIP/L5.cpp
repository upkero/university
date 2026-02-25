#include <iostream>
#include <ctime>
#include <iomanip>
using namespace std;

void fillArray(int** const, const int, const int);
void fillArrayManualy(int** const, const int, const int);
void showArray(int** const, const int, const int);
double calcAM(int** const, const int, const int);
int calcSum(int** const, const int, const int);
//void rotate(int**&, const int);

int main() {
	int n, m;
	cout << "Enter value of n: "; cin >> n;
	cout << "Enter value of m: "; cin >> m;

	int** arr = new int* [n];
	for (int i = 0; i < n; i++) {
		arr[i] = new int[m];
	}

	fillArrayManualy(arr, n, m);
	showArray(arr, n, m);
	cout << "Arithmetic mean of numbers after main diagonal: " << calcAM(arr, n, m) << endl;
	cout << "Sum of numbers before side diagonal: " << calcSum(arr, n, m) << endl;
	
	for (int i = 0; i < n; i++) {
		delete[] arr[i];
	}
	delete[] arr;
	arr = NULL;

	return 0;
}
void fillArray(int** const arr, const int n, const int m) {
	srand(time(NULL));
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			arr[i][j] = rand() % 21 - 10;
		}
	}
}
void fillArrayManualy(int** const arr, const int n, const int m) {
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			cout << "Enter [" << i << "][" << j << "] element of matrix: "; cin >> arr[i][j];
		}
	}
}
void showArray(int** const arr, const int n, const int m) {
	cout << "Your array:" << endl;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			cout << setw(4) << arr[i][j];
		}
		cout << endl;
	}
}
double calcAM(int** const arr, const int n, const int m) {
	double sum = 0;
	int amount = 0;
	for (int row = 0; row < n; row++) {
		for (int col = row; col < m; col++) {
			sum += arr[row][col];
			amount++;
		}
	}
	return sum / amount;
}
int calcSum(int** const arr, const int n, const int m) {
	double sum = 0;
	for (int row = n - 1, num = 0; num < n; row--, num++) {
		for (int col = num > m - 1 ? m - 1 : num; col >= 0; col--) {
			sum += arr[row][col]; 
		}
	}
	return sum;
}
//void rotate(int**& arr, const int n) {
//
//	int** newarr = new int* [n];
//	for (int i = 0; i < n; i++) {
//		newarr[i] = new int[n];
//	}
//
//	for (int j = 0; j < n; j++) {
//		for (int i = 0, k = n - 1; i < n; k--, i++) {
//			newarr[j][i] = arr[k][j];
//		}
//	}
//
//	for (int i = 0; i < n; i++) {
//		delete[] arr[i];
//	}
//	delete[] arr;
//
//	arr = newarr;
//
//	newarr = NULL;
//}