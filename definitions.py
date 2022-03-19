# Colors (Fixed Color Graph Indices)
# Returns (red, green, blue, opacity)

colors = [
	"EEEEEE", # White   (1, n)
	"FF0000", # Red     (i, s)
	"00FF00", # Green   (j, t)
	"0000FF", # Blue    (k, u)
	"DDDDDD", # Gray    (L, N)
	"00FFFF", # Cyan    (I, S)
	"FF00FF", # Magenta (J, T)
	"FFFF00", # Yellow  (K, U)
	"CCCCCC", # Gray    (m, o)
	"FF8000", # Orange  (p, v)
	"FF0080", # Pink    (q, w)
	"80FF00", # Lime    (r, x)
	"BBBBBB", # Gray    (M, O)
	"FF8000", # Teal    (P, V)
	"8000FF", # Purple  (Q, W)
	"0080FF", # Blue    (R, X)
] * 2

def color(order, id):

	negative = True if id >= 2**order else False
	id -= 2**order if negative else 0
	color = colors[id]
	out = [0, 0, 0, 1]

	for i in range(3):

		hex = color[i * 2 : i * 2 + 2]
		out[i] = int(hex, 16) / 0xFF

		if negative:

			out[i] *= 0.50 # Color 50% Darker If Negative

	return tuple(out)

# Location (Fixed Location Graph Indices)
# Returns [Horizontal, Vertical]

# Left / Top     := [-, -]
# Left / Bottom  := [-, +]
# Right / Bottom := [+, +]
# Right / Top    := [+, -]
# Center         := [0, 0]

locations = [
	[1, 0], [0, -1],								# 1, i, Complex
	[2, 2], [2, -2],								# j, k, Quaternion
	[-1.5, -4], [-4, -1.5], [-4, 1.5], [-1.5, 4],	# L, I, J, K Octonion
	[-2, -6], [-5, -6], [-6, -5], [-6, -2],			# m, p, q, r Sedenion
	[-6, 2], [-6, 5], [-5, 6], [-2, 6],				# M, P, Q, R Sedenion
	[-6, -9], [-8, -9], [-9, -8], [-9, -6],			# n, s, t, u Pathion
	[-9, 6], [-9, 8], [-8, 9], [-6, +9],			# N, S, T, U Pathion
	[-9, 4], [-11, 3], [-11, -3], [-9, -4],			# o, v, w, x Pathion
	[4, 9], [3, 11], [-3, 11], [-4, 9],				# O, V, W, X Pathion
]

def location(order, id):

	negative = True if id >= 2**order else False
	id -= 2**order if negative else 0
	location = locations[id]

	for i in range(2):

		if negative:

			location[i] *= -1 # Reversed Location If Negative

	return location
