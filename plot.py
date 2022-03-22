import argparse
import matplotlib
import seaborn
import pylab
import numpy

# Color Maps: https://matplotlib.org/stable/tutorials/colors/colormaps.html

def plot(self, **options):

	def option(name, default, **options):

		if name in options:

			return options[name]

		return default

	showneg = option("negatives", False, **options)
	poscmap = option("colormap", "RdBu_r", **options)
	negcmap = option("ncolormap", "PiYG_r", **options)
	diverge = option("diverging", False, **options)
	figsize = option("figsize", 6.0, **options)
	figdpis = option("figdpi", 100.0, **options)
	order = option("order", None, **options)

	if self == None:

		from hypercomplex import Order

		self = Order.get(order, None)

	if self == None or (hasattr(self, "order") and self.order > 8):

		raise NotImplementedError

	seaborn.set_style("white")

	size = self.dimensions
	matrix = self.matrix(asindex=True)
	figure, axis = pylab.subplots(figsize=(figsize, figsize), dpi=figdpis)
	numcolors = 2 * size + 1 if diverge else size
	positives = seaborn.color_palette(poscmap, numcolors)
	negatives = seaborn.color_palette(negcmap, numcolors)
	rectangle = matplotlib.patches.Rectangle
	extras = {"snap":False,"lw":1,"zorder":1}

	for (x, y), value in numpy.ndenumerate(matrix):

		location = (y, size - x - 1)
		value = value + size if diverge else abs(value) - 1
		color = negatives[value] if showneg and not diverge and value < 0 else positives[value]
		patch = rectangle(location, 1, 1, edgecolor=color, facecolor=color, **extras)
		axis.add_patch(patch)

	axis.get_xaxis().set_ticks([])
	axis.get_yaxis().set_ticks([])
	axis.set_xlim(0, size)
	axis.set_ylim(0, size)

	pylab.tight_layout()

	if option("save", False, **options):

		filename = option("filename", "P{order}.{filetype}", **options)
		filetype = option("filetype", "png", **options)

		output = ((filename).format(order=self.order, filetype=filetype))

		pylab.savefig(output)

	if option("show", False, **options):

		pylab.show()

if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--order", type=int, default=2)
	parser.add_argument("-f", "--filename", type=str, default="P{order}.{filetype}")
	parser.add_argument("-t", "--filetype", type=str, default="png")
	parser.add_argument("-s", "--figsize", type=float, default=6.0)
	parser.add_argument("-r", "--figdpi", type=int, default=100)
	parser.add_argument("-c", "--colormap", type=str, default="RdBu_r")
	parser.add_argument("-x", "--ncolormap", type=str, default="PiYG_r")

	parser.add_argument("--negatives", action="store_true")
	parser.add_argument("--diverging", action="store_true")
	parser.add_argument("--save", action="store_true")
	parser.add_argument("--show", action="store_true")

	args, urgs = parser.parse_known_args()

	plot(None, **vars(args))
