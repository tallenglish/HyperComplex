# Double Underscore Function Definitions

convert_unitary = ["bool", "complex", "float", "format", "hex", "index", "int", "long", "oct", "str", "unicode"]

# Common: bool, float, format, int, long, str, complex (Unitary Operators)
# Python 2: oct, hex (Unitary Operators)
# Python 3: index (Unitary Operators)

compare_unitary = ["eq", "ge", "gt", "le", "lt", "ne"]
compare_binary = ["and", "or", "xor"]
compare_reverse = ["rand", "ror", "rxor"]
compare_inplace = ["iand", "ior", "ixor"]

# "==", ">=", ">", "<=", "<", "!=" (Unitary Operators)
# "and", "&", "or", "|", "xor", "^" (Bianary/Reverse Operators)
# "&=", "|=", "^=" (Inplace Operators)

bitwise_unitary = ["invert"]
bitwise_binary = ["lshift", "rshift"]
bitwise_reverse = ["rlshift", "rrshift"]
bitwise_inplace = ["ilshift", "irshift"]

# "~" (Unitary Operators)
# "<<", ">>" (Bianary/Reverse Operators)
# ">>=", "<<=" (Inplace Operators)

get_unitary = ["get", "getattr", "getitem", "getslice"]
set_unitary = ["set", "setattr", "setitem", "setslice"]
del_unitary = ["del", "delattr", "delitem", "delslice"]
obj_unitary = ["coerce", "dict", "dir", "fspath", "hash", "import", "reduce", "repr", "slots"]
arr_unitary = ["contains", "missing", "nonzero", "len", "sizeof"]

# Python 2: nonzero, getslice, setslice, delslice

# x.y (Attribute)
# x[y] (Item)
# x[start:stop:step] (Slice)
# x.y = 10 (Set)
# print x.y (Get)
# del x.y (Del)

math_unitary = ["abs", "ceil", "floor", "neg", "pos", "round", "trunc"]
math_binary = ["add", "divmod", "floordiv", "mod", "mul", "matmul", "pow", "sub", "truediv"]
math_reverse = ["radd", "rdivmod", "rfloordiv", "rmod", "rmul", "rmatmul", "rpow", "rsub", "rtruediv"]
math_inplace = ["iadd", "ifloordiv", "imod", "imul", "imatmul", "ipow", "isub", "itruediv"]

# + add, - sub, * mul, // floordiv, / div, % mod, ** pow
# += iadd, -= isub, *= imul, //= ifloordiv, /= idiv, %= imod, **= ipow
# abs(x), ceil(x)

convert_all = convert_unitary
compare_all = compare_unitary + compare_binary + compare_reverse + compare_inplace
bitwise_all = bitwise_unitary + bitwise_binary + bitwise_reverse + bitwise_inplace
object_all = get_unitary + set_unitary + del_unitary + obj_unitary + arr_unitary
math_all = math_unitary + math_binary + math_reverse + math_inplace

def dunders(base=None, names=math_all, force=False):

	names = tuple(F"__{name}__" for name in names)

	def decorator(cls):

		nonlocal base

		if base is None:

			base = cls.__bases__[0]

		def add_dunder(name):

			def dunder(self, *kargs, **kwargs):

				result = getattr(base(self), name)(*kargs, **kwargs)

				if result is NotImplemented:

					return NotImplemented

				if type(result) is tuple:

					return tuple(map(cls, result))

				return cls(result)

			return dunder

		for name in names:

			cls_has_dunder = hasattr(cls, name) and getattr(cls, name) is not getattr(base, name)

			if force or not cls_has_dunder:

				setattr(cls, name, add_dunder(name))

		return cls

	return decorator
