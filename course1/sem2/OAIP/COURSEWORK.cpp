#include <conio.h>
#include <cstdio>
#include <iostream>
#define DEBUG
using namespace std;

class CarRepairSystem {
public:
	CarRepairSystem(const char* recordsPath);
	~CarRepairSystem();

	void start();
#ifdef DEBUG
	void randomFill(int amount);
#endif

private:
	enum class RepairType {
		Maintenance,          // ТО
		BodyRepair,           // кузовной ремонт
		PartsReplacement,     // замена деталей
		EngineRepair,         // ремонт двигателя
		ElectricalRepair,     // ремонт электрики
		BrakeSystemRepair,    // ремонт тормозной системы
		Other                 // другое
	};

	static const int AMOUNT_OF_REPAIR_TYPES;
	static const char* repairTypeStrings[];

	class RepairDate {
	public:
		int day;
		int month;
		int year;
		bool operator > (RepairDate other);
		bool operator < (RepairDate other);
	};

	class RepairRecord {
	public:
		char brand[25]{};
		char model[25]{};
		RepairType repairType;
		int repairCost;
		int mileage;
		RepairDate repairDate;

		RepairRecord(const char* brand = "", const char* model = "", RepairType repairType = {}, int repairCost = 0, int mileage = 0, RepairDate repairDate = {});
		void printRepairRecord(bool isFirst = false) const;
		void toString(char* buffer);
	};

	char recordsPath[255]{};
	int recordsCount;


	void readRepairRecords();
	void addRepairRecord();
	void editRepairRecord();
	void deleteRepairRecord();
	void modifyRepairRecord(bool isDelete);

	void linearSearchByModel(const char* model);
	void binarySearchByRepairCost(int repairCost);
	void searchByBrandAndMaxCost(const char* brand, int maxCost);

	void quickSortByRepairDate();
	void selectionSortByMileage();
	void insertionSortByRepairCost();

	void repairStats();
	void displayRepairsByType();
	void findMostExpensiveAndCheapestRepair();

	int startMenu();
	int editMenu();
	void fieldsEdit(RepairRecord& record);
	RepairType selectRepairType();

	RepairRecord* loadFromFile() const;
	void saveToFile(RepairRecord* list) const;
	void saveReportToFile(const char* content);

	void quickSort(RepairRecord* list, int left, int right);
	void selectionSort(RepairRecord* list);
	void insertionSort(RepairRecord* list);

	bool validateStr(char* buffer, int type, int minLen, int maxLen, const char* errorMsg);
	void getValidatedString(const char* prompt, char* buffer, int type, int minLen, int maxLen, const char* errorMsg);
	bool validateInt(int& value, int min, int max, const char* errorMsg);
	void getValidatedInt(const char* prompt, int& value, int min, int max, const char* errorMsg);
};

const int CarRepairSystem::AMOUNT_OF_REPAIR_TYPES = 7;

const char* CarRepairSystem::repairTypeStrings[CarRepairSystem::AMOUNT_OF_REPAIR_TYPES] = {
		"Maintenance", "Body Repair", "Parts Replacement", "Engine Repair",
		"Electrical Repair", "Brake System Repair", "Other"
};

CarRepairSystem::CarRepairSystem(const char* recordsPath) {
	strcpy_s(this->recordsPath, sizeof(this->recordsPath), recordsPath);

	FILE* recordsFile = nullptr;
	if (fopen_s(&recordsFile, recordsPath, "rb") || recordsFile == nullptr) {
		recordsCount = 0;
		return;
	}

	fseek(recordsFile, 0, SEEK_END);
	long recordsFileSize = ftell(recordsFile);
	fclose(recordsFile);

	if (recordsFileSize < 0) { recordsCount = 0; }
	else { recordsCount = recordsFileSize / sizeof(RepairRecord); }
}

CarRepairSystem::~CarRepairSystem() {

}

