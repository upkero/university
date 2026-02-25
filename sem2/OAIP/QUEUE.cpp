#include <iostream>
#include <conio.h>
using namespace std;

template<typename T>
class Queue
{
public:
	Queue();
	~Queue();
	void outBeginQueue();
	void outEndQueue();
	void inBeginQueue(T data);
	void inEndQueue(T data);
	void clear();
	int getSize() const { return size; }
	T getBegin() const {
		if (begin != nullptr) { return begin->data; }
		else { return T{ }; }
	}
	T getEnd() const {
		if (end != nullptr) { return end->data; }
		else { return T{}; }
	}
	void showQueue() const;
	void swap();
	void sortByParity();
private:

	template<typename T>
	class Node {
	public:
		Node* pPrev;
		Node* pNext;
		T data;

		Node(T data = T(), Node* pNext = nullptr, Node* pPrev = nullptr) {
			this->data = data;
			this->pPrev = pPrev;
			this->pNext = pNext;
		}
	};
	int size;
	Node<T>* begin;
	Node<T>* end;
};

template<typename T>
Queue<T>::Queue() {
	size = 0;
	begin = nullptr;
	end = nullptr;
}

template<typename T>
Queue<T>::~Queue() {
	clear();
}

template<typename T>
void Queue<T>::inBeginQueue(T data) {
	Node<T>* temp = begin;
	begin = new Node<T>(data, nullptr, temp);
	if (size == 0) { end = begin; }
	if (temp != nullptr) { temp->pNext = begin; }
	size++;
}

template<typename T>
void Queue<T>::inEndQueue(T data) {
	Node<T>* temp = end;
	end = new Node<T>(data, temp);
	if (size == 0) { begin = end; }
	if (temp != nullptr) { temp->pPrev = end; }
	size++;
}

template<typename T>
void Queue<T>::outBeginQueue() {
	Node<T>* temp = begin;
	begin = temp->pPrev;
	if (size == 1) { end = nullptr; }
	if (size != 1) { begin->pNext = nullptr; }
	delete temp;
	size--;
}

template<typename T>
void Queue<T>::outEndQueue() {
	Node<T>* temp = end;
	end = end->pNext;
	if (size == 1) { begin = nullptr; }
	if (size != 1) { end->pPrev = nullptr; }
	delete temp;
	size--;
}

template<typename T>
void Queue<T>::clear() {
	while (size) {
		outBeginQueue();
	}
}

template<typename T>
void Queue<T>::showQueue() const {
	if (size == 0) {
		cout << "Queue is empty!" << endl;
		return;
	}
	Node<T>* current = begin;
	while (current != nullptr) {
		cout << current->data;
		if (current->pPrev != nullptr) { cout << " <- "; }
		current = current->pPrev;
	}
	cout << endl;
}

template<typename T>
void Queue<T>::swap()
{
	if (size < 2) { return; }
	if (size == 2) {
		Node<T>* temp = begin;

		begin = end;
		end = temp;

		begin->pPrev = end;
		begin->pNext = nullptr;

		end->pPrev = nullptr;
		end->pNext = begin;
	}
	else {
		Node<T>* tempEnd = end;
		Node<T>* tempPrevious = end->pNext;

		end = begin;
		begin = tempEnd;

		begin->pPrev = end->pPrev;
		end->pPrev->pNext = begin;
		begin->pNext = nullptr;

		end->pPrev = nullptr;
		end->pNext = tempPrevious;
		tempPrevious->pPrev = end;
	}
}

template<typename T>
void Queue<T>::sortByParity() {
	if (size <= 1) { return; }
	Node<T>* current = end;
	Node<T>* afterCurrent = current->pNext;
	for (int i = size; i > 0; i--) {
		if (current->data % 2 == 0) {
			if (current->pPrev != nullptr) { current->pPrev->pNext = current->pNext; }
			else { end = current->pNext; }
			current->pNext->pPrev = current->pPrev;
			current->pNext = nullptr;
			current->pPrev = begin;
			begin->pNext = current;
			begin = current;
		}
		current = afterCurrent;
		afterCurrent = current->pNext;
	}
}

int menu() {
	cout << "1. Add element in begin of queue" << endl
		<< "2. Add element in end of queue" << endl
		<< "3. Delete first element from queue" << endl
		<< "4. Delete last element from queue" << endl
		<< "5. Show first element of queue" << endl
		<< "6. Show last element of queue" << endl
		<< "7. Swap first and last elements" << endl
		<< "8. Sort queue by parity" << endl
		<< "9. Show queue" << endl
		<< "10. Get queue size" << endl
		<< "11. Clear queue" << endl
		<< "Any key to exit" << endl
		<< "Please make choice: ";
	int choice;
	cin >> choice;
	return (cin.fail()) ? 0 : choice;
}

int main()
{
	using T = int;
	Queue<T> queue;
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
			queue.inBeginQueue(element);
			break;
		case 2:
			cout << "Enter element: ";
			while (!(cin >> element)) {
				cin.clear();
				cin.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Error. Try again: ";
			}
			queue.inEndQueue(element);
			break;
		case 3:
			queue.outBeginQueue();
			cout << "First element has been successfully deleted!" << endl;
			break;
		case 4:
			queue.outEndQueue();
			cout << "Last element has been successfully deleted!" << endl;
			break;
		case 5:
			cout << "First element is " << queue.getBegin() << endl;
			break;
		case 6:
			cout << "Last element is " << queue.getEnd() << endl;
			break;
		case 7:
			queue.swap();
			cout << "First and last elements has been successfully swaped!" << endl;
			break;
		case 8:
			queue.sortByParity();
			cout << "Queue has been successfully sorted by parity!" << endl;
			break;
		case 9:
			queue.showQueue();
			break;
		case 10:
			cout << "Queue size is " << queue.getSize() << endl;
			break;
		case 11:
			queue.clear();
			cout << "Queue has been successfully cleared!" << endl;
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