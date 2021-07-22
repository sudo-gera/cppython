from sys import argv
from functools import reduce
from re import *
from pprint import pprint
from ast import *
try:
	from icecream import ic
	ic.configureOutput(includeContext=True)
except:
	ic=lambda *a:a[0] if len(a)==1 else [None,a][min(len(a),1)]

def error(*q,**a):
	print('\x1b[31mERROR\x1b[0m')
	for w in gen_stack:
		print('\x1b[33mat '+w.__class__.__name__+'\x1b[0m')
	print('\x1b[32m',end='')
	print(*q,**a)
	exit(1)

filename=None
if len(argv)>1:
	filename=argv[1]
	text=open(filename).read()
else:
	from sys import stdin
	text=stdin.read()
	print()

random_string_seed=1000000000000000000
def random_string(name=None):
	global random_string_seed
	random_string_seed+=1
	return '_'+str(random_string_seed)+(make_comment(name) if name !=None else '')

def make_comment(q):
	return ' /*'+str(q).replace('*/','*_/')+'*/ '

def esc(q):
	q=[q[w:w+3] for w in range(len(q))]
	return ''.join(['_0' if w[0]=='_' and w[1:]=='0x' else w[0] if w[0] in '1234567890poiuytrewqasdfghjklmnbvcxz_ZXCVBNMLKJHGFDSAQWERTYUIOP' else '_'+str(hex(ord(w[0])))+'x0_' for w in q])

var_creation=[]
def name(q,t=None):
	if t==None:
		if q not in var_creation[-1]:
			error('name',q,'is not defined')
	else:
		z=esc(q)
		x=esc(t)
		for w in range(z.count('_')+1,2,-1):
			z=z.replace('0'+'_'*w+'0','0'+'_'*(w+1)+'0')
		for w in range(x.count('_')+1,2,-1):
			x=x.replace('0'+'_'*w+'0','0'+'_'*(w+1)+'0')
		var_creation[-1][q]=z+'0___0'+x
		var_creation[-1][(q,t)]=var_creation[-1][q]
	return var_creation[-1][q]

indent=-1

before_main=''

	
def typeof(astobj):
	return 'int64_t'

gen_stack=[]

def generate(astobj):
	gen_stack.append(astobj)
	try:
		dump(astobj)
	except:
		print(astobj)
	global indent,before_main
	indent+=1
	ret=''
	if 0:
		ret=''
	elif type(astobj)==Module:
		var_creation.append({})
		r=''.join([generate(q) for q in astobj.body])
		ret=''.join(['\t'*indent+'\t'+w[1]+' '+var_creation[-1][w]+';\n' for w in var_creation[-1] if type(w)==tuple])+r
		var_creation.pop()
	elif type(astobj)==Expr:
		ret='\t'*indent+generate(astobj.value)+';\n'
	elif type(astobj)==Assign:
		for q in astobj.targets:
			if type(q)==Name:
				name(q.id,typeof(astobj.value))
		ret='\t'*indent+''.join([generate(w)+'=' for w in astobj.targets])+generate(astobj.value)+';\n'
	elif type(astobj)==Call:
		if type(astobj.func)==Name and astobj.func.id=='exec' and len(astobj.args)==1 and type(astobj.args[0])==Constant and type(astobj.args[0].value)==str:
			ret=astobj.args[0].value
		else:
			ret=generate(astobj.func)+'('+','.join([generate(w) for w in astobj.args])+')'			
	elif type(astobj)==Name:
		if astobj.id.startswith('__python__'):
			ret=str(astobj.id)
		else:
			# ret=('varible_get(' if type(astobj.ctx)!=Store else 'variable_set(')+name(astobj.id)+')'
			ret=name(astobj.id)
	elif type(astobj)==Constant:
		if type(astobj.value)==type(True):
			ret=str(astobj.value).lower()
		if type(astobj.value)==type(0):
			ret='int64_t('+str(astobj.value)+')'
		if type(astobj.value)==type(0.0):
			ret='(long double)('+str(astobj.value)+')'
		if type(astobj.value)==type(''):
			ret='std::u32string({'+','.join([str(ord(w)) for w in astobj.value])+'})'+make_comment(astobj.value)
	elif type(astobj)==List:
		ret='std::vector<>({'+','.join(['var('+generate(w)+')' for w in astobj.elts])+'})'
	elif type(astobj)==FunctionDef:
		var_creation.append({})
		arglist=astobj.args.posonlyargs+astobj.args.args
		arglist=[w.arg for w in arglist]
		defaults=astobj.args.defaults
		defaults=[None]*(len(arglist)-len(defaults))+defaults
		arglist=[w for w in zip(arglist,defaults)]
		before_main+=\
			'template <'+','.join(['typename t'+str(w[0])+('='+typeof(w[1]) if w[1]!=None else '') for w in enumerate(defaults)])+'>\n'+\
			'auto '+name(astobj.name,'function')+'('+','.join(['t'+str(w[0])+' '+name(w[1][0])+('='+generate(w[1][1]) if w[1][1]!=None else '') for w in enumerate(arglist)])+'){\n'
		r=\
			''.join([generate(w) for w in astobj.body])
		r=''.join(['\t'*indent+'\t'+w[1]+' '+var_creation[-1][w]+';\n' for w in var_creation[-1] if type(w)==tuple])+r
		before_main+=r+\
			'}'
		var_creation.pop()
	elif type(astobj)==Pass:
		ret=make_comment('pass')+'\n'
	else:
		ret=make_comment('\n'+dump(astobj,indent='\t')+'\n')
	indent-=1
	gen_stack.pop()
	return ret

# from headers import *

text=generate(parse(text))

text='''
'''.strip()+before_main+'''
'''.strip()+text

if filename!=None:
	open(filename+'.cpp','w').write(text)
	from subprocess import run
	if run(['g++','-o',filename+'.exe','-std=c++17','-Wfatal-errors',filename+'.cpp']).returncode==0:
		run(['./a.out'])
else:
	print(text,end='\n' if text[-1:]!='\n' else '')





