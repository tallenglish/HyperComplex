#!/usr/anaconda3/bin/python

from functions import mathdunders, memoize
from classes import Numeric
from numbers import Number

import numpy
import pylab
import itertools
import matplotlib
import graph_tool
import graph_tool.draw
import seaborn
import networkx
import pandas

def cayley_dickson_real_base(base=float):

	if not issubclass(base, Number):

		raise TypeError("The base type must be derived from numbers.Number.")

	@mathdunders(base=base)
	class Real(Numeric, base):

		dimensions = 1

		@staticmethod
		def base():

			return base

		@property
		def real(self):

			return base(self)

		@property
		def imag(self):

			return 0

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

	class HyperComplex(Numeric):

		# Class Data Properties

		dimensions = 2 * parent.dimensions

		@property
		def real(self):

			return self.a.real

		@property
		def imag(self):

			if len(self) == 2:

				return self.b

			return tuple(self.a.imag) + self.b.coefficients()

		# Class Data Functionality

		@staticmethod
		def coerce(other):

			try:

				return HyperComplex(other)

			except TypeError:

				return None

		@staticmethod
		def base():

			return parent.base()

		def indexes(self, index):

			base = self.base()
			result = [base(0)] * self.dimensions
			result[index] = base(1)

			return HyperComplex(*result)

		def values(self, index):

			coefficients = self.coefficients()

			base = self.base()
			result = [base(0)] * self.dimensions
			result[index] = coefficients[index]

			return HyperComplex(*result)

		def named(self, input, **args):

			numeric   = ("numeric"   in args and [args["numeric"]]   or [False])[0]
			identity  = ("identity"  in args and [args["identity"]]  or [False])[0]
			translate = ("translate" in args and [args["translate"]] or [False])[0]
			element   = ("element"   in args and [args["element"]]   or ["e"])[0]
			groups    = ("groups"    in args and [args["groups"]]    or [False])[0]

			translations = list("1ijkmIJKnpqrMPQR")
			base = self.base()

			if hasattr(input, "coefficients"):

				if not input:

					return 0

				coefficients = input.coefficients()
				enum = enumerate(coefficients)

				index, value = next( ( (index, value) for index, value in enum if value))

			elif groups:

				value = (input >= len(self) and [base(-1)] or [base(1)])[0]
				index = (input >= len(self) and [input - len(self)] or [input])[0]

			sign  = ((value < 0) and ["-"] or [""])[0]

			if identity:

				if groups and value < 0:

					index += len(self)

				input = (groups and [F"{index}"] or [F"{sign}{index+1}"])[0]

			elif not numeric:

				value = ((value == base(1) or value == base(-1)) and [""] or [abs(value)])[0]
				input = F"{sign}{value}{element}{index}"

				if translate and self.dimensions <= 16:

					value = ((index == 0 and value == "") and ["1"] or [value])[0]
					input = ((index == 0) and [F"{sign}{value}"] or [F"{sign}{value}{translations[index]}"])[0]

			return input

		def coefficients(self):

			return self.a.coefficients() + self.b.coefficients()

		def zero(self):

			if isinstance(self.a, Number):

				return HyperComplex(0, 0, pair=True)

			else:

				return HyperComplex(self.a.zero(), self.b.zero(), pair=True)

		def __init__(self, *args, pair=False):

			if pair:

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

			self.terms = len(self)

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

		# Class Display Functionality

		def matrix(self, **args):

			string = ("string" in args and [args["string"]] or [False])[0]

			a = list(map(self.indexes, range(self.dimensions)))

			result = [[self.named(i * j, **args) for j in a] for i in a]

			if string:

				result = [list(map(str, row)) for row in result]
				length = max(len(cell) for row in result for cell in row)
				offset = length - max(len(row[0]) for row in result)
				rows = [" ".join(cell.rjust(length) for cell in row)[offset:] for row in result]

				return "\n".join(rows)

			return result

		# Mathematical Type Conversion

		def convert(self, to_type, dimensions=1):

			coefficients = self.coefficients()

			if any(coefficients[dimensions:]):

				raise TypeError(f"Can't convert {self.__class__.__name__}[{self.dimensions}] to {to_type.__name__} when there are non-zero incompatible coefficients.")

			return to_type(*coefficients[:dimensions])

		def __bool__(self):

			return bool(self.a) or bool(self.b)

		def __int__(self):

			return self.convert(int)

		def __float__(self):

			return self.convert(float)

		def __complex__(self):

			return self.convert(complex, 2)

		# Comparison Functionality

		def __eq__(self, other):

			coerced = HyperComplex.coerce(other)

			if coerced is None:

				self = other.__class__.coerce(self)

			else:

				other = coerced

			return self.a == other.a and self.b == other.b

		# Graphical Operations

		def group(self, translate=False):

			def identity():

				sz  = len(self)
				id  = [[(i == j and [1] or [0])[0] for j in range(0, sz)] for i in range(0, sz)]
				id += [[(i == j and [-1] or [0])[0] for j in range(0, sz)] for i in range(0, sz)]

				for i in range(0, sz * 2):

					id[i] = HyperComplex(tuple(id[i]))

				return id

			def edge_matrix(idx):

				ex = numpy.zeros((size, size), dtype=int)

				for k in range(size):

					ex[k][groups[k][idx]] = 1

				return ex

			edge_color_set = [
				(0.89411765336990356, 0.10196078568696976, 0.1098039224743843100, 0.9),
				(0.21602460800432691, 0.49487120380588606, 0.7198769869757634100, 0.9),
				(0.30426760128900115, 0.68329106055054012, 0.2929334996962079700, 0.9),
				(0.60083047361934883, 0.30814303335021526, 0.6316955229815315300, 0.9),
				(1.00000000000000000, 0.50591311045721465, 0.0031372549487095253, 0.9),
				(0.99315647868549117, 0.98700499826786570, 0.1991541745031581200, 0.9),
				(0.65845446095747107, 0.34122261685483596, 0.1707958535236471000, 0.9),
				(0.95850826852461868, 0.50846600392285513, 0.7449288887136122900, 0.9)
			] * 10

			size = len(self) * 2
			groups = numpy.zeros((size, size), dtype=int)
			members = identity()

			for a, b in itertools.product(members, repeat=2):

				x = int(self.named(a, identity=True, groups=True))
				y = int(self.named(b, identity=True, groups=True))
				z = int(self.named(a * b, identity=True, groups=True))

				groups[x, y] = z

			connections = []

			for k in range(1, size):

				connections.append(edge_matrix(k))
				g = networkx.from_numpy_matrix(sum(connections))

				if networkx.is_connected(g):

					break

			g_loop = networkx.from_numpy_matrix(connections[0])
			loops = sorted(list(networkx.connected_components(g_loop)))
			loops = [numpy.roll(x, -k) for k, x in enumerate(loops)]
			square = numpy.array([[-1, -1.0], [-1, 1], [1, 1], [1, -1]]) * (1 / numpy.sqrt(2))
			g = graph_tool.Graph(directed=True)
			g.add_vertex(size)

			pos = g.new_vertex_property("vector<double>")
			label = g.new_vertex_property("string")

			for k, loop in enumerate(loops):

				for idx, r in zip(loop.tolist(), square):

					v = g.vertex(idx)
					name = self.named(idx, groups=True, translate=translate)
					pos[v] = r * (k + 1)
					label[v] = name

			edge_color = g.new_edge_property("vector<double>")

			for k, c in enumerate(connections):

				edges = zip(*numpy.where(c))

				for e1, e2 in edges:

					ex = g.add_edge(e1, e2)
					edge_color[ex] = edge_color_set[k]

			g_args = {
				"edge_color": edge_color,
				"output_size": (int(600),) * 2,
				"vertex_text": label,
				"vertex_font_size": 14,
				"vertex_size": 40,
				"pos": pos,
			}

			graph_tool.draw.graph_draw(g, **g_args)

		def plot(self, diverging=False):

			seaborn.set_style("white")

			size = len(self)
			identity = self.matrix(identity=True)
			figure, axis = pylab.subplots(figsize=(6, 6))
			options = (diverging and [2 * size + 1] or [size])[0]
			palette = seaborn.color_palette("RdBu_r", options)
			rectangle = matplotlib.patches.Rectangle

			for (i, j), z in numpy.ndenumerate(identity):

				location = (j, size - i - 1)
				options = (diverging and [int(z) + size] or [abs(int(z)) - 1])[0]
				color = palette[options]

				R = rectangle(location, 1, 1, snap=False, edgecolor=color, facecolor=color, lw=1, zorder=1)
				axis.add_patch(R)

			axis.get_xaxis().set_ticks([])
			axis.get_yaxis().set_ticks([])

			axis.set_xlim(0, size)
			axis.set_ylim(0, size)

			pylab.tight_layout()
			pylab.show()

		# Mathematical Operations

		def outerproduct(self, other, **args):

			string = ("string" in args and [args["string"]] or [False])[0]

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			other = other.conjugate()

			a = list(map(self.values, range(self.dimensions)))
			b = list(map(other.values, range(other.dimensions)))

			result = [[self.named(i * j, **args) for j in b] for i in a]

			if string:

				result = [list(map(str, row)) for row in result]
				length = max(len(cell) for row in result for cell in row)
				offset = length - max(len(row[0]) for row in result)
				rows = [" ".join(cell.rjust(length) for cell in row)[offset:] for row in result]

				return "\n".join(rows)

			return result

		def innerproduct(self, other):

			return (self.conjugate() * other).real

		def conjugate(self):

			return HyperComplex(self.a.conjugate(), -self.b, pair=True)

		def __neg__(self):

			return HyperComplex(-self.a, -self.b, pair=True)

		def __pos__(self):

			return HyperComplex(+self.a, +self.b, pair=True)

		def __add__(self, other):

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			return HyperComplex(self.a + other.a, self.b + other.b, pair=True)

		def __radd__(self, other):

			return HyperComplex(other) + self

		def __mul__(self, other):

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			a = self.a * other.a - other.b.conjugate() * self.b
			b = other.b * self.a + self.b * other.a.conjugate()

			return HyperComplex(a, b, pair=True)

		def __rmul__(self, other):

			return HyperComplex(other) * self

		def __pow__(self, other):

			if not isinstance(other, int):

				return NotImplemented

			value = HyperComplex(HyperComplex.base()(1))

			if other:

				multiplier = self if other > 0 else self.inverse()

				for _ in range(abs(other)):

					value *= multiplier

			return value

		def __sub__(self, other):

			other = HyperComplex.coerce(other)

			if other is None:

				return NotImplemented

			return HyperComplex(self.a - other.a, self.b - other.b, pair=True)

		def __rsub__(self, other):

			return HyperComplex(other) - self

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

R = Real = cayley_dickson_real_base()
C = Complex = cayley_dickson_construction(R)
H = Quaternion = cayley_dickson_construction(C)
O = Octonion = cayley_dickson_construction(H)
S = Sedenion = cayley_dickson_construction(O)
P = Pathion = cayley_dickson_construction(S)
X = Chingon = cayley_dickson_construction(P)
U = Routon = cayley_dickson_construction(X)
V = Voudon = cayley_dickson_construction(U)