import argparse
import hypercomplex
import graph_tool.draw
import graph_tool
import itertools
import networkx
import numpy

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

# [-Left|+Right, -Top|+Bottom]
# Left/Top     -n, -n
# Left/Bottom  -n, +n
# Right/Bottom +n, +n
# Right/Top    +n, -n

edge_vertex_locations = [
	[[+1.00, +0.00], [+0.00, -1.00], [-1.00, +0.00], [+0.00, +1.00]],  # +1, +i, -1, -i Complex
	[[-1.50, -1.50], [-1.50, +1.50], [+1.50, +1.50], [+1.50, -1.50]],  # +j, +k, -j, -k Quaternion
	[[-2.00, -3.00], [-3.00, -2.00], [+2.00, +3.00], [+3.00, +2.00]],  # +m, +I, -m, -I Octonion
	[[-3.00, +2.00], [-2.00, +3.00], [+3.00, -2.00], [+2.00, -3.00]],  # +J, +K, -J, -K Octonion
	[[-2.00, -4.00], [-2.50, -3.50], [+2.00, +4.00], [+2.50, +3.50]],  # +n, +p, -m, -p Sedenion
	[[-3.50, -2.50], [-4.00, -2.00], [+3.50, +2.50], [+4.00, +2.00]],  # +q, +r, -q, -r Sedenion
	[[-4.00, +2.00], [-3.50, +2.50], [+4.00, -2.00], [+3.50, -2.50]],  # +M, +P, -M, -P Sedenion
	[[-2.50, +3.50], [-2.00, +4.00], [+2.50, -3.50], [+2.00, -4.00]],  # +Q, +R, -Q, -R Sedenion
]

def group(self, **args):

	if self.order > 4 | self.dimensions > 16:

		raise NotImplementedError

	HyperComplex = self.__class__
	dimensions = self.dimensions
	order = self.order

	save = args["save"] if "save" in args else False
	show = args["show"] if "show" in args else False
	showall = args["showall"] if "showall" in args else False
	translate = args["translate"] if "translate" in args else False
	negatives = args["negatives"] if "negatives" in args else False
	positives = args["positives"] if "positives" in args else False
	directed = args["directed"] if "directed" in args else True
	filename = args["filename"] if "filename" in args else "K{order}"
	extension = args["extension"] if "extension" in args else "png"
	fontsize = args["fontsize"] if "fontsize" in args else 18
	layers = args["layers"] if "layers" in args else ""
	indices = args["indices"] if "indices" in args else "1ijkmIJKnpqrMPQR"
	element = args["element"] if "element" in args else "e"
	figsize = args["figsize"] if "figsize" in args else 6.0
	dpi = args["dpi"] if "dpi" in args else 100

	HyperComplex = self.__class__

	def KD_identity():

		sz  = len(self)
		rg  = range(0, sz)
		id  = [[+1 if i == j else 0 for j in rg] for i in rg]
		id += [[-1 if i == j else 0 for j in rg] for i in rg]

		for i in range(0, sz * 2):

			id[i] = HyperComplex(tuple(id[i]))

		return id

	def KD_edges(index):

		edges = numpy.zeros(groups.shape, dtype=int)

		for id in range(size):

			edges[id, groups[id, index]] = 1

		return edges

	def KD_groups(input):

		if not input:

			return 0

		coefficients = input.coefficients()
		enum = enumerate(coefficients)

		index, value = next(((index, value) for index, value in enum if value))

		if value < 0:

			index += len(input)

		return index

	def KD_sorter(input):

		test = input.tolist()
		test = sorted(test)
		work = [int(0)] * len(test)

		for i in range(len(test)):

			work[i] = test[i]

		return sorted(work)

	size = dimensions * 2
	groups = numpy.zeros((size, size), dtype=int)
	members = KD_identity()
	layers = layers.split(",")
	indices = list(indices)
	connections = []

	for a, b in itertools.product(members, repeat=2):

		x = KD_groups(a)
		y = KD_groups(b)
		z = KD_groups(a * b)

		groups[x, y] = z

	for index in range(0, len(layers)):

		temp = layers[index]

		if temp.isdigit() and int(temp) <= len(indices):

			layers[index] = int(temp)

		elif temp.isalpha() and translate and temp in indices:

			layers[index] = indices.index(temp)

		elif temp.isalpha() and temp[:1] == element:

			layers[index] = int(temp[1:])

		else:

			del layers[index]

	if negatives and not positives:

		ranged = range(1 + dimensions, size)

	elif positives and not negatives:

		ranged = range(1, dimensions)

	else:

		ranged = range(1, size)

	layered = layers if len(layers) > 0 and layers[0] != "0" else ranged
	showall = True if len(layers) > 0 and layers[0] != "0" else showall

	for index in layered:

		if index == 0 or index == dimensions:

			continue

		connections.append(KD_edges(index))
		g = networkx.from_numpy_matrix(sum(connections))

		if networkx.is_connected(g) and not showall:

			break

	g_loop = networkx.from_numpy_matrix(connections[0])

	loops = networkx.connected_components(g_loop)
	loops = [numpy.roll(x, -k) for k, x in enumerate(loops)]

	g = graph_tool.Graph(directed=directed)
	g.add_vertex(size)

	position = g.new_vertex_property("vector<double>")
	label = g.new_vertex_property("string")

	for id, loop in enumerate(loops):

		loop = KD_sorter(loop)

		for index, location in zip(loop, edge_vertex_locations[id]):

			v = g.vertex(index)

			label[v] = self.named(1, index=index, asstring=True, **args)
			position[v] = location

	edge_color = g.new_edge_property("vector<double>")

	for id, connection in enumerate(connections):

		edges = zip(*numpy.where(connection))

		for e1, e2 in edges:

			edge = g.add_edge(e1, e2)
			edge_color[edge] = edge_color_set[id]

	options = {
		"edge_color": edge_color,
		"output_size": (figsize * dpi, figsize * dpi),
		"vertex_font_size": fontsize,
		"vertex_text": label,
		"vertex_size": 30,
		"pos": position,
	}

	if save:

		output = ((filename).format(order=order) + "." + extension)

		graph_tool.draw.graph_draw(g, output=output, fmt=extension, **options)

	if show:

		graph_tool.draw.graph_draw(g, **options)

