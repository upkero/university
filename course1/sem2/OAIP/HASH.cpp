#include <iostream>
using namespace std;

class Hash {
public:
	void insert(const char* surname, const char* address, int phoneNumber) {
		if (!isInTable(phoneNumber)) {
			if (table[hashFunc(phoneNumber)] == nullptr) {
				table[hashFunc(phoneNumber)] = new Node(surname, address, phoneNumber);
			}
			else {
				Node* current = table[hashFunc(phoneNumber)];
				while (current->pNext != nullptr) { current = current->pNext; }
				current->pNext = new Node(surname, address, phoneNumber);
			}
		}
		else { cout << "Element already in the table" << endl; }
	}
	void find(int phoneNumber) {
		Node* current = table[hashFunc(phoneNumber)];
		while (current != nullptr && current->phoneNumber != phoneNumber) { current = current->pNext; }
		if (current != nullptr) {
			cout << "Surname: " << current->surname << endl << "Address: " << current->address << endl << "Phone number: " << current->phoneNumber << endl;
		}
		else {
			cout << "Element with this key wasnt found";
		}
	}
	~Hash() {
		for (int i = 0; i < TABLE_SIZE; i++) {
			if (table[i] != nullptr) {
				Node* current = table[i];
				Node* afterCurrent = current->pNext;
				while (afterCurrent != nullptr) {
					delete current;
					current = afterCurrent;
					afterCurrent = current->pNext;
				}
			}
		}
	}
private:
	class Node {
	public:
		char surname[26]{};
		char address[50]{};
		int phoneNumber;
		Node* pNext;
		Node(const char* surname, const char* address, int phoneNumber) {
			strcpy_s(this->surname, surname);
			strcpy_s(this->address, address);
			this->phoneNumber = phoneNumber;
			this->pNext = nullptr;
		}
	};
	static const int TABLE_SIZE = 10;
	Node* table[TABLE_SIZE] = { nullptr };
	int hashFunc(int phoneNumber) {
		int sum = 0;
		while (phoneNumber > 0) {
			sum += phoneNumber % 10;
			phoneNumber /= 10;
		}
		return sum % TABLE_SIZE;
	}
	bool isInTable(int key) {
		Node* current = table[hashFunc(key)];
		while (current != nullptr && current->phoneNumber != key) { current = current->pNext; }
		if (current != nullptr) {
			return true;
		}
		else {
			return false;
		}
	}
};
const int Hash::TABLE_SIZE;


int main() {
	Hash hash;
	hash.insert("Petrov", "Platonava st. 3", 5692312);
	hash.insert("Ivanov", "Kolesnikova st. 69", 8573234);
	hash.insert("Borisov", "Botanicheskaya st. 40", 6678833);
	hash.insert("Harmoshkin", "Semashko st. 6", 9980123);
	hash.insert("Kilkin", "Pushkina av. 55", 1230909);
	hash.insert("Savushkin", "Ulianovskaya st. 89", 5671234);
	hash.insert("Malishev", "Pobediteley av. 45", 6641209);
	hash.insert("Johnson", "Timiriazeva st. 56", 5036617);
	hash.insert("Barabulkin", "Odzincova st. 46", 1091287);

	hash.find(9980123);
	return 0;
}