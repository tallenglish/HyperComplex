from functools import lru_cache
from dunders import dunders, math_all
from numbers import Number

import numpy as np

class BaseNumber(Number):

	def copy(self):

		return self.__class__(self)

	def inverse(self):

		return self.conjugate() / self.square()

	def square(self):

		return (self.conjugate() * self).real

	def norm(self):

		return np.sqrt(self.square())

	def __abs__(self):

		return self.norm()

	def __len__(self):

		return self.dimensions

	def __getitem__(self, index):

		return self.coefficients()[index]

	def __contains__(self, needle):

		return needle in self.coefficients()

	def __str__(self):

		return format(self)

	def __repr__(self):

		return str(self)

	def __format__(self, spec):

		# spec      ::=  [[fill]align][sign][#][0][width][group][.precision][type]
		# fill      ::=  <any character>
		# align     ::=  "<" | ">" | "=" | "^"
		# sign      ::=  "+" | "-" | " "
		# width     ::=  digit+
		# group     ::=  "_" | ","
		# precision ::=  digit+
		# type      ::=  b | c | d | e | E | f | F | g | G | n | o | s | x | X | %

		# https://docs.python.org/3.9/library/string.html#formatspec

		if not spec:

			spec = "g"

		coefficients = [F"{c:{spec}}" for c in self.coefficients()]

		return "(" + " ".join(coefficients) + ")"

def cayley_dickson_real_base(base=float):

	if not issubclass(base, Number):

		raise TypeError("The base type must be derived from Number.")

	@dunders(base=base, names=math_all, force=False)
	class Real(BaseNumber, base):

		dimensions = 1
		order = 0

		@staticmethod
		def base():

			return base

		@property
		def real(self):

			return base(self)

		@property
		def imag(self):

			return base(0)

		def coefficients(self):

			return (self.real,)

		def conjugate(self):

			return Real(self)

		def __hash__(self):

			return hash(base(self))

	return Real

