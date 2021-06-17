from sys import argv
from functools import reduce
from re import *
from pprint import pprint
from ast import *
def error(q):
# def error(l,q):
# 	print('\x1b[31m[error line '+str(l)+']\x1b[0m',q)
	print('\x1b[31m[error]\x1b[0m',q)
	exit(1)
def lprint(q):
	print('lprint',q)
	return q

filename=None
if len(argv)>1:
	filename=argv[1]
	text=open(filename).read()
else:
	from sys import stdin
	text=stdin.read()
	print()

# body=parse(text).body
# print(*[dump(w,indent=4) for w in body],sep='\n')

random_string_seed=1000000000000000000
def random_string():
	global random_string_seed
	random_string_seed+=1
	return '_'+str(random_string_seed)

# print(dump(parse(text),indent=4))

indent_sign='\t'
indent=-1

to_include={'levels','python_variable','cmp'}

def make_comment(q):
	return '/*'+str(q).replace('*/','*\\/')+'*/'

debug=0

main_text_converted=0

before_main=''

def add(*q):
	global main_text_converted
	if main_text_converted==0:
		for w in q:
			to_include.add(w)

def generate(astobj):
	global main_text_converted
	print(dump(astobj,indent=4))
	global indent
	indent+=1
	# if astobj.__class__.__name__=='Module':
	# 	ret=indent_sign*indent+'int main(int argc,char **argv){\n'\
	# 	+indent_sign*indent+indent_sign+'python_create_level()\n'\
	# 	+indent_sign*indent+indent_sign+'python_headers\n'\
	# 	+''.join([generate(w)+'\n' for w in astobj.body])+indent_sign*indent+indent_sign+'python_delete_level()}'
	if 0:
		ret=''
	elif astobj.__class__.__name__=='Expr':
		ret=indent_sign*indent+generate(astobj.value)+';\n'
	elif astobj.__class__.__name__=='FunctionDef':
		# if hasattr(astobj,'returns') and generate(astobj.returns)==generate(Constant(value='__simple_function__')):
		# 	pass
		drn=dict([[(astobj.args.posonlyargs+astobj.args.args)[w-len(astobj.args.defaults)].arg,[astobj.args.defaults[w],random_string()]] for w in range(len(astobj.args.defaults))])
		kdrn=dict([[(astobj.args.kwonlyargs)[w-len(astobj.args.kw_defaults)].arg,[astobj.args.kw_defaults[w],random_string()]] for w in range(len(astobj.args.kw_defaults)) if astobj.args.kw_defaults[w]!=None])
		fn=random_string()
		ret =''\
			+''.join([indent_sign*indent+drn[w][1]+'='+generate(drn[w][0])+';\n' for w in drn])\
			+''.join([indent_sign*indent+kdrn[w][1]+'='+generate(kdrn[w][0])+';\n' if kdrn[w][0]!=None else '' for w in kdrn])\
			+indent_sign*indent+indent_sign+generate(Name(id=astobj.name,ctx=Store()))+'='+fn+';\n'\
			+''.join([generate(Assign(targets=[Name(id=astobj.name,ctx=Store())],value=Call(func=w,args=[Name(id=astobj.name,ctx=Load())],keywords=[])))+'\n' for w in astobj.decorator_list[::-1]])+'\n'
		global before_main
		before_main+=indent_sign*indent+make_comment(astobj.name)+'\n'\
			+''.join([indent_sign*indent+'var '+drn[w][1]+';\n' for w in drn])\
			+''.join([indent_sign*indent+'var '+kdrn[w][1]+';\n' if kdrn[w][0]!=None else '' for w in kdrn])\
			+indent_sign*indent+'var '+fn+'(var args, var kwargs){\n'\
			+indent_sign*indent+indent_sign+'python_create_level()\n'\
			+''.join([indent_sign*indent+indent_sign+generate(Name(id=w,ctx=Store()))+'='+drn[w][1]+';\n' for w in drn])\
			+''.join([indent_sign*indent+indent_sign+generate(Name(id=w,ctx=Store()))+'='+kdrn[w][1]+';\n' if kdrn[w][0]!=None else '' for w in kdrn])\
			+''.join([indent_sign*indent+indent_sign+'if(cast(kwargs,python_dict).count('+generate(Constant(value=w[1].arg))+')){'+generate(Name(id=w[1].arg,ctx=Store()))+'=cast(kwargs,python_dict)['+generate(Constant(value=w[1].arg))+'];}\n' for w in enumerate(astobj.args.posonlyargs+astobj.args.args+astobj.args.kwonlyargs)])\
			+''.join([indent_sign*indent+indent_sign+'if(cast(args,python_list).size()>'+str(w[0])+'){'+generate(Name(id=w[1].arg,ctx=Store()))+'=cast(args,python_list)['+str(w[0])+'];}\n' for w in enumerate(astobj.args.posonlyargs+astobj.args.args)])\
			+(indent_sign*indent+indent_sign+generate(Name(id=astobj.args.vararg.arg,ctx=Store()))+'=python_list();\n' if astobj.args.vararg!=None else '')\
			+(indent_sign*indent+indent_sign+'if(cast(args,python_list).size()>'+str(len(astobj.args.posonlyargs+astobj.args.args))+'){'+generate(Name(id=astobj.args.vararg.arg,ctx=Store()))+'=python_list(cast(args,python_list).begin()+'+str(len(astobj.args.posonlyargs+astobj.args.args))+',cast(args,python_list).end());}\n' if astobj.args.vararg!=None else '')\
			+'\n'.join([generate(w) for w in astobj.body])+'\n'\
			+generate(Return(value=None))+';\n'\
			+indent_sign*indent+'}\n'
	elif astobj.__class__.__name__=='If':
		add('python__bool')
		ret=indent_sign*indent+'if(python__bool('+generate(astobj.test)+')){\n'+''.join([generate(w)+'\n' for w in astobj.body])+indent_sign*indent+'}else{\n'+''.join([indent_sign*indent+generate(w)+'\n' for w in astobj.orelse])+indent_sign*indent+'}'
	elif astobj.__class__.__name__=='While':
		add('python__bool')
		ret=indent_sign*indent+'while(python__bool('+astobj.test+')){\n'+''.join([generate(w)+'\n' for w in astobj.body])+indent_sign*indent+'}'
	elif astobj.__class__.__name__=='Pass':
		ret=indent_sign*indent+'/*pass*/'
	elif astobj.__class__.__name__=='Global':
		ret=indent_sign*indent+'python_global('+','.join([generate(Constant(value=w)) for w in astobj.names])+')'
	elif astobj.__class__.__name__=='For':
		fn=random_string()
		ret =indent_sign*indent+'for(var '+fn+':python_iterate('+generate(astobj.iter)+')){\n'\
			+indent_sign*indent+indent_sign+generate(astobj.target)+'='+fn+';\n'\
			+''.join([generate(w)+'\n' for w in astobj.body])+indent_sign*indent+'}'
	elif astobj.__class__.__name__=='Nonlocal':
		ret=indent_sign*indent+'python_nonlocal('+','.join([Constant(value=w) for w in astobj.names])+')'
	elif astobj.__class__.__name__=='Return':
		ret =''\
			+indent_sign*indent+'{var to_return='+(generate(astobj.value) if astobj.value!=None else generate(Constant(value=None)))+';\n'\
			+indent_sign*indent+'python_delete_level()\n'\
			+indent_sign*indent+'return to_return;}'
	# elif astobj.__class__.__name__=='Delete':
	# 	ret=indent_sign*indent+'python_delete_list('+','.join([generate(w) for w in astobj.targets])+');'
	# elif astobj.__class__.__name__=='Delete':
	# 	add('debug_str')
	# 	add('iostream')
	# 	# ret=indent_sign*indent+'python_delete_list('+','.join([generate(w) for w in astobj.targets])+');'
	# 	ret=indent_sign*indent+'std::cout<<'+'<<" "<<'.join(['python_debug_str('+generate(w)+')' for w in astobj.targets])+'<<std::endl;'
	elif astobj.__class__.__name__=='Assign':
		ret=indent_sign*indent+''.join([generate(w)+'=' for w in astobj.targets])+generate(astobj.value)+';'
	# elif astobj.__class__.__name__=='AugAssign':
	# 	ret=indent_sign*indent+generate(Call(func=Name(id='',ctx=Load()),args=[],keywords=[]))
	elif astobj.__class__.__name__=='Call':
		if astobj.func.__class__.__name__=='Name' and astobj.func.id.startswith('__python__'):
			ret=generate(astobj.func)+'('+','.join([generate(w) for w in astobj.args])+')'			
		else:
			add('None')
			add('func_example')
			# ret='(*cast('+generate(astobj.func)+',decltype(&func_example)))('+generate(List(elts=astobj.args,ctx=Load()))+',python_None)'
			ret='(*cast('+generate(astobj.func)+',decltype(&func_example)))('+generate(List(elts=astobj.args,ctx=Load()))+','+generate(Dict(keys=[Constant(value=w.arg,ctx=Load()) for w in astobj.keywords],values=[w.value for w in astobj.keywords]))+')'
	elif astobj.__class__.__name__=='List':
		add('builtins_list','vector')
		if all([w.__class__.__name__!='Starred' for w in astobj.elts]):
			ret='python_list({'+','.join(['var('+generate(w)+')' for w in astobj.elts])+'})'
		else:
			rsum=List(elts=[])
			for w in astobj.elts:
				if w.__class__.__name__=='Starred':
					rsum=BinOp(left=rsum,op=Add(),right=Call(func=Name(id='__python__list',ctx=Load()),args=[w.value],keywords=[]))
				else:
					rsum=BinOp(left=rsum,op=Add(),right=List(elts=[w]))
			ret=generate(rsum)
	elif astobj.__class__.__name__=='Set':
		add('builtins_set','set','cmp')
		if all([w.__class__.__name__!='Starred' for w in astobj.elts]):
			ret='python_set({'+','.join(['var('+generate(w)+')' for w in astobj.elts])+'})'
		else:
			rsum=List(elts=[])
			for w in astobj.elts:
				if w.__class__.__name__=='Starred':
					rsum=BinOp(left=rsum,op=BinOr(),right=Call(func=Name(id='__python__set',ctx=Load()),args=[w.value],keywords=[]))
				else:
					rsum=BinOp(left=rsum,op=BinOr(),right=Set(elts=[w]))
			ret=generate(rsum)
	elif astobj.__class__.__name__=='Dict':
		add('builtins_dict','map','cmp')
		if all([w!=None for w in astobj.keys]):
			ret='python_dict({'+','.join(['{var('+generate(w[0])+'),var('+generate(w[1])+')}' for w in zip(astobj.keys,astobj.values)])+'})'
		else:
			rsum=List(elts=[])
			for w in zip(astobj.keys,astobj.values):
				if w[0]==None:
					rsum=BinOp(left=rsum,op=BinOr(),right=Call(func=Name(id='__python__dict',ctx=Load()),args=[w[1]],keywords=[]))
				else:
					rsum=BinOp(left=rsum,op=BinOr(),right=Dict(keys=[w[0]],values=[w[1]]))
			ret=generate(rsum)

		# add('builtins_dict')
		# retlist=List(elts=[])
		# for w in zip(astobj.keys,astobj.values):
		# 	if w[0]==None:
		# 		retlist.elts.append(Starred(value=Call(func=Name(id='python_dict_to_list_of_pairs',ctx=Load()),args=[Call(func=Name(id='__python__dict',ctx=Load()),args=[w[1]],keywords=[])],keywords=[]),ctx=Load()))
		# 	else:
		# 		retlist.elts.append(List(elts=list(w)))
		# ret='__python__dict('+generate(retlist)+')'
	elif astobj.__class__.__name__=='BinOp':
		add('operator_'+astobj.op.__class__.__name__)
		# ret='python_operator_'+astobj.op.__class__.__name__+'('+generate(astobj.left)+','+generate(astobj.right)+')'
		if astobj.op.__class__.__name__ in sum(op_names,[]):
			ret='(var('+generate(astobj.left)+')'+[w for w in operators if w['name']==astobj.op.__class__.__name__][0]['sign']+'var('+generate(astobj.right)+'))'
		else:
			ret='python_operator_'+astobj.op.__class__.__name__+'('+generate(astobj.left)+','+generate(astobj.right)+')'			
	elif astobj.__class__.__name__=='BoolOp':
		add('python__bool')
		ret='('+(' '+astobj.op.__class__.__name__.lower()+' ').join(['python__bool('+generate(w)+')' for w in astobj.values])+')'
	elif astobj.__class__.__name__=='UnaryOp':
		add('operator_'+astobj.op.__class__.__name__)
		# ret='python_operator_'+astobj.op.__class__.__name__+'('+generate(astobj.operand)+')'
		ret='('+[w for w in operators if w['name']==astobj.op.__class__.__name__][0]['sign']+generate(astobj.right)+')'
	elif astobj.__class__.__name__=='Compare':
		add('builtins_bool','cache')
		cl=[astobj.left]+sum([list(w) for w in zip(astobj.ops,astobj.comparators)],[])
		ps=[]
		for w in range(1,len(cl),2):
			add('operator_'+cl[w].__class__.__name__)
			add('python__bool')
			if cl[w].__class__.__name__ not in 'In NotIn Is IsNot'.split():
				r='python__bool(var('
				if w==1:
					r+=generate(cl[0])
				else:
					r+='del_cache("'+rn+'")'
				r+=')'+[e for e in operators if e['name']==cl[w].__class__.__name__][0]['sign']+'var('
				if w==len(cl)-2:
					r+=generate(cl[w+1])
				else:
					rn=random_string()
					r+='set_cache('+generate(cl[w+1])+',"'+rn+'")'
				r+='))'
			else:
				r='python__bool(python_operator_'+cl[w].__class__.__name__+'('
				if w==1:
					r+=generate(cl[0])
				else:
					r+='del_cache("'+rn+'")'
				r+=','
				if w==len(cl)-2:
					r+=generate(cl[w+1])
				else:
					rn=random_string()
					r+='set_cache('+generate(cl[w+1])+',"'+rn+'")'
				r+='))'
			ps.append(r)				
		ret='('+' and '.join(ps)+')'
	elif astobj.__class__.__name__=='Name':
		if debug:
			ret=str(astobj.id)
		else:
			chn=astobj.id
			if chn.startswith('__python__'):
				chn=chn[len('__python__'):]
			if chn.startswith('python__builtins__'):
				chn=chn[len('python__builtins__'):]
			chn='builtins_'+chn
			global main_text_converted
			if main_text_converted==0 and chn in builtins:
				add(chn)
			if astobj.id.startswith('__python__'):
				ret=str(astobj.id)
			else:
				ret=('python_level_get(' if astobj.ctx.__class__.__name__!='Store' else 'python_level_set(')+generate(Constant(value=astobj.id))+')'
	elif astobj.__class__.__name__=='Constant':
		if debug:
			ret=str(astobj.value)
		else:
			if type(astobj.value)==type(None):
				add('None')
				ret='python_None'
			if type(astobj.value)==type(True):
				ret=str(astobj.value).lower()
			if type(astobj.value)==type(...):
				add('Ellipsis')
				ret='python_Ellipsis'
			if type(astobj.value)==type(0):
				ret='python_int('+str(astobj.value)+')'
			if type(astobj.value)==type(1j):
				add('complex')
				ret='python_complex(0,'+str(astobj.value.imag)+')'
			if type(astobj.value)==type(0.0):
				ret='(python_float)('+str(astobj.value)+')'
			if type(astobj.value)==type(''):
				add('string')
				ret='std::u32string({'+','.join([str(ord(w)) for w in astobj.value])+'})'+make_comment(astobj.value)
	else:
		ret='\x1b[31m'+dump(astobj,indent=4)+'\x1b[0m'
	indent-=1
	return ret