void CarRepairSystem::start() {
	char tempStr[25]{};
	int tempInt;
	while (true) {
		tempInt = 0;
		for (int i = 0; tempStr[i]; i++) { tempStr[i] = '\0'; }
		switch (startMenu()) {
		case 1: readRepairRecords(); break;
		case 2: addRepairRecord(); break;
		case 3: editRepairRecord(); break;
		case 4: deleteRepairRecord(); break;
		case 5: 
			getValidatedString("Enter car model: ", tempStr, 1, 2, 24, "Car model must have length between 2 and 24, contain numbers from 0 to 9, letters from a to z and A to Z and space.\nTry again: ");
			linearSearchByModel(tempStr);
			break;
		case 6:
			getValidatedInt("Enter repair cost in dollars: ", tempInt, 1, 1000000, "Repair cost must be a number between 1 and 1000000.\nTry again: ");
			binarySearchByRepairCost(tempInt);
			break;
		case 7:
			getValidatedString("Enter car brand: ", tempStr, 0, 3, 24, "Car brand must have length between 3 and 24, contain letters from a to z and A to Z.\nTry again: ");
			getValidatedInt("Enter max repair cost in dollars: ", tempInt, 1, 1000000, "Repair cost must be a number between 1 and 1000000.\nTry again: ");
			searchByBrandAndMaxCost(tempStr, tempInt);
			break;
		case 8: quickSortByRepairDate(); break;
		case 9: selectionSortByMileage(); break;
		case 10: insertionSortByRepairCost(); break;
		case 11: repairStats(); break;
		default:
			return;
		}
		cout << "Press any key to continue..";
		_getch();
		system("cls");
	}
}

void CarRepairSystem::addRepairRecord() {
	FILE* recordsFile;
	if (fopen_s(&recordsFile, recordsPath, "ab")) {
		cout << "Error opening records file." << endl;
		return;
	}
	char tempBrand[25]{};
	char tempModel[25]{};
	RepairType tempRepairType;
	int tempRepairCost;
	int tempMileage;
	RepairDate tempRepairDate = {};

	getValidatedString("Enter car brand: ", tempBrand, 0, 3, 24, "Car brand must have length between 3 and 24, contain letters from a to z and A to Z.\nTry again: ");
	getValidatedString("Enter car model: ", tempModel, 1, 2, 24, "Car model must have length between 2 and 24, contain numbers from 0 to 9, letters from a to z and A to Z and space.\nTry again: ");
	tempRepairType = selectRepairType();
	getValidatedInt("Enter repair cost in dollars: ", tempRepairCost, 1, 1000000, "Repair cost must be a number between 1 and 1000000.\nTry again: ");
	getValidatedInt("Enter mileage in kilometers: ", tempMileage, 1, 5000000, "Mileage must be a number between 1 and 5000000.\nTry again: ");
	cout << "Enter date of repair:\n";
	getValidatedInt("Day: ", tempRepairDate.day, 1, 31, "Day must be a number between 1 and 31.\nTry again: ");
	getValidatedInt("Month: ", tempRepairDate.month, 1, 12, "Month must be a number between 1 and 12.\nTry again: ");
	getValidatedInt("Year: ", tempRepairDate.year, 1900, 2100, "Year must be a number between 1900 and 2100.\nTry again: ");
	cin.ignore(numeric_limits<streamsize>::max(), '\n');
	cin.clear();

	RepairRecord tempRecord(tempBrand, tempModel, tempRepairType, tempRepairCost, tempMileage, tempRepairDate);
	
	char reportContent[512]{};
	strcat_s(reportContent, sizeof(reportContent), "Added record :\n");
	char recordStr[256]{};
	tempRecord.toString(recordStr);
	strcat_s(reportContent, sizeof(reportContent), recordStr);
	saveReportToFile(reportContent);

	fwrite(&tempRecord, sizeof(RepairRecord), 1, recordsFile);
	cout << "Repair record added successfully." << endl;
	recordsCount++;
	fclose(recordsFile);
}

void CarRepairSystem::readRepairRecords() {
	FILE* recordsFile;
	if (fopen_s(&recordsFile, recordsPath, "rb")) {
		cout << "Error opening records file." << endl;
		return;
	}

	RepairRecord tempRecord;
	fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile);
	tempRecord.printRepairRecord(true);
	while (fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile)) { tempRecord.printRepairRecord(); }
	saveReportToFile("User has viewed all repair records.\n");

	fclose(recordsFile);
}

void CarRepairSystem::editRepairRecord() {
	modifyRepairRecord(false);
}

