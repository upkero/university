#include <iostream>
#include <conio.h>
using namespace std;

template<typename T>
class Stack
{
public:
	Stack();
	Stack(const Stack& other);
	~Stack();
	void outStack();
	void inStack(T data);
	void clear();
	int getSize() const { return size; }
	T getTop() const {
		if (top != nullptr) { return top->data; }
		else { return T{ }; }
	}
	void showStack() const;
	void swap();
	void deleteBetweenZeros();
private:

	template<typename T>
	class Node {
	public:
		Node* pPrev;
		T data;

		Node(T data = T(), Node* pPrev = nullptr) {
			this->data = data;
			this->pPrev = pPrev;
		}
	};
	int size;
	Node<T>* top;
};

template<typename T>
Stack<T>::Stack() {
	size = 0;
	top = nullptr;
}

template<typename T>
Stack<T>::~Stack() {
	clear();
}

template<typename T>
Stack<T>::Stack(const Stack& other) {
	size = 0;
	top = nullptr;
	Node<T>* current = other.top;
	while (current != nullptr) {
		inStack(current->data);
		current = current->pPrev;
	}
}

template<typename T>
void Stack<T>::outStack() {
	if (size != 0) {
		Node<T>* temp = top;
		top = top->pPrev;
		delete temp;
		size--;
	}
}

template<typename T>
void Stack<T>::inStack(T data) {
	top = new Node<T>(data, top);
	size++;
}

template<typename T>
void Stack<T>::clear() {
	while (size) {
		outStack();
	}
}

template<typename T>
void Stack<T>::showStack() const {
	if (size == 0) {
		cout << "Stack is empty!" << endl;
		return;
	}
	Node<T>* current = top;
	while (current != nullptr) {
		cout << current->data;
		if (current->pPrev != nullptr) { cout << " -> "; }
		current = current->pPrev;
	}
	cout << endl;
}

template<typename T>
void Stack<T>::swap() {
	if (size < 2) { return; }
	if (size == 2) {
		Node<T>* first = top;
		Node<T>* second = top->pPrev;
		top = second;
		second->pPrev = first;
		first->pPrev = nullptr;
	}
	else {
		Node<T>* first = top;
		Node<T>* last = top;
		Node<T>* previous = nullptr;
		while (last->pPrev != nullptr) {
			previous = last;
			last = last->pPrev;
		}
		top = last;
		last->pPrev = first->pPrev;
		first->pPrev = nullptr;
		previous->pPrev = first;
	}
}

template<typename T>
void Stack<T>::deleteBetweenZeros() {
	Node<T>* current = top;
	while (current != nullptr) {
		if (current->data == 0) {
			Node<T>* check = current->pPrev;
			bool isThereOtherZero = false;
			while (check != nullptr) {
				if (check->data == 0) { 
					isThereOtherZero = true; 
					break; 
				}
				check = check->pPrev;
			}
			if (isThereOtherZero) {
				if (current->pPrev != check) {
					Node<T>* nodeForDelete = current->pPrev;
					Node<T>* afterNodeForDelete = nodeForDelete->pPrev;
					current->pPrev = check;
					while (nodeForDelete != check) {
						delete nodeForDelete;
						size--;
						nodeForDelete = afterNodeForDelete;
						afterNodeForDelete = nodeForDelete->pPrev;
					}
				}
				current = check;
			}
		}
		current = current->pPrev;
	}
}

int menu() {
	cout << "1. Add element in stack" << endl
		<< "2. Delete last element from stack" << endl
		<< "3. Show last element of stack" << endl
		<< "4. Swap first and last elements" << endl
		<< "5. Delete elements between zeros" << endl
		<< "6. Show stack" << endl
		<< "7. Get stack size" << endl
		<< "8. Clear stack" << endl
		<< "Any key to exit" << endl
		<< "Please make choice: ";
	int choice;
	cin >> choice;
	return (cin.fail()) ? 0 : choice;
}

int main()
{
	using T = int;
	Stack<T> stack;
	T element;
	while (true) {
		switch (menu())
		{
		case 1:
			cout << "Enter element: ";
			while (!(cin >> element)) {
				cin.clear();
				cin.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Error. Try again: ";
			}
			stack.inStack(element);
			break;
		case 2:
			stack.outStack();
			cout << "Last element has been successfully deleted!" << endl;
			break;
		case 3:
			cout << "Last element is " << stack.getTop() << endl;
			break;
		case 4:
			stack.swap();
			cout << "First and last elements has been successfully swaped!" << endl;
			break;
		case 5:
			stack.deleteBetweenZeros();
			cout << "Elements between zeros have been successfully removed!" << endl;
			break;
		case 6:
			stack.showStack();
			break;
		case 7:
			cout << "Stack size is " << stack.getSize() << endl;
			break;
		case 8:
			stack.clear();
			cout << "Stack has been successfully cleared!" << endl;
			break;
		default:
			return 0;
		}
		cout << "Press any key to continue..";
		_getch();

		system("cls");
	}
	return 0;
}

