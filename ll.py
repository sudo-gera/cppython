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
	return '_'+str(random_string_seed)+(esc(name) if name !=None else '')+'_'

def make_comment(q):
	return ' /*'+str(q).replace('*/','*_/').replace('\x00','\\x00').replace('\n','\\n').replace('\r','\\r')+'*/ '

def esc(q):
	q=[q[w:w+3] for w in range(len(q))]
	return ''.join(['_0' if w[0]=='_' and w[1:]=='0x' else w[0] if w[0] in '1234567890poiuytrewqasdfghjklmnbvcxz_ZXCVBNMLKJHGFDSAQWERTYUIOP' else '_'+str(hex(ord(w[0])))+'x0_' for w in q])

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
		return s==typename(o)
	def __getattr__(s,n):
		return s.q[n]
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
	def __repr__(s):
		return 'to_call'+repr(s.q)
calls=[
	to_call(name='bool',returns='bool',args=[],code=lambda args:'bool()',headers=[]),
	to_call(name='bool',returns='bool',args=['bool'],code=lambda args:'bool('+generate(args[0])+')',headers=[]),
	to_call(name='bool',returns='bool',args=['int'],code=lambda args:'bool('+generate(args[0])+')',headers=[]),
	to_call(name='bool',returns='bool',args=['float'],code=lambda args:'bool('+generate(args[0])+')',headers=[]),
	to_call(name='bool',returns='bool',args=['str'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	to_call(name='bool',returns='bool',args=['bytes'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	to_call(name='bool',returns='bool',args=['bytearray'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	to_call(name='bool',returns='bool',args=['list'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	to_call(name='bool',returns='bool',args=['tuple'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	to_call(name='bool',returns='bool',args=['set'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	to_call(name='bool',returns='bool',args=['frozenset'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	to_call(name='bool',returns='bool',args=['dict'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),

	to_call(name='int',returns='int',args=[],code=lambda args:'int64_t()',headers=[]),
	to_call(name='int',returns='int',args=['bool'],code=lambda args:'int64_t('+generate(args[0])+')',headers=[]),
	to_call(name='int',returns='int',args=['int'],code=lambda args:'int64_t('+generate(args[0])+')',headers=[]),
	to_call(name='int',returns='int',args=['float'],code=lambda args:'int64_t('+generate(args[0])+')',headers=[]),
	to_call(name='int',returns='int',args=['str'],code=lambda args:'int64_t(to_u32(stoll('+generate(args[0])+')))',headers=[]),
	to_call(name='int',returns='int',args=['bytes'],code=lambda args:'int64_t(stoll('+args[0]+'))',headers=[]),
	to_call(name='int',returns='int',args=['bytearray'],code=lambda args:'int64_t(stoll('+args[0]+'))',headers=[]),

	to_call(name='float',returns='float',args=[],code=lambda args:'(long double)()',headers=[]),
	to_call(name='float',returns='float',args=['bool'],code=lambda args:'(long double)('+generate(args[0])+')',headers=[]),
	to_call(name='float',returns='float',args=['int'],code=lambda args:'(long double)('+generate(args[0])+')',headers=[]),
	to_call(name='float',returns='float',args=['float'],code=lambda args:'(long double)('+generate(args[0])+')',headers=[]),
	to_call(name='float',returns='float',args=['str'],code=lambda args:'(long double)(to_u32(stold('+generate(args[0])+')))',headers=['unicode_convert']),
	to_call(name='float',returns='float',args=['bytes'],code=lambda args:'(long double)(stoll('+args[0]+'))',headers=[]),
	to_call(name='float',returns='float',args=['bytearray'],code=lambda args:'(long double)(stoll('+args[0]+'))',headers=[]),

	to_call(name='str',returns='str',args=[],code=lambda args:'u32string()',headers=['unicode_convert']),
	to_call(name='str',returns='str',args=['bool'],code=lambda args:'to_u32(('+generate(args[0])+')?"True":"False")',headers=['unicode_convert']),
	to_call(name='str',returns='str',args=['int'],code=lambda args:'to_u32(to_string('+generate(args[0])+'))',headers=['unicode_convert']),
	to_call(name='str',returns='str',args=['float'],code=lambda args:'to_u32(to_string('+generate(args[0])+'))',headers=['unicode_convert']),
	to_call(name='str',returns='str',args=['str'],code=lambda args:'('+generate(args[0])+')',headers=[]),
	to_call(name='str',returns='str',args=['bytes'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='str',returns='str',args=['bytearray'],code=lambda args:'u32string({\'b\',\'y\',\'t\',\'e\',\'a\',\'r\',\'r\',\'a\',\'y\',\'(\'})+repr('+generate(args[0])+')+u32string({\')\'})',headers=['repr']),
	to_call(name='str',returns='str',args=['list'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='str',returns='str',args=['tuple'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='str',returns='str',args=['set'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='str',returns='str',args=['frozenset'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='str',returns='str',args=['dict'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),

	to_call(name='repr',returns='str',args=['bool'],code=lambda args:'to_u32(('+generate(args[0])+')?"True":"False")',headers=['unicode_convert']),
	to_call(name='repr',returns='str',args=['int'],code=lambda args:'to_u32(to_string('+generate(args[0])+'))',headers=['unicode_convert']),
	to_call(name='repr',returns='str',args=['float'],code=lambda args:'to_u32(to_string('+generate(args[0])+'))',headers=['unicode_convert']),
	to_call(name='repr',returns='str',args=['str'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='repr',returns='str',args=['bytes'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='repr',returns='str',args=['bytearray'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='repr',returns='str',args=['list'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='repr',returns='str',args=['tuple'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='repr',returns='str',args=['set'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='repr',returns='str',args=['frozenset'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),
	to_call(name='repr',returns='str',args=['dict'],code=lambda args:'repr('+generate(args[0])+')',headers=['repr']),

	to_call(name='bytes',returns='bytes',args=[],code=lambda args:'string()',headers=[]),
	to_call(name='bytes',returns='bytes',args=['bool'],code=lambda args:'string(('+generate(args[0])+')?"True":"False")',headers=[]),
	# to_call(name='bytes',returns='bytes',args=['int'],code=lambda args:'bool('+generate(args[0])+')',headers=[]),
	to_call(name='bytes',returns='bytes',args=['str'],code=lambda args:'to_u8('+generate(args[0])+')',headers=['unicode_convert']),
	to_call(name='bytes',returns='bytes',args=['bytes'],code=lambda args:'('+generate(args[0])+')',headers=[]),
	to_call(name='bytes',returns='bytes',args=['bytearray'],code=lambda args:'('+generate(args[0])+')',headers=[]),
	# to_call(name='bytes',returns='bytes',args=['list'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	# to_call(name='bytes',returns='bytes',args=['tuple'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	# to_call(name='bytes',returns='bytes',args=['set'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	# to_call(name='bytes',returns='bytes',args=['frozenset'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	# to_call(name='bytes',returns='bytes',args=['dict'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),

	to_call(name='bytearray',returns='bytes',args=[],code=lambda args:'string()',headers=[]),
	to_call(name='bytearray',returns='bytearray',args=['bool'],code=lambda args:'string(('+generate(args[0])+')?"True":"False")',headers=[]),
	# to_call(name='bytearray',returns='bytearray',args=['int'],code=lambda args:'bool('+generate(args[0])+')',headers=[]),
	to_call(name='bytearray',returns='bytearray',args=['str'],code=lambda args:'to_u8('+generate(args[0])+')',headers=['unicode_convert']),
	to_call(name='bytearray',returns='bytearray',args=['bytes'],code=lambda args:'('+generate(args[0])+')',headers=[]),
	to_call(name='bytearray',returns='bytearray',args=['bytearray'],code=lambda args:'('+generate(args[0])+')',headers=[]),
	# to_call(name='bytearray',returns='bytearray',args=['list'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	# to_call(name='bytearray',returns='bytearray',args=['tuple'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	# to_call(name='bytearray',returns='bytearray',args=['set'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	# to_call(name='bytearray',returns='bytearray',args=['frozenset'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),
	# to_call(name='bytearray',returns='bytearray',args=['dict'],code=lambda args:'bool(('+generate(args[0])+').size())',headers=[]),

	to_call(name='range',returns=typename(name='list',elt='int'),args=['int'            ],code=lambda args:'range('+','.join([generate(w) for w in args])+')',headers=['range']),
	to_call(name='range',returns=typename(name='list',elt='int'),args=['int','int'      ],code=lambda args:'range('+','.join([generate(w) for w in args])+')',headers=['range']),
	to_call(name='range',returns=typename(name='list',elt='int'),args=['int','int','int'],code=lambda args:'range('+','.join([generate(w) for w in args])+')',headers=['range']),
	to_call(name='chr',returns=typename(name='str'),args=['int'],code=lambda args:'u32string({chr('+generate(args[0])+')})',headers=['unicode_convert']),
	to_call(name='ord',returns=typename(name='int'),args=['str'],code=lambda args:'ord(('+generate(args[0])+')[0])',headers=['unicode_convert']),
	to_call(name='abs',returns=typename(name='int'),args=['int'],code=lambda args:'abs('+generate(args[0])+')',headers=['unicode_convert']),
	to_call(name='abs',returns=typename(name='float'),args=['float'],code=lambda args:'abs('+generate(args[0])+')',headers=['unicode_convert']),
	to_call(name='all',returns='bool',args=['list'],code=lambda args:[convert(headers()['all']['python_code']),generate(Call(func=Name(id='all',ctx=Load()),args=args,keywords={}))][1],headers=['all']),
	to_call(name='any',returns='bool',args=['list'],code=lambda args:[convert(headers()['any']['python_code']),generate(Call(func=Name(id='any',ctx=Load()),args=args,keywords={}))][1],headers=['any']),
]
def convert(q,a=1):
	if a:
		while '\n' in q[:-len(q.lstrip())]:
			q=q[1:]
		while '\r' in q[:-len(q.lstrip())]:
			q=q[1:]
		l=(len(q)-len(q.lstrip()))
		q=q.split('\n')
		q='\n'.join([w[l:] for w in q])
	return generate(parse(q))

attributes=[
	# ...
]

for w in calls:
	w.returns=typename(w.returns)
	w.args=[typename(w) for w in w.args]

for w in attributes:
	w.returns=typename(w.returns)
	w.value=typename(w.value)
	w.args=[typename(w) for w in w.args]

headers=lambda :{
	'repr':{
		'c++_code':
			r'''
				u32string repr(bool q){
					return to_u32(q?"True":"False");
				}
				u32string repr(int64_t q){
					return to_u32(to_string(q));
				}
				u32string repr(long double q){
					return to_u32(to_string(q));
				}
				template<typename T>
				u32string repr(basic_string<T> q){
					auto ret=u32string();
					auto bs=vector<int>({31, 126, 160, 172, 173, 887, 889, 895, 899, 906, 907, 908, 909, 929, 930, 1327, 1328, 1366, 1368, 1418, 1420, 1423, 1424, 1479, 1487, 1514, 1518, 1524, 1541, 1563, 1565, 1756, 1757, 1805, 1807, 1866, 1868, 1969, 1983, 2042, 2044, 2093, 2095, 2110, 2111, 2139, 2141, 2142, 2143, 2154, 2207, 2228, 2229, 2247, 2258, 2273, 2274, 2435, 2436, 2444, 2446, 2448, 2450, 2472, 2473, 2480, 2481, 2482, 2485, 2489, 2491, 2500, 2502, 2504, 2506, 2510, 2518, 2519, 2523, 2525, 2526, 2531, 2533, 2558, 2560, 2563, 2564, 2570, 2574, 2576, 2578, 2600, 2601, 2608, 2609, 2611, 2612, 2614, 2615, 2617, 2619, 2620, 2621, 2626, 2630, 2632, 2634, 2637, 2640, 2641, 2648, 2652, 2653, 2654, 2661, 2678, 2688, 2691, 2692, 2701, 2702, 2705, 2706, 2728, 2729, 2736, 2737, 2739, 2740, 2745, 2747, 2757, 2758, 2761, 2762, 2765, 2767, 2768, 2783, 2787, 2789, 2801, 2808, 2815, 2816, 2819, 2820, 2828, 2830, 2832, 2834, 2856, 2857, 2864, 2865, 2867, 2868, 2873, 2875, 2884, 2886, 2888, 2890, 2893, 2900, 2903, 2907, 2909, 2910, 2915, 2917, 2935, 2945, 2947, 2948, 2954, 2957, 2960, 2961, 2965, 2968, 2970, 2971, 2972, 2973, 2975, 2978, 2980, 2983, 2986, 2989, 3001, 3005, 3010, 3013, 3016, 3017, 3021, 3023, 3024, 3030, 3031, 3045, 3066, 3071, 3084, 3085, 3088, 3089, 3112, 3113, 3129, 3132, 3140, 3141, 3144, 3145, 3149, 3156, 3158, 3159, 3162, 3167, 3171, 3173, 3183, 3190, 3212, 3213, 3216, 3217, 3240, 3241, 3251, 3252, 3257, 3259, 3268, 3269, 3272, 3273, 3277, 3284, 3286, 3293, 3294, 3295, 3299, 3301, 3311, 3312, 3314, 3327, 3340, 3341, 3344, 3345, 3396, 3397, 3400, 3401, 3407, 3411, 3427, 3429, 3455, 3456, 3459, 3460, 3478, 3481, 3505, 3506, 3515, 3516, 3517, 3519, 3526, 3529, 3530, 3534, 3540, 3541, 3542, 3543, 3551, 3557, 3567, 3569, 3572, 3584, 3642, 3646, 3675, 3712, 3714, 3715, 3716, 3717, 3722, 3723, 3747, 3748, 3749, 3750, 3773, 3775, 3780, 3781, 3782, 3783, 3789, 3791, 3801, 3803, 3807, 3839, 3911, 3912, 3948, 3952, 3991, 3992, 4028, 4029, 4044, 4045, 4058, 4095, 4293, 4294, 4295, 4300, 4301, 4303, 4680, 4681, 4685, 4687, 4694, 4695, 4696, 4697, 4701, 4703, 4744, 4745, 4749, 4751, 4784, 4785, 4789, 4791, 4798, 4799, 4800, 4801, 4805, 4807, 4822, 4823, 4880, 4881, 4885, 4887, 4954, 4956, 4988, 4991, 5017, 5023, 5109, 5111, 5117, 5119, 5759, 5760, 5788, 5791, 5880, 5887, 5900, 5901, 5908, 5919, 5942, 5951, 5971, 5983, 5996, 5997, 6000, 6001, 6003, 6015, 6109, 6111, 6121, 6127, 6137, 6143, 6157, 6159, 6169, 6175, 6264, 6271, 6314, 6319, 6389, 6399, 6430, 6431, 6443, 6447, 6459, 6463, 6464, 6467, 6509, 6511, 6516, 6527, 6571, 6575, 6601, 6607, 6618, 6621, 6683, 6685, 6750, 6751, 6780, 6782, 6793, 6799, 6809, 6815, 6829, 6831, 6848, 6911, 6987, 6991, 7036, 7039, 7155, 7163, 7223, 7226, 7241, 7244, 7304, 7311, 7354, 7356, 7367, 7375, 7418, 7423, 7673, 7674, 7957, 7959, 7965, 7967, 8005, 8007, 8013, 8015, 8023, 8024, 8025, 8026, 8027, 8028, 8029, 8030, 8061, 8063, 8116, 8117, 8132, 8133, 8147, 8149, 8155, 8156, 8175, 8177, 8180, 8181, 8190, 8207, 8231, 8239, 8286, 8303, 8305, 8307, 8334, 8335, 8348, 8351, 8383, 8399, 8432, 8447, 8587, 8591, 9254, 9279, 9290, 9311, 11123, 11125, 11157, 11158, 11310, 11311, 11358, 11359, 11507, 11512, 11557, 11558, 11559, 11564, 11565, 11567, 11623, 11630, 11632, 11646, 11670, 11679, 11686, 11687, 11694, 11695, 11702, 11703, 11710, 11711, 11718, 11719, 11726, 11727, 11734, 11735, 11742, 11743, 11858, 11903, 11929, 11930, 12019, 12031, 12245, 12271, 12283, 12288, 12351, 12352, 12438, 12440, 12543, 12548, 12591, 12592, 12686, 12687, 12771, 12783, 12830, 12831, 40956, 40959, 42124, 42127, 42182, 42191, 42539, 42559, 42743, 42751, 42943, 42945, 42954, 42996, 43052, 43055, 43065, 43071, 43127, 43135, 43205, 43213, 43225, 43231, 43347, 43358, 43388, 43391, 43469, 43470, 43481, 43485, 43518, 43519, 43574, 43583, 43597, 43599, 43609, 43611, 43714, 43738, 43766, 43776, 43782, 43784, 43790, 43792, 43798, 43807, 43814, 43815, 43822, 43823, 43883, 43887, 44013, 44015, 44025, 44031, 55203, 55215, 55238, 55242, 55291, 63743, 64109, 64111, 64217, 64255, 64262, 64274, 64279, 64284, 64310, 64311, 64316, 64317, 64318, 64319, 64321, 64322, 64324, 64325, 64449, 64466, 64831, 64847, 64911, 64913, 64967, 65007, 65021, 65023, 65049, 65055, 65106, 65107, 65126, 65127, 65131, 65135, 65140, 65141, 65276, 65280, 65470, 65473, 65479, 65481, 65487, 65489, 65495, 65497, 65500, 65503, 65510, 65511, 65518, 65531, 65533, 65535, 65547, 65548, 65574, 65575, 65594, 65595, 65597, 65598, 65613, 65615, 65629, 65663, 65786, 65791, 65794, 65798, 65843, 65846, 65934, 65935, 65948, 65951, 65952, 65999, 66045, 66175, 66204, 66207, 66256, 66271, 66299, 66303, 66339, 66348, 66378, 66383, 66426, 66431, 66461, 66462, 66499, 66503, 66517, 66559, 66717, 66719, 66729, 66735, 66771, 66775, 66811, 66815, 66855, 66863, 66915, 66926, 66927, 67071, 67382, 67391, 67413, 67423, 67431, 67583, 67589, 67591, 67592, 67593, 67637, 67638, 67640, 67643, 67644, 67646, 67669, 67670, 67742, 67750, 67759, 67807, 67826, 67827, 67829, 67834, 67867, 67870, 67897, 67902, 67903, 67967, 68023, 68027, 68047, 68049, 68099, 68100, 68102, 68107, 68115, 68116, 68119, 68120, 68149, 68151, 68154, 68158, 68168, 68175, 68184, 68191, 68255, 68287, 68326, 68330, 68342, 68351, 68405, 68408, 68437, 68439, 68466, 68471, 68497, 68504, 68508, 68520, 68527, 68607, 68680, 68735, 68786, 68799, 68850, 68857, 68903, 68911, 68921, 69215, 69246, 69247, 69289, 69290, 69293, 69295, 69297, 69375, 69415, 69423, 69465, 69551, 69579, 69599, 69622, 69631, 69709, 69713, 69743, 69758, 69820, 69821, 69825, 69839, 69864, 69871, 69881, 69887, 69940, 69941, 69959, 69967, 70006, 70015, 70111, 70112, 70132, 70143, 70161, 70162, 70206, 70271, 70278, 70279, 70280, 70281, 70285, 70286, 70301, 70302, 70313, 70319, 70378, 70383, 70393, 70399, 70403, 70404, 70412, 70414, 70416, 70418, 70440, 70441, 70448, 70449, 70451, 70452, 70457, 70458, 70468, 70470, 70472, 70474, 70477, 70479, 70480, 70486, 70487, 70492, 70499, 70501, 70508, 70511, 70516, 70655, 70747, 70748, 70753, 70783, 70855, 70863, 70873, 71039, 71093, 71095, 71133, 71167, 71236, 71247, 71257, 71263, 71276, 71295, 71352, 71359, 71369, 71423, 71450, 71452, 71467, 71471, 71487, 71679, 71739, 71839, 71922, 71934, 71942, 71944, 71945, 71947, 71955, 71956, 71958, 71959, 71989, 71990, 71992, 71994, 72006, 72015, 72025, 72095, 72103, 72105, 72151, 72153, 72164, 72191, 72263, 72271, 72354, 72383, 72440, 72703, 72712, 72713, 72758, 72759, 72773, 72783, 72812, 72815, 72847, 72849, 72871, 72872, 72886, 72959, 72966, 72967, 72969, 72970, 73014, 73017, 73018, 73019, 73021, 73022, 73031, 73039, 73049, 73055, 73061, 73062, 73064, 73065, 73102, 73103, 73105, 73106, 73112, 73119, 73129, 73439, 73464, 73647, 73648, 73663, 73713, 73726, 74649, 74751, 74862, 74863, 74868, 74879, 75075, 77823, 78894, 82943, 83526, 92159, 92728, 92735, 92766, 92767, 92777, 92781, 92783, 92879, 92909, 92911, 92917, 92927, 92997, 93007, 93017, 93018, 93025, 93026, 93047, 93052, 93071, 93759, 93850, 93951, 94026, 94030, 94087, 94094, 94111, 94175, 94180, 94191, 94193, 94207, 100343, 100351, 101589, 101631, 101640, 110591, 110878, 110927, 110930, 110947, 110951, 110959, 111355, 113663, 113770, 113775, 113788, 113791, 113800, 113807, 113817, 113819, 113823, 118783, 119029, 119039, 119078, 119080, 119154, 119162, 119272, 119295, 119365, 119519, 119539, 119551, 119638, 119647, 119672, 119807, 119892, 119893, 119964, 119965, 119967, 119969, 119970, 119972, 119974, 119976, 119980, 119981, 119993, 119994, 119995, 119996, 120003, 120004, 120069, 120070, 120074, 120076, 120084, 120085, 120092, 120093, 120121, 120122, 120126, 120127, 120132, 120133, 120134, 120137, 120144, 120145, 120485, 120487, 120779, 120781, 121483, 121498, 121503, 121504, 121519, 122879, 122886, 122887, 122904, 122906, 122913, 122914, 122916, 122917, 122922, 123135, 123180, 123183, 123197, 123199, 123209, 123213, 123215, 123583, 123641, 123646, 123647, 124927, 125124, 125126, 125142, 125183, 125259, 125263, 125273, 125277, 125279, 126064, 126132, 126208, 126269, 126463, 126467, 126468, 126495, 126496, 126498, 126499, 126500, 126502, 126503, 126504, 126514, 126515, 126519, 126520, 126521, 126522, 126523, 126529, 126530, 126534, 126535, 126536, 126537, 126538, 126539, 126540, 126543, 126544, 126546, 126547, 126548, 126550, 126551, 126552, 126553, 126554, 126555, 126556, 126557, 126558, 126559, 126560, 126562, 126563, 126564, 126566, 126570, 126571, 126578, 126579, 126583, 126584, 126588, 126589, 126590, 126591, 126601, 126602, 126619, 126624, 126627, 126628, 126633, 126634, 126651, 126703, 126705, 126975, 127019, 127023, 127123, 127135, 127150, 127152, 127167, 127168, 127183, 127184, 127221, 127231, 127405, 127461, 127490, 127503, 127547, 127551, 127560, 127567, 127569, 127583, 127589, 127743, 128727, 128735, 128748, 128751, 128764, 128767, 128883, 128895, 128984, 128991, 129003, 129023, 129035, 129039, 129095, 129103, 129113, 129119, 129159, 129167, 129197, 129199, 129201, 129279, 129400, 129401, 129483, 129484, 129619, 129631, 129645, 129647, 129652, 129655, 129658, 129663, 129670, 129679, 129704, 129711, 129718, 129727, 129730, 129743, 129750, 129791, 129938, 129939, 129994, 130031, 130041, 131071, 173789, 173823, 177972, 177983, 178205, 178207, 183969, 183983, 191456, 194559, 195101, 196607, 201546, 917759, 917999});
					int qu=0;
					for (auto w:q){
						if (w=='\'' and qu==0){
							qu=1;
						}
						if (w=='"'){
							qu=2;
						}
						if(w==0){
							ret+=u32string({'\\','x','0','0'});
						}else if(w==9){
							ret+=u32string({'\\','t'});
						}else if(w==10){
							ret+=u32string({'\\','n'});
						}else if(w==13){
							ret+=u32string({'\\','r'});
						}else if(w==90){
							ret+=u32string({'\\','\\'});
						}else if ((lower_bound(bs.begin(),bs.end(),w)-bs.begin())%2){
							ret+=u32string({' '});
							ret[ret.size()-1]=w;
						}else{
							cout<<__LINE__<<' '<<to_u8(ret)<<endl;
							if (w>0xffff){
								ret+=u32string({'\\','U','0','0','0','0','0','0','0','0'});
							}else if (w>0xff){
								ret+=u32string({'\\','u','0','0','0','0'});
							}else{
								ret+=u32string({'\\','x','0','0'});
							}
							cout<<__LINE__<<' '<<to_u8(ret)<<endl;
							{
								cout<<sizeof(w)<<endl;
								auto q=w;

								cout<<__LINE__<<' '<<q<<endl;
								int c=0;
								while (q){
									c+=1;
									decltype(ret[0]+1) h[]={'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'};
									ret[ret.size()-c]=h[q&0xf];
									q>>=4;
								}
							}
							cout<<__LINE__<<' '<<to_u8(ret)<<endl;
						}
					}
					if (qu==1){
						ret=u32string({'"'})+ret+u32string({'"'});
					}else{
						ret=u32string({'\''})+ret+u32string({'\''});
					}
					if (sizeof(T)<sizeof(u32string)){
						ret=u32string({'b'})+ret;
					}
					return ret;
				}
				template<typename T>
				u32string repr(vector<T> q){
					auto ret=u32string({'['});
					bool c=0;
					for (auto w:q){
						if (c){
							ret+=u32string({',',' '});
						}else{
							c=1;
						}
						ret+=repr(w);
					}
					ret+=u32string({']'});
					return ret;
				}
				template<typename T>
				u32string repr(set<T> q){
					if (q.size()){
						auto ret=u32string({'{'});
						bool c=0;
						for (auto w:q){
							if (c){
								ret+=u32string({',',' '});
							}else{
								c=1;
							}
							ret+=repr(w);
						}
						ret+=u32string({'}'});
						return ret;
					}else{
						return u32string({'s','e','t','(',')'});
					}
				}
				template<typename T1,typename T2>
				u32string repr(map<T1,T2> q){
					auto ret=u32string({'{'});
					bool c=0;
					for (auto w:q){
						if (c){
							ret+=u32string({',',' '});
						}else{
							c=1;
						}
						ret+=repr(w.first);
						ret+=u32string({':',' '});
						ret+=repr(w.second);
					}
					ret+=u32string({'}'});
					return ret;
				}
			''',
		'python_code':
			r'''
			''',
		'depends':['unicode_convert'],
	},
	'range':{
		'c++_code':
			r'''
				vector<int64_t> range(int64_t q,int64_t w=0xffffffffffffffff,int64_t e=1){
					if (w==0xffffffffffffffff){
						w=q;
						q=0;
					}
					vector<int64_t> res;
					for (;e>0 and q<w or e<0 and q>w;q+=e){
						res.push_back(q);
					}
					return res;
				}
			''',
		'python_code':
			r'''
			''',
		'depends':[],
	},
	'all':{
		'c++_code':
			r'''
			''',
		'python_code':
			r'''
				def all(q):
					for w in q:
						if not w:
							return False
					return True
			''',
		'depends':[],
	},
	'any':{
		'c++_code':
			r'''
			''',
		'python_code':
			r'''
				def any(q):
					for w in q:
						if w:
							return True
					return False
			''',
		'depends':[],
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
			''' if unicode else r'''
				#define to_u8
				#define to_u32
				#define chr
				#define ord
			''',
		'python_code':'',
		'depends':[]
	},
}

var_creation=[]
var_escape=[]
var_global=[]
var_nonlocal=[]

unicode=0

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
				if q.name in 'list set frozenset tuple'.split():
					z,x=q.name,'L_'+'__'.join([pname(w) for w in [q.elt]])+'_J'
				elif q.name in 'dict'.split():
					z,x=q.name,'L_'+'__'.join([pname(w) for w in [q.key,q.value]])+'_J'
				elif q.name=='callable':
					z,x=q.name,'L_'+'__'.join([pname(w) for w in q.args[:-1]])+'_J'
				else:
					z,x=q.name,''
				# z=[(w if w==w.lower() else '_'+w.lower()+'_') if e else (w if w==w.upper() else '_'+w.upper()+'_').lower() for e,w in enumerate(z)]
				return ''.join(z)+('_'+x if x else '')
			if t.name in 'int bool float str list set frozenset tuple dict callable bytes bytearray'.split():
				c='0____0'
				x=pname(t)
			else:
				x=esc(type_convert(t))
			z=esc(q)
			for w in range(z.count('_')+1,2,-1):
				z=z.replace('0'+'_'*w+'0','0'+'_'*(w+3)+'0')
			for w in range(x.count('_')+1,2,-1):
				x=x.replace('0'+'_'*w+'0','0'+'_'*(w+3)+'0')
			if all(['___' not in w[None] for w in var_creation[1:index+1]]):
				v=''.join([w[None]+'_____' for w in var_creation[1:index+1]])
			v=''.join([w[None]+'0_____0' for w in var_creation[1:index+1]])
			if '___' not in z and '___' not in x:
				c=c[1:-1]
			v=z+c+x

		var_creation[index][q]=v
		var_creation[index][(q,t)]=var_creation[index][q]
		if e:
			var_escape[index][q]=var_creation[index][q]
			var_escape[index][(q,t)]=var_creation[index][q]
		return var_creation[index][q]

indent=-1

var_create=''
before_main=''

to_include=set()

def typeof(astobj):
	gen_stack.append(astobj)
	try:
		(dump(astobj,indent=4))
	except:
		error('call cannot process',astobj)
	ret=None
	if 0:
		pass
	elif type(astobj)==UnaryOp:
		if type(astobj.op)==UAdd:
			ret=typeof(astobj.operand)
		elif type(astobj.op)==USub:
			ret=typeof(astobj.operand)
		elif type(astobj.op)==Not:
			ret=typename('bool')
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
		elif typeof(astobj.left).name=='frozenset':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='frozenset':
			ret=typeof(astobj.right)
		elif typeof(astobj.left).name=='dict':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='dict':
			ret=typeof(astobj.right)
		elif typeof(astobj.left).name=='int':
			ret=typeof(astobj.left)
		elif typeof(astobj.right).name=='int':
			ret=typeof(astobj.right)
		ret=typeof(astobj.left)
	elif type(astobj)==BoolOp:
		ret=typename('bool')
	elif type(astobj)==Compare:
		ret=typename('bool')
	elif type(astobj)==IfExp:
		if typeof(astobj.body)!=typeof(astobj.orelse):
			error('different types in',type(astobj).__name__.lower())
		ret=typeof(astobj.body)
	elif type(astobj)==NamedExpr:
		ret=typeof(astobj.value)
	elif type(astobj)==JoinedStr:
		ret=typename('str')
	elif type(astobj)==Constant:
		# if typenameenable:
		ret=typename(type(astobj.value).__name__)
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
		ret=typename('list',elt=t)
	elif type(astobj)==ast.Tuple:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.elts)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.elts[w])!=typeof(astobj.elts[w+1]) for w in range(len(astobj.elts)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.elts[0])
		ret=typename('tuple',elt=t)
	elif type(astobj)==ast.Set:
		if hasattr(astobj,'type'):
			t=astobj.type
		else:
			if len(astobj.elts)==0:
				error('emply',type(astobj).__name__.lower())
			if any([typeof(astobj.elts[w])!=typeof(astobj.elts[w+1]) for w in range(len(astobj.elts)-1)]):
				error('different types in',type(astobj).__name__.lower())
			t=typeof(astobj.elts[0])
		ret=typename('set',elt=t)
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
		ret=typename('dict',key=t[0],value=t[1])
	elif type(astobj)==ListComp:
		ret=typename('list',elt=typeof(astobj.elt))
	elif type(astobj)==GeneratorExp:
		ret=typename('tuple',elt=typeof(astobj.elt))
	elif type(astobj)==SetComp:
		ret=typename('set',elt=typeof(astobj.elt))
	elif type(astobj)==DictComp:
		ret=typename('dict',key=typeof(astobj.key),value=typeof(astobj.value))
	elif type(astobj)==Subscript:
		if type(astobj.slice)==Slice:
			pass
		else:
			if typeof(astobj.value).name=='str':
				ret=typename('str')
			if typeof(astobj.value).name in ['bytes','bytearray']:
				ret=typename('int')
			if typeof(astobj.value).name in ['list','set','frozenset','tuple']:
				ret=typeof(astobj.value).elt
			if typeof(astobj.value).name in ['dict']:
				ret=typeof(astobj.value).value
	elif type(astobj)==Call:
		if type(astobj.func)==Name:
			if astobj.func.id in functions:
				f=functions[astobj.func.id]
				ret=return_type(f.body)
			else:
				r=[w for w in calls if w.args==[typeof(e).name for e in astobj.args] and w.name==astobj.func.id]
				if len(r)==1:
					ret=r[0].returns
				else:
					error('found',len(r),'ways to call',astobj.func.id,'with parameters',*[typeof(w).name for w in astobj.args])
		elif type(astobj.func)==Attribute:
			r=[w for w in attributes if w.args==[typeof(e).name for e in astobj.args] and w.value==typeof(astobj.func.value) and w.attr==astobj.func.attr]
			if len(r)==1:
				ret=r[0].returns
			else:
				error('found',len(r),'ways to call',astobj.func.attr,'from',typeof(astobj.func.value).name,'with parameters',*[typeof(w).name for w in astobj.args])
	if ret==None:
		try:
			dump(astobj)
		except:
			error('cannot find type of',astobj)
		else:
			error('cannot find type of\n'+dump(astobj,indent='\t'))
	gen_stack.pop()
	return ret

def type_convert(q):
	if q==typename('int'):
		return 'int64_t'
	if q==typename('bool'):
		return 'bool'
	if q==typename('float'):
		return 'long double'
	if q==typename('str'):
		return 'u32string'
	if q==typename('bytes'):
		return 'string'
	if q==typename('bytearray'):
		return 'string'
	if q.name=='list':
		return 'vector<'+','.join([type_convert(w) for w in [q.elt]])+'>'
	if q.name=='tuple':
		return 'vector<'+','.join([type_convert(w) for w in [q.elt]])+'>'
	if q.name=='set':
		return 'set<'+','.join([type_convert(w) for w in [q.elt]])+'>'
	if q.name=='frozenset':
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
			ret.append(typename('void'))
		return ret[0]
	else:
		return ret

gen_stack=[]

functions={}

def generate(astobj):
	global unicode
	gen_stack.append(astobj)
	try:
		(dump(astobj,indent=4))
	except:
		error('generate cannot process',astobj)
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
			if (astobj.name,typename('callable',args=[w[2] for w in arglist])) not in var_creation[-1]:
				fn=name(astobj.name,typename('callable',args=[w[2] for w in arglist]),e=1)
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
		if type(astobj.func)==Name:
			if astobj.func.id in functions:
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
			elif astobj.func.id=='exec' and len(astobj.args)==1 and type(astobj.args[0])==Constant and type(astobj.args[0].value)==str:
				ret=astobj.args[0].value
			elif astobj.func.id=='print':
				to_include.add('unicode_convert')
				sep=' '
				end='\n'
				if any([w.arg=='sep' for w in astobj.keywords]) and type([w for w in astobj.keywords if w.arg=='sep'][0].value)==Constant:
					sep=[w for w in astobj.keywords if w.arg=='sep'][0].value.value
				if any([w.arg=='end' for w in astobj.keywords]) and type([w for w in astobj.keywords if w.arg=='end'][0].value)==Constant:
					end=[w for w in astobj.keywords if w.arg=='end'][0].value.value
				ret='cout'+('<<"'+repr(sep)[1:-1]+'"').join(['<<to_u8('+generate(Call(func=Name(id='str',ctx=Load()),args=[w],keywords={}))+')' for w in astobj.args])+'<<"'+repr(end)[1:-1]+'"'
			else:
				args=[generate(w) for w in astobj.args]
				r=[w for w in calls if w.args==[typeof(e).name for e in astobj.args] and w.name==astobj.func.id]
				if len(r)==1:
					for w in r[0].headers:
						to_include.add(w)
					ret=r[0].code(astobj.args)
				else:
					error('found',len(r),'ways to call',astobj.func.id,'with parameters',*[typeof(w).name for w in astobj.args])
		elif type(astobj.func)==Attribute:
			args=[generate(w) for w in astobj.args]
			value=generate(astobj.func.value)
			r=[w for w in attributes if w.args==[typeof(e).name for e in astobj.args] and w.value==typeof(astobj.func.value) and w.attr==astobj.func.attr]
			if len(r)==1:
				for w in r[0].headers:
					to_include.add(w)
				ret=r[0].code(astobj.args)
			else:
					error('found',len(r),'ways to call',astobj.func.attr,'from',typeof(astobj.func.value).name,'with parameters',*[typeof(w).name for w in astobj.args])
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
			if unicode==0 and all([0<ord(w)<256 for w in astobj.value]):
				ret='u32string("'+repr(astobj.value)[1:-1].replace('"','\\"')+'")'
			elif unicode==0:
				ret='u32string({'+','.join([str(w) for w in astobj.value.encode()])+'})'+make_comment(astobj.value)
			else:
				ret='u32string({'+','.join([str(ord(w)) for w in astobj.value])+'})'+make_comment(astobj.value)
		if type(astobj.value)==type(b''):
			if all([0<w<256 for w in astobj.value]):
				ret='string("'+repr(astobj.value)[2:-1].replace('"','\\"')+'")'
			else:
				ret='string({'+','.join([str(w) for w in astobj.value])+'})'+make_comment(astobj.value)
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
			astobj.type=typename('void')
			ret='\t'*indent+'return ;\n'
		else:
			astobj.type=typeof(astobj.value)
			ret='\t'*indent+'return '+generate(astobj.value)+';\n'
	elif type(astobj)==Break:
		ret='\t'*indent+'break;\n'
	elif type(astobj)==Continue:
		ret='\t'*indent+'continue;\n'
	elif type(astobj)==If:
		ret='\t'*indent+'if ('+generate(Call(func=Name(id='bool',ctx=Load()),args=[astobj.test],keywords={}))+'){\n'+\
		''.join([generate(w) for w in astobj.body])+\
		'\t'*indent+'}else{\n'+\
		''.join([generate(w) for w in astobj.orelse])+\
		'\t'*indent+'}'
	elif type(astobj)==While:
		ret='\t'*indent+'while ('+generate(Call(func=Name(id='bool',ctx=Load()),args=[astobj.test],keywords={}))+'){\n'+\
		''.join([generate(w) for w in astobj.body])+\
		'\t'*indent+'}`'
	elif type(astobj)==For:
		r=generate(astobj.iter)
		t=typeof(astobj.iter)
		if type(astobj.target)==Name:
			if t.name in 'list tuple set frozenset'.split():
				name(astobj.target.id,t.elt)
			elif t.name in 'dict'.split():
				name(astobj.target.id,t.key)
			else:
				name(astobj.target.id,t)
		ret='\t'*indent+'for (auto iterator:'+r+'){\n'+\
		'\t'*indent+'\t'+generate(astobj.target)+'='+(type_convert(t)+'({iterator})' if t.name not in 'list tuple set frozenset dict'.split() else 'iterator.first' if t.name=='dict' else 'iterator')+';\n'+\
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
			ret='(!('+generate(Call(func=Name(id='bool',ctx=Load()),args=[astobj.operand],keywords={}))+'))'
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
			ret='('+'||'.join(['('+generate(Call(func=Name(id='bool',ctx=Load()),args=[w],keywords={}))+')' for w in astobj.values])+')'
		if type(astobj.op)==And:
			ret='('+'&&'.join(['('+generate(Call(func=Name(id='bool',ctx=Load()),args=[w],keywords={}))+')' for w in astobj.values])+')'
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
		if type(astobj.slice)==Slice:
			pass
		else:
			value=generate(astobj.value)
			slice=generate(astobj.slice)
			if typeof(astobj.value).name=='str':
				ret='u32string({'+value+'['+slice+']})'
			if typeof(astobj.value).name in ['bytes','bytearray']:
				ret='int64_t(uint64_t(uint8_t('+value+'['+slice+'])))'
			if typeof(astobj.value).name in ['list','set','frozenset','tuple','dict']:
				ret='('+value+'['+slice+'])'
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
	elif type(astobj)==Import:
		for w in astobj.names:
			if w.name=='unicodedata':
				unicode=1
				ret=''
	indent-=1
	gen_stack.pop()
	return ret

text=generate(parse(text))

to_include=list(to_include)
for w in to_include:
	try:
		to_include+=headers()[w]['depends']
	except:
		error('header',w,'not found')
to_include=to_include[::-1]
to_include=reduce(lambda a,s:a+[s] if s not in a else a,to_include,[])
to_include_first=''.join([headers()[w]['c++_code']+'\n' for w in to_include])
# to_include_second=''.join([''.join([generate(w) for w in parse(headers()[w]['python_code']).body])+'\n' for w in to_include])
to_include_second=''

text='''
#include <bits/stdc++.h>
using namespace std;
'''+('#define u32string string\n' if not(unicode) else '')\
+to_include_first+to_include_second+'\n'+var_create+before_main+text

if filename!=None:
	open(filename+'.cpp','w').write(text)
	from subprocess import run
	a=run(['g++','-o',filename+'.exe','-std=c++17','-Wfatal-errors',filename+'.cpp']).returncode
	if a==0:
		a=run([filename+'.exe']).returncode
	exit(a)
else:
	print(text,end='\n' if text[-1:]!='\n' else '')





