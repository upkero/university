#include <iostream>
#include <conio.h>
#include <fstream>
#include <string>
#include <ctime>
//#define DEBUG
using namespace std;

struct Student {
private:
    char surname[25]{};
    int groupNumber;
    int* mathGrades;
    int amountOfMathGrades;
    int sumOfMathGrades;
    int* infGrades;
    int amountOfInfGrades;
    int sumOfInfGrades;
    int* physGrades;
    int amountOfPhysGrades;
    int sumOfPhysGrades;
    double avMathGrade, avPhysGrade, avInfGrade, avGrade;

    inline void calcAvGrade() {
        avGrade = (double)(sumOfMathGrades + sumOfInfGrades + sumOfPhysGrades) / (amountOfMathGrades + amountOfInfGrades + amountOfPhysGrades);
    }

public:
    Student() {
        groupNumber = 0;
        mathGrades = nullptr;
        amountOfMathGrades = 0;
        infGrades = nullptr;
        amountOfInfGrades = 0;
        physGrades = nullptr;
        amountOfPhysGrades = 0;
        avMathGrade = avPhysGrade = avInfGrade = avGrade = 0;
        sumOfMathGrades = sumOfInfGrades = sumOfPhysGrades = 0;
    }
    Student(const Student& other) {
        this->setSurname(other.surname);
        this->groupNumber = other.groupNumber;

        this->amountOfMathGrades = other.amountOfMathGrades;
        this->mathGrades = new int[this->amountOfMathGrades];
        for (int i = 0; i < this->amountOfMathGrades; i++) { this->mathGrades[i] = other.mathGrades[i]; }
        this->sumOfMathGrades = other.sumOfMathGrades;

        this->amountOfInfGrades = other.amountOfInfGrades;
        this->infGrades = new int[this->amountOfInfGrades];
        for (int i = 0; i < this->amountOfInfGrades; i++) { this->infGrades[i] = other.infGrades[i]; }
        this->sumOfInfGrades = other.sumOfInfGrades;

        this->amountOfPhysGrades = other.amountOfPhysGrades;
        this->physGrades = new int[this->amountOfPhysGrades];
        for (int i = 0; i < this->amountOfPhysGrades; i++) { this->physGrades[i] = other.physGrades[i]; }
        this->sumOfPhysGrades = other.sumOfPhysGrades;

        this->avMathGrade = other.avMathGrade;
        this->avPhysGrade = other.avPhysGrade;
        this->avInfGrade = other.avInfGrade;
        this->avGrade = other.avGrade;
    }
    ~Student() {
        delete[]mathGrades;
        delete[]infGrades;
        delete[]physGrades;
        mathGrades = nullptr;
        infGrades = nullptr;
        physGrades = nullptr;
    }

    int getGroupNumber() const { return this->groupNumber; }
    void setGroupNumber(int groupNumber) { this->groupNumber = groupNumber; }

    const char* getSurname() { return this->surname; }
    void setSurname(const char* surname) {
        for (int i = 0; this->surname[i]; i++) { this->surname[i] = '\0'; }
        for (int i = 0; i < strlen(surname); i++) { this->surname[i] = surname[i]; }
    }

    double getAvMathGrade() const { return this->avMathGrade; }
    double getAvInfGrade() const { return this->avInfGrade; }
    double getAvPhysGrade() const { return this->avPhysGrade; }

