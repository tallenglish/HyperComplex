## **`HyperComplex Python Library`**

A Python library for working with quaternions, octonions, sedenions, and beyond following the Cayley-Dickson construction of hypercomplex numbers.

The [complex numbers](https://en.wikipedia.org/wiki/Complex_number) may be viewed as an extension of the everyday [real numbers](https://en.wikipedia.org/wiki/Real_number). A complex number has two real-number coefficients, one multiplied by 1, the other multiplied by [i](https://en.wikipedia.org/wiki/Imaginary_unit).

In a similar way, a [quaternion](https://en.wikipedia.org/wiki/Quaternion), which has 4 components, can be constructed by combining two complex numbers. Likewise, two quaternions can construct an [octonion](https://en.wikipedia.org/wiki/Octonion) (8 components), and two octonions can construct a [sedenion](https://en.wikipedia.org/wiki/Sedenion) (16 components).

The method for this construction is known as the [Cayley-Dickson construction](https://en.wikipedia.org/wiki/Cayley%E2%80%93Dickson_construction) and the resulting classes of numbers are types of [hypercomplex numbers](https://en.wikipedia.org/wiki/Hypercomplex_number). There is no limit to the number of times you can repeat the Cayley-Dickson construction to create new types of hypercomplex numbers, doubling the number of components each time.

This Python 3 package allows the creation of number classes at any repetition level of Cayley-Dickson constructions, and has built-ins for the lower, named levels such as quaternion, octonion, and sedenion.

![Diagram](images/diagram.png "Diagram")

### **`Special Thanks`**

This package is a combination of the work done by [discretegames](https://github.com/discretegames) providing the [mathdunders](https://github.com/discretegames/mathdunders) and most of the [hypercomplex](https://github.com/discretegames/hypercomplex) base functionality, but also [thoppe](https://github.com/thoppe) for providing the base graphical plot functionality from [cayley-dickson](https://github.com/thoppe/Cayley-Dickson).

### **`Additions To Above Libraries`**

This library has been taylored to use ***`Jupiter / Visual Studio Code Notebooks`*** as well as work with command line for the graphical portions.  I have also added to these base packages, functionality for `inner, outer and hadamard products` as well as extending the graphical capabilities of the Cayley-Dickson graphs to include layers, so as to improve readability when graphing high order complex numbers, sucj as Octonions or Sedenions.  This allows the user to visualise each individual rotation group easilly if so wished, or limit the graph to a specific number of layers, and specific direction of rotation as clockwise `-` and anti-clockwise `+` rotations are handled as seperate layers.

### **`Coming Soon`**

One major issue with the `group()` method is its reliance on graph-tool, while a very good tool
for network graphs, it is only availible on Linux or OSX. I will be updating this to
use plotly instead, so it is also compatabile with Windows.

### **`Requirements`**

The following packages are required, mostly for the graphical functionality, if you remove the group() and plot() methods, you no longer need these requirements and the package can work standalone:

- functools (HyperComplex)
- numbers (HyperComplex)
- numpy (HyperComplex, Group, Plot)
- argparse (Group, Plot)
- itertools (Group)
- graph_tool (Group)
- networkx (Group)
- matplotlib (Plot)
- seaborn (Plot)
- pylab (Plot)

### **`Import Librarys`**

```python
from hypercomplex import *
from group import *
from plot import *
```

### **`Basic Usage`**

You can any of the following:

- `R`, `Real` for real numbers (1 bit)
- `C`, `Complex` for complex numbers (2 bit)
- `H`, `Q`, `Quaternion` for quaternion numbers (4 bit)
- `O`, `Octonion` for octonion numbers (8 bit)
- `S`, `Sedenion` for sedenion numbers (16 bit)
- `P`, `Pathion` for pathion numbers (32 bit)
- `X`, `Chingon` for chingon numbers (64 bit)
- `U`, `Routon` for routon numbers (128 bit)
- `V`, `Voudon` for voudon numbers (256 bit)

Higher order numbers can be created using the function `cayley_dickson_construction(N)` where N is the previous basis of the one you are trying to create.

```python
AA = H(1,2,3,4)
AB = H(Complex(1,2),C(3,4))
AC = H((1,2),(3,4))
AD = H((1,2,3,4))
AE = H([1,-2,-3,-4])
AF = O()
AG = cayley_dickson_construction(V)()

debug("Addition:", AF + AA, AF + O(0, AA))
debug("Multiplication:", 2 * AA)
debug("Comparison:", AA == (1,2,3,4))
debug("Lengths:", len(AA), len(AG))
debug("Square:", AA.square())
debug("Norm:", AA.norm())
debug("Inverse:", AA.inverse(), 1 / AA)
debug("Cacheing:", H.__mul__.cache_info())
```

```
Addition:
 (1 2 3 4 0 0 0 0)
 (0 0 0 0 1 2 3 4)

Multiplication:
 (2 4 6 8)

Comparison:
 True

Lengths:
 4
 512

Square:
 30.0

Norm:
 5.477225575051661

Inverse:
 (0.0333333 -0.0666667 -0.1 -0.133333)
 (0.0333333 -0.0666667 -0.1 -0.133333)

Cacheing:
 CacheInfo(hits=103435, misses=100, maxsize=128, currsize=100)
```

### **`HyperComplex Methods`**

```python
debug("Real Part:", AA.real)
debug("Imaginary Part:", AA.imag)
debug("Coefficients:", AA.coefficients())
debug("Conjugate:", AA.conjugate())
```

```
Real Part:
 1.0

Imaginary Part:
 (2.0, 3.0, 4.0)

Coefficients:
 (1.0, 2.0, 3.0, 4.0)

Conjugate:
 (1 -2 -3 -4)
```

```python
debug("String Format:", AA.asstring(translate=True))
debug("String Format:", AE.asstring(translate=True))
debug("Tuple Format:", AA.astuple())
debug("List Format:", AA.aslist())
debug("Object Format:", AA.asobject())
```

```
String Format:
 1 + 2.0i + 3.0j + 4.0k

String Format:
 1 - 2.0i - 3.0j - 4.0k

Tuple Format:
 (1.0, 2.0, 3.0, 4.0)

List Format:
 [1.0, 2.0, 3.0, 4.0]

Object Format:
 (1 2 3 4)
```

### **`HyperComplex Products`**

#### **`Inner, Dot, Scalar Product`**

Geometrically, it is the product of the Euclidean magnitudes of the two vectors and the cosine of the angle between them. In the case of vector spaces, the dot product is used for defining lengths (the length of a vector is the square root of the dot product of the vector by itself) and angles (the cosine of the angle of two vectors is the quotient of their dot product by the product of their lengths).

The dot and inner product are commutative:

&#10092; A &vert; B &#10093; = A &middot; B = A<sub>&mu;</sub> B<sup>&nu;</sup>

#### **`Outer, Kroneecker, Tensor Product`**

The outer product of two coordinate vectors is a matrix. If the two vectors have dimensions n and m, then their outer product is an n × m matrix. More generally, given two tensors (multidimensional arrays of numbers), their outer product is a tensor. The outer product of tensors is also referred to as their tensor product and can be used to define the tensor algebra.

Like the cross product, the outer product is anti-commutative.

&vert; A &#10093; &#10092; B &vert; = A &otimes; B = A<sup>&mu;</sup> B<sub>&nu;</sub>

#### **`Hadamard, Entrywise, Schur Product`**

The Hadamard product (also known as the element-wise, entrywise or Schur product) is a binary operation that takes two matrices of the same dimensions and produces another matrix of the same dimension as the operands where each element i, j is the product of elements i, j of the original two matrices. It should not be confused with the more common matrix product.

The Hadamard product is associative and distributive. Unlike the matrix product, it is also commutative.

&#10092; A &vert; &#10092; B &vert; = A &middot; B = A<sub>&mu;</sub> B<sub>&nu;</sub>

&vert; A &#10093; &vert; B &#10093; = A &middot; B = A<sub>&mu;</sub> B<sub>&nu;</sub>

```python
debug("Inner Product:", AA.innerproduct(AB))
debug("Outer Product:", AA.outerproduct(AB, asstring=True, translate=True))
debug("Hadamard Product:", AA.hadamardproduct(AB, asobject=True))
```

```
Inner Product:
 30.0

Outer Product:
    1  -2.0i  -3.0j  -4.0k
 2.0i    4.0  -6.0k   8.0j
 3.0j   6.0k    9.0 -12.0i
 4.0k  -8.0j  12.0i   16.0

Hadamard Product:
 (1 4 9 16)
 ```

### **`HyperComplex Multiplication Matricies`**

These can have various options to alter how the data is handed back, `asstring=True` will output the array as a string, adding by default `e0, e1, ...` as the index names, however you can add `translate=True` to change them to `1 + i + j + k, ...` format.  You can also use custom indexes by either changing the `element=e` option or `indices=1ijkmIJKnpqrMPQR` option.

If you select `asobject=True (default)` then the function will output list of HyperComplex objects, `astuple=True` and `aslist=True` will return a tuple or list array accordingly.  There is also `asindex=True`, which returns the sign and index id for each cell.

```python
debug("String Matrix:", AF.matrix(asstring=True, translate=True))
debug("Index Matrix:", AF.matrix(asindex=True, asstring=True))
```

```
String Matrix:
 1  i  j  k  L  I  J  K
 i -1  k -j  I -L -K  J
 j -k -1  i  J  K -L -I
 k  j -i -1  K -J  I -L
 L -I -J -K -1  i  j  k
 I  L -K  J -i -1 -k  j
 J  K  L -I -j  k -1 -i
 K -J  I  L -k -j  i -1

Index Matrix:
 1  2  3  4  5  6  7  8
 2 -1  4 -3  6 -5 -8  7
 3 -4 -1  2  7  8 -5 -6
 4  3 -2 -1  8 -7  6 -5
 5 -6 -7 -8 -1  2  3  4
 6  5 -8  7 -2 -1 -4  3
 7  8  5 -6 -3  4 -1 -2
 8 -7  6  5 -4 -3  2 -1
```

```python
debug("String Matrix:", AF.matrix(asstring=True, translate=True, indices="1abcdefgh"))
debug("Object Matrix:", AF.matrix(asobject=True))
```

```
String Matrix:
 1  a  b  c  d  e  f  g
 a -1  c -b  e -d -g  f
 b -c -1  a  f  g -d -e
 c  b -a -1  g -f  e -d
 d -e -f -g -1  a  b  c
 e  d -g  f -a -1 -c  b
 f  g  d -e -b  c -1 -a
 g -f  e  d -c -b  a -1

Object Matrix:
[[(1 0 0 0), ( 0 1 0 0), (0 0 1 0), (0 0 0 1)],
 [(0 1 0 0), (-1 0 0 0), (0 0 0 1), (0 0 -1 0)],
 [(0 0 1 0), ( 0 0 0 -1), (-1 0 0 0), (0 1 0 0)],
 [(0 0 0 1), ( 0 0 1 0), (0 -1 0 0), (-1 0 0 0)]]
```

### **`HyperComplex Plots`**

The `plot()` method, which produces images so we can visualize the multiplication tables with either one or two colormaps.  Using the default options and diverging colurmap, `red` displays positive values, `blue` negative values. For example, with the complex numbers 1 => least red, i => most red, -1 => least blue, -i => most blue.

For a full list of supported colormaps supported by , please visit [Matplotlib Colormaps](https://matplotlib.org/stable/tutorials/colors/colormaps.html)

Options:

- `named=None` : name of the hyper complex object to use.
- `order=None` : order of the hyper complex object to use.
- `filename="P{order}.{filetype}"` : images filename E.g. P3.png
- `filetype="png"` : the file extension used above.
- `figsize=6.0` : figure size in inches.
- `figdpi=100.0` : figure dpi (pixels per inch).
- `colormap="RdBu_r"` : default matplotlib colormap to use.
- `ncolormap="PiYG_r"` : matplotlib colormap to use for negatives.
- `diverging=False` : use diverging colormap.
- `negatives=False` : show negative values using ncolormap above (ignored if diverging used).
- `show=False` : show figure to screen.
- `save=False` : save figure to disk.

### **`HyperComplex Cayley Graphs`**

For the smaller algebras (up to Pathion), we can construct the [Cayley Graph](http://en.wikipedia.org/wiki/Cayley_graph) using `group()` to display the various rotations of various imaginary indices as shown below for quaternions.

When displaying edges, the color of the edge will be the same as the vertex points they relate to, E.g. `i` will always be `red`, `j` will be `green` and so on.  Negative rotations will be displayed in a darker variant of the color to stand out.

Options:

- `named=None` : name of the hyper complex object to use.
- `order=None` : order of the hyper complex object to use.
- `filename="G{order}.{filetype}"` : images filename E.g. G3.png.
- `filetype="png"` : the file extension used above.
- `figsize=6.0` : figure size in inches.
- `figdpi=100.0` : figure dpi (pixels per inch).
- `fontsize=14` : font size used for labels.
- `element="e"` : used when displaying as string, but not translating to index.
- `indices="1ijkLIJKmpqrMPQRnstuNSTUovwxOVWX"` : used to translate indicies.
- `layers="..."` : select which rotations to display, can be positive or negative.
- `translate=False` : tranlates the indicies for easy reading.
- `positives=False` : show all positive translations.
- `negatives=False` : show all negative rotations.
- `directed=True` : show arrows indicating direction of rotation.
- `translate=False` : tranlates the indicies for easy reading.
- `showall=False` : show all rotations.
- `show=False` : show figure to screen.
- `save=False` : save figure to disk.

### **`Complex Numbers`**

A [complex number](http://en.wikipedia.org/wiki/Complex_number) is a number that can be expressed in the form `a + bi`, where `a` and `b` are real numbers and `i` is the imaginary unit, imaginary being the root of a negative square number `i = sqrt(-1)`. They are a normed division algebra over the real numbers. There is no natural linear ordering (commutativity) on the set of complex numbers.

The significance of the imaginary unit:

- i² = -1

```python
# NOTE: Takes less than 2s

group(order=1, translate=True, show=True, showall=True)
group(order=1, translate=True, show=True, positives=True)
group(order=1, translate=True, show=True, negatives=True)

plot(order=1, diverging=False, show=True)
plot(order=1, diverging=True, show=True)
```

![Complex](images/complex_g_all.png "Complex")
![Complex](images/complex_g_pos.png "Complex")
![Complex](images/complex_g_neg.png "Complex")
![Complex](images/complex.png "Complex")
![Complex](images/complex_d.png "Complex")

### **`Quaternion Numbers`**

[Quaternions](http://en.wikipedia.org/wiki/Quaternion) are a normed division algebra over the real numbers that can be expressed in the form `a + bi + cj + dk`, where `a`, `b`, `c` and `d` are real numbers and `i`, `j`, `k` are the imaginary units.  They are noncommutative. The unit quaternions can be thought of as a choice of a group structure on the 3-sphere S3 that gives the group Spin(3), which is isomorphic to SU(2) and also to the universal cover of SO(3).

The significance of the higher order imaginary units:

- i = jk
- j = ki
- k = ij
- i² = j² = k² = -1
- ijk = -1

```python
# NOTE: Takes less than 2s

group(order=2, translate=True, show=True, showall=True)
group(order=2, translate=True, show=True, positives=True)
group(order=2, translate=True, show=True, negatives=True)

plot(order=2, diverging=False, show=True)
plot(order=2, diverging=True, show=True)
```

![Quaternions](images/quaternion_g_all.png "Quaternions")
![Quaternions](images/quaternion_g_pos.png "Quaternions")
![Quaternions](images/quaternion_g_neg.png "Quaternions")
![Quaternions](images/quaternion.png "Quaternions")
![Quaternions](images/quaternion_d.png "Quaternions")

### **`Octonion Numbers`**

[Octonions](http://en.wikipedia.org/wiki/Octonion) are a normed division algebra over the real numbers. They are noncommutative and nonassociative, but satisfy a weaker form of associativity, namely they are alternative. The Cayley graph is hard project into two-dimensions, there overlapping edges along the diagonals. That can be expressed in the form `a + bi + cj + dk + eL + fI + gJ + hK`, where `a .. h` are real numbers and `i, j, k, L, I, J, K` are the imaginary units.

The significance of the higher order imaginary units:

- [L, I, J, K] = [1, i, j, k] * L
- L² = I² = J² = K² = -1
- IJK = L

```python
# NOTE: Takes about 3s

group(order=3, translate=True, show=True, layers="L,i,j,k")
group(order=3, translate=True, show=True, layers="-L,-i,-j,-k")
group(order=3, translate=True, show=True, layers="L,I,J,K")
group(order=3, translate=True, show=True, layers="-L,-I,-J,-K")

plot(order=3, diverging=False, show=True)
plot(order=3, diverging=True, show=True)
```

![Octonion](images/octonion_g_Lijk_pos.png "Octonion")
![Octonion](images/octonion_g_Lijk_neg.png "Octonion")
![Octonion](images/octonion_g_LIJK_pos.png "Octonion")
![Octonion](images/octonion_g_LIJK_neg.png "Octonion")
![Octonion](images/octonion.png "Octonion")
![Octonion](images/octonion_d.png "Octonion")

### **`Sedenion Numbers`**

[Sedenion](http://en.wikipedia.org/wiki/Sedenion) orm a 16-dimensional noncommutative and nonassociative algebra over the reals obtained by applying the Cayley–Dickson construction to the octonions. That can be expressed in the form `a + i + j + k + L + I + J + K...`, where `a...` are real numbers and `i, j, k, L, I, J, K, m, p, q, r, M, P, Q, R` are the imaginary units.

The significance of the higher order imaginary units:

- [m, p, q, r] = [1, i, j, k] * m
- [M, P, Q, R] = [L, I, J, K] * m
- m² = p² = q² = r² = -1
- M² = P² = Q² = R² = -1
- pqr = m
- PQR = M

Now things are getting very complicated (pun intended), we will only show the positive layers, for each of the four main rotational groups, `L,i,j,k`, `L,I,J,K` as for Octonions and their duals `m,p,q,r` and `M,P,Q,R`.  Even as they are, it is still hard to visualise, but displaying fewer layers per image will rectify that, you need to display a minimum of one layer - so you could just display singular rotational groups for maximum readability.

```python
# NOTE: Takes less than 8s

group(order=4, translate=True, show=True, layers="L,i,j,k")
group(order=4, translate=True, show=True, layers="L,I,J,K")
group(order=4, translate=True, show=True, layers="m,p,q,r")
group(order=4, translate=True, show=True, layers="M,P,Q,R")

plot(order=4, diverging=False, show=True)
plot(order=4, diverging=True, show=True)
```

![Sedenion](images/sedenion_g_Lijk_pos.png "Sedenion")
![Sedenion](images/sedenion_g_LIJK_pos.png "Sedenion")
![Sedenion](images/sedenion_g_mpqr_pos.png "Sedenion")
![Sedenion](images/sedenion_g_MPQR_pos.png "Sedenion")
![Sedenion](images/sedenion.png "Sedenion")
![Sedenion](images/sedenion_d.png "Sedenion")

### **`Pathion Numbers`**

Pathions form a 32-dimensional algebra over the reals obtained by applying the Cayley–Dickson construction to the sedenions.

The significance of the higher order imaginary units:

- [n, s, t, u] = [1, i, j, k] * n
- [N, S, T, U] = [L, I, J, K] * n
- [o, v, w, x] = [m, p, q, r] * n
- [O, V, W, X] = [M, P, Q, R] * n
- n² = s² = t² = u² = o² = v² = w² = x² = -1
- N² = S² = T² = U² = O² = V² = W² = X² = -1
- stu = n
- STU = N
- vwx = o
- VWX = O

As before we will only show the positive layers, for each of the four main rotational groups, `1,i,j,k`, `L,I,J,K`, `m,p,q,r` and `M,P,Q,R` for Sedenions we have their duals `n,s,t,u`, `N,S,T,U`, `o,v,w,x`, and `O,V,W,X`.  Even as they are, it is still hard to visualise, but displaying a single layers per image will give maximum readability.

```python
# NOTE: Takes about 42s

group(order=5, translate=True, show=True, layers="L")
group(order=5, translate=True, show=True, layers="m")
group(order=5, translate=True, show=True, layers="n")
group(order=5, translate=True, show=True, layers="o")

plot(order=5, diverging=False, show=True)
plot(order=5, diverging=True, show=True)
```

![Pathion](images/pathion_g_L_pos.png "Pathion")
![Pathion](images/pathion_g_m_pos.png "Pathion")
![Pathion](images/pathion_g_n_pos.png "Pathion")
![Pathion](images/pathion_g_o_pos.png "Pathion")
![Pathion](images/pathion.png "Pathion")
![Pathion](images/pathion_d.png "Pathion")

### **`Chingon Numbers`**

Chingons form a 64-dimensional algebra over the reals obtained by applying the Cayley–Dickson construction to the pathion.

group() is disabled, as it is far too busy/messy.

```python
# NOTE: Takes about 1m

plot(order=6, diverging=False, show=True)
plot(order=6, diverging=True, show=True)
```

![Chingon](images/chingon.png "Chingon")
![Chingon](images/chingon_d.png "Chingon")

### **`Routon Numbers`**

Routons form a 128-dimensional algebra over the reals obtained by applying the Cayley–Dickson construction to the chingons.

group() is disabled, as it is far too busy/messy.

```python
# NOTE: Takes about 10m40s

plot(order=7, diverging=False, show=True)
plot(order=7, diverging=True, show=True)
```

![Routon](images/routon.png "Routon")
![Routon](images/routon_d.png "Routon")

### **`Voudon Numbers`**

Voudons form a 256-dimensional algebra over the reals obtained by applying the Cayley–Dickson construction to the routons.

group() is disabled, as it is far too busy/messy.

```python
# NOTE: Takes very long time

plot(order=8, diverging=False, show=True)
plot(order=8, diverging=True, show=True)
```

![Voudon](images/voudon_d.png "Voudon")
