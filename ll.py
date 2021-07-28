from sys import argv
from functools import *
from re import *
from pprint import pprint
from ast import *
import ast
from copy import copy
try:
	from icecream import ic as _ic
	_ic.configureOutput(includeContext=True)
except:
	_ic=lambda *a:a[0] if len(a)==1 else [None,a][min(len(a),1)]
ic=_ic

def error(*q,**a):
	print('\x1b[31mERROR\x1b[0m')
	for w in gen_stack:
		print('\x1b[33min '+w.__class__.__name__+'\x1b[0m')
	print('\x1b[32m',end='')
	print(*q,**a)
	print('\x1b[0m',end='')
	raise BaseException
	# exit(1)

filename=None
if len(argv)>1:
	filename=argv[1]
	text=open(filename).read()
else:
	from sys import stdin
	text=stdin.read()
	print()

random_string_seed=100000000
def random_string(name=None):
	global random_string_seed
	random_string_seed+=1
	return '_'+str(random_string_seed)+(make_comment(name) if name !=None else '')+'_'

def make_comment(q):
	return ' /*'+str(q).replace('*/','*_/')+'*/ '

def esc(q):
	q=[q[w:w+3] for w in range(len(q))]
	return ''.join(['_0' if w[0]=='_' and w[1:]=='0x' else w[0] if w[0] in '1234567890poiuytrewqasdfghjklmnbvcxz_ZXCVBNMLKJHGFDSAQWERTYUIOP' else '_'+str(hex(ord(w[0])))+'x0_' for w in q])

class typename:
	def __init__(s,o=None,**q):
		if type(o)==dict:
			q=o
		s.q=q
		if type(s)==type(o):
			s.q.update(o.q)
	def __eq__(s,o):
		if type(s)==type(o):
			return s.__dict__==o.__dict__
		return False
	def __getattr__(s,n):
		if n in s.q:
			return s.q[n]
		else:
			error(s.name,'has no',n)
	def __hash__(s):
		from pickle import dumps
		return hash(dumps(s.q))
	def __reduce__(s):
		return typename,(s.q,)
	def __repr__(s):
		return 'typename'+repr(s.q)

var_creation=[]
var_escape=[]
var_global=[]
var_nonlocal=[]

def name(q,t=None,e=0):
	if t==None:
		index=len(var_global)-1
		while index>-1 and q in var_global[index] or q in var_nonlocal[index]:
			if q in var_nonlocal[index]:
				index-=1
			if q in var_global[index]:
				index=0
		for w in var_creation[:index+1][::-1]:
			if q in w:
				return w[q]
		error('name',q,'is not defined')
	else:
		index=len(var_global)-1
		while index>-1 and q in var_global[index] or q in var_nonlocal[index]:
			if q in var_nonlocal[index]:
				index-=1
			if q in var_global[index]:
				index=0

		if q.startswith('__python__'):
			v=q
		else:
			c='0___0'
			def pname(q):
				if q.name in 'list set tuple'.split():
					z,x=q.name,'L_'+'__'.join([pname(w) for w in [q.elt]])+'_J'
				elif q.name in 'dict'.split():
					z,x=q.name,'L_'+'__'.join([pname(w) for w in [q.key,q.value]])+'_J'
				elif q.name=='callable':
					z,x=q.name,'L_'+'__'.join([pname(w) for w in q.args[:-1]])+'_J'
				else:
					z,x=q.name,''
				# z=[(w if w==w.lower() else '_'+w.lower()+'_') if e else (w if w==w.upper() else '_'+w.upper()+'_').lower() for e,w in enumerate(z)]
				return ''.join(z)+('_'+x if x else '')
			if t.name in 'int bool float str list set tuple dict callable bytes bytearray'.split():
				c='0____0'
				x=pname(t)
			else:
				x=esc(type_convert(t))
			z=esc(q)
			for w in range(z.count('_')+1,2,-1):
				z=z.replace('0'+'_'*w+'0','0'+'_'*(w+3)+'0')
			for w in range(x.count('_')+1,2,-1):
				x=x.replace('0'+'_'*w+'0','0'+'_'*(w+3)+'0')
			v=''.join([w[None]+'0_____0' for w in var_creation[1:index+1]])+z+c+x

		var_creation[index][q]=v
		var_creation[index][(q,t)]=var_creation[index][q]
		if e:
			var_escape[index][q]=var_creation[index][q]
			var_escape[index][(q,t)]=var_creation[index][q]
		return var_creation[index][q]

