#include <iostream>
#include <conio.h>
using namespace std;

template<typename T>
class Stack
{
public:
	Stack();
	~Stack();
	void inStack(T data);
	void outStack();
	void clear();
	T getTop() const {
		if (top != nullptr) { return top->data; }
		else { return T{ }; }
	}
	int getSize() const { return size; }
	
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
void Stack<T>::inStack(T data) {
	top = new Node<T>(data, top);
	size++;
}

template<typename T>
void Stack<T>::outStack() {
	if (size != 0) {
		Node<T>* temp = top;
		top = temp->pPrev;
		delete temp;
		size--;
	}
}

template<typename T>
void Stack<T>::clear() {
	while (size) {
		outStack();
	}
}

void toRPN(char* inStr, char* outStr) {
	Stack<char> stack;
	int j = 0;
	int priority[50] = {0};
	priority['+'] = 1;
	priority['-'] = 1;
	priority['*'] = 2;
	priority['/'] = 2;
	for (int i = 0; inStr[i]; i++) {
		if (inStr[i] >= 'a' && inStr[i] <= 'z') { outStr[j++] = inStr[i]; }
		else if (inStr[i] == '(') { stack.inStack(inStr[i]); }
		else if (inStr[i] == ')') {
			while (stack.getTop() != '(' && stack.getSize() > 0) {
				outStr[j++] = stack.getTop();
				stack.outStack();
			}
			stack.outStack();
		}
		else if (inStr[i] == '*' || inStr[i] == '/' || inStr[i] == '-' || inStr[i] == '+') {
			while (priority[stack.getTop()] >= priority[inStr[i]] && stack.getTop() != '(' && stack.getSize() > 0) {
				outStr[j++] = stack.getTop();
				stack.outStack();
			}
			stack.inStack(inStr[i]);
		}
		else {
			cout << "Symbol \'" << inStr[i] << "\' not accounted for in RPN" << endl;
		}
	}
	while (stack.getSize() > 0) {
		outStr[j++] = stack.getTop();
		stack.outStack();
	}
	outStr[j] = '\0';
}

double calcRPN(char* rpn) {
	Stack<double> stack;
	for (int i = 0; rpn[i]; i++) {
		char ch = rpn[i];
		if (ch >= 'a' && ch <= 'z') { 
			double value;
			cout << "Enter " << ch << ": ";
			while (!(cin >> value)) {
				cin.clear();
				cin.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Error. Try again: ";
			}
			stack.inStack(value); 
		}
		else {
			double secondItem = stack.getTop(); stack.outStack();
			double firstItem = stack.getTop(); stack.outStack();
			switch (ch) {
			case'+': stack.inStack(firstItem + secondItem); break;
			case'-': stack.inStack(firstItem - secondItem); break;
			case'*': stack.inStack(firstItem * secondItem); break;
			case'/': stack.inStack(firstItem / secondItem); break;
			}
		}
	}
	return stack.getTop();
}

int main()
{
	char inStr[255] = {};
	cout << "Enter infix expression: ";
	while (!(cin >> inStr)) {
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "Error. Try again: ";
	}
	char outStr[255] = {};
	toRPN(inStr, outStr);
	cout << "Infix: " << inStr << endl;
	cout << "RPN: " << outStr << endl;
	cout << "Result: " << calcRPN(outStr) << endl;
	//-131.006
	return 0;
}

