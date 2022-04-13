from hypercomplex import Order, Names

import argparse as ap
import definitions as df
import graph_tool as gt
import graph_tool.draw as gtd
import itertools as it
import networkx as nx
import numpy as np

def group(**options):

	def option(name, default, **options):

		if name in options:

			return options[name]

		return default

	def identity():

		rg  = range(0, self.dimensions)
		id  = [[+1 if i == j else 0 for j in rg] for i in rg]
		id += [[-1 if i == j else 0 for j in rg] for i in rg]

		for i in range(0, self.dimensions * 2):

			id[i] = self.__class__(tuple(id[i]))

		return id

	def edges(index):

		found = np.zeros(groups.shape, dtype=int)

		for id in range(size):

			found[id, groups[id, index]] = 1

		return found

	def indexer(input):

		if not input:

			return 0

		coefficients = input.coefficients()
		id, val = next(((id, val) for id, val in enumerate(coefficients) if val))
		id += input.dimensions if val < 0 else 0

		return id

	element = option("element", "e", **options)
	indices = option("indices", "1ijkLIJKmpqrMPQRnstuNSTUovwxOVWX", **options)
	fontsize = option("fontsize", 14, **options)
	figsize = option("figsize", 6.0, **options)
	figdpi = option("figdpi", 100.0, **options)
	filename = option("filename", "G{order}.{filetype}", **options)
	filetype = option("filetype", "png", **options)
	directed = option("directed", False, **options)
	showneg = option("negatives", False, **options)
	showpos = option("positives", False, **options)
	showall = option("showall", False, **options)
	layers = option("layers", False, **options)
	order = option("order", None, **options)
	named = option("named", None, **options)
	save = option("save", False, **options)
	show = option("show", False, **options)

	if named != None:

		self = Names.get(named, None)

	elif order != None:

		self = Order.get(order, None)

	else:

		self = None

	if self == None or (hasattr(self, "order") and self.order > 5):

		raise NotImplementedError

	size = self.dimensions * 2
	groups = np.zeros((size, size), dtype=int)
	indices = list(indices)
	connections = []
	layered = []
	indexes = []

	for a, b in it.product(identity(), repeat=2):

		groups[indexer(a), indexer(b)] = indexer(a * b)

	if layers:

		layers = layers.split(",")
		layered = [0] * len(layers)
		showall = True

		for index in range(0, len(layers)):

			layer = layers[index]
			id = 0

			if layer[:1] == "-" or layer[:1] == "+": # first handle sign

				id += self.dimensions if layer[:1] == "-" else 0
				layer = layer[1:]

			if element in layer: # handle e0,e12,e4, etc.

				x = layer.index(element)
				id += int(layer[x+1:])

			elif layer.isdigit(): # handle numbers

				id += int(layer)

			elif layer.isalpha() and layer in indices: # handle i,j,k, etc

				id += indices.index(layer)

			layered[index] = id

	elif showneg and not showpos and not showall:

		layered = range(self.dimensions, size)

	elif showpos and not showneg and not showall:

		layered = range(0, self.dimensions)

	else:

		if showneg and showpos:

			showall = True

		layered = range(0, size)

	for index in layered:

		if index == 0 or index == self.dimensions: # inore the +1, -1 layers

			continue

		connections.append(edges(index))
		total = nx.from_numpy_matrix(sum(connections))
		indexes.append(index)

		if nx.is_connected(total) and not (showall or showpos or showneg):

			break

	first = nx.from_numpy_matrix(connections[0])
	loops = nx.connected_components(first)
	loops = [np.roll(x, -k) for k, x in enumerate(loops)]
	graph = gt.Graph(directed=directed)
	text = graph.new_vertex_property("string")
	pos = graph.new_vertex_property("vector<double>")
	fill = graph.new_vertex_property("vector<double>")
	color = graph.new_edge_property("vector<double>")

	graph.add_vertex(size)

	# Position Indices Consistantly

	for id in range(size):

		vertex = graph.vertex(id)

		text[vertex] = self.named(1, index=id, asstring=True, **options)
		fill[vertex] = df.color(self.order, id)
		pos[vertex] = df.location(self.order, id)

	# Add Rotations

	for id, connection in enumerate(connections):

		for e1, e2 in zip(*np.where(connection)):

			edge = graph.add_edge(e1, e2)

			color[edge] = df.color(self.order, indexes[id])

	opts = {
		"edge_color": color,
		"edge_pen_width": 2,
		"edge_marker_size": 20,
		"edge_start_marker": "none",
			# “none”, “arrow”, “circle”, “square”, “diamond”, “bar”
		"edge_end_marker": "arrow",
			# “none”, “arrow”, “circle”, “square”, “diamond”, “bar”
		"output_size": (int(figsize * figdpi), int(figsize * figdpi)),
		"vertex_font_size": fontsize,
		"vertex_fill_color": fill,
		"vertex_text": text,
		"vertex_shape": "circle",
			# “circle”, “triangle”, “square”, “pentagon”, “hexagon”,
			# “heptagon”, “octagon” “double_circle”, “double_triangle”, “double_square”,
			# “double_pentagon”, “double_hexagon”, “double_heptagon”, “double_octagon”,
			# “pie”, “none”
		"vertex_pen_width": 1,
		"vertex_size": 30,
		"pos": pos,
	}

	if save:

		output = ((filename).format(order=self.order, filetype=filetype))

		gtd.graph_draw(graph, output=output, fmt=filetype, **opts)

	if show:

		gtd.graph_draw(graph, **opts)

if __name__ == "__main__":

	parser = ap.ArgumentParser()

	parser.add_argument("-o", "--order", type=int, default=2)
	parser.add_argument("-e", "--element", type=str, default="e")
	parser.add_argument("-i", "--indices", type=str, default="1ijkLIJKmpqrMPQRnstuNSTUovwxOVWX")
	parser.add_argument("-f", "--filename", type=str, default="G{order}.{filetype}")
	parser.add_argument("-t", "--filetype", type=str, default="png")
	parser.add_argument("-s", "--figsize", type=float, default=6.0)
	parser.add_argument("-r", "--figdpi", type=float, default=100.0)
	parser.add_argument("-x", "--fontsize", type=int, default=14)
	parser.add_argument("-l", "--layers", type=str)
	parser.add_argument("-n", "--named", type=str)

	parser.add_argument("--directed", action="store_true")
	parser.add_argument("--translate", action="store_true")
	parser.add_argument("--negatives", action="store_true")
	parser.add_argument("--positives", action="store_true")
	parser.add_argument("--showall", action="store_true")
	parser.add_argument("--save", action="store_true")
	parser.add_argument("--show", action="store_true")

	args, urgs = parser.parse_known_args()

	group(**vars(args))