if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--order", type=int, default=2)
	parser.add_argument("-f", "--filename", type=str, default="G{order}")
	parser.add_argument("-e", "--extension", type=str, default="png")
	parser.add_argument("-x", "--fontsize", type=int, default=18)
	parser.add_argument("-s", "--figsize", type=float, default=6)
	parser.add_argument("-l", "--layers", type=str)
	parser.add_argument("-r", "--dpi", type=float, default=100)
	parser.add_argument("--indices", type=str, default="1ijkmIJKnpqrMPQR")
	parser.add_argument("--element", type=str, default="e")
	parser.add_argument("--directed", action="store_true")
	parser.add_argument("--translate", action="store_true")
	parser.add_argument("--negatives", action="store_true")
	parser.add_argument("--positives", action="store_true")
	parser.add_argument("--save", action="store_true")
	parser.add_argument("--show", action="store_true")

	args, urgs = parser.parse_known_args()

	self = hypercomplex.R() if args.order == 0 else None
	self = hypercomplex.C() if args.order == 1 else self
	self = hypercomplex.Q() if args.order == 2 else self
	self = hypercomplex.O() if args.order == 3 else self
	self = hypercomplex.S() if args.order == 4 else self

	if self == None:

		raise NotImplementedError

	options = {
		"dpi": args.dpi,
		"layers": args.layers,
		"figsize": args.figsize,
		"fontsize": args.fontsize,
		"filename": args.filename,
		"directed": args.directed,
		"translate": args.translate,
		"negatives": args.negatives,
		"positives": args.positives,
		"element": args.element,
		"indices": args.indices,
		"save": args.save,
		"show": args.show,
	}

	group(self, **options)
