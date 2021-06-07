#include <bits/stdc++.h>
#include "python_object.cpp"
using namespace std;

class python_iterable{
	python_object a;
	python_iterable(){

	}
	~python_iterable(){

	}
};


int main(){
	std::vector<int> v({1});
	auto s=0;
	for (auto &w:v){
		v.push_back(s);
		s++;
		if (s==10){
			break;
		}
	}
	for (auto w:v){
		cout<<w<<endl;
	}
}