    void addMathGrade(int grade) {
        int* temp = this->mathGrades;
        mathGrades = new int[this->amountOfMathGrades + 1];
        for (int i = 0; i < amountOfMathGrades; i++) { mathGrades[i] = temp[i]; }
        delete[] temp;
        mathGrades[amountOfMathGrades++] = grade;
        sumOfMathGrades += grade;
        avMathGrade = sumOfMathGrades / amountOfMathGrades;
        calcAvGrade();
    }
    void addInfGrade(int grade) {
        int* temp = this->infGrades;
        infGrades = new int[this->amountOfInfGrades + 1];
        for (int i = 0; i < amountOfInfGrades; i++) { infGrades[i] = temp[i]; }
        delete[] temp;
        infGrades[amountOfInfGrades++] = grade;
        sumOfInfGrades += grade;
        avInfGrade = sumOfInfGrades / amountOfInfGrades;
        calcAvGrade();
    }
    void addPhysGrade(int grade) {
        int* temp = this->physGrades;
        physGrades = new int[this->amountOfPhysGrades + 1];
        for (int i = 0; i < amountOfPhysGrades; i++) { physGrades[i] = temp[i]; }
        delete[] temp;
        physGrades[amountOfPhysGrades++] = grade;
        sumOfPhysGrades += grade;
        avPhysGrade = sumOfPhysGrades / amountOfPhysGrades;
        calcAvGrade();
    }

    Student& operator = (Student& other) {
        this->setSurname(other.surname);
        this->groupNumber = other.groupNumber;

        this->amountOfMathGrades = other.amountOfMathGrades;
        delete[] this->mathGrades;
        this->mathGrades = new int[this->amountOfMathGrades];
        for (int i = 0; i < this->amountOfMathGrades; i++) { this->mathGrades[i] = other.mathGrades[i]; }
        this->sumOfMathGrades = other.sumOfMathGrades;

        this->amountOfInfGrades = other.amountOfInfGrades;
        delete[] this->infGrades;
        this->infGrades = new int[this->amountOfInfGrades];
        for (int i = 0; i < this->amountOfInfGrades; i++) { this->infGrades[i] = other.infGrades[i]; }
        this->sumOfInfGrades = other.sumOfInfGrades;

        this->amountOfPhysGrades = other.amountOfPhysGrades;
        delete[] this->physGrades;
        this->physGrades = new int[this->amountOfPhysGrades];
        for (int i = 0; i < this->amountOfPhysGrades; i++) { this->physGrades[i] = other.physGrades[i]; }
        this->sumOfPhysGrades = other.sumOfPhysGrades;

        this->avMathGrade = other.avMathGrade;
        this->avPhysGrade = other.avPhysGrade;
        this->avInfGrade = other.avInfGrade;
        this->avGrade = other.avGrade;

        return *this;
    }

    bool operator > (Student& other) {
        int cmp = strcmp(this->surname, other.surname);
        if (cmp > 0) { return true; }
        else { return false; }
    }
    bool operator < (Student& other) {
        int cmp = strcmp(this->surname, other.surname);
        if (cmp < 0) { return true; }
        else { return false; }
    }