def convert(q,a=1):
	if a:
		while '\n' in q[:-len(q.lstrip())]:
			q=q[1:]
		while '\r' in q[:-len(q.lstrip())]:
			q=q[1:]
		l=(len(q)-len(q.lstrip()))
		q=q.split('\n')
		q='\n'.join([w[l:] for w in q])
	return '\n'.join([generate(w) for w in parse(q).body])+'\n'


# from json import loads
# from os.path import dirname
# headers=loads(open(str(dirname(__file__))+'/headers.json').read())

from headers import *

builtins=[w for w in headers if w.startswith('builtins_')]

text=convert(text,a=0)

before_main_of_main=before_main

before_main=''

main_text_converted=1

to_include=list(to_include)
for w in to_include:
	try:
		to_include+=headers[w]['depends']
	except:
		print('header',w,'not found, but there are some similar:')
		from difflib import ndiff
		for e in headers:
			r=list(ndiff(w,e))
			if len([t for t in r if t[0]==' '])/len(r)>0.5:
				print(e)
to_include=to_include[::-1]
to_include=reduce(lambda a,s:a+[s] if s not in a else a,to_include,[])
to_include_first=''.join(['\n/*'+'*'*76+'*/\n/*defining '+w+'*/\n'+headers[w]['c++_code']+'\n' for w in to_include])
to_include_second=''.join(['\n/*'+'*'*76+'*/\n/*defining '+w+'*/\n'+convert(headers[w]['python_code'])+'\n' for w in to_include])
text=to_include_first+'\n'\
	+'/'*80+'\n//before main code\n'\
	+before_main\
	+before_main_of_main\
	+'/'*80+'\n//main code\n'\
	+'int main(int argc,char **argv){\n'\
	+'python_create_level()\n'\
	+to_include_second\
	+'/'*80+'\n//main code\n'\
		+text\
	+'python_delete_level()}'

# text=to_include_first+'\n'+'/'*80+'\n//main code\n'+text
# print(text)
if filename!=None:
	open(filename+'.cpp','w').write(text)
	from subprocess import run
	if run(['g++','-std=c++17','-Wfatal-errors',filename+'.cpp']).returncode==0:
		run(['./a.out'])