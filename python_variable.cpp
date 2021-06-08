#include <bits/stdc++.h>
using namespace std;
// #include <iostream>
// #include <any>


#define python_iftype(a,...) __VA_ARGS__ s;\
	if ((a).type()==typeid(std::declval<python_variable<__VA_ARGS__>>())){\
		s=cast((a),__VA_ARGS__);\
	}\
	if ((a).type()==typeid(std::declval<python_variable<__VA_ARGS__>>()))

#define cast(q,...) (q.cast_with_line<__VA_ARGS__>(__LINE__))

#define print_line() std::cout<<__LINE__<<std::endl;

template<typename T>
class python_variable{
public:
	T*p;
	int64_t*c;
	T &value(){
		return *p;
	}
	python_variable(T a=int64_t(0)){
		c=new int64_t(1);
		p=new T(a);
	}
	python_variable(const python_variable &a){
		p=a.p;
		c=a.c;
		*c+=1;
	}
	python_variable operator=(T a){
		c=new int64_t(1);
		p=new T(a);
	}
	python_variable operator=(const python_variable &a){
		p=a.p;
		c=a.c;
		*c+=1;
	}
	~python_variable(){
		*c-=1;
		if (*c==0){
			delete p;
			delete c;
		}
	}
};

template <typename T>
std::any to_var(T q){
	std::any t=python_variable<T>(q);
	return t;
}

template <typename T>
T &from_var(std::any q,int64_t line){
	if (q.type()!=typeid(std::declval<python_variable<T>>())){
		std::cout<<"wrong cast"<<std::endl;
		std::cout<<"    line "<<line<<std::endl;
		std::cout<<"    have "<<q.type().name()<<std::endl;
		std::cout<<"    want "<<typeid(std::declval<python_variable<T>>()).name()<<std::endl;
	}
	return std::any_cast<python_variable<T>>(q).value();
}

class var{
public:
	std::any a;
	template<typename t>
	var(t q){
		a=to_var(q);
	}
	var(){
		a=to_var(int64_t(0));
	}
	template<typename t>
	var operator=(t q){
		a=to_var(q);
		return *this;
	}
	template<typename t>
	t &cast_with_line(int64_t line){
		return from_var<t>(a,line);
	}
	auto&type(){
		return a.type();
	}
};

class python_iterate{
public:
	var orig;
	python_iterate(var q):orig(q){}
	class iterator:std::forward_iterator_tag{
	public:
		var orig;
		var iter;
		iterator(var q):orig(q),iter(q){
			{python_iftype(orig,std::vector<var>){
				iter=cast(orig,decltype(s)).begin();
			}}
		}
		
		void operator++(){
			{python_iftype(orig,std::vector<var>){
				 ++cast(iter,decltype(s)::iterator);
			}}
		}
		bool operator!=(iterator o){
			{python_iftype(orig,std::vector<var>){
				return cast(iter,decltype(s)::iterator)!=cast(orig,decltype(s)).end();
			}}
		}
		var &operator*(){
			{python_iftype(orig,std::vector<var>){
				return *cast(iter,decltype(s)::iterator);
			}}
		}
	};
	iterator begin(){
		return iterator(orig);
	}
	iterator end(){
		return iterator(orig);
	}
};







class something{
public:
	int64_t q;
	something(){
		q=rand();
		std::cout<<q<<" created"<<std::endl;
	}
	something(something&a){
		q=rand();
		std::cout<<q<<" created"<<std::endl;
	}
	~something(){
		std::cout<<q<<" deleted"<<std::endl;
		q=0;
	}
};



// python_variable f(python_variable a){
// 		print_line()
// 	return a;
// }

int main(){
	// print_line()
	// {
	// 	print_line()
	// 	var a=something();
	// 	print_line()
	// 	any s=a;
	// 	print_line()
	// }
	// print_line()


	// var a=int64_t(1);
	// {python_iftype(a,int){
	// 	std::cout<<"int"<<s<<std::endl;
	// }}
	// {python_iftype(a,int64_t){
	// 	std::cout<<"int64_t"<<s<<std::endl;
	// }}

	// var a=vector<int>();
	// var s=a;
	// cast(s,vector<int>).push_back(123);
	// cout<<cast(a,vector<int>)[0]<<endl;

	// var a=std::vector<var>();
	// cast(a,std::vector<var>).push_back(1);
	// cast(a,std::vector<var>).push_back(2);
	// cast(a,std::vector<var>).push_back(3);
	// for (var w:python_iterate(a)){
	// 	std::cout<<cast(w,int)<<std::endl;
	// }

	// var a=std::vector<var>();
	// cast(a,std::vector<var>).push_back(1);
	// cast(a,std::vector<var>).push_back(2);
	// cast(a,std::vector<var>).push_back(3);
	// auto d=python_iterate(a);
	// var s=std::vector<var>();
	// for (var w:python_iterate(a)){
	// 	cast(s,std::vector<var>).push_back(w);
	// }
	// cast(cast(s,std::vector<var>)[0],int)++;
	// for (var w:python_iterate(a)){
	// 	std::cout<<cast(w,int)<<std::endl;
	// }

	// print_line()
	// var a(1);
	// print_line()
	// a=2;
	// print_line()
	// a=vector<int>();
	// print_line()
	// cast(a,vector<int>).push_back(1);
	// print_line()
	// cout<<cast(a,vector<int>)[0]<<endl;
	// print_line()

	// var a=something();
	// var s=a;
	// cout<<(&cast(a,something)==&cast(s,something))<<endl;

	// var a=vector<var>({1,2,3});
	// var s=a;
	// cast(s,vector<var>)[0]=4;
	// cout<<cast(cast(a,vector<var>)[0],int)<<endl;
}