class typename:
	def __init__(s,o=None,**q):
		s.q=q
		if type(o)==str:
			s.q['name']=o
		if type(o)==dict:
			s.q.update(o)
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
class to_call:
	def __init__(s,**q):
		s.q=q
	def __getattr__(s,n):
		return s.q[n]
functions=[
	...
]
attributes=[
	...
]

