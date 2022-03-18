# (r, g, b, opacity)

def graph_colors(size, id):

	color_set = [
		[240, 240, 240, 1], # White   #808080
		[255, 0, 0, 1],     # Red     #FF0000
		[0, 255, 0, 1],     # Green   #00FF00
		[0, 0, 255, 1],     # Blue    #0000FF
		[235, 235, 235, 1], # Gray    #EBEBEB
		[0, 255, 255, 1],   # Cyan    #00FFFF
		[255, 0, 255, 1],   # Magenta #FF00FF
		[255, 255, 0, 1],   # Yellow  #FFFF00
		[202, 202, 202, 1], # Gray    #CACACA
		[255, 128, 0, 1],   # Orange  #FF8000
		[255, 0, 128, 1],   # Pink    #FF0080
		[128, 255, 0, 1],   # Lime    #80FF00
		[168, 168, 168, 1], # Gray    #A8A8A8
		[0, 255, 128, 1],   # Teal    #FF8000
		[128, 0, 255, 1],   # Purple  #8000FF
		[0, 128, 255, 1],   # Blue    #0080FF
	] * 2

	is_negative = True if id >= size else False

	id -= size if is_negative else 0
	cs = color_set[id]

	for i in range(3):

		cs[i] *= 0.75 / 255 if is_negative else 1 / 255

	return tuple(cs)

# [-Left|+Right, -Top|+Bottom]
# Left/Top     -n, -n
# Left/Bottom  -n, +n
# Right/Bottom +n, +n
# Right/Top    +n, -n

def graph_locations(size, id):

	location_pos_set = [
		[+1, +0], [+0, -1], [+2, +2], [+2, -2], # 1, i, j, k
		[-2, -4], [-4, -2], [-4, +2], [-2, +4], # L, I, J, K
		[-1, -5], [-4, -5], [-5, -4], [-5, -1], # m, p, q, r
		[-5, +1], [-5, +4], [-4, +5], [-1, +5], # M, P, Q, R
		[-4, -7], [-6, -7], [-7, -6], [-7, -4], # n, s, t, u
		[-7, +4], [-7, +6], [-6, +7], [-4, +7], # N, S, T, U
		[-7, +2], [-9, +1], [-9, -1], [-7, -2], # o, v, w, x
		[+2, +7], [+1, +9], [-1, +9], [-2, +7], # O, V, W, X
	]

	location_neg_set = [
		[-1, +0], [+0, +1], [-2, -2], [-2, +2], # 1, i, j, k
		[+2, +4], [+4, +2], [+4, -2], [+2, -4], # L, I, J, K
		[+1, +5], [+4, +5], [+5, +4], [+5, +1], # m, p, q, r
		[+5, -1], [+5, -4], [+4, -5], [+1, -5], # M, P, Q, R
		[+4, +7], [+6, +7], [+7, +6], [+7, +4], # n, s, t, u
		[+7, -4], [+7, -6], [+6, -7], [+4, -7], # N, S, T, U
		[+7, -2], [+9, -1], [+9, +1], [+7, +2], # o, v, w, x
		[-2, -7], [-1, -9], [+1, -9], [+2, -7], # O, V, W, X
	]

	if id >= size:

		id -= size

		return location_neg_set[id]

	return location_pos_set[id]
