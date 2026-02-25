#include <iostream>
#include <ctime>
using namespace std;

void show_array(const int* const, const int);
void fill_array(int* const, const int);
void sort(int* const, const int);

int main() {
	int size;

	cout << "Enter array size: "; cin >> size;

	int* arr = new int[size];

	/*for (int i = 0; i < size; i++) {
		cout << "Enter arr[" << i << "] = "; cin >> arr[i];
	}*/

	fill_array(arr, size);
	show_array(arr, size);
	sort(arr, size);
	show_array(arr, size);

	delete[] arr;
	return 0;
}

void show_array(const int* const arr, const int size) {
	cout << "Your array:\t";
	for (int i = 0; i < size; i++) {
		cout << arr[i] << " ";
	}
	cout << endl;
}

void fill_array(int* const arr, const int size) {
	srand(time(NULL));
	for (int i = 0; i < size; i++) {
		arr[i] = rand() % 20 - 10;
	}
}

void sort(int* const arr, const int size) {
	int temp;
	for (int i = 0, evencounter = 0, oddcounter = 0; i < size; i++) {
		if (arr[i] < 0 && arr[i] % -2 == 0) {
			for (int k = i; evencounter < k; k--) {
				temp = arr[k - 1];
				arr[k - 1] = arr[k];
				arr[k] = temp;
			}
			evencounter++;
			oddcounter++;
		}
		else {
			if (arr[i] < 0) {
				for (int k = i; oddcounter < k; k--) {
					temp = arr[k - 1];
					arr[k - 1] = arr[k];
					arr[k] = temp;
				}
				oddcounter++;
			}
		}
	}
}