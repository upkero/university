#include <iostream>
#include <math.h>
#include <iomanip>
using namespace std;

double y(double);
double s(double, double, int&);

int main() {

    double a, b, h, eps, sum;
    int k=0;

    cout << "Enter beginning of the range: a = "; cin >> a;
    cout << "Enter end of the range: b = "; cin >> b;
    cout << "Enter range ste: h = "; cin >> h;
    cout << "Enter the permissible error: eps = "; cin >> eps;

    cout << setw(8) << "x" << setw(15) << "y(x)" << setw(10) << "k" << endl;
    for (double x = a; x < b + h / 2; x += h) {
        cout << setw(8) << x << setw(15) << y(x) << setw(10) << "-" << endl;
    }
    cout << endl;

    cout << setw(8) << "x" << setw(15) << "s(x)" << setw(10) << "k" << endl;
    for (double x = a; x < b + h / 2; x += h) {
        cout << setw(8) << x << setw(15) << s(x, eps, k) << setw(10) << k << endl;
    }
    cout << endl;

    cout << "x - value of x," << endl << "y(x) - value of function," << endl << "s(x) - value of sum," << endl << "k - number of iterations." << endl;

    return 0;
}

double y(double x) {

    return cos(x);
}

double s(double x, double eps, int& k) {

    double c = 1, sum = 1;

    k = 1;

    while (fabs(sum - y(x)) >= eps) {
        c *= -pow(x, 2) / ((2 * k - 1) * (2 * k));
        sum += c;
        k++;
    }

    return sum;
}