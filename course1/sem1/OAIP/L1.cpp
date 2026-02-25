#include <iostream>
#include <math.h>
using namespace std;

int main()
{
	double x, y, z, a, b, c, h;
	
	cout << "Vvedite x: ";
		cin >> x;
	cout << "Vvedite y: ";
		cin >> y;
	cout << "Vvedite z: ";
		cin >> z;

	a = sqrt(x + pow(fabs(y), 1/4.));
	b = pow(exp(x - (1 / sin(z))), 1/3.);
	c = pow(2, -x);
	h = a * b * c;
	cout << "h = " << h << endl;
}