    friend ostream& operator << (ostream& os, Student& student) {
        if (os.rdbuf() == std::cout.rdbuf()) {
            os << "Surname:\t\t" << student.surname << endl
                << "Group number:\t\t" << student.groupNumber << endl
                << "Math grades:\t\t";
            for (int i = 0; i < student.amountOfMathGrades; i++) {
                os << student.mathGrades[i];
                if (i != student.amountOfMathGrades - 1) { os << ", "; }
            }
            os << endl << "Physics grades:\t\t";
            for (int i = 0; i < student.amountOfPhysGrades; i++) {
                os << student.physGrades[i];
                if (i != student.amountOfPhysGrades - 1) { os << ", "; }
            }
            os << endl << "Informatics grades:\t";
            for (int i = 0; i < student.amountOfInfGrades; i++) {
                os << student.infGrades[i];
                if (i != student.amountOfInfGrades - 1) { os << ", "; }
            }
            os << endl << "Average grade:\t\t" << student.avGrade << endl;
        }
        else {
            os << student.surname << " " << student.groupNumber << " " << student.amountOfMathGrades << " ";
            for (int i = 0; i < student.amountOfMathGrades; i++) { os << student.mathGrades[i] << " "; }
            os << student.amountOfPhysGrades << " ";
            for (int i = 0; i < student.amountOfPhysGrades; i++) { os << student.physGrades[i] << " "; }
            os << student.amountOfInfGrades << " ";
            for (int i = 0; i < student.amountOfInfGrades; i++) { os << student.infGrades[i] << " "; }
            os << student.avMathGrade << " " << student.avPhysGrade << " " << student.avInfGrade << " " << student.avGrade
                << " " << student.sumOfMathGrades << " " << student.sumOfInfGrades << " " << student.sumOfPhysGrades << "\n";
        }
        return os;
    }
    friend istream& operator >> (istream& is, Student& student) {
        is >> student.surname >> student.groupNumber;
        is >> student.amountOfMathGrades;
        if (student.mathGrades != nullptr) { delete[] student.mathGrades; }
        student.mathGrades = new int[student.amountOfMathGrades];
        for (int i = 0; i < student.amountOfMathGrades; i++) { is >> student.mathGrades[i]; }
        is >> student.amountOfPhysGrades;
        if (student.physGrades != nullptr) { delete[] student.physGrades; }
        student.physGrades = new int[student.amountOfPhysGrades];
        for (int i = 0; i < student.amountOfPhysGrades; i++) { is >> student.physGrades[i]; }
        is >> student.amountOfInfGrades;
        if (student.infGrades != nullptr) { delete[] student.infGrades; }
        student.infGrades = new int[student.amountOfInfGrades];
        for (int i = 0; i < student.amountOfInfGrades; i++) { is >> student.infGrades[i]; }
        is >> student.avMathGrade >> student.avPhysGrade >> student.avInfGrade >> student.avGrade
            >> student.sumOfMathGrades >> student.sumOfInfGrades >> student.sumOfPhysGrades;
        return is;
    }
};

string path = "students.txt";

int menu();
void browseAllStudents();
void addStudent();
void browseСertainStudents();
void editStudent();
void deleteStudent();
void sortStudents();
bool validateSurname(char*);
bool validateInt(int&, int, int, const char*);
bool validateGrade(int&);
void quickSort(Student*, int, int);


int main(int argc, char* argv[]) {
#ifdef DEBUG
    fstream fs;
    fs.open(path, fstream::out | fstream::in | fstream::app);
    srand(time(NULL));
    for (int i = 0; i < 6; i++) {
        char surname[25]{};
        Student student;
        cin >> surname;
        student.setSurname(surname);
        student.setGroupNumber(rand() % 899999 + 100000);
        for (int i = 0; i < rand() % 15 + 5; i++) {
            student.addMathGrade(rand() % 2 + 8);
        }
        for (int i = 0; i < rand() % 15 + 5; i++) {
            student.addPhysGrade(rand() % 11);
        }
        for (int i = 0; i < rand() % 15 + 5; i++) {
            student.addInfGrade(rand() % 11);
        }
        fs << student;
    }
    fs.close();
#else
    while (true) {
        switch (menu()) {
        case 1: browseAllStudents(); break;
        case 2: addStudent(); break;
        case 3: browseСertainStudents(); break;
        case 4: editStudent(); break;
        case 5: deleteStudent(); break;
        case 6: sortStudents(); break;
        default:
            return 0;
        }
        cout << "Press any key to continue..." << endl;
        _getch();
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
    }

#endif // DEBUG
    return 0;
}

int menu() {
    cout << "Choose one of the actions: " << endl
        << " 1. Browse all students" << endl
        << " 2. Add student" << endl
        << " 3. Browse sertain* students" << endl
        << " 4. Edit student" << endl
        << " 5. Delete student" << endl
        << " 6. Sort students" << endl
        << " 7. Exit" << endl << endl
        << " *Students who passed math with average score between 8 and 9, whose surnames begin with letter A." << endl;
    int choice;
    cin >> choice;
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
    return choice;
}

