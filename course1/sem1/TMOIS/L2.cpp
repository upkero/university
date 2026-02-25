#include <iostream>
#include <ctime>
using namespace std;

class Graph {
private:
	int** graph;
	int graphLength;
	int tupleLength;

public:
	Graph() {
		graph = nullptr;
		graphLength = 0;
		tupleLength = 2;
	}
	Graph(const Graph& other) {
		this->tupleLength = 2;
		this->graphLength = other.graphLength;
		this->graph = new int* [this->graphLength];
		for (int i = 0; i < this->graphLength; i++) { this->graph[i] = new int[this->tupleLength]; }
		for (int i = 0; i < this->graphLength; i++) {
			for (int j = 0; j < this->tupleLength; j++) { this->graph[i][j] = other.graph[i][j]; }
		}
	}
	~Graph() {
		for (int i = 0; i < graphLength; i++) { delete[] graph[i]; }
		delete[] graph;
		graph = nullptr;
	}
	Graph& operator = (const Graph& other) {
		if (this == &other) return *this;
		if (graph != nullptr) {
			for (int i = 0; i < this->graphLength; i++) { delete[] this->graph[i]; }
			delete[] this->graph;
		}
		this->graphLength = other.graphLength;
		this->graph = new int* [this->graphLength];
		for (int i = 0; i < this->graphLength; i++) { this->graph[i] = new int[this->tupleLength]; }
		for (int i = 0; i < this->graphLength; i++) {
			for (int j = 0; j < this->tupleLength; j++) { this->graph[i][j] = other.graph[i][j]; }
		}
		return *this;
	}

	void addTuple(int first, int second) {
		int** temp = graph;
		for (int i = 0; i < graphLength; i++) { temp[i] = graph[i]; }
		int tempLength = graphLength;
		graphLength++;
		graph = new int* [graphLength];
		for (int i = 0; i < graphLength; i++) { graph[i] = new int[tupleLength]; }
		for (int i = 0; i < tempLength; i++) {
			for (int j = 0; j < tupleLength; j++) { graph[i][j] = temp[i][j]; }
		}
		for (int i = 0; i < tempLength; i++) { delete[] temp[i]; }
		delete[] temp;
		graph[graphLength - 1][0] = first;
		graph[graphLength - 1][1] = second;
	}

	Graph inverse() const {
		Graph temp;
		temp.graphLength = this->graphLength;
		temp.graph = new int* [temp.graphLength];
		for (int i = 0; i < temp.graphLength; i++) {
			temp.graph[i] = new int[temp.tupleLength];
		}

		for (int i = 0; i < temp.graphLength; i++) {
			temp.graph[i][0] = this->graph[i][1];
			temp.graph[i][1] = this->graph[i][0];
		}
		return temp;
	}
	Graph projection(int axis) const {
		// axis = 0 ось х , axis = 1 ось y
		Graph temp;
		int i = 0, j = 0;
		temp.graphLength = 1;
		temp.tupleLength = 0;
		temp.graph = new int* [temp.graphLength];
		temp.graph[0] = new int[this->graphLength];
		while (i < this->graphLength) {
			if (unicProj(this->graph[i][axis], temp)) {
				temp.graph[0][j] = this->graph[i][axis];
				temp.tupleLength++;
				j++;
			}
			i++;
		}
		return temp;
	}
	friend bool unicProj(int el, Graph& other) {
		for (int i = 0; i < other.tupleLength; i++) {
			if (el == other.graph[0][i]) {
				return false;
			}
		}
		return true;
	}


	Graph compose(Graph& other) {
		Graph temp;
		for (int i = 0; i < this->graphLength; i++) {
			for (int j = 0; j < other.graphLength; j++) {
				if (this->graph[i][1] == other.graph[j][0]) {
					temp.addTuple(this->graph[i][0], other.graph[j][1]);
				}
			}
		}
		return temp;
	}
	Graph* cartPr(Graph& other) {
		int length = this->graphLength * other.graphLength;
		Graph* temp = new Graph[length + 1];

		for (int i = 0, j = 0, k = 0; i < length; i++, j = i / other.graphLength, k = i % other.graphLength) {
			temp[i].addTuple(this->graph[j][0], this->graph[j][1]);
			temp[i].addTuple(other.graph[k][0], other.graph[k][1]);
		}
		temp[length].graphLength = 0;
		return temp;
	}

