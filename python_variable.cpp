#include <bits/stdc++.h>
using namespace std;
#include "/Users/gera/pony/filt.hpp"
// #include <iostream>
// #include <any>


				#define python_complex				std::complex<long double>
				#define python_float				long double
				#define python_int					int64_t
				#define python_bool					bool
				#define python_bytearray			std::string
				#define python_str					std::u32string
				#define python_list					std::vector<var>
				#define python_set					std::set<var>
				#define python_dict					std::map<var,var>
				#define python_NoneType				python_NoneType
				#define python_ellipsis				python_ellipsis




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
						std::cout<<"    have "<<filt(q.type().name())<<std::endl;
						std::cout<<"    want "<<filt(typeid(std::declval<python_variable<T>>()).name())<<std::endl;
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
					var operator+(var o);
					var operator-(var o);
					var operator+();
					var operator-();
					var operator*(var o);
					var operator/(var o);
					var operator%(var o);
					var operator==(var o);
					var operator!=(var o);
					var operator>(var o);
					var operator<(var o);
					var operator>=(var o);
					var operator<=(var o);
					var operator!();
					var operator&&(var o);
					var operator||(var o);
					var operator~();
					var operator&(var o);
					var operator|(var o);
					var operator^(var o);
					var operator<<(var o);
					var operator>>(var o);
					var operator+=(var o);
					var operator-=(var o);
					var operator*=(var o);
					var operator/=(var o);
					var operator%=(var o);
					var operator&=(var o);	
					var operator|=(var o);
					var operator^=(var o);
					var operator<<=(var o);
					var operator>>=(var o);
					var operator[](var o);

					bool operator<(const var o) const{
						var q=*this;
						var w=o;
						var z=q<w;
						bool x=cast(z,bool);
						return x;
					}
				};

				class python_iterate{
				public:
					var orig;
					python_iterate(var q):orig(q){}
					class iterator{
					public:
						var orig;
						var iter;
						iterator(var q):orig(q),iter(q){
							{python_iftype(orig,python_list){
								iter=cast(orig,decltype(s)).begin();
							}}
							{python_iftype(orig,python_set){
								iter=cast(orig,decltype(s)).begin();
							}}
							{python_iftype(orig,python_dict){
								iter=cast(orig,decltype(s)).begin();
							}}
							{python_iftype(orig,python_str){
								iter=cast(orig,decltype(s)).begin();
							}}
							{python_iftype(orig,python_bytearray){
								iter=cast(orig,decltype(s)).begin();
							}}
						}
						
						void operator++(){
							{python_iftype(orig,python_list){
								 ++cast(iter,decltype(s)::iterator);
							}}
							{python_iftype(orig,python_set){
								 ++cast(iter,decltype(s)::iterator);
							}}
							{python_iftype(orig,python_dict){
								 ++cast(iter,decltype(s)::iterator);
							}}
							{python_iftype(orig,python_str){
								 ++cast(iter,decltype(s)::iterator);
							}}
							{python_iftype(orig,python_bytearray){
								 ++cast(iter,decltype(s)::iterator);
							}}
						}
						bool operator!=(iterator o){
							{python_iftype(orig,python_list){
								return cast(iter,decltype(s)::iterator)!=cast(orig,decltype(s)).end();
							}}
							{python_iftype(orig,python_set){
								return cast(iter,decltype(s)::iterator)!=cast(orig,decltype(s)).end();
							}}
							{python_iftype(orig,python_dict){
								return cast(iter,decltype(s)::iterator)!=cast(orig,decltype(s)).end();
							}}
							{python_iftype(orig,python_str){
								return cast(iter,decltype(s)::iterator)!=cast(orig,decltype(s)).end();
							}}
							{python_iftype(orig,python_bytearray){
								return cast(iter,decltype(s)::iterator)!=cast(orig,decltype(s)).end();
							}}
						}
						var operator*(){
							{python_iftype(orig,python_list){
								return *cast(iter,decltype(s)::iterator);
							}}
							{python_iftype(orig,python_set){
								return *cast(iter,decltype(s)::iterator);
							}}
							{python_iftype(orig,python_dict){
								return (*cast(iter,decltype(s)::iterator)).first;
							}}
							{python_iftype(orig,python_str){
								return python_str({*cast(iter,decltype(s)::iterator)});
							}}
							{python_iftype(orig,python_bytearray){
								return python_bytearray({*cast(iter,decltype(s)::iterator)});
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



// var f(var a){
// 		print_line()
// 	return a;
// }

int main(){
	var s=12;
	var a=var(s);
	cast(a,int)++;
	cout<<cast(s,int)<<endl;
}