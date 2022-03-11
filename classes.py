#!/usr/anaconda3/bin/python

from numbers import Number
from math import *

class Numeric(Number):

	def copy(self):

		return self.__class__(self)

	def inverse(self):

		return self.conjugate() / self.square()

	def square(self):

		return (self.conjugate() * self).real

	def norm(self):

		return sqrt(self.square())

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

		if not spec:

			spec = "g"

		coefficients = [f"{c:{spec}}" for c in self.coefficients()]

		return "(" + " ".join(coefficients) + ")"