	friend ostream& operator << (ostream& os, const Graph& graph) {
		if (graph.graphLength != 1) { os << "{"; }
		for (int i = 0; i < graph.graphLength; i++) {
			os << "<";
			for (int j = 0; j < graph.tupleLength; j++) {
				os << graph.graph[i][j];
				if (j + 1 != graph.tupleLength) { os << ", "; }
			}
			os << ">";
			if (i != graph.graphLength - 1) { os << ", "; }
		}
		if (graph.graphLength != 1) { os << "}"; }
		return os;
	}

	friend ostream& operator << (ostream& os, const Graph* graph) {
		os << "{";
		for (int i = 0; graph[i].graphLength != 0; i++) {
			os << "<";
			for (int j = 0; j < graph[i].graphLength; j++) {
				os << "<" << graph[i].graph[j][0] << ", " << graph[i].graph[j][1] << ">";
				if (j != graph[i].graphLength - 1) { os << ", "; }
			}
			os << ">";
			if (graph[i + 1].graphLength != 0) { cout << ", "; }
		}
		os << "}";
		delete[] graph;
		return os;
	}
};

bool validateInt(int&, int&, int, int, const char*);
bool validateInt(int&, int, int, const char*);

int main(int argc, char* argv[]) {
	Graph graph1;
	Graph graph2;
#ifdef DEBUG
	srand(time(NULL));
	for (int i = 0; i < rand() % 2 + 2; i++) { graph1.addTuple(rand() % 11, rand() % 11); }
	for (int i = 0; i < rand() % 2 + 2; i++) { graph2.addTuple(rand() % 11, rand() % 11); }
#else
	int power;
	int first, second;
	cout << "Enter power of graph P: ";
	while (!validateInt(power, 2, 5, "Invalid input. Please enter number from 2 to 5: "));
	for (int i = 1; i <= power; i++) {
		cout << "Enter " << i << " tuple of graph P: ";
		while (!validateInt(first, second, 0, 10, "Invalid input. Please enter numbers from 0 to 10: "));
		graph1.addTuple(first, second);
	}
	cout << "Enter power of graph Q: ";
	while (!validateInt(power, 2, 5, "Invalid input. Please enter number from 2 to 5: "));
	for (int i = 1; i <= power; i++) {
		cout << "Enter " << i << " tuple of graph Q: ";
		while (!validateInt(first, second, 0, 10, "Invalid input. Please enter numbers from 0 to 10: "));
		graph2.addTuple(first, second);
	}
#endif
	cout << "Graph P: " << endl << "  " << graph1 << endl;
	cout << "Graph Q: " << endl << "  " << graph2 << endl;
	cout << "Graph P inversion: " << endl << "  " << graph1.inverse() << endl;
	cout << "Graph Q inversion: " << endl << "  " << graph2.inverse() << endl;
	cout << "Graph composition Q*P: " << endl << "  " << graph1.compose(graph2) << endl;
	cout << "Graph composition P*Q: " << endl << "  " << graph2.compose(graph1) << endl;
	cout << "Cartesian product of graphs PxQ: " << endl << "  " << graph1.cartPr(graph2) << endl;
	cout << "Cartesian product of graphs QxP: " << endl << "  " << graph2.cartPr(graph1) << endl;
	cout << "Graph P projection along the X axis: " << endl << "  " << graph1.projection(0) << endl;
	cout << "Graph Q projection along the X axis: " << endl << "  " << graph2.projection(0) << endl;
	cout << "Graph P projection along the Y axis: " << endl << "  " << graph1.projection(1) << endl;
	cout << "Graph Q projection along the Y axis: " << endl << "  " << graph2.projection(1) << endl;
	return 0;
}

bool validateInt(int& first, int& second, int min, int max, const char* errorMessage) {
	cin >> first;
	cin >> second;
	if (cin.fail() || !(first <= max && first >= min) || !(second <= max && second >= min)) {
		if (cin.fail()) {
			cin.clear();
		}
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << errorMessage;
		return false;
	}
	cin.ignore(numeric_limits<streamsize>::max(), '\n');
	return true;
}
bool validateInt(int& first, int min, int max, const char* errorMessage) {
	cin >> first;
	if (cin.fail() || !(first <= max && first >= min)) {
		if (cin.fail()) {
			cin.clear();
		}
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << errorMessage;
		return false;
	}
	cin.ignore(numeric_limits<streamsize>::max(), '\n');
	return true;
}