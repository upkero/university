#include <iostream>
#include <vector>
#include <fstream>
#include <string>

//#define DEBUG

using namespace std;

class Graph {
private:
    vector<vector<int>> matrixIncidence;
    vector<vector<int>> adjacencyList;
    vector<vector<int>> allCycles;
    int n;
    int m;
    bool isConnected;

    void convertToAdjacencyList() {
        adjacencyList.resize(n);
        for (int j = 0; j < m; j++) {
            vector<int> edge;
            for (int i = 0; i < n; i++) {
                if (matrixIncidence[i][j] == 1) {
                    edge.push_back(i);
                }
            }
            if (edge.size() == 2) {
                adjacencyList[edge[0]].push_back(edge[1]);
                adjacencyList[edge[1]].push_back(edge[0]);
            }
        }
    }

    void displayMatrixIncidence() const {
        cout << "Matrix Incidence:\n";
        for (const auto& row : matrixIncidence) {
            for (int value : row) {
                cout << value << " ";
            }
            cout << "\n";
        }
        }

    void displayAdjacencyList() const {
        cout << "Adjacency List:\n";
        for (size_t i = 0; i < adjacencyList.size(); i++) {
            cout << i << ": ";
            for (int neighbor : adjacencyList[i]) {
                cout << neighbor << " ";
            }
            cout << "\n";
        }
    }

    void dfs(int v, vector<int>& visited, int parent, vector<int>& currentCycle, vector<vector<int>>& allCycles) {
        visited[v] = 1;
        currentCycle.push_back(v);
#ifdef DEPTHDEBUG
        cout << "DFS: current vertex " << v << ", parent " << parent << "\n";
        cout << "Current cycle: ";
        for (int x : currentCycle) cout << x << " ";
        cout << "\n";
#endif
        for (int to : adjacencyList[v]) {
            if (to == parent) continue;

            if (visited[to] == 0) {
                dfs(to, visited, v, currentCycle, allCycles);
            }
            else if (visited[to] == 1) {
                auto it = find(currentCycle.begin(), currentCycle.end(), to);
                if (it != currentCycle.end()) {
                    vector<int> cycle(it, currentCycle.end());
                    allCycles.push_back(cycle);

#ifdef DEBUG
                    cout << "Cycle detected: ";
                    for (int x : cycle) cout << x << " ";
                    cout << "\n";
#endif
                }
            }
        }
        visited[v] = 2;
        currentCycle.pop_back();
    }

    bool checkCycles(vector<vector<int>>& allCycles) {
        for (size_t i = 0; i < allCycles.size(); i++) {
            for (size_t j = i + 1; j < allCycles.size(); j++) {
                int commonVertexCount = 0;
#ifdef DEPTHDEBUG
                cout << "Checking cycles " << i << " and " << j << "\n";
                cout << "Cycle " << i << ": ";
                for (int v : allCycles[i]) cout << v << " ";
                cout << "\nCycle " << j << ": ";
                for (int v : allCycles[j]) cout << v << " ";
                cout << "\n";
#endif
                for (int v1 : allCycles[i]) {
                    for (int v2 : allCycles[j]) {
                        if (v1 == v2) {
                            commonVertexCount++;
                        }
                    }
                }
                if (commonVertexCount > 1) {
#ifdef DEBUG
                    cout << "Found more than one common vertex between cycles " << i << " and " << j << "\n";
#endif
                    return false;
                }
            }
        }
        return true;
    }

public:
    Graph(const string& filename) {
        ifstream file(filename);
        if (file.is_open()) {
            file >> n >> m;
            matrixIncidence.resize(n, vector<int>(m));

            for (int i = 0; i < n; i++) {
                for (int j = 0; j < m; j++) {
                    file >> matrixIncidence[i][j];
                }
            }

            convertToAdjacencyList();

#ifdef DEBUG
            displayMatrixIncidence();
            displayAdjacencyList();
#endif

            vector<int> visited(n, 0);
            vector<int> currentCycle;

            dfs(0, visited, -1, currentCycle, allCycles);

            for (int i = 0; i < n; i++) { isConnected = visited[i] != 0; }

        }
        else {
            throw runtime_error("Unable to open file: " + filename);
        }
    }

    bool isCactus() {
        if (!isConnected) {
#ifdef  DEBUG
            cout << "Graph is not connected" << endl;
#endif
            return false;
        }

        return checkCycles(allCycles);
    }
};

int main() {
    try {
        Graph graph("graph.txt");
        if (graph.isCactus() == true) {
            cout << "===============" << endl << "Graph is cactus" << endl << "===============" << endl;
        }
        else
        {
            cout << "==================" << endl << "Graph isn't cactus" << endl << "==================" << endl;
        }
    }
    catch (const exception& e) {
        cerr << e.what() << endl;
    }

    return 0;
}