void browseAllStudents() {
    fstream fs;

    try
    {
        fs.open(path, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }
    for (int i = 1; ; i++) {
        Student student;
        fs >> student;
        if (fs.eof()) { break; }
        cout << "Student " << i << ":" << endl << student << endl;
    }
    fs.close();
}
void addStudent() {
    fstream fs;

    try
    {
        fs.open(path, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }
    Student student;
    char tempChar[255]{};
    int amountOfGrades;
    int tempInt;
    cout << "Enter student surname: ";
    while (!validateSurname(tempChar));
    student.setSurname(tempChar);

    cout << "Enter group number: ";
    while (!validateInt(tempInt, 100000, 999999, "Invalid input. Please enter a six-digit number: "));
    student.setGroupNumber(tempInt);

    cout << "How many math grades you want to add: ";
    while (!validateInt(amountOfGrades, 0, 20, "Amount of grades must be positive number up to 20. Try again: "));

    cout << "Enter math grades: ";
    for (int i = 0; i < amountOfGrades; i++) {
        while (!validateGrade(tempInt));
        student.addMathGrade(tempInt);
    }

    cout << "How many physics grades you want to add: ";
    while (!validateInt(amountOfGrades, 0, 20, "Amount of grades must be positive number up to 20. Try again: "));

    cout << "Enter physics grades: ";
    for (int i = 0; i < amountOfGrades; i++) {
        while (!validateGrade(tempInt));
        student.addPhysGrade(tempInt);
    }
    cout << "How many informatics grades you want to add: ";
    while (!validateInt(amountOfGrades, 0, 20, "Amount of grades must be positive number up to 20. Try again: "));

    cout << "Enter informatics grades: ";
    for (int i = 0; i < amountOfGrades; i++) {
        while (!validateGrade(tempInt));
        student.addInfGrade(tempInt);
    }

    fs << student;
    fs.close();
}
void browseСertainStudents() {
    fstream fs;

    try
    {
        fs.open(path, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }
    for (int i = 1; ; i++) {
        Student student;
        fs >> student;
        if (fs.eof()) { break; }
        if (student.getAvMathGrade() >= 8 && student.getAvMathGrade() <= 9 && (student.getSurname())[0] == 'A') {
            cout << "Student " << i << ":" << endl << student << endl;
        }
    }
    fs.close();
}

void editStudent() {
    fstream fs;

    fstream tempfs;
    string temp = "temp.txt";
    int maxChoice = 1;
    int choice;
    int menuChoice;
    try
    {
        fs.open(path, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }
    cout << "Select student you want to edit:" << endl;
    while (true) {
        Student student;
        fs >> student;
        if (fs.eof()) { break; }
        cout << maxChoice << ".\t" << student.getSurname() << endl;
        maxChoice++;
    }
    fs.close();

    while (!validateInt(choice, 0, maxChoice, ("Invalid input. Please enter number from 1 to " + to_string(maxChoice - 1) + ": ").c_str()));

#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif

    cout << "What do you want to change?" << endl
        << " 1. Change surname" << endl
        << " 2. Change group number" << endl
        << " 3. Add math grade" << endl
        << " 4. Add physics grade" << endl
        << " 5. Add informatics grade" << endl;

    while (!validateInt(menuChoice, 0, 6, "Invalid input. Please enter number from 1 to 5: "));

    try
    {
        fs.open(path, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }

    try
    {
        tempfs.open(temp, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }

    for (int i = 1; ; i++) {
        Student student;
        char tempChar[255];
        int tempInt;
        fs >> student;
        if (fs.eof()) { break; }
        if (i == choice) {
            switch (menuChoice) {
            case 1: {
                cout << "Enter new student surname: ";
                while (!validateSurname(tempChar));
                student.setSurname(tempChar);
                break;
            }
            case 2: {
                cout << "Enter new group number: ";
                while (!validateInt(tempInt, 100000, 999999, "Invalid input. Please enter a six-digit number: "));
                student.setGroupNumber(tempInt);
                break;
            }
            case 3: {
                cout << "Enter grade: ";
                while (!validateGrade(tempInt));
                student.addMathGrade(tempInt);
                break;
            }
            case 4: {
                cout << "Enter grade: ";
                while (!validateGrade(tempInt));
                student.addPhysGrade(tempInt);
                break;
            }
            case 5: {
                cout << "Enter grade: ";
                while (!validateGrade(tempInt));
                student.addInfGrade(tempInt);
                break;
            }
            }
        }
        tempfs << student;
    }
    fs.close();
    tempfs.close();
    remove(path.c_str());
    rename(temp.c_str(), path.c_str());
    cout << "Student has been successfully edited." << endl;
}
void deleteStudent() {
    fstream fs;

    try
    {
        fs.open(path, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }

    string temp = "temp.txt";

    int maxChoice = 1;
    int choice;

    cout << "Select student you want to delete:" << endl;
    while (true) {
        Student student;
        fs >> student;
        if (fs.eof()) { break; }
        cout << maxChoice << ".\t" << student.getSurname() << endl;
        maxChoice++;
    }
    fs.close();

    while (!validateInt(choice, 0, maxChoice, ("Invalid input. Please enter number from 1 to " + to_string(maxChoice - 1) + ": ").c_str()));

    try
    {
        fs.open(path, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }

    fstream tempfs;
    try
    {
        tempfs.open(temp, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }
    for (int i = 1; ; i++) {
        Student student;
        fs >> student;
        if (fs.eof()) { break; }
        if (i != choice) {
            tempfs << student;
        }
    }
    fs.close();
    tempfs.close();

    remove(path.c_str());
    rename(temp.c_str(), path.c_str());

    cout << "Student has been successfully deleted." << endl;
}
void sortStudents() {
    fstream fs;
    try
    {
        fs.open(path, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }

    int amountOfStudents = 0;

    while (true) {
        Student student;
        fs >> student;
        if (fs.eof()) { break; }
        amountOfStudents++;
    }
    fs.close();

    try
    {
        fs.open(path, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }
    Student* list = new Student[amountOfStudents];
    for (int i = 0; ; i++) {
        Student student;
        fs >> student;
        if (fs.eof()) { break; }
        list[i] = student;
    }
    fs.close();

    quickSort(list, 0, amountOfStudents - 1);

    fstream tempfs;
    string temp = "temp.txt";
    try
    {
        tempfs.open(temp, fstream::in | fstream::out | fstream::app);
    }
    catch (const std::exception& ex)
    {
        cout << "Error while opening file: " << ex.what() << endl;
    }
    for (int i = 0; i < amountOfStudents; i++) {
        tempfs << list[i];
    }
    delete[] list;
    tempfs.close();
    remove(path.c_str());
    rename(temp.c_str(), path.c_str());
    cout << "Students have been successfully sorted." << endl;
}


bool validateSurname(char* surname) {
    cin >> surname;
    int surnameLength = strlen(surname);
    char errorMessage[] = "Surname must have length between 2 and 24, begin with letter from A to Z, and contain letters from a to z.\nTry again : ";
    if ((surnameLength > 24 || surnameLength < 2) || !(surname[0] >= 'A' && surname[0] <= 'Z')) { cout << errorMessage; return false; }
    for (int i = 1; i < surnameLength; i++) {
        if (!(surname[i] >= 'a' && surname[i] <= 'z')) {
            cout << errorMessage;
            return false;
            break;
        }
    }
    return true;
}
bool validateInt(int& value, int min, int max, const char* errorMessage) {
    if (cin.peek() != '\n') {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
    cin >> value;
    if (cin.fail() || !(value < max && value > min)) {
        if (cin.fail()) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
        cout << errorMessage;
        return false;
    }
    return true;
}
bool validateGrade(int& grade) {
    return validateInt(grade, -1, 11, "The grade must be between 0 and 10. Try again: ");
}

void quickSort(Student* array, int left, int right) {
    if (left > right) return;
    Student s = array[(left + right) / 2];
    int i = left;
    int j = right;
    while (i <= j) {
        while (array[i] < s) i++;
        while (array[j] > s) j--;
        if (i <= j) {
            Student temp = array[i];
            array[i] = array[j];
            array[j] = temp;
            i++;
            j--;
        }
    }
    quickSort(array, left, j);
    quickSort(array, i, right);
}