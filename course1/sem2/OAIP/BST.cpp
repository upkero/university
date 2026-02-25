#include <iostream>
#include <conio.h>
using namespace std;

template<typename keyType, typename dataType>
class BST
{
public:
	BST();
	~BST();
	int getSize() const { return size; }
	void insert(keyType key, dataType data);
	dataType getDataAt(keyType key) const;
	void deleteAt(keyType key);
	void printPreOrder() const;
	void printPostOrder() const;
	void printInOrder() const;
	int getMaxDepth() const;
	void clear();
private:
	template<typename keyType, typename dataType>
	class Node {
	public:
		Node* pLeft;
		Node* pRight;
		keyType key;
		dataType data;

		Node(keyType key = keyType(), dataType data = dataType(), Node* pLeft = nullptr, Node* pRight = nullptr) {
			this->key = key;
			this->data = data;
			this->pLeft = pLeft;
			this->pRight = pRight;
		}
	};
	int size;
	Node<keyType, dataType>* root;
	void printPreOrderRecursive(Node<keyType, dataType>* currentNode) const;
	void printPostOrderRecursive(Node<keyType, dataType>* currentNode) const;
	void printInOrderRecursive(Node<keyType, dataType>* currentNode) const;
	int getMaxDepthRecursive(Node<keyType, dataType>* currentNode) const;
	void clearRecursive(Node<keyType, dataType>*& currentNode);
};

template<typename keyType, typename dataType>
BST<keyType, dataType>::BST() {
	size = 0;
	root = nullptr;
}

template<typename keyType, typename dataType>
BST<keyType, dataType>::~BST() { clear(); }

template<typename keyType, typename dataType>
void BST<keyType, dataType>::insert(keyType key, dataType data) {
	if (size == 0) {
		root = new Node<keyType, dataType>(key, data);
		size++;
		return;
	}
	Node<keyType, dataType>* current = root;
	while (current != nullptr) {
		if (key < current->key) {
			if (current->pLeft == nullptr) {
				current->pLeft = new Node<keyType, dataType>(key, data);
				size++;
				return;
			}
			current = current->pLeft;
		}
		else if (key > current->key) {
			if (current->pRight == nullptr) {
				current->pRight = new Node<keyType, dataType>(key, data);
				size++;
				return;
			}
			current = current->pRight;
		}
		else {
			cout << "Key " << key << " already exists in the tree." << endl;
			return;
		}
	}
}

template<typename keyType, typename dataType>
dataType BST<keyType, dataType>::getDataAt(keyType key) const {
	const Node<keyType, dataType>* current = root;

	while (current != nullptr) {
		if (current->key == key) { return current->data; }
		current = (key > current->key) ? current->pRight : current->pLeft;
	}
	cout << "Key " << key << " wasn't found in the tree." << endl;
	return dataType{};
}

template<typename keyType, typename dataType>
void BST<keyType, dataType>::deleteAt(keyType key) {
	Node<keyType, dataType>* current = root;
	Node<keyType, dataType>* preCurrent = nullptr;
	bool isCurrentLeft = false;

	while (current != nullptr && current->key != key) {
		preCurrent = current;
		if (current->key > key) {
			current = current->pLeft;
			isCurrentLeft = true;
		}
		else {
			current = current->pRight;
			isCurrentLeft = false;
		}
	}

	if (current == nullptr) {
		cout << "Key " << key << " wasn't found in the tree." << endl;
		return;
	}

	if (current->pLeft != nullptr && current->pRight != nullptr) {
		Node<keyType, dataType>* replace = current->pLeft;
		Node<keyType, dataType>* preReplace = current;

		while (replace->pRight != nullptr) {
			preReplace = replace;
			replace = replace->pRight;
		}

		if (preReplace != current) {
			preReplace->pRight = replace->pLeft;
			replace->pLeft = current->pLeft;
		}
		replace->pRight = current->pRight;

		if (preCurrent == nullptr) { root = replace; }
		else if (isCurrentLeft) { preCurrent->pLeft = replace; }
		else { preCurrent->pRight = replace; }
	}
	else {
		Node<keyType, dataType>* child = (current->pLeft != nullptr) ? current->pLeft : current->pRight;
		if (preCurrent == nullptr) { root = child; }
		else if (isCurrentLeft) { preCurrent->pLeft = child; }
		else { preCurrent->pRight = child; }
	}
	delete current;
	size--;
}

template<typename keyType, typename dataType>
void BST<keyType, dataType>::printPreOrder() const {
	if (root == nullptr) {
		cout << "BST is empty" << endl;
		return;
	}
	cout << "Key: " << root->key << " Data: " << root->data << endl;
	printPreOrderRecursive(root->pLeft);
	printPreOrderRecursive(root->pRight);
}

template<typename keyType, typename dataType>
void BST<keyType, dataType>::printPreOrderRecursive(Node<keyType, dataType>* currentNode) const {
	if (currentNode == nullptr) return;
	cout << "Key: " << currentNode->key << " Data: " << currentNode->data << endl;
	printPreOrderRecursive(currentNode->pLeft);
	printPreOrderRecursive(currentNode->pRight);
}