def cayley_dickson_construction(parent):

	if not hasattr(parent, "coefficients"):

		raise ValueError("The parent type must be Real or HyperComplex. (No coefficients found.)")

	def option(name, default, **options):

		if name in options:

			return options[name]

		return default

	class HyperComplex(BaseNumber):

		# Class Data Properties

		dimensions = parent.dimensions * 2
		order = parent.order + 1

		@property
		def real(self):

			return self.a.real

		@property
		def imag(self):

			if len(self) == 2:

				return self.b

			return tuple(self.a.imag) + self.b.coefficients()

		# HyperComplex Data Manipulation

		@staticmethod
		def coerce(other):

			try:

				return HyperComplex(other)

			except TypeError:

				return None

		@staticmethod
		def base():

			return parent.base()

		# HyperComplex.indexes(index) returns base index for HyperComplex.matric use
		# HyperComplex.values(index)  returns index value for HyperComplex.outerproduct use
		# HyperComplex.named(input)   returns named index (e0, e1) or (1, i), etc

		def indexes(self, index, **args):

			base = self.base()
			result = [base(0)] * self.dimensions
			result[index] = base(1)

			return HyperComplex(*result)

		def values(self, index, **args):

			base = self.base()
			coefficients = self.coefficients()
			result = [base(0)] * self.dimensions
			result[index] = coefficients[index]

			return HyperComplex(*result)

		def named(self, input, **args):

			# Optional Arguments

			element = option("element", "e", **args)
			indices = option("indices", "1ijkLIJKmpqrMPQRnstuNSTUovwxOVWX", **args)
			translate = option("translate", False, **args)
			asindex = option("asindex", False, **args)
			asstring = option("asstring", False, **args)
			astuple = option("astuple", False, **args)
			aslist = option("aslist", False, **args)
			asobject = option("asobject", False, **args)
			showplus = option("showplus", False, **args)
			index = option("index", None, **args)
			value = option("value", input, **args)

			plus = "+" if showplus else ""
			base = self.base()

			if type(indices) != list:

				indices = list(indices)

			# index, value filters

			if hasattr(input, "coefficients"):

				# Added this to fix issue when doing outerproduct and having 0 values anywhere
				# if any value is 0, return 0 immediately so the next() section doesn't throw a
				# type error

				if not input:

					return 0

				coefficients = input.coefficients()
				enum = enumerate(coefficients)

				index, value = next(((index, value) for index, value in enum if value))

			elif type(value) is int and type(index) is int:

				# Used by the group() function to add named elements
				# to the rotation graph

				# group() required 0 index, plot() 1 index starting arrays,
				# group() also shows negativity as > len(self) numbering

				is_negative = index >= len(self)

				if asstring and translate:

					value = base(-1) if is_negative else base(+1)
					index -= len(self) if is_negative else 0

			# text filters

			if asindex:

				# Used bu the HyperComplex.plot() functions to generate
				# the base matricies used to generate the graphs

				input = int(F"-{index+1}") if value < 0 else int(F"{index+1}")

			elif asstring and not (asobject | astuple | aslist):

				# Output Named/String Array, using either e0 + e1 + e2 + e3 format or the
				# letter indices like 1 + i + j + k

				enabled = translate and self.dimensions <= len(indices)
				translated = indices[index] if enabled else F"{element}{index}"

				sign = "-" if value < 0 else plus
				value = "" if abs(value) == base(1) else abs(value)
				translated = "" if translated == "1" and value else translated
				input = F"{sign}{value}{translated}"

			return input

		def coefficients(self):

			return self.a.coefficients() + self.b.coefficients()

		def zero(self):

			if isinstance(self.a, Number):

				return HyperComplex(0, 0)

			else:

				return HyperComplex(self.a.zero(), self.b.zero())

		def __init__(self, *args):

			# Added list/tuple type as allowed arguments
			# Remove need for pair=True

			if len(args) == 2:

				self.a, self.b = map(parent, args)

			else:

				if len(args) == 1:

					if hasattr(args[0], "coefficients"):

						args = args[0].coefficients()

					elif isinstance(args[0], complex):

						args = args[0].real, args[0].imag

					elif type(args[0]) is tuple:

						args = args[0]

					elif type(args[0]) is list:

						args = tuple(args[0])

				if len(args) > len(self):

					raise TypeError(f"Too many args. Got {len(args)} expecting at most {len(self)}.")

				if len(self) != len(args):

					args += (HyperComplex.base()(),) * (len(self) - len(args))

				self.a = parent(*args[:len(self) // 2])
				self.b = parent(*args[len(self) // 2:])

		def __hash__(self):

			return hash(self.coefficients())

		def __iter__(self):

			if isinstance(self.a, Number):

				yield self.a
				yield self.b

				return

			for i in self.a:

				yield i

			for i in self.b:

				yield i

		# HyperComplex Products Display

		# HyperComplex.outerproduct()    returns tensor outer product of AB'
		# HyperCompex.innerproctuct()    returns scalar inner product of A'B
		# HyperCompex.hadamardproctuct() returns vector hadamard product of AB
		# HyperCompex.matrix()           returns multiplication matrix

		def matrixdisplay(self, result, **args):

			asstring = option("asstring", False, **args)
			asobject = option("asobject", False, **args)
			astuple = option("astuple", False, **args)
			aslist = option("aslist", False, **args)

			if asstring and not (asobject | astuple | aslist):

				result = [list(map(str, row)) for row in result]
				length = max(len(cell) for row in result for cell in row)
				offset = length - max(len(row[0]) for row in result)
				rows = [" ".join(cell.rjust(length) for cell in row)[offset:] for row in result]

				return "\n".join(rows)

			return result

		def outerproduct(self, other, **args):

			asobject = option("asobject", False, **args)
			astuple = option("astuple", False, **args)
			aslist = option("aslist", False, **args)

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			other = other.conjugate()

			a = list(map(self.values, range(self.dimensions)))
			b = list(map(other.values, range(other.dimensions)))

			result = [[self.named(i * j, **args) for j in b] for i in a]

			if asobject | astuple | aslist:

				size = len(result)

				for i, j in np.ndindex(size, size):

					temp = result[i][j]
					temp = temp.astuple() if astuple else temp
					temp = temp.asobject() if asobject else temp
					temp = temp.aslist() if aslist else temp

					result[i][j] = temp

			result = self.matrixdisplay(result, **args)

			return result

		def innerproduct(self, other):

			return (self.conjugate() * other).real

		def hadamardproduct(self, other, **args):

			asobject = option("asobject", False, **args)
			astuple = option("astuple", False, **args)
			aslist = option("aslist", False, **args)

			other = HyperComplex.coerce(other)
			base = self.base()

			if other is None:

				return NotImplemented

			a = self.coefficients()
			b = other.coefficients()

			result = [base(0)] * self.dimensions

			for i in range(self.dimensions):

				x = a[i]
				y = b[i]

				result[i] = self.named(base(x * y), index=i, **args)

			if asobject | astuple | aslist:

				result = HyperComplex(result)

				result = result.astuple() if astuple else result
				result = result.asobject() if asobject else result
				result = result.aslist() if aslist else result

			result = self.matrixdisplay(result, **args)

			return result

		def matrix(self, **args):

			asobject = option("asobject", False, **args)
			astuple = option("astuple", False, **args)
			aslist = option("aslist", False, **args)

			a = list(map(self.indexes, range(self.dimensions)))

			result = [[self.named(i * j, **args) for j in a] for i in a]

			if asobject | astuple | aslist:

				size = len(result)

				for i, j in np.ndindex(size, size):

					temp = result[i][j]
					temp = temp.astuple() if astuple else temp
					temp = temp.asobject() if asobject else temp
					temp = temp.aslist() if aslist else temp

					result[i][j] = temp

			result = self.matrixdisplay(result, **args)

			return result

		# Output Types

		def asobject(self):

			return HyperComplex(self)

		def astuple(self):

			return tuple(self.coefficients())

		def aslist(self):

			return list(self.coefficients())

		def asstring(self, **args):

			values = list(map(self.values, range(self.dimensions)))
			values = [self.named(i, asstring=True, **args) for i in values]
			values = [str(row) for row in values]

			result = values.pop(0)

			for value in values:

				result += (value[:1] == "-" and [" - " + value[1:]] or [" + " + value])[0]

			return result

		# HyperComplex Comparison

		def __eq__(self, other):

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			return self.a == other.a and self.b == other.b

		def __ne__(self, other):

			return not self == other

		def __lt__(self, other):

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			return self.square() < other.square()

		def __le__(self, other):

			return self < other or self == other

		def __gt__(self, other):

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			return self.square() > other.square()

		def __ge__(self, other):

			return self > other or self == other

		# Mathematical Conversion

		def convert(self, ctype, dimensions=1):

			coefficients = self.coefficients()

			if any(coefficients[dimensions:]):

				size = self.dimensions
				classname = self.__class__.__name__
				typename = ctype.__name__

				a = F"Error converting {classname}[{size}] to {typename}"
				b = "There are non-zero incompatible coefficients."

				raise TypeError(a + ": " + b)

			return ctype(*coefficients[:dimensions])

		def __bool__(self):

			return bool(self.a) or bool(self.b)

		def __int__(self):

			return self.convert(int, 1)

		def __float__(self):

			return self.convert(float, 1)

		def __complex__(self):

			return self.convert(complex, 2)

		# Mathematical Operations

		def conjugate(self):

			return HyperComplex(self.a.conjugate(), -self.b)

		def __neg__(self):

			return HyperComplex(-self.a, -self.b)

		def __pos__(self):

			return HyperComplex(+self.a, +self.b)

		def __add__(self, other):

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			return HyperComplex(self.a + other.a, self.b + other.b)

		def __radd__(self, other):

			return HyperComplex(other) + self

		def __sub__(self, other):

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			return HyperComplex(self.a - other.a, self.b - other.b)

		def __rsub__(self, other):

			return HyperComplex(other) - self

		@lru_cache(maxsize=128)
		def __pow__(self, power):

			if not isinstance(power, int):

				return NotImplemented

			base = HyperComplex.base()
			value = HyperComplex(base(1))

			if power:

				multiplier = self if power > 0 else self.inverse()

				for _ in range(abs(power)):

					value *= multiplier

			return value

		@lru_cache(maxsize=128)
		def __mul__(self, other):

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			a = self.a * other.a - other.b.conjugate() * self.b
			b = other.b * self.a + self.b * other.a.conjugate()

			return HyperComplex(a, b)

		@lru_cache(maxsize=128)
		def __rmul__(self, other):

			return HyperComplex(other) * self

		@lru_cache(maxsize=128)
		def __truediv__(self, other):

			base = HyperComplex.base()

			if isinstance(other, base):

				other = base(1) / other

			else:

				other = HyperComplex.coerce(other)

				if other is None:

					return NotImplemented

				other = other.inverse()

			return self * other

		@lru_cache(maxsize=128)
		def __rtruediv__(self, other):

			return HyperComplex(other) / self

	return HyperComplex

def cayley_dickson_algebra(level, base=float):

	if not isinstance(level, int) or level < 0:

		raise ValueError("The level must be a positive integer.")

	numbers = cayley_dickson_real_base(base)

	for _ in range(level):

		numbers = cayley_dickson_construction(numbers)

	return numbers

def debug(*values):

	print(*values, sep="\n", end="\n\n")

Real       = R     = cayley_dickson_real_base()
Complex    = C     = cayley_dickson_construction(R)
Quaternion = Q = H = cayley_dickson_construction(C)
Octonion   = O     = cayley_dickson_construction(H)
Sedenion   = S     = cayley_dickson_construction(O)
Pathion    = P     = cayley_dickson_construction(S)
Chingon    = X     = cayley_dickson_construction(P)
Routon     = U     = cayley_dickson_construction(X)
Voudon     = V     = cayley_dickson_construction(U)

Order = {
	0: Real(),
	1: Complex(),
	2: Quaternion(),
	3: Octonion(),
	4: Sedenion(),
	5: Pathion(),
	6: Chingon(),
	7: Routon(),
	8: Voudon()
}

Names = {
	"Real": Real(),
	"Complex": Complex(),
	"Quaternion": Quaternion(),
	"Octonion": Octonion(),
	"Sedenion": Sedenion(),
	"Pathion": Pathion(),
	"Chingon": Chingon(),
	"Routon": Routon(),
	"Voudon": Voudon()
}