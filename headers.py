headers={}

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
	{'name':'In',		'sign':'',		'args':2},
	{'name':'NotIn',	'sign':'',		'args':2},
	{'name':'Is',		'sign':'',		'args':2},
	{'name':'InNot',	'sign':'',		'args':2},
]

rules={
	('python_list','Add','python_list'):{
		'c++_code':
			r'''
				auto r=python_list(a.begin(),a.end());
				r.insert(r.end(),s.begin(),s.end());
				return r;
			''',
	},
	('python_list','Add','python_str'):{
		'c++_code':
			r'''
				auto r=python_list(a.begin(),a.end());
				for (auto w:s){
					r.push_back(python_str({w}));
				}
				return r;
			''',
	},
	('python_list','Add','python_bytearray'):{
		'c++_code':
			r'''
				auto r=python_list(a.begin(),a.end());
				for (auto w:s){
					r.push_back(python_bytearray({w}));
				}
				return r;
			''',
	},
	('python_list','Mult','python_int'):{
		'c++_code':
			r'''
				auto r=decltype(a)();
				for (python_int e=0;e<s;++e){
					r.insert(r.end(),a.begin(),a.end());
				}
				return r;
			''',
	},
	('python_int','Mult','python_list'):{
		'c++_code':
			r'''
				auto r=decltype(s)();
				for (python_int e=0;e<a;++e){
					r.insert(r.end(),s.begin(),s.end());
				}
				return r;
			''',
	},
	('python_list','Mult','python_bool'):{
		'c++_code':
			r'''
				auto r=decltype(a)();
				for (python_int e=0;e<s;++e){
					r.insert(r.end(),a.begin(),a.end());
				}
				return r;
			''',
	},
	('python_bool','Mult','python_list'):{
		'c++_code':
			r'''
				auto r=decltype(s)();
				for (python_int e=0;e<a;++e){
					r.insert(r.end(),s.begin(),s.end());
				}
				return r;
			''',
	},
	('python_str','Mult','python_int'):{
		'c++_code':
			r'''
				auto r=decltype(a)();
				for (python_int e=0;e<s;++e){
					r.insert(r.end(),a.begin(),a.end());
				}
				return r;
			''',
	},
	('python_int','Mult','python_str'):{
		'c++_code':
			r'''
				auto r=decltype(s)();
				for (python_int e=0;e<a;++e){
					r.insert(r.end(),s.begin(),s.end());
				}
				return r;
			''',
	},
	('python_str','Mult','python_bool'):{
		'c++_code':
			r'''
				auto r=decltype(a)();
				for (python_int e=0;e<s;++e){
					r.insert(r.end(),a.begin(),a.end());
				}
				return r;
			''',
	},
	('python_bool','Mult','python_str'):{
		'c++_code':
			r'''
				auto r=decltype(s)();
				for (python_int e=0;e<a;++e){
					r.insert(r.end(),s.begin(),s.end());
				}
				return r;
			''',
	},
	('python_bytearray','Mult','python_int'):{
		'c++_code':
			r'''
				auto r=decltype(a)();
				for (python_int e=0;e<s;++e){
					r.insert(r.end(),a.begin(),a.end());
				}
				return r;
			''',
	},
	('python_int','Mult','python_bytearray'):{
		'c++_code':
			r'''
				auto r=decltype(s)();
				for (python_int e=0;e<a;++e){
					r.insert(r.end(),s.begin(),s.end());
				}
				return r;
			''',
	},
	('python_bytearray','Mult','python_bool'):{
		'c++_code':
			r'''
				auto r=decltype(a)();
				for (python_int e=0;e<s;++e){
					r.insert(r.end(),a.begin(),a.end());
				}
				return r;
			''',
	},
	('python_bool','Mult','python_bytearray'):{
		'c++_code':
			r'''
				auto r=decltype(s)();
				for (python_int e=0;e<a;++e){
					r.insert(r.end(),s.begin(),s.end());
				}
				return r;
			''',
	},

	('python_int','Div','python_int'):{
		'c++_code':
			r'''
				return (python_float)(1.0)*a/s;
			''',
	},
	('python_int','Div','python_bool'):{
		'c++_code':
			r'''
				return (python_float)(1.0)*a/s;
			''',
	},
	('python_bool','Div','python_int'):{
		'c++_code':
			r'''
				return (python_float)(1.0)*a/s;
			''',
	},
	('python_bool','Div','python_bool'):{
		'c++_code':
			r'''
				return (python_float)(1.0)*a/s;
			''',
	},
	('python_float','FloorDiv','python_float'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[0];
			''',
		'depends':['builtins_divmod']
	},
	('python_float','FloorDiv','python_int'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[0];
			''',
		'depends':['builtins_divmod']
	},
	('python_float','FloorDiv','python_bool'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[0];
			''',
		'depends':['builtins_divmod']
	},
	('python_int','FloorDiv','python_float'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[0];
			''',
		'depends':['builtins_divmod']
	},
	('python_bool','FloorDiv','python_float'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[0];
			''',
		'depends':['builtins_divmod']
	},
	('python_float','Mod','python_float'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[1];
			''',
		'depends':['builtins_divmod']
	},
	('python_float','Mod','python_int'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[1];
			''',
		'depends':['builtins_divmod']
	},
	('python_float','Mod','python_bool'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[1];
			''',
		'depends':['builtins_divmod']
	},
	('python_int','Mod','python_float'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[1];
			''',
		'depends':['builtins_divmod']
	},
	('python_bool','Mod','python_float'):{
		'c++_code':
			r'''
				return cast(__python__divmod(q,w),python_list)[1];
			''',
		'depends':['builtins_divmod']
	},

	('python_int','Add','python_complex'):{
		'c++_code':
			r'''
				return (python_float)(a)+s;
			''',
		'depends':['builtins_divmod']
	},
	('python_int','Sub','python_complex'):{
		'c++_code':
			r'''
				return (python_float)(a)-s;
			''',
		'depends':['builtins_divmod']
	},
	('python_int','Mult','python_complex'):{
		'c++_code':
			r'''
				return (python_float)(a)*s;
			''',
		'depends':['builtins_divmod']
	},
	('python_int','Div','python_complex'):{
		'c++_code':
			r'''
				return (python_float)(a)/s;
			''',
		'depends':['builtins_divmod']
	},
	('python_bool','Add','python_complex'):{
		'c++_code':
			r'''
				return (python_float)(a)+s;
			''',
		'depends':['builtins_divmod']
	},
	('python_bool','Sub','python_complex'):{
		'c++_code':
			r'''
				return (python_float)(a)-s;
			''',
		'depends':['builtins_divmod']
	},
	('python_bool','Mult','python_complex'):{
		'c++_code':
			r'''
				return (python_float)(a)*s;
			''',
		'depends':['builtins_divmod']
	},
	('python_bool','Div','python_complex'):{
		'c++_code':
			r'''
				return (python_float)(a)/s;
			''',
		'depends':['builtins_divmod']
	},
	('python_complex','Add','python_int'):{
		'c++_code':
			r'''
				return a+(python_float)(s);
			''',
		'depends':['builtins_divmod']
	},
	('python_complex','Sub','python_int'):{
		'c++_code':
			r'''
				return a-(python_float)(s);
			''',
		'depends':['builtins_divmod']
	},
	('python_complex','Mult','python_int'):{
		'c++_code':
			r'''
				return a*(python_float)(s);
			''',
		'depends':['builtins_divmod']
	},
	('python_complex','Div','python_int'):{
		'c++_code':
			r'''
				return a/(python_float)(s);
			''',
		'depends':['builtins_divmod']
	},
	('python_complex','Add','python_bool'):{
		'c++_code':
			r'''
				return a+(python_float)(s);
			''',
		'depends':['builtins_divmod']
	},
	('python_complex','Sub','python_bool'):{
		'c++_code':
			r'''
				return a-(python_float)(s);
			''',
		'depends':['builtins_divmod']
	},
	('python_complex','Mult','python_bool'):{
		'c++_code':
			r'''
				return a*(python_float)(s);
			''',
		'depends':['builtins_divmod']
	},
	('python_complex','Div','python_bool'):{
		'c++_code':
			r'''
				return a/(python_float)(s);
			''',
		'depends':['builtins_divmod']
	},
	('python_set','Sub','python_set'):{
		'c++_code':
			r'''
				auto z=python_set(a);
				for (auto x:s){
					z.erase(x);
				}
				return z;
			''',
		'depends':['builtins_divmod']
	},
}


support='''
python_complex                  |7|77770000000
python_float                    |8|78880000000
python_int                      |9|78993330000
python_bool                     |9|78993330000
python_bytearray                |0|00334000000
python_str                      |0|00330400000
python_list                     |0|00330040000
python_set                      |0|00000006000
python_dict                     |0|00000000500
python_NoneType                 |0|00000000000
python_ellipsis                 |0|00000000000
'''

# support='''
# python_complex                  |7|77000000000
# python_float                    |8|78880000000
# python_int                      |9|08990000000
# python_bool                     |9|08990000000
# python_bytearray                |0|00004000000
# python_str                      |0|00000400000
# python_list                     |0|00000040000
# python_set                      |0|00000006000
# python_dict                     |0|00000000500
# python_NoneType                 |0|00000000000
# python_ellipsis                 |0|00000000000
# '''

support=[w.split('|') for w in support.strip().split('\n')]
support=[ [w[0].strip(),int(w[1]),[int(e) for e in w[2]]] for w in support]
types=[w[0] for w in support]
support=[w[1:] for w in support]
support=list(zip(*support))
support=dict([[types[w],support[0][w]] for w in range(len(support[0]))]+[[(types[w],types[e]),support[1][w][e]] for w in range(len(support[1])) for e in range(len(support[1][w]))])

usual=[
]

not_supported=[
	# ('python_list','Eq','python_list')
]

op_names=[
	[0,                                                                                                                         ],
	[1,                                                                                                                         ],
	[2,                                                                                                                         ],
	[3,                                        'Mult',                                                                          ],
	[4,                          'Add',                                                                                         ],
	[5,                                                                                              'BitOr',                   ],
	[6,                                 'Sub',                                                       'BitOr', 'BitXor', 'BitAnd'],
	[7,'UAdd', 'USub',           'Add', 'Sub', 'Mult', 'Div',                                                                   ],
	[8,'UAdd', 'USub',           'Add', 'Sub', 'Mult', 'Div', 'FloorDiv', 'Mod',                                                ],
	[9,'UAdd', 'USub', 'Invert', 'Add', 'Sub', 'Mult', 'Div', 'FloorDiv', 'Mod', 'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd'],
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
				'\t\t\treturn a'+[r['sign'] for r in operators if r['name']==w][0]+'s;\n'+\
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
				'\t\treturn '+[r['sign'] for r in operators if r['name']==w][0]+'s;\n'+\
				'\t}}\n'				
		return ''

for op in [op for op in operators if op['name'] in sum(op_names,[])]:
	typelist=[[]]
	for w in range(op['args']):
		typelist=[e+[r] for e in typelist for r in types]
	# headers['operator_'+op['name']]={'c++_code':'var python_operator_'+op['name']+'('+','.join(['var '+'qw'[w] for w in range(op['args'])])+'){\n'\
	# print('operator_'+op['name'])
	headers['operator_'+op['name']]={'c++_code':'var var::operator'+op['sign']+'('+','.join(['var '+'qw'[w] for w in range(1,op['args'])])+'){\n'\
	+'\tvar&q=*this;\n'\
	+''.join([
		make_code(ts[0],op['name'],ts[1]) if len(ts)==2 else make_code(op['name'],ts[0])
	for ts in typelist])\
	+'\tstd::cout<<'+('filt(q.type().name())<<' if op['args']==2 else '')+'" '+op['sign']+' "<<filt('+'qw'[op['args']-1]+'.type().name())'+'<<" is unsupported"<<std::endl;\n'\
	+'\tfend()}',
	'python_code':'','depends':['iostream','vector','string','filt','complex']+sum([
			rules[w]['depends']
		for w in [
			((w[0],op['name'],w[1]) if len(w)==2 else (op['name'],w[0]))
		for w in typelist]
		if w in rules and 'depends' in rules[w]],[])}

def same_for_all_types(vars_,code,types=types):
	ind=max([len(w[:w.index(w.strip())]) for w in code.split('\n')])-1
	typelist=[[]]
	for w in range(len(vars_)):
		typelist=[e+[r] for e in typelist for r in types]
	return '\n'.join([
		 ''.join(['\t'*ind+'\t'*w+'{python_iftype('+vars_[w]+','+ts[w]+'){auto '+vars_[w]+'s=s;\n' for w in range(len(vars_))])\
		+'\t'*(ind+len(vars_))+code.strip()+'\n'\
		+''.join(['\t'*ind+'\t'*w+'}}\n' for w in range(len(vars_)-1,-1,-1)])\
	for ts in typelist])



headers.update({
	'python__bool':{
		'c++_code':
			r'''
				bool python__bool(var q){
					return cast(__python__bool(q),bool);
				}
			''',
		'python_code':'',
		'depends':['python_variable','builtins_bool']
	},
	'cache':{
		'c++_code':
			r'''
				std::map<python_bytearray,var> python_cache;
				var set_cache(var q,python_bytearray w){
					python_cache[w]=q;
					return q;
				}
				var get_cache(python_bytearray w){
					return python_cache[w];
				}
				var del_cache(python_bytearray w){
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
			r'''


				#define fend(q) std::cout<<"line "<<__LINE__<<":\n\tunexpected exit from function"<<std::endl;return make_value(q);

				class python_NoneType{};
				python_NoneType python_None;

				class python_ellipsis{};
				python_ellipsis python_Ellipsis;

				template <typename T=python_NoneType>
				auto make_value(T a=python_None){
					return a;
				}

				#define python_complex				std::complex<double>
				#define python_float				double
				#define python_int					int64_t
				#define python_bool					bool
				#define python_bytearray			std::string
				#define python_bytes				std::string
				#define python_str					std::u32string
				#define python_list					std::vector<var>
				#define python_set					std::set<var>
				#define python_dict					std::map<var,var>
				#define python_NoneType				python_NoneType
				#define python_ellipsis				python_ellipsis




				#define python_iftype(a,...) __VA_ARGS__ s;\
					if (var(a).type()==typeid(std::declval<python_variable<__VA_ARGS__>>())){\
						s=cast(var(a),__VA_ARGS__);\
					}\
					if (var(a).type()==typeid(std::declval<python_variable<__VA_ARGS__>>()))

				#define cast(q,...) (var(q).cast_with_line<__VA_ARGS__>(__LINE__))

				#define super_cast(q,...) cast(__python__##__VA_ARGS__(q),python_##__VA_ARGS__)

				#define print_line() std::cout<<__LINE__<<std::endl;

				template<typename T>
				class python_variable{
				public:
					T*p;
					python_int*c;
					T &value(){
						return *p;
					}
					python_variable(T a=python_int(0)){
						c=new python_int(1);
						p=new T(a);
					}
					python_variable(const python_variable &a){
						p=a.p;
						c=a.c;
						*c+=1;
					}
					python_variable operator=(T a){
						c=new python_int(1);
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
				T &from_var(std::any q,python_int line){
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
						a=to_var(python_int(0));
					}
					template<typename t>
					var operator=(t q){
						a=to_var(q);
						return *this;
					}
					template<typename t>
					t &cast_with_line(python_int line){
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
					bool operator<(const var o) const;
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
							int64_t c=0;
							{python_iftype(orig,python_list){
								iter=cast(orig,decltype(s)).begin();
								c=1;
							}}
							{python_iftype(orig,python_set){
								iter=cast(orig,decltype(s)).begin();
								c=1;
							}}
							{python_iftype(orig,python_dict){
								iter=cast(orig,decltype(s)).begin();
								c=1;
							}}
							{python_iftype(orig,python_str){
								iter=cast(orig,decltype(s)).begin();
								c=1;
							}}
							{python_iftype(orig,python_bytearray){
								iter=cast(orig,decltype(s)).begin();
								c=1;
							}}
							if(!c){
								std::cout<<filt(orig.type().name())<<" is not iterable"<<std::endl;
							}
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
							fend(0)
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
							fend();
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
		'python_code':'Ellipsis=...',
		'depends':['any','iostream','string','vector','filt','set','map','complex','initializer_list','stdc++']
	},
	'cmp':{
		'c++_code':
			r'''
				python_int cmp(var q,var w){
					'''+same_for_all_types(['q','w'],r'''
						auto qa=cast(__python__complex(q),python_complex);
						auto wa=cast(__python__complex(w),python_complex);
						auto z=python_int(qa.real()<wa.real()?-1:(qa.real()>wa.real()?1:0));
						auto x=python_int(qa.imag()<wa.imag()?-1:(qa.imag()>wa.imag()?1:0));
						if (z){
							return z;
						}else{
							return x;
						}
					''',['python_int','python_bool','python_float','python_complex'])+r'''
					{python_iftype(q,python_int){
						{python_iftype(w,python_float){
						}}
					}}
					{python_iftype(w,python_int){
						{python_iftype(q,python_float){
							return cmp(q,(python_float)(cast(w,python_int)));
						}}
					}}
					if (q.type()!=w.type()){
						return cmp(std::string(q.type().name()),std::string(w.type().name()));
					}
					{python_iftype(w,python_complex){
						auto a=cast(q,decltype(s));
						return cmp(cmp(a.real(),s.real())*4+cmp(a.imag(),s.imag()),python_int(0));
					}}
					{python_iftype(w,python_NoneType){
						return python_int(0);
					}}
					{python_iftype(w,python_ellipsis){
						return python_int(0);
					}}
					'''+same_for_all_types(['w'],r'''
						auto qs=cast(q,decltype(ws));
						return python_int(qs<ws?-1:(qs>ws?1:0));
					''',[w for w in types if w not in ['python_complex','python_NoneType','python_ellipsis','builtins_complex']])+r'''
					std::cout<<"failed to compare "<<q.type().name()<<" and "<<w.type().name()<<std::endl;
					fend(0)
				}

				bool var::operator<(const var o) const{
						var q=*this;
						var w=o;
						return cmp(q,w)<0;
					}
			''',
		'python_code':
			r'''
			''',
		'depends':['any','iostream','string','vector','filt','set','map','complex','builtins_complex']
	},
	'filt':{
		'c++_code':
			r'''
				std::string exec(std::string command) {
					char buffer[128];
					std::string result = "";

					// Open pipe to file
					FILE* pipe = popen(command.c_str(), "r");
					if (!pipe) {
						return "popen failed!";
					}

					// read till end of process:
					while (!feof(pipe)) {

						// use buffer to read and add to result
						if (fgets(buffer, 128, pipe) != NULL)
							result += buffer;
					}

					pclose(pipe);
					return result;
				}

				std::string filt(std::string q){
					auto a=exec(std::string("c++filt -t ")+q);
					auto symbs=std::vector<char>(33);
					iota(symbs.begin(),symbs.end(),0);
					while(count(symbs.begin(),symbs.end(),a[0])){
						a=std::string(a.begin()+1,a.end());
					}
					while(count(symbs.begin(),symbs.end(),a[a.size()-1])){
						a=std::string(a.begin(),a.end()-1);
					}
					return a;
				}
			''',
		'python_code':
			r'''
			''',
		'depends':['string','vector','numeric']
	},
	'func_example':{
		'c++_code':
			r'''
				var func_example(var args,var kwargs){fend()}
			''',
		'python_code':
			r'''
			''',
		'depends':[]
	},
	'builtins_abs':{
		'c++_code':
			r'''
			var __python__abs(var a){
				'''+same_for_all_types(['a'],r'''
					return std::abs(s);
				''',['python_int','int','python_float','python_complex'])+r'''
				fend()
			}
			''',
		'python_code':
			r'''
				def abs(x):return __python__abs(x)
			''',
		'depends':['python_variable','cmath']
	},
	'builtins_all':{
		'c++_code':
			r'''
			''',
		'python_code':
			r'''
				def all(iterable):
					for element in iterable:
						if not element:
							return False
					return True
			''',
		'depends':['python_variable','cmath']
	},
	'builtins_any':{
		'c++_code':
			r'''
			''',
		'python_code':
			r'''
				def any(iterable):
					for element in iterable:
						if element:
							return True
					return False
			''',
		'depends':['python_variable','cmath']
	},
	'builtins_bin':{
		'c++_code':
			r'''
			var __python__bin(var a){
				python_bytearray f;
				python_int d=cast(a,python_int);
				python_int s=d<0?1:0;
				d=std::abs(d);
				if (d==0){
					f.push_back('0');
				}
				while (d){
					f.push_back(d%2+'0');
					d/=2;
				}
				reverse(f.begin(),f.end());
				f=python_bytearray({'0','b'})+f;
				if (s){
					f=python_bytearray({'-'})+f;
				}
				return f;
			}
			''',
		'python_code':
			r'''
				def bin(x):return __python__bin(x)
			''',
		'depends':['python_variable','cmath','string','algorithm']
	},
	'builtins_bool':{
		'c++_code':
			r'''
			var __python__bool(var a=python_None){
				{python_iftype(a,python_NoneType){
					return false;
				}
				}
				{python_iftype(a,python_ellipsis){
					return true;
				}
				}
				{python_iftype(a,int){
					return s!=0;
				}
				}
				{python_iftype(a,python_bool){
					return s!=0;
				}
				}
				{python_iftype(a,python_int){
					return s!=0;
				}
				}
				{python_iftype(a,python_bytearray){
					return s.size()!=0;
				}
				}
				{python_iftype(a,python_str){
					return s.size()!=0;
				}
				}
				{python_iftype(a,python_list){
					return s.size()!=0;
				}
				}
				{python_iftype(a,python_set){
					return s.size()!=0;
				}
				}
				{python_iftype(a,python_dict){
					return s.size()!=0;
				}
				}
				fend()
			}
			''',
		'python_code':
			r'''
				def python_bool(x):return __python__bool(x)
			''',
		'depends':['python_variable','vector','string']
	},
	'builtins_bytearray':{
		'c++_code':
			r'''
			var __python__bytearray(var q=python_bytearray(),var w=python_bytearray()){
				{python_iftype(q,python_bytearray){
					return s;
				}
				}
				{python_iftype(q,python_str){
					return to_u8(s);
				}
				}
				{python_iftype(q,python_int){
					auto a=std::vector<char>(s);
					return python_bytearray(a.begin(),a.end());
				}
				}
				auto a=cast(__python__list(q),python_list);
				auto r=python_bytearray();
				for (auto w:a){
					r+=python_bytearray({char(cast(w,python_int))});
				}
				return r;
			}
			''',
		'python_code':
			r'''
				def bytearray(x):return __python__bytearray(x)
			''',
		'depends':['python_variable','unicode_convert','string','builtins_list']
	},
	'builtins_bytes':{
		'c++_code':
			r'''
			''',
		'python_code':
			r'''
				def bytes(x):return __python__bytearray(x)
			''',
		'depends':['python_variable','unicode_convert','string','builtins_bytearray']
	},
	'builtins_chr':{
		'c++_code':
			r'''
			var __python__chr(var q){
				return python_str({chr(cast(q,python_int))});
			}
			''',
		'python_code':
			r'''
				def chr(x):return __python__chr(x)
			''',
		'depends':['python_variable','unicode_convert','string']
	},
	'builtins_complex':{
		'c++_code':
			r'''
			var __python__complex(var q=python_int(0),var w=python_int(0)){
				{python_iftype(q,python_complex){
				}else{
					q=python_complex(cast(__python__float(q),python_float),0);
				}
				}
				{python_iftype(w,python_complex){
				}else{
					w=python_complex(cast(__python__float(w),python_float),0);
				}
				}
				return cast(q,python_complex)+python_complex(0,1)*cast(w,python_complex);
			}
			''',
		'python_code':
			r'''
				def complex(x=0,y=0):return __python__complex(x,y)
			''',
		'depends':['python_variable','complex','builtins_float']
	},
	'builtins_dict':{
		'c++_code':
			r'''
				var __python__dict(var q=python_dict()){
					auto s=python_dict();
					return s;
				}
			''',
		'python_code':
			r'''
				def dict(x):return __python__dict(x)
			''',
		'depends':['python_variable']
	},
	'builtins_divmod':{
		'c++_code':
			r'''
			var __python__divmod(var q,var w){
				auto ret=python_list();
				{python_iftype(q,python_int){
					auto d=s;
					{python_iftype(w,python_int){
						ret[0]=d/s;
						ret[1]=d%s;
					}
					}
				}
				}
				if (ret.size()==0){
					q=__python__float(q);
					w=__python__float(w);
					auto e=cast(q,python_float);
					auto r=cast(w,python_float);
					auto t=std::floor(e/r);
					ret.push_back(t);
					ret.push_back(e-t*r);
				}
				return ret;
			}
			''',
		'python_code':
			r'''
				def divmmod(x,y):return __python__divmod(x,y)
			''',
		'depends':['python_variable','cmath','vector','builtins_float']
	},
	'builtins_float':{
		'c++_code':
			r'''
				var __python__float(var q=python_int(0)){
				//	{python_iftype(q,python_str){
				//		return s;
				//	}
				//	}
				//	{python_iftype(q,python_bytearray){
				//		return to_u32(s);
				//	}
				//	}
					{python_iftype(q,python_int){
						return (python_float)(s);
					}
					}
					{python_iftype(q,python_float){
						return s;
					}
					}
					{python_iftype(q,int){
						return (python_float)(s);
					}
					}
					fend()
				}
			''',
		'python_code':
			r'''
				def float(x):return __python__float(x)
			''',
		'depends':['python_variable','string']
	},
	'builtins_id':{
		'c++_code':
			r'''
			var __python__id(var q){
				'''+same_for_all_types(['q'],r'''
					return python_int(&cast(q,decltype(s)));
				''')+r'''
				fend()
			}
			''',
		'python_code':
			r'''
				def id(x):return __python__id(x)
			''',
		'depends':['python_variable','string','vector']
	},
	'builtins_int':{
		'c++_code':
			r'''
			var __python__int(var q=python_int(0),var w=python_int(0)){
				{python_iftype(w,python_int){	
				}else{
					w=__python__int(w);					
				}}
				'''+same_for_all_types(['q'],r'''
					return python_int(qs);
				''',['python_int','python_float','python_bool'])+r'''
				fend()
			}
			''',
		'python_code':
			r'''
				def int(x):return __python__int(x)
			''',
		'depends':['python_variable','string']
	},
	'builtins_len':{
		'c++_code':
			r'''
				var __python__len(var q){
					{python_iftype(q,python_list){
						return python_int(s.size());
					}}
					{python_iftype(q,python_set){
						return python_int(s.size());
					}}
					{python_iftype(q,python_dict){
						return python_int(s.size());
					}}
					{python_iftype(q,python_str){
						return python_int(s.size());
					}}
					{python_iftype(q,python_bytearray){
						return python_int(s.size());
					}}
					fend()
				}
			''',
		'python_code':
			r'''
				def len(x):return __python__len(x)
			''',
		'depends':['python_variable','vector']
	},
	'builtins_list':{
		'c++_code':
			r'''
				var __python__list(var q=python_list()){
					auto s=python_list();
					for (var w:python_iterate(q)){
						s.push_back(w);
					}
					return s;
				}
			''',
		'python_code':
			r'''
				def list(x):return __python__list(x)
			''',
		'depends':['python_variable','vector']
	},
	'builtins_print':{
		'c++_code':
			r'''
				var __python__print(var q=python_list(),var sep=python_str({' '}),var end=python_str({'\n'})){
					auto s=python_str();
					auto _end=cast(__python__str(end),python_str);
					auto _sep=cast(__python__str(sep),python_str);
					auto c=python_int(0);
					{python_iftype(q,python_list){}else{
						q=python_list({q});
					}}
					for (var w:python_iterate(q)){
						s+=(c?_sep:python_str())+cast(__python__str(w),python_str);
						c=c?c:1;
					}
					s+=_end;
					std::cout<<to_u8(s);
					return python_None;
				}
			''',
		'python_code':
			r'''
				def print(*q,sep=' ',end='\n'):return __python__print(q,sep,end)
			''',
		'depends':['python_variable','vector','string','builtins_str','iostream','unicode_convert']
	},
	'builtins_range':{
		'c++_code':
			r'''
				struct range_struct{
					struct range_iterator{
						python_int val, step;
						inline iterator(python_int v,python_int s){
							val=v;
							step=s;
						}
						inline bool operator!=(iterator o){
							if (step>0 and val>=o.val){
								return false;
							}
							if (step<0 and val<=o.val){
								return false;
							}
							if (step==0 and val==o.val){
								return false;
							}
							return true;
						}
						inline void operator++(){
							val+=step;
						}
						inline int64_t operator*(){
							return val;
						}
					};
					int64_t start, stop, step;
					inline iterator begin(){
						iterator r(start,step);
						return r;
					}
					inline iterator end(){
						iterator r(stop,step);
						return r;
					}
				};

				var __python__range(var q,var w,var e){
					return range_struct(cast(q,int),cast(w,int),cast(e,int));
				}
			''',
		'python_code':
			r'''
				def range(q,w=None,e=None):
					if w==None:
						return __python__range(0,q,1)
					if e==None:
						return __python__range(q,w,1)
					return __python__range(q,w,e)
			''',
		'depends':['python_variable','']
	},
	'builtins_set':{
		'c++_code':
			r'''
				var __python__set(var q=python_set()){
					auto s=python_set();
					for (var w:python_iterate(q)){
						s.insert(w);
					}
					return s;
				}
			''',
		'python_code':
			r'''
				def set(x):return __python__set(x)
			''',
		'depends':['python_variable','set']
	},
	'builtins_str':{
		'c++_code':
			r'''
				var __python__str(var q=python_str()){
					{python_iftype(q,python_str){
						return s;
					}
					}
					{python_iftype(q,python_bytearray){
						python_bytes r="b'";
						for (auto _w:s){
							auto w=(unsigned char)(_w);
							if(w==9){
								r+="\\t";
							}else if(w==10){
								r+="\\n";
							}else if(w==13){
								r+="\\r";
							}else if(w==76){
								r+="\\\\";
							}else if(w>126 or w<32){
								r+=python_bytes({'\\','x',python_bytes("0123456789abcdef")[w/16],python_bytes("0123456789abcdef")[w%16]});
							}else{
								r+=python_bytes({_w});
							}
						}
						r+="'";
						return to_u32(r);
					}
					}
					{python_iftype(q,python_int){
						return to_u32(std::to_string(s));
					}
					}
					{python_iftype(q,python_float){
						return to_u32(std::to_string(s));
					}
					}
					{python_iftype(q,python_complex){
						if (s.imag()<0){
							return to_u32(std::to_string(s.real())+std::to_string(s.imag())+"j");
						}else{
							return to_u32(std::to_string(s.real())+"+"+std::to_string(s.imag())+"j");
						}
					}
					}
					{python_iftype(q,int){
						return to_u32(std::to_string(s));
					}
					}
					{python_iftype(q,python_bool){
						return to_u32(s?"True":"False");
					}
					}
					{python_iftype(q,python_NoneType){
						return to_u32("None");
					}
					}
					{python_iftype(q,python_ellipsis){
						return to_u32("Ellipsis");
					}
					}

					fend()
				}
			''',
		'python_code':
			r'''
				def str(x):return __python__str(x)
			''',
		'depends':['python_variable','vector','string','unicode_convert','complex']
	},
	'builtins_time':{
		'c++_code':
			r'''
				// Get time stamp in milliseconds.
				uint64_t millis()
				{
				    uint64_t ms = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::
				                  now().time_since_epoch()).count();
				    return ms; 
				}

				// Get time stamp in microseconds.
				uint64_t micros()
				{
				    uint64_t us = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::
				                  now().time_since_epoch()).count();
				    return us; 
				}

				// Get time stamp in nanoseconds.
				uint64_t nanos()
				{
				    uint64_t ns = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::high_resolution_clock::
				                  now().time_since_epoch()).count();
				    return ns; 
				}
				var __python__time(){
					return python_float(nanos())/1000000000;
				}
			''',
		'python_code':
			r'''
				def time(x):return __python__time()
			''',
		'depends':['python_variable','set']
	},
	'builtins_type':{
		'c++_code':
			r'''
				var __python__type(var q){
					return to_u32(filt(q.type().name()));
				}
			''',
		'python_code':
			r'''
				def type(x):return __python__type(x)
			''',
		'depends':['python_variable','unicode_convert','filt',]
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
	'operator_Not':{
		'c++_code':
		'''
			var operator!(var q){
				q=__python__bool(q);
				return !cast(q,python_bool);
				}
			}
		''',
		'python_code':'',
		'depends':
			['python_variable'],
	},
	'operator_Pow':{
		'c++_code':
		'''
			auto python_operator_Pow=__python__pow;
		''',
		'python_code':'',
		'depends':
			['python_variable','builtins_pow'],
	},
	'operator_Eq':{
		'c++_code':
		'''
			var var::operator==(var w){
				var q=*this;
				return cast(cmp(q,w),python_int)==0;
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','cmp'],
	},
	'operator_NotEq':{
		'c++_code':
		'''
			var var::operator!=(var w){
				var q=*this;
				return cast(cmp(q,w),python_int)!=0;
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','cmp'],
	},
	'operator_Gt':{
		'c++_code':
		'''
			var var::operator>(var w){
				var q=*this;
				return cast(cmp(q,w),python_int)>0;
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','cmp'],
	},
	'operator_GtE':{
		'c++_code':
		'''
			var var::operator>=(var w){
				var q=*this;
				return cast(cmp(q,w),python_int)>=0;
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','cmp'],
	},
	'operator_Lt':{
		'c++_code':
		'''
			var var::operator<(var w){
				var q=*this;
				return cast(cmp(q,w),python_int)<0;
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','cmp'],
	},
	'operator_LtE':{
		'c++_code':
		'''
			var var::operator<=(var w){
				var q=*this;
				return cast(cmp(q,w),python_int)<=0;
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','cmp'],
	},
	'operator_Is':{
		'c++_code':
		'''
			var python_operator_Is(var q,var w){
				return __python__id(q)==__python__id(w);
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
				return __python__id(q)!=__python__id(w);
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','operator_Is'],
	},
	'operator_In':{
		'c++_code':
		'''
			var python_operator_In(var q,var w){
				for (auto e:python_iterate(w)){
					if (cast(q==e,bool)){
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
				for (auto e:python_iterate(w)){
					if (cast(q==e,bool)){
						return false;
					}
				}
				return true;
			}
		''',
		'python_code':'',
		'depends':
			['python_variable','operator_Eq'],
	},
	'any':{'c++_code':'#include<any>','python_code':'','depends':[]},
	'set':{'c++_code':'#include<set>','python_code':'','depends':[]},
	'map':{'c++_code':'#include<map>','python_code':'','depends':[]},
	'cmath':{'c++_code':'#include<cmath>','python_code':'','depends':[]},
	'stdc++':{'c++_code':'#include<bits/stdc++.h>','python_code':'','depends':[]},
	'vector':{'c++_code':'#include<vector>','python_code':'','depends':[]},
	'cstdio':{'c++_code':'#include<cstdio>','python_code':'','depends':[]},
	'chrono':{'c++_code':'#include<chrono>','python_code':'','depends':[]},
	'string':{'c++_code':'#include<string>','python_code':'','depends':[]},
	'cstdlib':{'c++_code':'#include<cstdlib>','python_code':'','depends':[]},
	'numeric':{'c++_code':'#include<numeric>','python_code':'','depends':[]},
	'complex':{'c++_code':'#include<complex>','python_code':'','depends':[]},
	'iostream':{'c++_code':'#include<iostream>','python_code':'','depends':[]},
	'algorithm':{'c++_code':'#include<algorithm>','python_code':'','depends':[]},
	'functional':{'c++_code':'#include<functional>','python_code':'','depends':[]},
	'unordered_map':{'c++_code':'#include<unordered_map>','python_code':'','depends':[]},
	'unordered_set':{'c++_code':'#include<unordered_set>','python_code':'','depends':[]},
	'initializer_list':{'c++_code':'#include<initializer_list>','python_code':'','depends':[]},
	'levels':{
		'c++_code':
			r'''
				#define python_level_type_first python_str
				#define python_level_type_second var
				#define convert_first_type to_u8
				std::vector<std::unordered_map<python_level_type_first,python_level_type_second*>> python_globals;
				std::vector<std::unordered_map<python_level_type_first,python_level_type_second>*> python_locals_pointers;
				#define python_global(q)\
				 	if (!python_globals[0].count(q)){\
						(*(python_locals_pointers[0]))[q]=int64_t(0);\
						python_globals[0][q]=&((*(python_locals_pointers[0]))[q]);\
					}\
					python_globals[python_globals.size()-1][q]=python_globals[0][q];

				#define python_nonlocal(q)\
				 	if (!python_globals[python_globals.size()-2].count(q)){\
						(*(python_locals_pointers[python_locals_pointers.size()-2]))[q]=int64_t(0);\
						python_globals[python_globals.size()-2][q]=&((*(python_locals_pointers[python_locals_pointers.size()-2]))[q]);\
					}\
					python_globals[python_globals.size()-1][q]=python_globals[python_globals.size()-2][q];
					
				#define python_level_get(...) python_level_get_with_line(__VA_ARGS__,__LINE__)

				python_level_type_second& python_level_get_with_line(python_level_type_first q,int64_t line){
					for (int64_t w=python_globals.size()-1;w>=0;--w){
						if (python_globals[w].count(q)){
							return *(python_globals[w][q]);
						}
					}
					std::cout<<std::string("line ")<<line<<std::string("\nname ")+convert_first_type(q)+std::string(" is undefined")<<std::endl;
					return *(python_globals[0][q]);
				}

				bool __python__isdefined(python_level_type_first q){
					for (auto w=python_globals.size()-1;w>=0;--w){
						if (python_globals[w].count(q)){
							return true;
						}
					}
					return false;
				}

				python_level_type_second& python_level_set(python_level_type_first q){
					if (!python_globals[python_globals.size()-1].count(q)) {
						(*(python_locals_pointers[python_locals_pointers.size()-1]))[q]=int64_t(0);
						python_globals[python_globals.size()-1][q]=&((*(python_locals_pointers[python_locals_pointers.size()-1]))[q]);
					}
					return *(python_globals[python_globals.size()-1][q]);
				}

				#define python_create_level()\
					python_globals.emplace_back();\
					std::unordered_map<python_level_type_first,python_level_type_second> python_locals;\
					python_locals_pointers.push_back(&python_locals);

				#define python_delete_level()\
					python_globals.pop_back();\
					python_locals_pointers.pop_back();
			''',
		'python_code':'',
		'depends':
			['vector','string','unordered_map','python_variable','unicode_convert'],
	},
	'attribute_conjugate':{
		'c++_code':
		'''
			var __python__attribute__conjugate(var a){
				{python_iftype(a,python_complex){
					return __python__complex(s.real(),-s.imag());
				}}
				{python_iftype(a,python_float){
					return s;
				}}
				{python_iftype(a,python_int){
					return s;
				}}
				{python_iftype(a,python_bool){
					return s;
				}}
				fend()
			}
		''',
		'python_code':'def attribute_conjugate(q):return __python__attribute__conjugate(q)',
		'depends':
			['python_variable','builtins_complex'],
	},
	'attribute_imag':{
		'c++_code':
		'''
			var __python__attribute__imag(var a){
				{python_iftype(a,python_complex){
					return s.imag();
				}}
				{python_iftype(a,python_float){
					return 0;
				}}
				{python_iftype(a,python_int){
					return 0;
				}}
				{python_iftype(a,python_bool){
					return 0;
				}}
				fend()
			}
		''',
		'python_code':'def attribute_imag(q):__python__attribute__imag(q)',
		'depends':
			['python_variable','complex'],
	},
	'attribute_real':{
		'c++_code':
		'''
			var __python__attribute__real(var a){
				{python_iftype(a,python_complex){
					return s.real();
				}}
				{python_iftype(a,python_float){
					return s;
				}}
				{python_iftype(a,python_int){
					return s;
				}}
				{python_iftype(a,python_bool){
					return s;
				}}
				fend()
			}
		''',
		'python_code':'def attribute_real(q):__python__attribute__real(q)',
		'depends':
			['python_variable','complex'],
	},
	'attribute_is_integer':{
		'c++_code':
		'''
			var __python__attribute__is_integer(var a){
				{python_iftype(a,python_float){
					return python_int(s)==s;
				}}
				fend()
			}
		''',
		'python_code':'def attribute_is_integer(q):__python__attribute__is_integer(q)',
		'depends':
			['python_variable'],
	},
	'attribute_bit_length':{
		'c++_code':
		'''
			var __python__attribute__bit_length(var a){
				{python_iftype(a,python_int){
					python_int q=0;
					while (s){
						s/=2;
						q+=1;
					}
					return q;
				}}
				{python_iftype(a,python_bool){
					python_int q=0;
					while (s){
						s/=2;
						q+=1;
					}
					return q;
				}}
				fend()
			}
		''',
		'python_code':'def attribute_bit_length(q):__python__attribute__bit_length(q)',
		'depends':
			['python_variable'],
	},
	'attribute_denominator':{
		'c++_code':
		'''
			var __python__attribute__denominator(var a){
				return 1;
				fend()
			}
		''',
		'python_code':'def attribute_denominator(q):__python__attribute__denominator(q)',
		'depends':
			['python_variable'],
	},
	'attribute_numerator':{
		'c++_code':
		'''
			var __python__attribute__numerator(var a){
				{python_iftype(a,python_int){
					return s;
				}}
				{python_iftype(a,python_bool){
					return s;
				}}
				fend()
			}
		''',
		'python_code':'def attribute_numerator(q):__python__attribute__numerator(q)',
		'depends':
			['python_variable','builtins_int'],
	},
	'attribute_to_bytes':{
		'c++_code':
		'''
			var __python__attribute__to_bytes(var a,var s,var d){
				auto q=cast(__python__int(a),python_int);
				auto w=cast(__python__int(s),python_int);
				auto e=cast(d,python_str);
				python_bytes r;
				while(q){
					r+=python_bytes({char(q%256)});
					q/=256;
				}
				reverse(r.begin(),r.end());
				while (r.size()<w){
					r+=python_bytes({char(0)});
				}
				if (e==python_str({'b','i','g'})){
					reverse(r.begin(),r.end());
				}
				return r;
				fend()
			}
		''',
		'python_code':'def attribute_to_bytes(q,length,byteorder,):__python__attribute__to_bytes(q)',
		'depends':
			['python_variable','string','algorithm','builtins_int'],
	},
	'attribute_append':{
		'c++_code':
		'''
			var __python__attribute__append(var a,var q){
				python_iftype(a,python_bytearray){
					cast(a,decltype(s)).push_back((char)cast(__python__int(q),python_int));
				}
				python_iftype(a,python_str){
					cast(a,decltype(s)).push_back((chat32_t)cast(__python__int(q),python_int));
				}
				python_iftype(a,python_list){
					cast(a,decltype(s)).push_back(q);
				}
				return python_None;
				fend()
			}
		''',
		'python_code':'',
		'depends':
			['builtins_int'],
	},
	'attribute_add':{
		'c++_code':
		'''
			var __python__attribute__add(var a,var q){
				python_iftype(a,python_set){
					cast(a,decltype(s)).insert(q);
				}
				return python_None;
				fend()
			}
		''',
		'python_code':'',
		'depends':
			[],
	},
})

# from json import dumps
# from os.path import dirname
# open(str(dirname(__file__))+'/headers.json','w').write(dumps(headers))
