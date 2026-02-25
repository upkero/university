#include <iostream>
#include <math.h>
using namespace std;

int main()
{
    double min, maxxy, maxyz, m, x, y, z;
    cout << "Enter x: "; cin >> x;
    cout << "Enter y: "; cin >> y;
    cout << "Enter z: "; cin >> z;
    maxxy = x > y ? x : y;
    maxyz = y > z ? y : z;
    if (maxyz == 0) abort;
    min = maxxy < maxyz ? maxxy : maxyz;
    m = min / maxyz;
    cout << "Your result: " << m << endl;
    return 0;
}