void CarRepairSystem::deleteRepairRecord() {
	modifyRepairRecord(true);
}

void CarRepairSystem::linearSearchByModel(const char* model) {
	FILE* recordsFile;

	if (fopen_s(&recordsFile, recordsPath, "rb")) {
		cout << "Error opening records file." << endl;
		return;
	}

	RepairRecord tempRecord;
	bool isFound = false;
	bool isFirst = true;
	char reportContent[10000]{};
	strcat_s(reportContent, sizeof(reportContent), "Linear search by model ");
	strcat_s(reportContent, sizeof(reportContent), model);
	strcat_s(reportContent, sizeof(reportContent), ":\n");

	while (fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile)) {
		if (strcmp(tempRecord.model, model) == 0) {
			if (isFirst) cout << "Found records: " << endl;
			tempRecord.printRepairRecord(isFirst);

			char recordStr[256];
			tempRecord.toString(recordStr);
			strcat_s(reportContent, sizeof(reportContent), recordStr);

			isFound = true;
			isFirst = false;
		}
	}
	
	if (!isFound) {
		cout << "Records not found." << endl;
		strcat_s(reportContent, sizeof(reportContent), "Records not found.\n");
	}
	saveReportToFile(reportContent);
	fclose(recordsFile);
}

void CarRepairSystem::binarySearchByRepairCost(int repairCost) {
	insertionSortByRepairCost();
	cout << "File was sorted by repair cost for binary search." << endl;

	FILE* recordsFile;

	if (fopen_s(&recordsFile, recordsPath, "rb")) {
		cout << "Error opening records file." << endl;
		return;
	}

	int left = 0;
	int right = recordsCount - 1;
	int mid;
	RepairRecord tempRecord;
	bool isFound = false;

	while (left <= right) {
		mid = left + (right - left) / 2;
		fseek(recordsFile, mid * sizeof(RepairRecord), SEEK_SET);
		fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile);

		if (tempRecord.repairCost > repairCost) { right = mid - 1; }
		else if (tempRecord.repairCost < repairCost) { left = mid + 1; }
		else {
			isFound = true;
			break;
		}
	}
	if (!isFound) {
		cout << "Records not found." << endl;
		fclose(recordsFile);
		saveReportToFile("Binary search with repair cost:\nRecords not found.\n");
		return;
	}
	int first = mid;
	int last = mid;

	while (first > 0) {
		fseek(recordsFile, (first - 1) * sizeof(RepairRecord), SEEK_SET);
		fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile);
		if (tempRecord.repairCost == repairCost) { first--; }
		else { break; }
	}
	while (last < recordsCount - 1) {
		fseek(recordsFile, (last + 1) * sizeof(RepairRecord), SEEK_SET);
		fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile);
		if (tempRecord.repairCost == repairCost) { last++; }
		else { break; }
	}
	char reportContent[10000] = "Binary search with repair cost $"; 
	char tempBuffer[32]{};
	sprintf_s(tempBuffer, sizeof(tempBuffer), "%d", repairCost);
	strcat_s(reportContent, sizeof(reportContent), tempBuffer);
	strcat_s(reportContent, sizeof(reportContent), ":\n");
	
	cout << "Found records with repair cost $" << repairCost << ":" << endl;
	for (int i = first; i <= last; i++) {
		fseek(recordsFile, i * sizeof(RepairRecord), SEEK_SET);
		fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile);
		tempRecord.printRepairRecord(i == first);
		char recordStr[256];
		tempRecord.toString(recordStr);
		strcat_s(reportContent, sizeof(reportContent), recordStr);
	}
	fclose(recordsFile);
	saveReportToFile(reportContent);
}

