#include<iostream>
#include<windows.h>
#include<ctime>
using namespace std;

class factorial{
    int num;
    unsigned long long fact;
    public:
    factorial(int n): num(n){
        calculateFact();
    }

    void calculateFact(){
        fact=1;
        for(int i=1;i<=num;++i){
            fact*=i;
        }
    }

    void display(){
        cout<<"Factorial of "<<num<<" is: "<<fact<<endl;
    }
};

int main(){
int n;
char userInput;
do{
    clock_t start = clock();
    Beep(2000, 50);
    int n;
    cout<<"Enter a number: ";cin>>n;
    factorial f(n);
    if(n<0){
        cout<<"Factorial of negative number is not possible"<<endl;
    }
    else{
        f.display();
    }
    clock_t end = clock();
    cout<<"Time taken: "<<(end-start)/100<<" ms"<<endl;
    
    cout << "Do you want to continue? (y/n): ";
    cin >> userInput;
}
while( userInput!='n');
Beep(4000, 50);
return 0;
}