template<typename keyType, typename dataType>
void BST<keyType, dataType>::printPostOrder() const {
	if (root == nullptr) {
		cout << "BST is empty" << endl;
		return;
	}
	printPostOrderRecursive(root);
}

template<typename keyType, typename dataType>
void BST<keyType, dataType>::printPostOrderRecursive(Node<keyType, dataType>* currentNode) const {
	if (currentNode == nullptr) return;
	printPostOrderRecursive(currentNode->pLeft);
	printPostOrderRecursive(currentNode->pRight);
	cout << "Key: " << currentNode->key << " Data: " << currentNode->data << endl;
}

template<typename keyType, typename dataType>
void BST<keyType, dataType>::printInOrder() const {
	if (root == nullptr) {
		cout << "BST is empty" << endl;
		return;
	}
	printInOrderRecursive(root);
}

template<typename keyType, typename dataType>
void BST<keyType, dataType>::printInOrderRecursive(Node<keyType, dataType>* currentNode) const {
	if (currentNode == nullptr) return;
	printInOrderRecursive(currentNode->pLeft);
	cout << "Key: " << currentNode->key << " Data: " << currentNode->data << endl;
	printInOrderRecursive(currentNode->pRight);
}

template<typename keyType, typename dataType>
int BST<keyType, dataType>::getMaxDepth() const {
	return getMaxDepthRecursive(root);
}

template<typename keyType, typename dataType>
int BST<keyType, dataType>::getMaxDepthRecursive(Node<keyType, dataType>* currentNode) const {
	if (currentNode == nullptr) return 0;

	int leftDepth = getMaxDepthRecursive(currentNode->pLeft);
	int rightDepth = getMaxDepthRecursive(currentNode->pRight);

	return max(leftDepth, rightDepth) + 1;
}

template<typename keyType, typename dataType>
void BST<keyType, dataType>::clear() {
	clearRecursive(root);
	root = nullptr;
	size = 0;
}

template<typename keyType, typename dataType>
void BST<keyType, dataType>::clearRecursive(Node<keyType, dataType>*& currentNode) {
	if (currentNode == nullptr) { return; }
	clearRecursive(currentNode->pLeft);
	clearRecursive(currentNode->pRight);
	delete currentNode;
	currentNode = nullptr;
}

int menu() {
	cout << "1. Add element to BST" << endl
		<< "2. Delete element from BST by key" << endl
		<< "3. Print PreOrder" << endl
		<< "4. Print PostOrder" << endl
		<< "5. Print InOrder" << endl
		<< "6. Get data by key" << endl
		<< "7. Get BST size" << endl
		<< "8. Get the maximum depth of BST" << endl
		<< "9. Clear BST" << endl
		<< "Any other key to exit" << endl
		<< "Please make choice: ";
	int choice;
	cin >> choice;
	return (cin.fail()) ? 0 : choice;
}

int main()
{
	using T1 = int;
	using T2 = int;
	BST<T1, T2> bst;

	T1 key;
	T2 data;
	bst.insert(50, 1);
	bst.insert(49, 1);
	bst.insert(80, 1);
	bst.insert(31, 1);
	bst.insert(44, 1);
	bst.insert(15, 1);
	bst.insert(2, 1);
	bst.insert(1, 1);
	bst.insert(100, 1);
	bst.insert(55, 1);
	bst.insert(56, 1);
	bst.insert(26, 1);
	bst.insert(6, 1);
	bst.insert(3, 1);
	bst.insert(53, 1);
	while (true) {
		switch (menu()) {
		case 1:
			cout << "Enter key: ";
			while (!(cin >> key)) {
				cin.clear();
				cin.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Error. Try again: ";
			}
			cout << "Enter data: ";
			while(!(cin >> data)) {
				cin.clear();
				cin.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Error. Try again: ";
			}
			bst.insert(key, data);
			break;

		case 2:
			cout << "Enter key to delete: ";
			while (!(cin >> key)) {
				cin.clear();
				cin.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Error. Try again: ";
			}
			bst.deleteAt(key);
			break;

		case 3: bst.printPreOrder(); break;

		case 4: bst.printPostOrder(); break;

		case 5: bst.printInOrder(); break;

		case 6:
			cout << "Enter key to get data: ";
			while (!(cin >> key)) {
				cin.clear();
				cin.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Error. Try again: ";
			}
			cout << "Data: " << bst.getDataAt(key) << endl;
			break;

		case 7:	cout << "BST size is " << bst.getSize() << endl; break;

		case 8: cout << "Max depth is " << bst.getMaxDepth() << endl; break;

		case 9:
			bst.clear();
			cout << "BST has been successfully cleared!" << endl;
			break;

		default:
			cout << "Exiting program..." << endl;
			return 0;
		}
		cout << "Press any key to continue..." << endl;
		_getch();
		system("cls");
	}
}