void CarRepairSystem::searchByBrandAndMaxCost(const char* brand, int maxCost) {
	FILE* recordsFile;

	if (fopen_s(&recordsFile, recordsPath, "rb")) {
		cout << "Error opening records file." << endl;
		return;
	}

	RepairRecord tempRecord;
	bool isFound = false;
	int resultCounter = 0;

	while (fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile)) {
		if (strcmp(tempRecord.brand, brand) == 0 && tempRecord.repairCost <= maxCost) {
			resultCounter++;
			isFound = true;
		}
	}
	if (!isFound) {
		cout << "Records not found." << endl;
		fclose(recordsFile);
		return;
	}

	RepairRecord* list = new RepairRecord[resultCounter];
	int position = 0;
	rewind(recordsFile);
	while (fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile)) {
		if (strcmp(tempRecord.brand, brand) == 0 && tempRecord.repairCost <= maxCost) {
			list[position] = tempRecord;
			position++;
		}
	}

	fclose(recordsFile);

	quickSort(list, 0, resultCounter - 1);
	cout << "Found records:" << endl;
	char reportContent[10000] = "Search by brand and max cost: ";
	char tempBuffer[32]{};
	strcat_s(reportContent, sizeof(reportContent), brand);
	sprintf_s(tempBuffer, sizeof(tempBuffer), ", %d", maxCost);
	strcat_s(reportContent, sizeof(reportContent), tempBuffer);
	strcat_s(reportContent, sizeof(reportContent), ":\n");
	for (int i = resultCounter; i > 0; i--) { 
		list[i - 1].printRepairRecord(i == resultCounter); 
		char recordStr[256];
		list[i - 1].toString(recordStr);
		strcat_s(reportContent, sizeof(reportContent), recordStr);
	}
	saveReportToFile(reportContent);
	delete[] list;
	list = nullptr;
}

void CarRepairSystem::quickSortByRepairDate() {
	RepairRecord* list = loadFromFile();
	if (list == nullptr) {
		cout << "Error loading data from file." << endl;
		return;
	}
	quickSort(list, 0, recordsCount - 1);
	saveToFile(list);
	saveReportToFile("File sorted by quick sort by date\n");
	cout << "File was sorted successfully." << endl;
}

void CarRepairSystem::selectionSortByMileage() {
	RepairRecord* list = loadFromFile();
	if (list == nullptr) {
		cout << "Error loading data from file." << endl;
		return;
	}
	selectionSort(list);
	saveToFile(list);
	saveReportToFile("File sorted by selection sort by mileage\n");
	cout << "File was sorted successfully." << endl;
}

void CarRepairSystem::insertionSortByRepairCost() {
	RepairRecord* list = loadFromFile();
	if (list == nullptr) {
		cout << "Error loading data from file." << endl;
		return;
	}
	insertionSort(list);
	saveToFile(list);
	saveReportToFile("File sorted by insertion sort by cost\n");
	cout << "File was sorted successfully." << endl;
}

void CarRepairSystem::repairStats() {
	displayRepairsByType();
	findMostExpensiveAndCheapestRepair();
}

void CarRepairSystem::displayRepairsByType() {
	RepairRecord* list = loadFromFile();
	quickSort(list, 0, recordsCount - 1);
	bool isFound;
	bool isFirst;
	char reportContent[10000]{};
	for (int i = 0; i < AMOUNT_OF_REPAIR_TYPES; i++) {
		isFound = false;
		isFirst = true;
		cout << repairTypeStrings[i] << ": " << endl;
		strcat_s(reportContent, sizeof(reportContent), repairTypeStrings[i]);
		strcat_s(reportContent, sizeof(reportContent), ":\n");
		for (int j = 0; j < recordsCount; j++) {
			if (list[j].repairType == static_cast<RepairType>(i)) {

				list[j].printRepairRecord(isFirst);
				
				char recordStr[256];
				list[j].toString(recordStr);
				strcat_s(reportContent, sizeof(reportContent), recordStr);

				isFound = true;
				isFirst = false;
			}
		}
		if (!isFound) {
			cout << "Records not found." << endl;
			strcat_s(reportContent, sizeof(reportContent), "Records not found.\n");
		}
	}
	saveReportToFile(reportContent);
	delete[] list;
	list = nullptr;
}