indent=-1

var_create=''
before_main=''

def typeof(astobj):
	gen_stack.append(astobj)
	try:
		(dump(astobj,indent=4))
	except:
		print(astobj)
	ret=None
	if 0:
		pass
	elif type(astobj)==UnaryOp:
		if type(astobj.op)==UAdd:
			ret=typeof(astobj.operand)
		elif type(astobj.op)==USub:
			ret=typeof(astobj.operand)
		elif type(astobj.op)==Not:
			ret=typename(name='bool')
		elif type(astobj.op)==Invert:
			ret=typeof(astobj.operand)
	elif type(astobj)==BinOp:
		if typeof(astobj.left).name=='float':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='float':
			ret=typeof(astobj.right)
		elif typeof(astobj.left).name=='str':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='str':
			ret=typeof(astobj.right)
		elif typeof(astobj.left).name=='bytes':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='bytes':
			ret=typeof(astobj.right)
		elif typeof(astobj.left).name=='bytearray':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='bytearray':
			ret=typeof(astobj.right)
		elif typeof(astobj.left).name=='tuple':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='tuple':
			ret=typeof(astobj.right)
		elif typeof(astobj.left).name=='set':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='set':
			ret=typeof(astobj.right)
		elif typeof(astobj.left).name=='dict':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='dict':
			ret=typeof(astobj.right)
		elif typeof(astobj.left)==int:
			ret=typeof(astobj.left)
		elif typeof(astobj.right)==int:
			ret=typeof(astobj.right)
		ret=typeof(astobj.left)
	elif type(astobj)==BoolOp:
		ret=typename(name='bool')
	elif type(astobj)==Compare:
		ret=typename(name='bool')
	elif type(astobj)==IfExp:
		if typeof(astobj.body)!=typeof(astobj.orelse):
			error('different types in',type(astobj).__name__.lower())
		ret=typeof(astobj.body)
	elif type(astobj)==NamedExpr:
		ret=typeof(astobj.value)
	elif type(astobj)==JoinedStr:
		ret=typename(name='str')
	elif type(astobj)==Constant:
		# if typenameenable:
		ret=typename(name=type(astobj.value).__name__)
		# else:
		# 	ret=type(astobj.value)
	elif type(astobj)==Name:
		r=[]
		q=astobj.id
		index=len(var_global)-1
		while index>-1 and q in var_global[index] or q in var_nonlocal[index]:
			if q in var_nonlocal[index]:
				index-=1
			if q in var_global[index]:
				index=0
		for w in var_creation[:index+1]:
			if q in w:
				r=[e[1] for e in w if type(e)==tuple and e[0]==q and w[e]==w[q]]
		if len(r)!=1:
			error('found',len(r),'possible types for name',astobj.id)
		ret=r[0]
	elif type(astobj)==ast.List:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.elts)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.elts[w])!=typeof(astobj.elts[w+1]) for w in range(len(astobj.elts)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.elts[0])
		ret=typename(name='list',elt=t)
	elif type(astobj)==ast.Tuple:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.elts)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.elts[w])!=typeof(astobj.elts[w+1]) for w in range(len(astobj.elts)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.elts[0])
		ret=typename(name='tuple',elt=t)
	elif type(astobj)==ast.Set:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.elts)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.elts[w])!=typeof(astobj.elts[w+1]) for w in range(len(astobj.elts)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.elts[0])
		ret=typename(name='set',elt=t)
	elif type(astobj)==ast.Dict:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.keys)==0:
				error('emply',type(astobj).__name__.lower())
			if len(astobj.values)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.keys[w])!=typeof(astobj.keys[w+1]) for w in range(len(astobj.keys)-1)]):
				error('different types in',type(astobj).__name__.lower())
			if any([typeof(astobj.values[w])!=typeof(astobj.values[w+1]) for w in range(len(astobj.values)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.keys[0]),typeof(astobj.values[0])
		ret=typename(name='dict',key=t[0],value=t[1])
	elif type(astobj)==ListComp:
		ret=typename(name='list',elt=typeof(astobj.elt))
	elif type(astobj)==GeneratorExp:
		ret=typename(name='tuple',elt=typeof(astobj.elt))
	elif type(astobj)==SetComp:
		ret=typename(name='set',elt=typeof(astobj.elt))
	elif type(astobj)==DictComp:
		ret=typename(name='dict',key=typeof(astobj.key),value=typeof(astobj.value))
	elif type(astobj)==Subscript:
		if typeof(astobj.value) in 'list tuple set'.split():
			ret=typeof(astobj.value).elt
		elif typeof(astobj.value) in 'dict'.split():
			ret=typeof(astobj.value).value
		else:
			ret=typeof(astobj.value)
	elif type(astobj)==Call:
		if type(astobj.func)==Name:
			return return_type(functions[astobj.func.id].body)
	if ret==None:
		try:
			dump(astobj)
		except:
			error('cannot find type of',astobj)
		else:
			error('cannot find type of\n',dump(astobj,indent='\t'),sep='')
	gen_stack.pop()
	return ret

def type_convert(q):
	if q==typename(name='int'):
		return 'int64_t'
	if q==typename(name='bool'):
		return 'bool'
	if q==typename(name='float'):
		return 'long double'
	if q==typename(name='str'):
		return 'u32string'
	if q==typename(name='bytes'):
		return 'string'
	if q==typename(name='bytearray'):
		return 'string'
	if q.name=='list':
		return 'vector<'+','.join([type_convert(w) for w in [q.elt]])+'>'
	if q.name=='tuple':
		return 'vector<'+','.join([type_convert(w) for w in [q.elt]])+'>'
	if q.name=='set':
		return 'set<'+','.join([type_convert(w) for w in [q.elt]])+'>'
	if q.name=='dict':
		return 'map<'+','.join([type_convert(w) for w in [q.key,q.value]])+'>'
	if q.name=='void':
		return 'void'
	if q.name=='callable':
		return 'function'
	error('type',q,'not found')

def return_type(astobj,r=0):
	gen_stack.append(astobj)
	ret=[]
	if 0:
		pass
	elif type(astobj)==list:
		ret=sum([return_type(w,1) for w in astobj],[])
	elif type(astobj)==Return:
		if hasattr(astobj,'type'):
			ret=[astobj.type]
		else:
			error('return type not found')
	elif type(astobj)==For:
		ret=sum([return_type(w,1) for w in astobj.body+astobj.orelse],[])
	elif type(astobj)==If:
		ret=sum([return_type(w,1) for w in astobj.body+astobj.orelse],[])
	elif type(astobj)==While:
		ret=sum([return_type(w,1) for w in astobj.body+astobj.orelse],[])
	ret=list(set(ret))
	if len(ret)>1:
		error('different types in',type(astobj).__name__.lower())
	gen_stack.pop()
	if r==0:
		if len(ret)==0:
			ret.append(typename(name='void'))
		return ret[0]
	else:
		return ret

gen_stack=[]

functions={}

def generate(astobj):
	gen_stack.append(astobj)
	try:
		(dump(astobj,indent=4))
	except:
		print(astobj)
	global indent,before_main,var_create
	indent+=1
	ret=make_comment('\n'+dump(astobj,indent='\t')+'\n')
	if 0:
		ret=''
	elif type(astobj)==Module:
		var_creation.append({None:'Module'})
		var_escape.append({})
		var_nonlocal.append(set())
		var_global.append(set())
		r=''.join([generate(q) for q in astobj.body])
		# ret='int main(){\n'+''.join(['\t'*indent+'\t'+type_convert(w[1])+' '+var_creation[-1][w]+';\n' for w in var_creation[-1] if w not in var_escape[-1] and type(w)==tuple])+r+'\n}'
		ret='int main(){\n'+r+'\n}'
		var_create+=''.join([type_convert(w[1])+' '+var_creation[-1][w]+';\n' for w in var_creation[-1] if w not in var_escape[-1] and type(w)==tuple])
		var_creation.pop()
		var_escape.pop()
		var_nonlocal.pop()
		var_global.pop()
	elif type(astobj)==FunctionDef:
		arglist=astobj.args.posonlyargs+astobj.args.args
		defaults=astobj.args.defaults
		defaults=[None]*(len(arglist)-len(defaults))+defaults
		arglist=[w for w in zip(arglist,defaults)]
		if all([w[0].annotation!=None or w[1]!=None for w in arglist]):
			arglist=[[w[0].arg,w[1],w[0].annotation] for w in arglist]
			if (astobj.name,typename(name='callable',args=[w[2] for w in arglist])) not in var_creation[-1]:
				fn=name(astobj.name,typename(name='callable',args=[w[2] for w in arglist]),e=1)
				var_creation.append({None:astobj.name})
				var_escape.append({})
				var_nonlocal.append(set())
				var_global.append(set())
				for w in arglist:
					if w[1]!=None and typeof(w[1])!=w[2]:
						w[1]=None
				closed=0
				for w in arglist[::-1]:
					if w[1]==None:
						closed=1
					if closed:
						w[1]=None
				# r1=' '+fn+'('+','.join([type_convert(w[1][2])+' '+name(w[1][0],w[1][2],e=1)+('='+generate(w[1][1]) if w[1][1]!=None else '') for w in enumerate(arglist)])+'){\n'
				r1=' '+fn+'('+','.join([type_convert(w[1][2])+' '+name(f'arg{w[0]}_',w[1][2],e=1)+('='+generate(w[1][1]) if w[1][1]!=None else '') for w in enumerate(arglist)])+'){\n'
				r1+=''.join([generate(Assign(targets=[Name(id=w[0],ctx=Store())],value=Name(id=f'arg{q}_',ctx=Load()))) for q,w in enumerate(arglist)])
				r=''.join([generate(w) for w in astobj.body])
				# r=''.join(['\t'*indent+'\t'+type_convert(w[1])+' '+var_creation[-1][w]+';\n' for w in var_creation[-1] if w not in var_escape[-1] and type(w)==tuple])+r
				var_create+=''.join([type_convert(w[1])+' '+var_creation[-1][w]+';\n' for w in var_creation[-1] if w not in var_escape[-1] and type(w)==tuple])
				r2=type_convert(return_type(astobj.body))
				before_main+=r2+r1+r+\
					'}\n'
				var_creation.pop()
				var_escape.pop()
				var_nonlocal.pop()
				var_global.pop()
		if astobj.name not in functions:
			functions[astobj.name]=astobj
		ret=''
	elif type(astobj)==Call:
		if type(astobj.func)==Name and astobj.func.id=='exec' and len(astobj.args)==1 and type(astobj.args[0])==Constant and type(astobj.args[0].value)==str:
			ret=astobj.args[0].value
		elif type(astobj.func)==Name and astobj.func.id in functions:
			f=functions[astobj.func.id]
			f=copy(f)
			defaults=f.args.defaults
			defaults=[None]*(len(f.args.posonlyargs+f.args.args)-len(defaults))+defaults
			for q,w in enumerate(f.args.posonlyargs+f.args.args):
				if q<len(astobj.args):
					w.annotation=typeof(astobj.args[q])
				else:
					w.annotation=typeof(defaults[q])
			generate(f)
			ret=generate(astobj.func)+'('+','.join([generate(w) for w in astobj.args])+')'
	elif type(astobj)==Expr:
		ret='\t'*indent+generate(astobj.value)+';\n'
	elif type(astobj)==Assign:
		r=generate(astobj.value)
		for q in astobj.targets:
			if type(q)==Name:
				name(q.id,typeof(astobj.value))
		ret='\t'*indent+''.join([generate(w)+'=' for w in astobj.targets])+r+';\n'
	elif type(astobj)==Name:
		# if astobj.id.startswith('__python__'):
		# 	ret=str(astobj.id)
		# else:
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
			ret='u32string({'+','.join([str(ord(w)) for w in astobj.value])+'})'+make_comment(astobj.value)
	elif type(astobj)==ast.List:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.elts)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.elts[w])!=typeof(astobj.elts[w+1]) for w in range(len(astobj.elts)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.elts[0])
		ret='vector<'+type_convert(t)+'>({'+','.join([generate(w) for w in astobj.elts])+'})'
	elif type(astobj)==ast.Tuple:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.elts)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.elts[w])!=typeof(astobj.elts[w+1]) for w in range(len(astobj.elts)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.elts[0])
		ret='vector<'+type_convert(t)+'>({'+','.join([generate(w) for w in astobj.elts])+'})'
	elif type(astobj)==ast.Set:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.elts)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.elts[w])!=typeof(astobj.elts[w+1]) for w in range(len(astobj.elts)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.elts[0])
		ret='set<'+type_convert(t)+'>({'+','.join([generate(w) for w in astobj.elts])+'})'
	elif type(astobj)==ast.Dict:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.keys)==0:
				error('emply',type(astobj).__name__.lower())
			if len(astobj.values)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.keys[w])!=typeof(astobj.keys[w+1]) for w in range(len(astobj.keys)-1)]):
				error('different types in',type(astobj).__name__.lower())
			if any([typeof(astobj.values[w])!=typeof(astobj.values[w+1]) for w in range(len(astobj.values)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.keys[0]),typeof(astobj.keys[0])
		ret='map<'+type_convert(t[0])+','+type_convert(t[1])+'>({'+','.join(['{'+generate(w[0])+','+generate(w[1])+'}' for w in zip(astobj.keys,astobj.values)])+'})'
	elif type(astobj)==Pass:
		ret='\t'*indent+make_comment('pass')+'\n'
	elif type(astobj)==Return:
		if astobj.value==None:
			astobj.type=typename(name='void')
			ret='\t'*indent+'return ;\n'
		else:
			astobj.type=typeof(astobj.value)
			ret='\t'*indent+'return '+generate(astobj.value)+';\n'
	elif type(astobj)==Break:
		ret='\t'*indent+'break;\n'
	elif type(astobj)==Continue:
		ret='\t'*indent+'continue;\n'
	elif type(astobj)==If:
		ret='\t'*indent+'if ('+generate(astobj.test)+'){\n'+\
		''.join([generate(w) for w in astobj.body])+\
		'\t'*indent+'}else{\n'+\
		''.join([generate(w) for w in astobj.orelse])+\
		'\t'*indent+'}'
	elif type(astobj)==While:
		ret='\t'*indent+'while ('+generate(astobj.test)+'){\n'+\
		''.join([generate(w) for w in astobj.body])+\
		'\t'*indent+'}`'
	elif type(astobj)==For:
		r=generate(astobj.iter)
		t=typeof(astobj.iter)
		if type(astobj.target)==Name:
			if t.name in 'list tuple set'.split():
				name(astobj.target.id,t.elt)
			elif t.name in 'dict'.split():
				name(astobj.target.id,t.key)
			else:
				name(astobj.target.id,t)
		ret='\t'*indent+'for (auto iterator:'+r+'){\n'+\
		'\t'*indent+'\t'+generate(astobj.target)+'='+(type_convert(t)+'({iterator})' if t.name not in 'list tuple set dict'.split() else 'iterator.first' if t.name=='dict' else 'iterator')+';\n'+\
		''.join([generate(w) for w in astobj.body])+\
		'\t'*indent+'}'
	elif type(astobj)==ListComp:
		fn=random_string()
		ln=random_string()
		ro=Expr(value=Call(func=Attribute(value=Name(id=ln,ctx=Load()),attr='append',ctx=Load()),args=[astobj.elt],keywords=[]))
		targets=[]
		for w in astobj.generators[::-1]:
			for e in w.ifs:
				ro=If(test=e,orelse=[],body=[ro])
			ro=For(target=w.target,iter=w.iter,orelse=[],body=[ro])
			if type(w.target)==Name:
				targets.append(w.target.id)
		r=generate(ro).replace('\t','    ')
		l=ast.List(elts=[],type=typeof(astobj.elt))
		generate(FunctionDef(name=fn,args=arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),body=[
			Assign(targets=[Name(id=ln,ctx=Store())],value=l),
			Call(func=Name(id='exec',ctx=Load()),args=[Constant(value=r)],keywords={}),
			Return(value=Name(id=ln,ctx=Load()))
		],decorator_list=[]))
		ret=generate(Call(func=Name(id=fn,ctx=Load()),args=[]))
	elif type(astobj)==GeneratorExp:
		fn=random_string()
		ln=random_string()
		ro=Expr(value=Call(func=Attribute(value=Name(id=ln,ctx=Load()),attr='append',ctx=Load()),args=[astobj.elt],keywords=[]))
		targets=[]
		for w in astobj.generators[::-1]:
			for e in w.ifs:
				ro=If(test=e,orelse=[],body=[ro])
			ro=For(target=w.target,iter=w.iter,orelse=[],body=[ro])
			if type(w.target)==Name:
				targets.append(w.target.id)
		generate(ro)
		l=ast.Tuple(elts=[],type=typeof(astobj.elt))
		generate(FunctionDef(name=fn,args=arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),body=[
			Assign(targets=[Name(id=ln,ctx=Store())],value=l),
			Nonlocal(names=targets),
			ro,
			Return(value=Name(id=ln,ctx=Load()))
		],decorator_list=[]))
		ret=generate(Call(func=Name(id=fn,ctx=Load()),args=[]))
	elif type(astobj)==SetComp:
		fn=random_string()
		ln=random_string()
		ro=Expr(value=Call(func=Attribute(value=Name(id=ln,ctx=Load()),attr='add',ctx=Load()),args=[astobj.elt],keywords=[]))
		targets=[]
		for w in astobj.generators[::-1]:
			for e in w.ifs:
				ro=If(test=e,orelse=[],body=[ro])
			ro=For(target=w.target,iter=w.iter,orelse=[],body=[ro])
			if type(w.target)==Name:
				targets.append(w.target.id)
		generate(ro)
		l=ast.Set(elts=[],type=typeof(astobj.elt))
		generate(FunctionDef(name=fn,args=arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),body=[
			Assign(targets=[Name(id=ln,ctx=Store())],value=l),
			Nonlocal(names=targets),
			ro,
			Return(value=Name(id=ln,ctx=Load()))
		],decorator_list=[]))
		ret=generate(Call(func=Name(id=fn,ctx=Load()),args=[]))
	elif type(astobj)==DictComp:
		fn=random_string()
		ln=random_string()
		ro=Expr(value=Call(func=Attribute(value=Name(id=ln,ctx=Load()),attr='update',ctx=Load()),args=[ast.Dict(keys=[astobj.key],values=[astobj.value],ctx=Load())],keywords=[]))
		targets=[]
		for w in astobj.generators[::-1]:
			for e in w.ifs:
				ro=If(test=e,orelse=[],body=[ro])
			ro=For(target=w.target,iter=w.iter,orelse=[],body=[ro])
			if type(w.target)==Name:
				targets.append(w.target.id)
		generate(ro)
		l=ast.Dict(keys=[],values=[],type=(typeof(astobj.key),typeof(astobj.value)))
		generate(FunctionDef(name=fn,args=arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),body=[
			Assign(targets=[Name(id=ln,ctx=Store())],value=l),
			Nonlocal(names=targets),
			ro,
			Return(value=Name(id=ln,ctx=Load()))
		],decorator_list=[]))
		ret=generate(Call(func=Name(id=fn,ctx=Load()),args=[]))
	elif type(astobj)==UnaryOp:
		if type(astobj.op)==UAdd:
			ret='(+('+generate(astobj.operand)+'))'
		if type(astobj.op)==USub:
			ret='(-('+generate(astobj.operand)+'))'
		if type(astobj.op)==Not:
			ret='(!!('+generate(astobj.operand)+'))'
		if type(astobj.op)==Invert:
			ret='(~('+generate(astobj.operand)+'))'
	elif type(astobj)==BinOp:
		if type(astobj.op)==Add:
			ret='(('+generate(astobj.left)+')+('+generate(astobj.right)+'))'
		if type(astobj.op)==Sub:
			ret='(('+generate(astobj.left)+')-('+generate(astobj.right)+'))'
		if type(astobj.op)==Mult:
			ret='(('+generate(astobj.left)+')*('+generate(astobj.right)+'))'
		if type(astobj.op)==Div:
			ret='(('+generate(astobj.left)+')/('+generate(astobj.right)+'))'
		if type(astobj.op)==FloorDiv:
			ret='(('+generate(astobj.left)+')/('+generate(astobj.right)+'))'
		if type(astobj.op)==Mod:
			ret='(('+generate(astobj.left)+')%('+generate(astobj.right)+'))'
		if type(astobj.op)==LShift:
			ret='(('+generate(astobj.left)+')<<('+generate(astobj.right)+'))'
		if type(astobj.op)==RShift:
			ret='(('+generate(astobj.left)+')>>('+generate(astobj.right)+'))'
		if type(astobj.op)==BitOr:
			ret='(('+generate(astobj.left)+')|('+generate(astobj.right)+'))'
		if type(astobj.op)==BitAnd:
			ret='(('+generate(astobj.left)+')&('+generate(astobj.right)+'))'
	elif type(astobj)==BoolOp:
		if type(astobj.op)==Or:
			ret='('+'||'.join(['('+generate(w)+')' for w in astobj.values])+')'
		if type(astobj.op)==And:
			ret='('+'||'.join(['('+generate(w)+')' for w in astobj.values])+')'
	elif type(astobj)==Global:
		for w in astobj.names:
			var_global[-1].add(w)
			var_global[-1].add((w,typeof(Name(id=w,ctx=Load()))))
		ret=''
	elif type(astobj)==Nonlocal:
		for w in astobj.names:
			var_nonlocal[-1].add(w)
			var_nonlocal[-1].add((w,typeof(Name(id=w,ctx=Load()))))
		ret=''
	elif type(astobj)==Subscript:
		if type(astobj.slice==Slice):
			pass
		else:
			ret=generate(astobj.value)+'['+generate(astobj.slice)+']' if typeof(astobj.value).name in 'list tuple set dict'.split() else type_convert(typeof(astobj.value))+'({'+generate(astobj.value)+'['+generate(astobj.slice)+']})'
	elif type(astobj)==AugAssign:
		if type(astobj.op)==Add:
			ret='(('+generate(astobj.target)+')+=('+generate(astobj.value)+'));'
		if type(astobj.op)==Sub:
			ret='(('+generate(astobj.target)+')-=('+generate(astobj.value)+'));'
		if type(astobj.op)==Mult:
			ret='(('+generate(astobj.target)+')*=('+generate(astobj.value)+'));'
		if type(astobj.op)==Div:
			ret='(('+generate(astobj.target)+')/=('+generate(astobj.value)+'));'
		if type(astobj.op)==FloorDiv:
			ret='(('+generate(astobj.target)+')/=('+generate(astobj.value)+'));'
		if type(astobj.op)==Mod:
			ret='(('+generate(astobj.target)+')%=('+generate(astobj.value)+'));'
		if type(astobj.op)==LShift:
			ret='(('+generate(astobj.target)+')<<=('+generate(astobj.value)+'));'
		if type(astobj.op)==RShift:
			ret='(('+generate(astobj.target)+')>>=('+generate(astobj.value)+'));'
		if type(astobj.op)==BitOr:
			ret='(('+generate(astobj.target)+')|=('+generate(astobj.value)+'));'
		if type(astobj.op)==BitAnd:
			ret='(('+generate(astobj.target)+')&=('+generate(astobj.value)+'));'
	indent-=1
	gen_stack.pop()
	return ret

# from headers import *

text=generate(parse(text))

text='''
#include <bits/stdc++.h>
using namespace std;
'''+var_create+before_main+text

if filename!=None:
	open(filename+'.cpp','w').write(text)
	from subprocess import run
	if run(['g++','-o',filename+'.exe','-std=c++17','-Wfatal-errors',filename+'.cpp']).returncode==0:
		run([filename+'.exe'])
else:
	print(text,end='\n' if text[-1:]!='\n' else '')





