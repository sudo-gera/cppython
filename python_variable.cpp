#include <bits/stdc++.h>
using namespace std;
// #include <iostream>
// #include <any>

#define python_iftype(a,...) __VA_ARGS__ s;if ((a).type()==typeid(std::declval<__VA_ARGS__>())){s=(a).cast<__VA_ARGS__>();}if ((a).type()==typeid(std::declval<__VA_ARGS__>()))


#define python_ifcollectons(a,...)\
	{python_iftype(a,vector<python_variable>){\
		__VA_ARGS__;\
	}}\
	// {python_iftype(a,set<python_variable>){\
	// 	__VA_ARGS__;\
	// }}
	// {python_iftype(a,map<python_variable,python_variable>){\
	// 	__VA_ARGS__;\
	// }}



#define print_line() cout<<__LINE__<<endl;

class python_variable{
public:
	std::any*p;
	int64_t*c;
	std::any &value(){
		return *p;
	}
	operator any(){
		return *p;
	}
	template <typename t>
	t cast(){
		return any_cast<t>(*p);
	}
	auto &type(){
		return (*p).type();
	}
	python_variable(std::any a=0){
		// std::cout<<"creating constructor"<<std::endl;
		c=new int64_t;
		*c=1;
		p=new std::any;
		*p=a;
		// {python_iftype(*this,int){
		// 	cout<<"with"<<s<<endl;
		// }}
	}
	python_variable(python_variable &a){
		// std::cout<<"copying constructor with "<<*(a.c)<<std::endl;
		p=a.p;
		c=a.c;
		*c+=1;
	}
	python_variable operator=(std::any a){
		// std::cout<<"creating constructor"<<std::endl;
		c=new int64_t;
		*c=1;
		p=new std::any;
		*p=a;
		// {python_iftype(*this,int){
		// 	cout<<"with"<<s<<endl;
		// }}
	}
	python_variable operator=(python_variable a){
		// std::cout<<"copying constructor with "<<*(a.c)<<std::endl;
		p=a.p;
		c=a.c;
		*c+=1;
	}
	~python_variable(){
		// std::cout<<"destructor with "<<*(c)<<std::endl;
		*c-=1;
		if (*c==0){
			delete p;
			delete c;
		}
	}
};

class python_iterate{
public:
	python_variable orig;
	// python_variable iter;
	vector<python_variable>::iterator iter;
	python_iterate(python_variable q){
		orig=q;
		{python_iftype(orig,vector<python_variable>){
			iter=s.begin();
		}}
		// {python_iftype(orig,vector<python_variable>){
		// 	any d=s.begin();
		// 	iter=d;
		// }}
		// {python_iftype(orig,set<python_variable>){
		// 	any d=s.begin();
		// 	iter=d;
		// }}
		// {python_iftype(orig,map<python_variable,python_variable>){
		// 	any d=s.begin();
		// 	iter=d;
		// }}
		// {python_iftype(orig,u32string){
		// 	any d=s.begin();
		// 	iter=d;
		// }}
	}
	bool not_end(){
		{python_iftype(orig,vector<python_variable>){
			iter!=s.end();
		}}
		// {python_iftype(orig,vector<python_variable>){
		// 	iter.cast<decltype(s.begin())>()!=s.end();
		// }}
		// {python_iftype(orig,set<python_variable>){
		// 	iter.cast<decltype(s.begin())>()!=s.end();
		// }}
		// {python_iftype(orig,map<python_variable,python_variable>){
		// 	iter.cast<decltype(s.begin())>()!=s.end();
		// }}
		// {python_iftype(orig,u32string){
		// 	iter.cast<decltype(s.begin())>()!=s.end();
		// }}
	}
	python_variable next(){
		{python_iftype(orig,vector<python_variable>){
			iter++;
			return *iter;
		}}
		// {python_iftype(orig,vector<python_variable>){
		// 	++iter.cast<decltype(s.begin())>();
		// 	return *(iter.cast<decltype(s.begin())>())
		// }}
		// {python_iftype(orig,set<python_variable>){
		// 	++iter.cast<decltype(s.begin())>();
		// 	return *(iter.cast<decltype(s.begin())>())
		// }}
		// {python_iftype(orig,map<python_variable,python_variable>){
		// 	++iter.cast<decltype(s.begin())>();
		// 	return *(iter.cast<decltype(s.begin())>())
		// }}
		// {python_iftype(orig,u32string){
		// 	++iter.cast<decltype(s.begin())>();
		// 	return *(iter.cast<decltype(s.begin())>())
		// }}
	}
};




// class something{
// public:
// 	int64_t q;
// 	something(){
// 		q=rand();
// 		std::cout<<q<<" created"<<std::endl;
// 	}
// 	// something(something&a){
// 	// 	q=rand();
// 	// 	std::cout<<q<<" created"<<std::endl;
// 	// }
// 	~something(){
// 		std::cout<<q<<" deleted"<<std::endl;
// 		q=0;
// 	}
// };


// python_variable f(python_variable a){
// 		print_line()
// 	return a;
// }

int main(){
	any a=any(vector<python_variable>());
	any_cast<vector<python_variable>>(a).push_back(any(1));
	cout<<any_cast<vector<python_variable>>(a).size()<<endl;
	// a.push_back(any(2));
	// a.push_back(any(3));
	// for(auto s=a.begin();s!=a.end();){
	// 	auto d=*s;
	// 	s++;
	// 	cout<<d.cast<int>()<<' ';
	// }
	// cout<<endl;
}