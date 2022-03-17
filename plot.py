import argparse
import hypercomplex
import matplotlib
import seaborn
import pylab
import numpy

def plot(self, **args):

	if self.order > 8 | self.dimensions > 256:

		raise NotImplementedError

	HyperComplex = self.__class__
	dimensions = self.dimensions
	order = self.order

	figsize = args["figsize"] if "figsize" in args else 6.0
	negatives = args["negatives"] if "negatives" in args else False
	diverging = args["diverging"] if "diverging" in args else False
	filename = args["filename"] if "filename" in args else "images/K{order}.{extension}"
	extension = args["extension"] if "extension" in args else "png"
	save = args["save"] if "save" in args else False
	show = args["show"] if "show" in args else False

	seaborn.set_style("white")

	size = len(self)
	identity = self.matrix(asindex=True)
	figure, axis = pylab.subplots(figsize=(figsize, figsize), dpi=100.0)
	options = 2 * size + 1 if diverging else size
	palette = seaborn.color_palette("RdBu_r", options)
	rectangle = matplotlib.patches.Rectangle

	for (i, j), z in numpy.ndenumerate(identity):

		location = (j, size - i - 1)
		options = int(z) + size if diverging else abs(int(z)) - 1
		color = palette[options]
		black = (0.0, 0.0, 0.0)

		if negatives and z < 0:

			R = rectangle(location, 1, 1, snap=False, edgecolor=black, facecolor=black, lw=1, zorder=2)

		else:

			R = rectangle(location, 1, 1, snap=False, edgecolor=color, facecolor=color, lw=1, zorder=1)

		axis.add_patch(R)

	axis.get_xaxis().set_ticks([])
	axis.get_yaxis().set_ticks([])

	axis.set_xlim(0, size)
	axis.set_ylim(0, size)

	pylab.tight_layout()

	if save:

		output = ((filename).format(order=order, extension=extension))

		pylab.savefig(output)

	if show:

		pylab.show()

if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--order", type=int, default=2)
	parser.add_argument("-f", "--filename", type=str, default="images/K{order}.{extension}")
	parser.add_argument("-e", "--extension", type=str, default="png")
	parser.add_argument("-s", "--figsize", type=float, default=6)
	parser.add_argument("-r", "--dpi", type=float, default=100)
	parser.add_argument("--negatives", action="store_true")
	parser.add_argument("--diverging", action="store_true")
	parser.add_argument("--dont-save", action="store_true")
	parser.add_argument("--dont-show", action="store_true")

	args, urgs = parser.parse_known_args()

	self = hypercomplex.R() if args.order == 0 else None
	self = hypercomplex.C() if args.order == 1 else self
	self = hypercomplex.Q() if args.order == 2 else self
	self = hypercomplex.O() if args.order == 3 else self
	self = hypercomplex.S() if args.order == 4 else self
	self = hypercomplex.P() if args.order == 5 else self
	self = hypercomplex.X() if args.order == 6 else self
	self = hypercomplex.U() if args.order == 7 else self
	self = hypercomplex.V() if args.order == 8 else self

	if self == None:

		raise NotImplementedError

	options = {
		"dpi": args.dpi,
		"figsize": args.figsize,
		"filename": args.filename,
		"negatives": args.negatives,
		"diverging": args.diverging,
		"save": not args.dont_save,
		"show": not args.dont_show
	}

	plot(self, **options)
