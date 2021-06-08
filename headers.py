headers={
	'None':{
		'c++_code':
			'''
				class python_NoneType{};
				python_NoneType python_None;
			''',
		'python_code':'',
		'depends':[]
	},
	'cache':{
		'c++_code':
			'''
				std::map<std::string,var> python_cache;
				var set_cache(var q,std::string w){
					python_cache[w]=q;
					return q;
				}
				var get_cache(std::string w){
					return python_cache[w];
				}
				var del_cache(std::string w){
					auto t=python_cache[w];
					python_cache.erase(w);
					return t;
				}
			''',
		'python_code':'',
		'depends':[]
	},
	'python_variable':{
		'c++_code':
			'''
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
					class iterator{
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
						var operator*(){
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
			''',
		'python_code':'',
		'depends':['any','iostream','string','vector']
	},
	'builtins__wrapper':{
		'c++_code':
			'''
			template<typename t>
			class __python__builtins__wrapper{
			public:
				t d;
				bool bc;
				__python__builtins__wrapper(t f,bool bc_=1){
					d=f;
					bc=bc_;
				}
				var operator()(var q,var w){
					auto a=cast(q,std::vector<var>);
					if (bc){
						for (auto &w:a){
							{python_iftype(w,bool){
								w=int64_t(s);
							}
							}
						}
					}
					if (a.size()==0){
						return d();
					}
					if (a.size()==1){
						return d(a[0]);
					}
					if (a.size()==2){
						return d(a[0],a[1]);
					}
					if (a.size()==3){
						return d(a[0],a[1],a[2]);
					}
					if (a.size()==4){
						return d(a[0],a[1],a[2],a[3]);
					}
					if (a.size()==5){
						return d(a[0],a[1],a[2],a[3],a[4]);
					}
					if (a.size()==6){
						return d(a[0],a[1],a[2],a[3],a[4],a[5]);
					}
					if (a.size()==7){
						return d(a[0],a[1],a[2],a[3],a[4],a[5],a[6]);
					}
					if (a.size()==8){
						return d(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]);
					}
				}
			};
			''',
		'python_code':'',
		'depends':['python_variable','vector']
	},
	'builtins_abs':{
		'c++_code':
			'''
			var __python___abs(var a){
				{python_iftype(a,int){
					return std::abs(s);
				}
				}
				{python_iftype(a,int64_t){
					return std::abs(s);
				}
				}
				{python_iftype(a,long float){
					return std::fabs(s);
				}
				}
			}
			''',
		'python_code':
			'''
			python__builtins__abs=__python__builtins__wrapper(__python__abs)
			''',
		'depends':['python_variable','builtins__wrapper','cmath']
	},
	'builtins_bin':{
		'c++_code':
			'''
			var __python__bin(var a){
				std::string f;
				int64_t d=cast(a,int64_t);
				int64_t s=d<0?1:0;
				d=std::abs(d);
				if (d==0){
					f.push_back('0');
				}
				while (d){
					f.push_back(d%2+'0');
					d/=2;
				}
				reverse(f.begin(),f.end());
				f=std::string({'0','b'})+f;
				if (s){
					f=std::string({'-'})+f;
				}
				return f;
			}
			''',
		'python_code':
			'''
				python__builtins__bin=__python__builtins__wrapper(__python__bin)
			''',
		'depends':['python_variable','cmath','builtins__wrapper','string','algorithm']
	},
	'builtins_bool':{
		'c++_code':
			'''
			var __python__bool(var a=python_None){
				{python_iftype(a,python_NoneType){
					return false;
				}
				}
				{python_iftype(a,int){
					return s!=0;
				}
				}
				{python_iftype(a,bool){
					return s!=0;
				}
				}
				{python_iftype(a,int64_t){
					return s!=0;
				}
				}
				{python_iftype(a,std::string){
					return s.size()!=0;
				}
				}
				{python_iftype(a,std::u32string){
					return s.size()!=0;
				}
				}
				{python_iftype(a,std::vector<var>){
					return s.size()!=0;
				}
				}
				// {python_iftype(a,std::set<var>){
				// 	return s.size()!=0;
				// }
				// }
				// {python_iftype(a,std::map<var,var>){
				// 	return s.size()!=0;
				// }
				// }
			}
			''',
		'python_code':
			'''
				python__builtins__bool=__python__builtins__wrapper(__python__bool)
			''',
		'depends':['python_variable','builtins__wrapper','None','vector','string']
	},
	'builtins_bytearray':{
		'c++_code':
			'''
			var __python__bytearray(var q=std::string(),var w=std::string()){
				{iftype(q,std::string){
					return s;
				}
				}
				{iftype(q,std::u32string){
					return to_u8(q);
				}
				}
				{iftype(q,int64_t){
					vector<char> a(t);
					return std::string(a.begin(),a.end());
				}
				}
				auto a=python_iterate(q)
				return std::string(a.begin(),a.end());
			}
			''',
		'python_code':
			'''
				python__builtins__bytearray=__python__builtins__wrapper(__python__bytearray)
			''',
		'depends':['python_variable','unicode_convert','builtins__wrapper','string']
	},
	'builtins_bytes':{
		'c++_code':
			'''
			''',
		'python_code':
			'''
				python__builtins__bytes=__python__builtins__wrapper(__python__bytearray)
			''',
		'depends':['python_variable','unicode_convert','builtins__wrapper','string']
	},
	'builtins_chr':{
		'c++_code':
			'''
			var __python__chr(var q){
				return std::u32string({chr(cast(q,int64_t))});
			}
			''',
		'python_code':
			'''
				python__builtins__chr=__python__builtins__wrapper(__python__chr)
			''',
		'depends':['python_variable','unicode_convert','builtins__wrapper','string']
	},
	'builtins_divmod':{
		'c++_code':
			'''
			var __python__divmod(var q,var w){
				auto ret=std::vector<var>();
				{python_iftype(q,int64_t){
					auto d=s;
					{python_iftype(w,int64_t){
						ret[0]=d/s;
						ret[1]=d%s;
					}
					}
				}
				}
				if (ret.size()==0){
					q=__python__float(q);
					w=__python__float(w);
					auto e=cast(q,long double);
					auto r=cast(w,long double);
					auto t=std::floor(e/r);
					ret.push_back(t);
					ret.push_back(e-t*r);
				}
				return ret;
			}
			''',
		'python_code':
			'''
				python__builtins__divmod=__python__builtins__wrapper(__python__divmod)
			''',
		'depends':['python_variable','cmath','builtins__wrapper','vector','builtins_float']
	},
	'builtins_float':{
		'c++_code':
			'''
				var __python__float(var q=int64_t(0)){
				//	{python_iftype(q,std::u32string){
				//		return s;
				//	}
				//	}
				//	{python_iftype(q,std::string){
				//		return to_u32(s);
				//	}
				//	}
					{python_iftype(q,int64_t){
						return (long double)(s);
					}
					}
					{python_iftype(q,long double){
						return s;
					}
					}
					{python_iftype(q,int){
						return (long double)(s);
					}
					}
				}
			''',
		'python_code':
			'''
				python__builtins__str=__python__builtins__wrapper(__python__float)
			''',
		'depends':['python_variable','builtins__wrapper','vector','string']
	},
	'builtins_id':{
		'c++_code':
			'''
			var __python__id(var q){
				{python_iftype(q,int64_t){
					return int64_t(&cast(q,decltype(s)));
				}
				}
				{python_iftype(q,long double){
					return int64_t(&cast(q,decltype(s)));
				}
				}
				{python_iftype(q,std::string){
					return int64_t(&cast(q,decltype(s)));
				}
				}
				{python_iftype(q,std::u32string){
					return int64_t(&cast(q,decltype(s)));
				}
				}
				{python_iftype(q,std::vector<var>){
					return int64_t(&cast(q,decltype(s)));
				}
				}
			}
			''',
		'python_code':
			'''
				python__builtins__divmod=__python__builtins__wrapper(__python__divmod,0)
			''',
		'depends':['python_variable','string','builtins__wrapper','vector']
	},
	'builtins_list':{
		'c++_code':
			'''
				var __python__list(var q=std::vector<var>()){
					auto s=std::vector<var>();
					for (var w:python_iterate(q)){
						s.push_back(w);
					}
					return s;
				}
			''',
		'python_code':
			'''
				python__builtins__list=__python__builtins__wrapper(__python__list)
			''',
		'depends':['python_variable','builtins__wrapper','vector']
	},
	'builtins_str':{
		'c++_code':
			'''
				var __python__str(var q=std::u32string()){
					{python_iftype(q,std::u32string){
						return s;
					}
					}
					{python_iftype(q,std::string){
						return to_u32(s);
					}
					}
					{python_iftype(q,int64_t){
						return to_u32(std::to_string(s));
					}
					}
					{python_iftype(q,int){
						return to_u32(std::to_string(s));
					}
					}
					{python_iftype(q,bool){
						return to_u32(s?"True":"False");
					}
					}
				}
			''',
		'python_code':
			'''
				python__builtins__str=__python__builtins__wrapper(__python__str,0)
			''',
		'depends':['python_variable','builtins__wrapper','vector','string']
	},
	'unicode_convert':{
		'c++_code':
			r'''
				char32_t chr(int64_t q){
					if(q<(1<<7)){
						return ((q&127)<<0);
					}
					if(q<(1<<11)){
						return 49280+((q&1984)<<2)+((q&63)<<0);
					}
					if(q<(1<<16)){
						return 14712960+((q&61440)<<4)+((q&4032)<<2)+((q&63)<<0);
					}
					if(q<(1<<21)){
						return 4034953344+((q&1835008)<<6)+((q&258048)<<4)+((q&4032)<<2)+((q&63)<<0);
					}
					return 0;
				}

				int64_t ord(char32_t q){
					int64_t r=0;
					int w,e;
					for (w=3*8;w>-1;w-=8){
						int started=0;
						for (e=7;e>-1;--e){
							if (started==0 and (q&(1<<(w+e)))==0){
								started=1;
							} else
							if (started){
								r=(r<<1)+!!(q&(1<<(w+e)));
							}
						}
					}
					return r;
				}

				std::u32string to_u32(std::string q){
					std::u32string r;
					for(int64_t w=0;w<q.size();++w){
						if ((q[w]&(0b10000000))==0){
							r.push_back(((int32_t(uint8_t(q[w]))<<0)));
						}
						if ((q[w]&(0b11100000))==0b11000000 and w<q.size()-1){
							r.push_back(((int32_t(uint8_t(q[w]))<<8)+(int32_t(uint8_t(q[w+1]))<<0)));
						}
						if ((q[w]&(0b11110000))==0b11100000 and w<q.size()-2){
							r.push_back(((int32_t(uint8_t(q[w]))<<16)+(int32_t(uint8_t(q[w+1]))<<8)+(int32_t(uint8_t(q[w+2]))<<0)));
						}
						if ((q[w]&(0b11111000))==0b11110000 and w<q.size()-3){
							r.push_back(((int32_t(uint8_t(q[w]))<<24)+(int32_t(uint8_t(q[w+1]))<<16)+(int32_t(uint8_t(q[w+2]))<<8)+(int32_t(uint8_t(q[w+3]))<<0)));
						}
					}
					for(auto &w:r){
						w=ord(w);
					}
					return r;
				}

				std::string to_u8(std::u32string q){
					for(auto &w:q){
						w=chr(w);
					}	
					std::string r;
					for(auto w:q){
						if (w&0b11111111000000000000000000000000){
							r.push_back((w&0b11111111000000000000000000000000)>>24);
						}
						if (w&0b111111110000000000000000){
							r.push_back((w&0b111111110000000000000000)>>16);
						}
						if (w&0b1111111100000000){
							r.push_back((w&0b1111111100000000)>>8);
						}
						r.push_back(w&0b11111111);
					}
					return r;
				}
			''',
		'python_code':'',
		'depends':['string']
	},
	'debug_str':{
		'c++_code':
		'''
				std::string python_debug_str(var a){
					std::string d="type not found";
					{python_iftype(a,std::string)d=s;}
					{python_iftype(a,std::u32string)d=to_u8(s);}
					{python_iftype(a,int)d=std::to_string(s);}
					{python_iftype(a,int64_t)d=std::to_string(s);}
					{python_iftype(a,long double)d=std::to_string(s);}
					{python_iftype(a,bool)d=s?"True":"False";}
					return d;
				}
		''',
		'python_code':'',
		'depends':
			['python_variable','unicode_convert'],
	},
	# 'operator_UAdd':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_UAdd(var q){
	# 			{python_iftype(q,int64_t){
	# 				return s;
	# 			}
	# 			}
	# 			{python_iftype(q,long double){
	# 				return s;
	# 			}
	# 			}
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable'],
	# },
	# 'operator_USub':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_USub(var q){
	# 			{python_iftype(q,int64_t){
	# 				return -s;
	# 			}
	# 			}
	# 			{python_iftype(q,long double){
	# 				return -s;
	# 			}
	# 			}
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable'],
	# },
	'operator_Not':{
		'c++_code':
		'''
			var python_operator_Not(var q){
				q=__python__bool(q);
				{python_iftype(q,bool){
					return !s;
				}
				}
			}
		''',
		'python_code':'',
		'depends':
			['python_variable'],
	},
	# 'operator_Invert':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_Invert(var q){
	# 			q=__python__int(q);
	# 			{python_iftype(q,int64_t){
	# 				return ~s;
	# 			}
	# 			}
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable'],
	# },
	# 'operator_Add':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_Add(var q,var w){
	# 			{python_iftype(q,int64_t){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					return d+s;
	# 				}
	# 				}
	# 				{python_iftype(w,long double){
	# 					return d+s;
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,long double){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					return d+s;
	# 				}
	# 				}
	# 				{python_iftype(w,long double){
	# 					return d+s;
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,std::string){
	# 				auto &d=s;
	# 				{python_iftype(w,std::string){
	# 					return d+s;
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,std::u32string){
	# 				auto &d=s;
	# 				{python_iftype(w,std::u32string){
	# 					return d+s;
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,std::vector<var>){
	# 				auto &d=s;
	# 				{python_iftype(w,std::vector<var>){
	# 					auto r=std::vector<var>(d.begin(),d.end());
	# 					r.insert(r.end(),s.begin(),s.end());
	# 					return r;
	# 				}
	# 				}
	# 			}
	# 			}
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable','string','vector'],
	# },
	# 'operator_Sub':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_Sub(var q,var w){
	# 			{python_iftype(q,int64_t){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					return d-s;
	# 				}
	# 				}
	# 				{python_iftype(w,long double){
	# 					return d-s;
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,long double){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					return d-s;
	# 				}
	# 				}
	# 				{python_iftype(w,long double){
	# 					return d-s;
	# 				}
	# 				}
	# 			}
	# 			}
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable'],
	# },
	# 'operator_Mult':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_Mult(var q,var w){
	# 			{python_iftype(q,int64_t){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					return d*s;
	# 				}
	# 				}
	# 				{python_iftype(w,long double){
	# 					return d*s;
	# 				}
	# 				}
	# 				{python_iftype(w,std::string){
	# 					return python_operator_Mult(w,q);
	# 				}
	# 				}
	# 				{python_iftype(w,std::u32string){
	# 					return python_operator_Mult(w,q);
	# 				}
	# 				}
	# 				{python_iftype(w,std::vector<var>){
	# 					return python_operator_Mult(w,q);
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,long double){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					return d*s;
	# 				}
	# 				}
	# 				{python_iftype(w,long double){
	# 					return d*s;
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,std::string){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					auto r=std::string();
	# 					for (auto e=0;e<w;++e){
	# 						r+=q;
	# 					}
	# 					return r;
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,std::u32string){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					auto r=std::u32string();
	# 					for (auto e=0;e<w;++e){
	# 						r+=q;
	# 					}
	# 					return r;
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,std::vector<var>){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					auto r=std::vector<var>();
	# 					for (auto e=0;e<w;++e){
	# 						r.insert(r.end(),q.begin(),q.end());
	# 					}
	# 					return r;
	# 				}
	# 				}
	# 			}
	# 			}
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable','string','vector'],
	# },
	# 'operator_Div':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_Div(var q,var w){
	# 			{python_iftype(q,int64_t){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					return (long double)(1.0)*d/s;
	# 				}
	# 				}
	# 				{python_iftype(w,long double){
	# 					return d/s;
	# 				}
	# 				}
	# 			}
	# 			}
	# 			{python_iftype(q,long double){
	# 				auto &d=s;
	# 				{python_iftype(w,int64_t){
	# 					return d/s;
	# 				}
	# 				}
	# 				{python_iftype(w,long double){
	# 					return d/s;
	# 				}
	# 				}
	# 			}
	# 			}
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable'],
	# },
	# 'operator_FloorDiv':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_FloorDiv(var q,var w){
	# 			return __python__divmod(q,w)[0];
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable','builtins_divmod'],
	# },
	# 'operator_Mod':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_Mod(var q,var w){
	# 			return __python__divmod(q,w)[1];
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable','builtins_divmod'],
	# },
	'operator_Pow':{
		'c++_code':
		'''
			auto python_operator_Pow=__python__pow;
		''',
		'python_code':'',
		'depends':
			['python_variable','builtins_pow'],
	},
	# 'operator_Eq':{
	# 	'c++_code':
	# 	'''
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable'],
	# },
	# 'operator_NotEq':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_NotEq(var q,var w){
	# 			return python_operator_Not(python_operator_Eq(q,w));
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable','operator_Eq'],
	# },
	# 'operator_Lt':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_LtE(var q,var w){
	# 			{python_iftype(q,int64_t){
	# 				auto &d=s;
	# 			}
	# 			}
	# 			{python_iftype(q,int64_t){
	# 				auto &d=s;
	# 			}
	# 			}
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable'],
	# },
	# 'operator_LtE':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_LtE(var q,var w){
	# 			return python_operator_Not(python_operator_Gt(q,w));
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable','operator_Gr'],
	# },
	# 'operator_Gt':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_Gt(var q,var w){
	# 			return python_operator_Lt(w,q);
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable'],
	# },
	# 'operator_GtE':{
	# 	'c++_code':
	# 	'''
	# 		var python_operator_GtE(var q,var w){
	# 			return python_operator_Not(python_operator_Lt(q,w));
	# 		}
	# 	''',
	# 	'python_code':'',
	# 	'depends':
	# 		['python_variable','operator_Lt'],
	# },
	'operator_Is':{
		'c++_code':
		'''
			var python_operator_Is(var q,var w){
				return python_operator_Eq(__python__id(q),__python__id(w));
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','builtins_id','operator_Eq'],
	},
	'operator_IsNot':{
		'c++_code':
		'''
			var python_operator_IsNot(var q,var w){
				return python_operator_Not(python_operator_Is(q,w));
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','operator_Is'],
	},
	'operator_In':{
		'c++_code':
		'''
			var python_operator_NotIn(var q,var w){
				for (auto e:python_iterate(w)){
					if (operator_Eq(q,e)){
						return true;
					}
				}
				return false;
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','operator_Eq'],
	},
	'operator_NotIn':{
		'c++_code':
		'''
			var python_operator_NotIn(var q,var w){
				return python_operator_Not(python_operator_In(q,w));
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','operator_In'],
	},
	'stdc++':{'c++_code':'#include<bits/stdc++.h>','python_code':'','depends':[]},
	'vector':{'c++_code':'#include<vector>','python_code':'','depends':[]},
	'string':{'c++_code':'#include<string>','python_code':'','depends':[]},
	'iostream':{'c++_code':'#include<iostream>','python_code':'','depends':[]},
	'algorithm':{'c++_code':'#include<algorithm>','python_code':'','depends':[]},
	'map':{'c++_code':'#include<map>','python_code':'','depends':[]},
	'any':{'c++_code':'#include<any>','python_code':'','depends':[]},
	'cmath':{'c++_code':'#include<cmath>','python_code':'','depends':[]},
	'cstdio':{'c++_code':'#include<cstdio>','python_code':'','depends':[]},
	'levels':{
		'c++_code':
			r'''
				#define python_level_type_first std::u32string
				#define python_level_type_second var
				std::vector<std::map<python_level_type_first,python_level_type_second*>> python_globals;
				#define python_global(q)\
				 	if (python_globals[python_globals.size()-1].find(q) == python_globals[python_globals.size()-1].end()){\
						python_locals[q]=int64_t(0);\
						python_globals[python_globals.size()-1][q]=&(python_locals[q]);\
					}\
					python_globals[python_globals.size()-1][q]=python_globals[0][q];\
					
				#define python_nonlocal(q)\
				 	if (python_globals[python_globals.size()-1].find(q) == python_globals[python_globals.size()-1].end()){\
						python_locals[q]=int64_t(0);\
						python_globals[python_globals.size()-1][q]=&(python_locals[q]);\
					}\
					python_globals[python_globals.size()-1][q]=python_globals[python_globals.size()-2][q];
					
				#define python_get(q) (*(python_globals[python_globals.size()-1][q]))

				#define python_set(q) python_set_(q,&python_locals)

				python_level_type_second& python_set_(python_level_type_first q,std::map<python_level_type_first,python_level_type_second> *python_locals_pointer){
					if (python_globals[python_globals.size()-1].find(q) == python_globals[python_globals.size()-1].end()){
						(*python_locals_pointer)[q]=int64_t(0);
						python_globals[python_globals.size()-1][q]=&((*python_locals_pointer)[q]);
					}
					return *(python_globals[python_globals.size()-1][q]);
				}

				#define python_create_level()\
					python_globals.emplace_back();\
					std::map<python_level_type_first,python_level_type_second> python_locals;

				#define python_delete_level()\
					python_globals.pop_back();
			''',
		'python_code':'',
		'depends':
			['vector','string','map','python_variable'],
	},
}


operators=[
	{'name':'UAdd',		'sign':'+',		'args':1},
	{'name':'USub',		'sign':'-',		'args':1},
	{'name':'Invert',	'sign':'~',		'args':1},
	{'name':'Add',		'sign':'+',		'args':2},
	{'name':'Sub',		'sign':'-',		'args':2},
	{'name':'Mult',		'sign':'*',		'args':2},
	{'name':'Div',		'sign':'/',		'args':2},
	{'name':'FloorDiv',	'sign':'/',		'args':2},
	{'name':'Mod',		'sign':'%',		'args':2},
	{'name':'LShift',	'sign':'<<',	'args':2},
	{'name':'RShift',	'sign':'>>',	'args':2},
	{'name':'BitOr',	'sign':'|',		'args':2},
	{'name':'BitXor',	'sign':'^',		'args':2},
	{'name':'BitAnd',	'sign':'&',		'args':2},
	{'name':'Eq',		'sign':'==',	'args':2},
	{'name':'NotEq',	'sign':'!=',	'args':2},
	{'name':'Lt',		'sign':'<',		'args':2},
	{'name':'LtE',		'sign':'<=',	'args':2},
	{'name':'Gt',		'sign':'>',		'args':2},
	{'name':'GtE',		'sign':'>=',	'args':2},
]

rules={
	('std::vector<var>','Add','std::vector<var>'):{
		'c++_code':
			'''
				auto r=std::vector<var>(a.begin(),a.end());
				r.insert(r.end(),s.begin(),s.end());
				return r;
			''',
	},
	('std::vector<var>','Add','std::u32string'):{
		'c++_code':
			'''
				auto r=std::vector<var>(a.begin(),a.end());
				for (auto w:s){
					r.push_back(std::u32string({w}));
				}
				return r;
			''',
	},
	('std::vector<var>','Add','std::string'):{
		'c++_code':
			'''
				auto r=std::vector<var>(a.begin(),a.end());
				for (auto w:s){
					r.push_back(std::string({w}));
				}
				return r;
			''',
	},
	('std::vector<var>','Mult','int64_t'):{
		'c++_code':
			'''
				auto r=decltype(a)();
				for (int64_t e=0;e<s;++e){
					r.insert(r.end(),a.begin(),a.end());
				}
				return r;
			''',
	},
	('int64_t','Mult','vector<var>'):{
		'c++_code':
			'''
				auto r=decltype(s)();
				for (int64_t e=0;e<a;++e){
					r.insert(r.end(),s.begin(),s.end());
				}
				return r;
			''',
	},
	('std::u32string','Mult','int64_t'):{
		'c++_code':
			'''
				auto r=decltype(a)();
				for (int64_t e=0;e<s;++e){
					r.insert(r.end(),a.begin(),a.end());
				}
				return r;
			''',
	},
	('int64_t','Mult','u32string'):{
		'c++_code':
			'''
				auto r=decltype(s)();
				for (int64_t e=0;e<a;++e){
					r.insert(r.end(),s.begin(),s.end());
				}
				return r;
			''',
	},
	('std::string','Mult','int64_t'):{
		'c++_code':
			'''
				auto r=decltype(a)();
				for (int64_t e=0;e<s;++e){
					r.insert(r.end(),a.begin(),a.end());
				}
				return r;
			''',
	},
	('int64_t','Mult','string'):{
		'c++_code':
			'''
				auto r=decltype(s)();
				for (int64_t e=0;e<a;++e){
					r.insert(r.end(),s.begin(),s.end());
				}
				return r;
			''',
	},
	('int64_t','Div','int64_t'):{
		'c++_code':
			'''
				return (long double)(1.0)*a/s;
			''',
	},
	('int64_t','Div','bool'):{
		'c++_code':
			'''
				return (long double)(1.0)*a/s;
			''',
	},
	('bool','Div','int64_t'):{
		'c++_code':
			'''
				return (long double)(1.0)*a/s;
			''',
	},
	('bool','Div','bool'):{
		'c++_code':
			'''
				return (long double)(1.0)*a/s;
			''',
	},
	('long double','FloorDiv','long double'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[0];
			''',
		'depends':['builtins_divmod']
	},
	('long double','FloorDiv','int64_t'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[0];
			''',
		'depends':['builtins_divmod']
	},
	('long double','FloorDiv','bool'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[0];
			''',
		'depends':['builtins_divmod']
	},
	('int64_t','FloorDiv','long double'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[0];
			''',
		'depends':['builtins_divmod']
	},
	('bool','FloorDiv','long double'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[0];
			''',
		'depends':['builtins_divmod']
	},
	('long double','Mod','long double'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[1];
			''',
		'depends':['builtins_divmod']
	},
	('long double','Mod','int64_t'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[1];
			''',
		'depends':['builtins_divmod']
	},
	('long double','Mod','bool'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[1];
			''',
		'depends':['builtins_divmod']
	},
	('int64_t','Mod','long double'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[1];
			''',
		'depends':['builtins_divmod']
	},
	('bool','Mod','long double'):{
		'c++_code':
			'''
				return cast(__python__divmod(q,w),std::vector<var>)[1];
			''',
		'depends':['builtins_divmod']
	},
}


support='''
long double     |3|333000
int64_t         |3|333000
bool            |3|333000
std::string     |0|000100
std::u32string  |0|000010
std::vector<var>|0|000001
'''

support=[w.split('|') for w in support.strip().split('\n')]
support=[ [w[0].strip(),int(w[1]),[int(e) for e in w[2]]] for w in support]
types=[w[0] for w in support]
support=[w[1:] for w in support]
support=list(zip(*support))
support=dict([[types[w],support[0][w]] for w in range(len(support[0]))]+[[(types[w],types[e]),support[1][w][e]] for w in range(len(support[1])) for e in range(len(support[1][w]))])

usual=[
]

not_supported=[
]

op_names=[
	[                                                                                                                                                                  ],
	[                          'Add',                                                                                           'Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE'],
	[                                                                                              'BitOr', 'BitXor', 'BitAnd', 'Eq', 'NotEq',                         ],
	['UAdd', 'USub', 'Invert', 'Add', 'Sub', 'Mult', 'Div', 'FloorDiv', 'Mod', 'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd', 'Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE'],
]



def make_code(q,w,e=None):
	if e!=None:
		if (q,w,e) in rules:
			return\
				'\t{python_iftype(q,'+q+'){\n'+\
				'\t\t{python_iftype(w,'+e+'){\n'+\
				'\t\t\tauto a=cast(q,'+q+');\n'+\
				rules[(q,w,e)]['c++_code']+\
				'\t\t}}\n'+\
				'\t}}\n'
		if (q,w,e) in not_supported:
			return ''
		if op['name'] in op_names[support[(q,e)]] or (q,w,e) in usual:
			return\
				'\t{python_iftype(q,'+q+'){\n'+\
				'\t\t{python_iftype(w,'+e+'){\n'+\
				'\t\t\tauto a=cast(q,'+q+');\n'+\
				'\t\t\treturn a'+[r['sign'] for r in operators if r['name']==w][0]+'s;'+\
				'\t\t}}\n'+\
				'\t}}\n'				
		return ''
	else:
		q,w,e=w,q,w
		if (w,e) in rules:
			return\
				'\t{python_iftype(q,'+q+'){\n'+\
				'\t\tauto a=cast(q,'+q+');\n'+\
				rules[(w,e)]+\
				'\t}}\n'
		if (w,e) in not_supported:
			return ''
		if op['name'] in op_names[support[q]] or (w,e) in usual:
			return\
				'\t{python_iftype(q,'+q+'){\n'+\
				'\t\treturn '+[r['sign'] for r in operators if r['name']==w][0]+'s;'+\
				'\t}}\n'				
		return ''

for op in operators:
	typelist=[[]]
	for w in range(op['args']):
		typelist=[e+[r] for e in typelist for r in types]
	headers['operator_'+op['name']]={'c++_code':'var python_operator_'+op['name']+'('+','.join(['var '+'qw'[w] for w in range(op['args'])])+'){\n'\
	+''.join([
		make_code(ts[0],op['name'],ts[1]) if len(ts)==2 else make_code(op['name'],ts[0])
	for ts in typelist])\
	+'\tstd::cout<<'+('q.type().name()<<' if op['args']==2 else '')+'"'+op['sign']+'"<<'+'qw'[op['args']-1]+'.type().name()'+'<<" is unsupported"<<std::endl;\n'\
	+'\treturn int64_t(0);}',
	'python_code':'','depends':['iostream','vector','string']+sum([
			rules[w]['depends']
		for w in [
			((w[0],op['name'],w[1]) if len(w)==2 else (op['name'],w[0]))
		for w in typelist]
		if w in rules and 'depends' in rules[w]],[])}

from json import dumps
from os.path import dirname
open(str(dirname(__file__))+'/headers.json','w').write(dumps(headers))