void CarRepairSystem::findMostExpensiveAndCheapestRepair() {
	/*RepairRecord* list = loadFromFile();
	if (list == nullptr) {
		cout << "Error in calculating most expensive and cheapest repairs. (Error loading data from file)" << endl;
		return;
	}
	insertionSort(list);
	cout << "Most expensive repair: $" << list[0].repairCost << endl;
	cout << "The cheapest repair: $" << list[recordsCount - 1].repairCost << endl;
	delete[] list;
	list = nullptr;*/


	FILE* recordsFile;
	if (fopen_s(&recordsFile, recordsPath, "rb")) {
		cout << "Error opening records file." << endl;
		return;
	}
	RepairRecord mostExpensive;
	RepairRecord cheapest;
	RepairRecord tempRecord;
	fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile);
	cheapest = mostExpensive = tempRecord;
	while (fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile)) {
		if (tempRecord.repairCost > mostExpensive.repairCost) { mostExpensive = tempRecord; }
		if (tempRecord.repairCost < cheapest.repairCost) { cheapest = tempRecord; }
	}
	cout << "Most expensive repair: $" << mostExpensive.repairCost << endl;
	cout << "The cheapest repair: $" << cheapest.repairCost << endl;
	char reportContent[10000] = "Most expensive repair: $";
	char tempBuffer[32]{};
	sprintf_s(tempBuffer, sizeof(tempBuffer), "%d", mostExpensive.repairCost);
	strcat_s(reportContent, sizeof(reportContent), tempBuffer);
	strcat_s(reportContent, sizeof(reportContent), "\nThe cheapest repair: $");
	sprintf_s(tempBuffer, sizeof(tempBuffer), "%d", cheapest.repairCost);
	strcat_s(reportContent, sizeof(reportContent), tempBuffer);
	strcat_s(reportContent, sizeof(reportContent), "\n");
	saveReportToFile(reportContent);
}

#ifdef DEBUG
void CarRepairSystem::randomFill(int amount) {
	const char cars[5][6][25] = {
		{"BMW", "3 Series", "5 Series", "X5", "M4", "iX"},
		{"Toyota", "Corolla", "Camry", "RAV4", "Supra", "Land Cruiser"},
		{"Mercedes", "C Class", "E Class", "GLE", "S Class", "AMG GT"},
		{"Ford", "Mustang", "F150", "Explorer", "Focus", "Bronco"},
		{"Audi", "A4", "A6", "Q7", "RS5", "etron GT"}
	};
	FILE* recordsFile;
	if (fopen_s(&recordsFile, recordsPath, "ab")) {
		cout << "Error opening records file." << endl;
		return;
	}
	srand(time(NULL));
	RepairDate randDate{};
	int randBrand;

	for (int i = 0; i < amount; i++) {
		randDate.day = rand() % 31 + 1;
		randDate.month = rand() % 12 + 1;
		randDate.year = rand() % 10 + 2015;
		randBrand = rand() % 5;

		RepairRecord randRecord(cars[randBrand][0], cars[randBrand][rand() % 5 + 1], static_cast<RepairType>(rand() % AMOUNT_OF_REPAIR_TYPES), rand() % 9901 + 100, rand() % 290001 + 10000, randDate);
		fwrite(&randRecord, sizeof(RepairRecord), 1, recordsFile);
		recordsCount++;
	}
	fclose(recordsFile);
}
#endif

void CarRepairSystem::modifyRepairRecord(bool isToDelete) {
	FILE* recordsFile;
	FILE* tempFile;

	if (fopen_s(&recordsFile, recordsPath, "rb")) {
		cout << "Error opening records file." << endl;
		return;
	}

	if (fopen_s(&tempFile, "temp.bin", "wb")) {
		cout << "Error opening temporary file." << endl;
		fclose(recordsFile);
		return;
	}

	RepairRecord tempRecord;
	bool isFound = false;
	bool isFirst = true;
	char reportContent[10000]{};
	char tempModel[25]{};
	char prompt[28]{};
	if (isToDelete) { strcpy_s(prompt, sizeof(prompt), "Enter car model to delete: "); }
	else { strcpy_s(prompt, sizeof(prompt), "Enter car model to edit: "); }
	getValidatedString(prompt, tempModel, 1, 2, 24, "Car model must have length between 2 and 24, contain numbers from 0 to 9, letters from a to z and A to Z and space.\nTry again: ");

	while (fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile)) {
		if (strcmp(tempRecord.model, tempModel) == 0) {
			if (isFirst && isToDelete) {
				cout << "Deleted records: " << endl;
				strcat_s(reportContent, sizeof(reportContent), "Deleted records: \n");
			}
			if (!isToDelete) cout << "Found record: " << endl;
			tempRecord.printRepairRecord(isFirst);
			if (!isToDelete) {
				fieldsEdit(tempRecord);
				fwrite(&tempRecord, sizeof(RepairRecord), 1, tempFile);
			}
			else { recordsCount--; }
			isFound = true;
			if (isToDelete) {
				isFirst = false;
				char recordStr[256];
				tempRecord.toString(recordStr);
				strcat_s(reportContent, sizeof(reportContent), recordStr);
			}
		}
		else { fwrite(&tempRecord, sizeof(RepairRecord), 1, tempFile); }
	}

	if (isFound) {
		if (isToDelete) { cout << "Records deleted successfully." << endl; }
		else { cout << "Records edited successfully." << endl; }
	}
	else { 
		cout << "Records not found." << endl; 
		if(isToDelete){ strcat_s(reportContent, sizeof(reportContent), "Records not found(deleting).\n"); }
		else { saveReportToFile("Records not found(editing).\n"); }
	}
	if (isToDelete) { saveReportToFile(reportContent); }
	fclose(recordsFile);
	fclose(tempFile);

	remove(recordsPath);
	if (rename("temp.bin", recordsPath)) { cout << "Error renaming file." << endl; }
	if (!isToDelete) {
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cin.clear();
	}
}

