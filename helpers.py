#!/usr/anaconda3/bin/python

import functools
import argparse

u_fn = "abs ceil floor neg pos round trunc".split()
b_fn = "add divmod floordiv mod mul pow sub truediv".split()
r_fn = [F"r{name}" for name in b_fn]

dunders = tuple(f"__{name}__" for name in u_fn + b_fn + r_fn)

def mathdunders(base=None, dunders=dunders, force=False):

	def decorator(cls):

		nonlocal base

		if base is None:

			base = cls.__bases__[0]

		def add_dunder(name):

			def dunder(self, *args):

				result = getattr(base(self), name)(*args)

				if result is NotImplemented:

					return NotImplemented

				if type(result) is tuple:

					return tuple(map(cls, result))

				return cls(result)

			return dunder

		for name in dunders:

			cls_has_dunder = hasattr(cls, name) and getattr(cls, name) is not getattr(base, name)

			if force or not cls_has_dunder:

				setattr(cls, name, add_dunder(name))

		return cls

	return decorator

memoize_enabled = True

def memoize(self):

	cache = self.cache = {}

	@functools.wraps(self)
	def enabled(*args):

		if args not in cache:

			cache[args] = self(*args)

		return cache[args]

	def disabled(*args):

		return self(*args)

	return enabled if memoize_enabled else disabled

def getargs():

	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--order", type=int, default=2)
	parser.add_argument("-d", "--dir", type=str, default="figures")
	parser.add_argument("-o", "--output", type=str, default="g{order}")
	parser.add_argument("-e", "--extension", choices=["ps", "pdf", "png", "svg"], default="png")
	parser.add_argument("-s", "--figsize", type=float, default=6.0)
	parser.add_argument("-x", "--fontsize", type=float, default=14)
	parser.add_argument("--save-ps", action="store_true")
	parser.add_argument("--save-pdf", action="store_true")
	parser.add_argument("--save-png", action="store_true")
	parser.add_argument("--save-svg", action="store_true")
	parser.add_argument("--save-all", action="store_true")

	args, urgs = parser.parse_known_args()

	return args
