/**
This Hello World application was created to test swig wrapping 
for python. It does a few simple things like input and output 
from the command line, and some simple string/math opperations.

Brian Thorne 2008
*/

// preprocessor include.
#include "Hello World.h"
#include <list>

using namespace std;

// Internal function prototypes (rest in header)
void printLine(string s);
string int2string(int i);

// Global var
string name;

int add(int var1, int var2,int var3,int var4)
{
	return var1 + var2 + var3 + var4;
}

/** Print the name of the program */
void printProgram(string programName)
{
	cout << "Hello World from " << AUTHOR << endl;
	cout << "Program running is '" << programName << "' and was built in " << yearMade << endl;
}

void printString()
{
	//Use a string
	string myNewLine = "This is a new string thing!";
	cout<<myNewLine<<endl;
}

string getName()
{
	printLine("Please enter your name: ");
	getline(cin,name);
	printLine("Thanks " + name);
	return name;
}

void simpleProcess()
{
	// declaring variables:
	int a, b;
	int result;

	// process:
	a = 5;
	b = 2;
	a = add(a,1);
	result = a - b;

	// print out the result:
	cout << "5+1-2= " << result <<endl;
}

void commaOp()
{
	// Comma operator 
	int i,j;
	j = (i = 5,i + 2);
	cout << endl << "j = (i = 5,i + 2)\nj:"<<j<<"\ni:"<<i<<endl;
}

void booltest()
{
	// Boolean test
	bool abool = true;
	cout << "trying to output a true boolean: " << abool << endl;
}

void wait4in()
{
	//Wait for user input so we can see the screen!
	string myLine;
	printLine("\n\nWe are all done " + name + ". Just press enter to quit");
	getline(cin,myLine);
}

/* Run all the functions */
void runAll(int argc, string v)
{
	printProgram(v);
	printString();
	name = getName();
	simpleProcess();
	commaOp();
	booltest();

	cout << endl << "While loop test" << endl;
	int i = 10;
	while (i)
	{
		cout << i-- << endl;
	}

	cout << endl << "for loop test 1" << endl;
	for (i = 0;i<5;i++)
	{
		cout << i << endl;
	}

	cout << endl << "for loop test 2" << endl;
	for (i = 0;i<5;i++)
	{
		if (i==1) continue;
		if (i == 3) break;
		cout << i << endl;
	}
	
	printLine("Test adding with a function!");
	cout << "4 + 2 = " << add(4,2) << endl;
	cout << "1 + 2 + 3 + 4 = " << add(1,2,3,4) << endl;

	printLine("Lets Recurse!");
	cout << "The factorial of 5 is: " << factorial(5) << endl;


	wait4in();
}

int main(int argc, char* argv[])
{
	string s = string(argv[0]);
	runAll(argc,s);

	return 0;
}

/* Test a simple function*/
void printLine(string s)
{
	cout << s << endl;
}

/* Test a recursive function */
int factorial(int num)
{
	if (num == 1) return 1;
	return num * factorial(num-1);
}

