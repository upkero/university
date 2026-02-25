#include <iostream>
using namespace std;

bool unic(const int* const, const int, const int);
void fill_array(int* const, const int);
void show_array(const int* const, const int);
int* uni(const int* const, const int, const int* const, const int, int&);
int* intersec(const int* const, const int, const int* const, const int, int&);
int* diff(const int* const, const int, const int* const, const int, int&);
int* symdiff(const int* const, const int, const int* const, const int, int&);
int* comp(const int* const, const int, int&);

int main() {
	int sizeA, sizeB, tempsize;
	cout << "==========================================================" << endl;
	cout << "The universal set contains the numbers from 1 to 100." << endl;
	cout << "==========================================================" << endl;
	cout << "Enter power of set A: "; cin >> sizeA;
	cout << "Enter power of set B: "; cin >> sizeB;
	cout << "==========================================================" << endl;

	int* arrA = new int[sizeA];
	int* arrB = new int[sizeB];
	int* temparr;

	cout << "Fill in the set A." << endl;
	fill_array(arrA, sizeA);
	cout << "==========================================================" << endl;
	cout << "Fill in the set B." << endl;
	fill_array(arrB, sizeB);
	cout << "==========================================================" << endl;

	cout << "Power of set A is " << sizeA << "." << endl << "Set A = ";
	show_array(arrA, sizeA);
	cout << "\nPower of set B is " << sizeB << "." << endl << "Set B = ";
	show_array(arrB, sizeB);
	cout << "==========================================================" << endl;

	cout << "1. Union of sets A and B = ";
	temparr = uni(arrA, sizeA, arrB, sizeB, tempsize);
	show_array(temparr, tempsize);
	delete[] temparr;

	cout << "\n2. Intersection of sets A and B = ";
	temparr = intersec(arrA, sizeA, arrB, sizeB, tempsize);
	show_array(temparr, tempsize);
	delete[] temparr;

	cout << "\n3. Difference of sets A and B = ";
	temparr = diff(arrA, sizeA, arrB, sizeB, tempsize);
	show_array(temparr, tempsize);
	delete[] temparr;

	cout << "\n4. Difference of sets B and A = ";
	temparr = diff(arrB, sizeB, arrA, sizeA, tempsize);
	show_array(temparr, tempsize);
	delete[] temparr;

	cout << "\n5. Symmetric difference of sets A and B = ";
	temparr = symdiff(arrA, sizeA, arrB, sizeB, tempsize);
	show_array(temparr, tempsize);
	delete[] temparr;

	cout << "\n6. Complement of set A = ";
	temparr = comp(arrA, sizeA, tempsize);
	show_array(temparr, tempsize);
	delete[] temparr;

	cout << "\n7. Complement of set B = ";
	temparr = comp(arrB, sizeB, tempsize);
	show_array(temparr, tempsize);
	delete[] temparr;

	cout << "==========================================================" << endl;

	delete[] arrA;
	delete[] arrB;
	return 0;
}

bool unic(const int* const arr, const int size, const int el) {
	for (int i = 0; i < size; i++) {
		if (el == arr[i]) {
			return false;
		}
	}
	return true;
}

void fill_array(int* const arr, const int size) {
	int item;
	for (int i = 0; i < size; i++) {
		cout << "Enter " << i + 1 << " item of set: "; cin >> item;
		if (unic(arr, i, item) && item > 0 && item < 101) {
			arr[i] = item;
		}
		else {
			cout << "This item is already in the set or isn't in the range from 1 to 100." << endl;
			i--;
		}
	}
}
void show_array(const int* const arr, const int size) {
	cout << "{";
	for (int i = 0; i < size; i++) {
		cout << arr[i];
		if (i < size - 1) {
			cout << ", ";
		}
	}
	cout << "}" << endl;
}

int* uni(const int* const arr1, const int size1, const int* const arr2, const int size2, int &tempsize) {
	int x = 0, counter = 0;
	for (int i = 0; i < size2; i++) {
		if (unic(arr1, size1, arr2[i])) x++;
	}
	tempsize = size1 + x;
	int* newarr = new int[tempsize];
	for (int i = 0; i < size1; i++, counter++) {
		newarr[counter] = arr1[counter];
	}
	for (int i = 0; i < size2; i++) {
		if (unic(arr1, size1, arr2[i])) {
			newarr[counter] = arr2[i];
			counter++;
		}
	}
	return newarr;
}
int* intersec(const int* const arr1, const int size1, const int* const arr2, const int size2, int& tempsize) {
	tempsize = 0;
	for (int i = 0; i < size2; i++) {
		if (!unic(arr1, size1, arr2[i])) tempsize++;
	}
	int* newarr = new int[tempsize];
	for (int i = 0, j = 0; i < size2; i++) {
		if (!unic(arr1, size1, arr2[i])) {
			newarr[j] = arr2[i];
			j++;
		}
	}
	return newarr;
}
int* diff(const int* const arr1, const int size1, const int* const arr2, const int size2, int& tempsize) {
	tempsize = 0;
	for (int i = 0; i < size1; i++) {
		if (unic(arr2, size2, arr1[i])) tempsize++;
	}
	int* newarr = new int[tempsize];
	for (int i = 0, j = 0; i < size1; i++) {
		if (unic(arr2, size2, arr1[i])) {
			newarr[j] = arr1[i];
			j++;
		}
	}
	return newarr;
}
int* symdiff(const int* const arr1, const int size1, const int* const arr2, const int size2, int& tempsize) {
	int counter = 0;
	tempsize = 0;
	for (int i = 0; i < size1; i++) {
		if (unic(arr2, size2, arr1[i])) tempsize++;
	}
	for (int i = 0; i < size2; i++) {
		if (unic(arr1, size1, arr2[i])) tempsize++;
	}
	int* newarr = new int[tempsize];
	for (int i = 0; i < size1; i++) {
		if (unic(arr2, size2, arr1[i])) {
			newarr[counter] = arr1[i];
			counter++;
		}
	}
	for (int i = 0; i < size2; i++) {
		if (unic(arr1, size1, arr2[i])) {
			newarr[counter] = arr2[i];
			counter++;
		}
	}
	return newarr;
}
int* comp(const int* const arr, const int size, int& tempsize) {
	int unisize = 100;
	int* universal = new int[unisize];
	for (int i = 0; i < unisize; i++) {
		universal[i] = i + 1;
	}
	tempsize = unisize - size;
	int* newarr = new int[tempsize];
	for (int i = 0, j = 0; i < unisize; i++) {
		if (unic(arr, size, universal[i])) {
			newarr[j] = universal[i];
			j++;
		}
	}
	delete[] universal;
	return newarr;
}