int CarRepairSystem::startMenu() {
	cout << " 1. View all records" << endl
		<< " 2. Add a new record" << endl
		<< " 3. Edit a record" << endl
		<< " 4. Delete a record" << endl
		<< " 5. Find a record by car model (Linear search)" << endl
		<< " 6. Find a record by repair cost (Binary search)" << endl
		<< " 7. Find records by brand and max cost" << endl
		<< " 8. Sort records by date (Quick sort)" << endl
		<< " 9. Sort records by mileage (Selection sort)" << endl
		<< "10. Sort records by repair cost (Insertion sort)" << endl
		<< "11. Repair statistics*" << endl
		<< " Any key to exit" << endl
		<< "\n* For each repair type, display a list of works sorted in ascending order by date. Find the most expensive and the cheapest repair.\n" << endl
		<< "Please make a choice: ";
	int choice;
	cin >> choice;
	cin.ignore(numeric_limits<streamsize>::max(), '\n');
	cin.clear();
	return (cin.fail()) ? 0 : choice;
}

int CarRepairSystem::editMenu() {
	cout << "What do you want to edit?" << endl
		<< " 1. Car brand" << endl
		<< " 2. Car model" << endl
		<< " 3. Repair type" << endl
		<< " 4. Repair cost" << endl
		<< " 5. Mileage" << endl
		<< " 6. Repair date" << endl
		<< " Any key to nothing" << endl
		<< "Please make choice: ";
	int choice;
	cin >> choice;
	return (cin.fail()) ? 0 : choice;
}

void CarRepairSystem::fieldsEdit(RepairRecord& record) {
	int tempInt;
	char tempStr[100]{};
	RepairDate tempRepairDate;
	while (true) {
		tempInt = 0;
		for (int i = 0; tempStr[i]; i++) { tempStr[i] = '\0'; }
		tempRepairDate = RepairDate{};
		switch (editMenu()) {
		case 1:
			getValidatedString("Enter car brand: ", tempStr, 0, 3, 24, "Car brand must have length between 3 and 24, contain letters from a to z and A to Z.\nTry again: ");
			strcpy_s(record.brand, sizeof(record.brand), tempStr);
			break;
		case 2:
			getValidatedString("Enter car model: ", tempStr, 1, 2, 24, "Car model must have length between 2 and 24, contain numbers from 0 to 9, letters from a to z and A to Z and space.\nTry again: ");
			strcpy_s(record.model, sizeof(record.model), tempStr);
			break;
		case 3:
			record.repairType = selectRepairType();
			break;
		case 4:
			getValidatedInt("Enter repair cost in dollars: ", tempInt, 1, 1000000, "Repair cost must be a number between 1 and 1000000.\nTry again: ");
			record.repairCost = tempInt;
			break;
		case 5:
			getValidatedInt("Enter mileage in kilometers: ", tempInt, 1, 5000000, "Mileage must be a number between 1 and 5000000.\nTry again: ");
			record.mileage = tempInt;
			break;
		case 6:
			cout << "Enter date of repair:\n";
			getValidatedInt("Day: ", tempRepairDate.day, 1, 31, "Day must be a number between 1 and 31.\nTry again: ");
			getValidatedInt("Month: ", tempRepairDate.month, 1, 12, "Month must be a number between 1 and 12.\nTry again: ");
			getValidatedInt("Year: ", tempRepairDate.year, 1900, 2100, "Year must be a number between 1900 and 2100.\nTry again: ");
			record.repairDate = tempRepairDate;
			break;
		default:
			return;
		}
		cout << "Would you like to edit another field? (Y/N): ";
		char choice = _getch();
		if (choice == 'n' || choice == 'N') {
			char reportContent[512] = "Edited record: \n";
			char recordStr[256];
			record.toString(recordStr);
			strcat_s(reportContent, sizeof(reportContent), recordStr);
			saveReportToFile(reportContent);
			break; 
		}
		system("cls");
	}
}

