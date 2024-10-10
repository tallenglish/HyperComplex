from hypercomplex import Order, Names

import argparse as ap
import definitions as df
import matplotlib.pyplot as plt
import itertools as it
import networkx as nx
import numpy as np
import warnings as wn

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

	def add_node(graph, a, color, label):

		graph.add_node(a, label=label, color=color)

	def add_edge(graph, a, b, color):

		rad_inc = 0.05
		rad_min = 0.05

		if (a, b) in graph.edges:

			rad_max = max(x[2]["radius"] for x in graph.edges(data=True) if sorted(x[:2]) == sorted([a,b]))

		else:

			rad_max = rad_min

		graph.add_edge(a, b, radius=rad_max+rad_inc, color=color)

	wn.filterwarnings("ignore")

	element = option("element", "e", **options)
	indices = option("indices", "1ijkLIJKmpqrMPQRnstuNSTUovwxOVWX", **options)
	fontsize = option("fontsize", 14, **options)
	figsize = option("figsize", 8.0, **options)
	figdpi = option("figdpi", 100.0, **options)
	filename = option("filename", "G{order}.{filetype}", **options)
	filetype = option("filetype", "png", **options)
	showneg = option("negatives", False, **options)
	showpos = option("positives", True, **options)
	showall = option("showall", False, **options)
	layers = option("layers", False, **options)
	order = option("order", None, **options)
	named = option("named", None, **options)
	save = option("save", False, **options)
	show = option("show", True, **options)

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
	figsize = (figsize, figsize)
	connections = []
	layered = []
	indexes = []

	for a, b in it.product(identity(), repeat=2):

		groups[indexer(a), indexer(b)] = indexer(a * b)

	if layers:

		layers = layers.split(",")
		layered = [0] * len(layers)
		showpos = True

		for index in range(0, len(layers)):

			layer = layers[index]
			id = 0

			if layer[:1] == "-" or layer[:1] == "+": # first handle sign

				id += self.dimensions if layer[:1] == "-" else 0
				showneg = True if layer[:1] == "-" else showneg
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
		total = nx.from_numpy_array(sum(connections))
		indexes.append(index)

		if nx.is_connected(total) and not (showall or showpos or showneg):

			break

	# Create Graph

	graph = nx.MultiDiGraph()
	fig, ax = plt.subplots(figsize=figsize, dpi=figdpi)
	pos = df.locationmap(self.order, size)
	fig.set_facecolor("black")
	ax.margins(0.05)
	ax.axis("off")

	# Add Nodes

	for id in range(size):

		label = self.named(1, index=id, asstring=True, **options)
		color = df.color(self.order, id)

		add_node(graph, id, color, label)

	# Add Edges

	for id, connection in enumerate(connections):

		color = df.color(self.order, indexes[id])

		for e1, e2 in zip(*np.where(connection)):

			add_edge(graph, e1, e2, color)

	# Draw Nodes

	for id, data in graph.nodes(data=True):

		nx_node_opts = {
			"nodelist": [id],
			"node_color": data["color"],
			"node_size": 750,
			"node_shape": "o",
			"edgecolors": "darkgray",
			"margins": 0.1
		}

		nx_label_opts = {
			"labels": {id: data["label"]},
			"font_size": fontsize,
			"font_color": "black"
		}

		nx.draw_networkx_nodes(graph, pos, **nx_node_opts)
		nx.draw_networkx_labels(graph, pos, **nx_label_opts)

	# Draw Edges

	for e1, e2, data in graph.edges(data=True):

		nx_edge_opts = {
			"edgelist": [(e1,e2)],
			"edge_color": data["color"],
			"connectionstyle": "arc3, rad = " + str(data["radius"]),
			"arrowstyle": "-|>",
			"arrowsize": 35,
			"arrows": True,
			"width": 1.0
		}

		nx.draw_networkx_edges(graph, pos, **nx_edge_opts)

	plt.tight_layout()

	if save:

		output = ((filename).format(order=self.order, filetype=filetype))

		plt.savefig(output, dpi=figdpi)

	elif show:

		plt.show()

if __name__ == "__main__":

	parser = ap.ArgumentParser()

	parser.add_argument("-o", "--order", type=int, default=2)
	parser.add_argument("-e", "--element", type=str, default="e")
	parser.add_argument("-i", "--indices", type=str, default="1ijkLIJKmpqrMPQRnstuNSTUovwxOVWX")
	parser.add_argument("-f", "--filename", type=str, default="G{order}.{filetype}")
	parser.add_argument("-t", "--filetype", type=str, default="png")
	parser.add_argument("-s", "--figsize", type=float, default=8.0)
	parser.add_argument("-r", "--figdpi", type=float, default=100.0)
	parser.add_argument("-x", "--fontsize", type=int, default=14)
	parser.add_argument("-l", "--layers", type=str)
	parser.add_argument("-n", "--named", type=str)

	parser.add_argument("--translate", action="store_true", default=True)
	parser.add_argument("--negatives", action="store_true", default=False)
	parser.add_argument("--positives", action="store_true", default=True)
	parser.add_argument("--showall", action="store_true", default=False)
	parser.add_argument("--save", action="store_true", default=False)
	parser.add_argument("--show", action="store_true", default=True)

	args, urgs = parser.parse_known_args()

	group(**vars(args))