CarRepairSystem::RepairType CarRepairSystem::selectRepairType() {
	cout << "Choose repair type: " << endl;
	for (int i = 0; i < AMOUNT_OF_REPAIR_TYPES - 1; i++) { cout << " " << (i + 1) << ". " << repairTypeStrings[i] << endl; }
	cout << " Any key to select Other" << endl << "Please make choice: ";
	int choice;
	cin >> choice;
	if (cin.fail()) {
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		choice = AMOUNT_OF_REPAIR_TYPES;
	}
	return (choice > 0 && choice < AMOUNT_OF_REPAIR_TYPES) ? static_cast<RepairType>(choice - 1) : RepairType::Other;
}

CarRepairSystem::RepairRecord* CarRepairSystem::loadFromFile() const {
	FILE* recordsFile;
	if (fopen_s(&recordsFile, recordsPath, "rb")) {
		cout << "Error opening records file." << endl;
		return nullptr;
	}

	RepairRecord tempRecord;
	RepairRecord* list = new RepairRecord[recordsCount];
	int counter = 0;

	while (fread(&tempRecord, sizeof(RepairRecord), 1, recordsFile)) {
		list[counter] = tempRecord;
		counter++;
	}

	fclose(recordsFile);

	return list;
}

void CarRepairSystem::saveToFile(RepairRecord* list) const {
	FILE* tempFile;
	if (fopen_s(&tempFile, "temp.bin", "wb")) {
		cout << "Error opening temporary file." << endl;
		return;
	}
	for (int i = 0; i < recordsCount; i++) { fwrite(&list[i], sizeof(RepairRecord), 1, tempFile); }
	fclose(tempFile);
	delete[] list;
	list = nullptr;
	remove(recordsPath);
	if (rename("temp.bin", recordsPath)) { cout << "Error renaming file." << endl; }
}

void CarRepairSystem::saveReportToFile(const char* content) {
	FILE* reportFile;
	if (fopen_s(&reportFile, "report.txt", "a")) {
		cout << "Error opening report file." << endl;
		return;
	}

	time_t now = time(0);
	char timestamp[64];
	ctime_s(timestamp, sizeof(timestamp), &now);
	fprintf(reportFile, "\n=== Report added on: %s", timestamp);

	if (fprintf(reportFile, "%s", content) < 0) {
		cout << "Error writing to report file." << endl;
	}
	fclose(reportFile);
}

void CarRepairSystem::quickSort(RepairRecord* list, int left, int right) {
	if (left > right) return;
	RepairRecord currentRecord = list[(left + right) / 2];
	int i = left;
	int j = right;
	while (i <= j) {
		while (list[i].repairDate < currentRecord.repairDate) i++;
		while (list[j].repairDate > currentRecord.repairDate) j--;
		if (i <= j) {
			RepairRecord tempRecord = list[i];
			list[i] = list[j];
			list[j] = tempRecord;
			i++;
			j--;
		}
	}
	quickSort(list, left, j);
	quickSort(list, i, right);
}

void CarRepairSystem::selectionSort(RepairRecord* list) {
	RepairRecord tempRecord;
	for (int positionToPut = 0; positionToPut < recordsCount - 1; positionToPut++) {
		int positionOfMinimum = positionToPut;
		for (int j = positionToPut + 1; j < recordsCount; j++) {
			if (list[j].mileage < list[positionOfMinimum].mileage) positionOfMinimum = j;
		}
		if (positionOfMinimum != positionToPut) {
			tempRecord = list[positionToPut];
			list[positionToPut] = list[positionOfMinimum];
			list[positionOfMinimum] = tempRecord;
		}
	}
}

void CarRepairSystem::insertionSort(RepairRecord* list) {
	RepairRecord tempRecord;
	for (int currentPosition = 1; currentPosition < recordsCount; currentPosition++) {
		int i = currentPosition;
		while (i > 0 && list[i].repairCost < list[i - 1].repairCost) {
			tempRecord = list[i];
			list[i] = list[i - 1];
			list[i - 1] = tempRecord;
			i--;
		}
	}
}

bool CarRepairSystem::validateStr(char* buffer, int type, int minLen, int maxLen, const char* errorMsg) {
	cin.getline(buffer, maxLen);
	int strLength = static_cast<int>(strlen(buffer));
	if (!(strLength <= maxLen && strLength >= minLen)) { cout << errorMsg; return false; }
	for (int i = 0; i < strLength; i++) {
		bool isValidChar = ((buffer[i] >= 'a' && buffer[i] <= 'z') || (buffer[i] >= 'A' && buffer[i] <= 'Z'));
		if (type == 1) { isValidChar = isValidChar || (buffer[i] == ' ') || (buffer[i] >= '0' && buffer[i] <= '9'); }
		if (!isValidChar) {
			cout << errorMsg;
			return false;
		}
	}
	return true;
}
void CarRepairSystem::getValidatedString(const char* prompt, char* buffer, int type, int minLen, int maxLen, const char* errorMsg) {
	cout << prompt;
	while (!validateStr(buffer, type, minLen, maxLen, errorMsg));
}

bool CarRepairSystem::validateInt(int& value, int min, int max, const char* errorMessage) {
	cin >> value;
	if (cin.fail() || !(value <= max && value >= min)) {
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
		}
		cout << errorMessage;
		return false;
	}
	return true;
}
void CarRepairSystem::getValidatedInt(const char* prompt, int& value, int min, int max, const char* errorMsg) {
	cout << prompt;
	while (!validateInt(value, min, max, errorMsg));
}

CarRepairSystem::RepairRecord::RepairRecord(const char* brand, const char* model, RepairType repairType, int repairCost, int mileage, RepairDate repairDate) {
	strcpy_s(this->brand, sizeof(this->brand), brand);
	strcpy_s(this->model, sizeof(this->model), model);
	this->repairType = repairType;
	this->repairCost = repairCost;
	this->mileage = mileage;
	this->repairDate = repairDate;
}

void CarRepairSystem::RepairRecord::printRepairRecord(bool isFirst) const {
	if (isFirst) cout << "-------------------------------------------\n";
	cout << "Car brand: " << this->brand << "\n"
		<< "Car model: " << this->model << "\n"
		<< "Repair type: " << repairTypeStrings[static_cast<int>(this->repairType)] << "\n"
		<< "Repair cost: $" << this->repairCost << "\n"
		<< "Mileage: " << this->mileage << "km" << "\n"
		<< "Date: " << this->repairDate.day << "." << this->repairDate.month << "." << this->repairDate.year << "\n"
		<< "-------------------------------------------" << endl;
}

void CarRepairSystem::RepairRecord::toString(char* buffer) {
	sprintf_s(buffer, 256, "%s %s, %s, $%d, %dkm, %02d.%02d.%04d\n",
		brand, model, repairTypeStrings[static_cast<int>(repairType)], repairCost, mileage, repairDate.day, repairDate.month, repairDate.year);
}

bool CarRepairSystem::RepairDate::operator>(RepairDate other) {
	if (year != other.year) return year > other.year;
	if (month != other.month) return month > other.month;
	return day > other.day;
}

bool CarRepairSystem::RepairDate::operator<(RepairDate other) {
	if (year != other.year) return year < other.year;
	if (month != other.month) return month < other.month;
	return day < other.day;
}

int main() {
	CarRepairSystem carRepairSystem("data.bin");
	carRepairSystem.start();
	return 0;
}