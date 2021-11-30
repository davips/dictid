![test](https://github.com/davips/ldict/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/ldict/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/ldict)
<a href="https://pypi.org/project/ldict">
<img src="https://img.shields.io/pypi/v/ldict.svg?label=release&color=blue&style=flat-square" alt="pypi">
</a>
![Python version](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue.svg)
[![license: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

<!--- [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5501845.svg)](https://doi.org/10.5281/zenodo.5501845) --->
[![arXiv](https://img.shields.io/badge/arXiv-2109.06028-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2109.06028)
[![API documentation](https://img.shields.io/badge/doc-API%20%28auto%29-a0a0a0.svg)](https://davips.github.io/ldict)

# ldict

A lazy `dict`.

[Latest release](https://pypi.org/project/ldict) |
[Current code](https://github.com/davips/ldict) |
[API documentation](https://davips.github.io/ldict)

## See also

* laziness+identity+persistence ([idict](https://pypi.org/project/idict))

## Overview

A `ldict` is a `dict` with `str` keys.

**Simple usage example**
<details>
<p>

```python3
from ldict import ldict

a = ldict(x=3)
print(a)
"""
{
    "x": 3
}
"""
```

```python3

b = ldict(y=5)
print(b)
"""
{
    "y": 5
}
"""
```

```python3

print(a >> b)
"""
{
    "x": 3,
    "y": 5
}
"""
```


</p>
</details>

We consider that every value is generated by a process, starting from an `empty` ldict. The process is a sequence of
transformation steps done through the operator `>>`, which symbolizes a data flow. There are two types of steps:

* **value insertion** - represented by dict-like objects
* **function application** - represented by ordinary python functions

A `ldict` is completely defined by its key-value pairs so that
it can be converted from/to a built-in dict.

Creating a ldict is not different from creating an ordinary dict. Optionally it can be created through the `>>` operator
used after `empty`:
![img.png](https://raw.githubusercontent.com/davips/ldict/main/examples/img.png)

Function application is done in the same way. The parameter names define the input fields, while the keys in the
returned dict define the output fields:
![img_1.png](https://raw.githubusercontent.com/davips/ldict/main/examples/img_1.png)

Similarly, for anonymous functions:
![img_5.png](https://raw.githubusercontent.com/davips/ldict/main/examples/img_5.png)

Finally, the result is only evaluated at request:
![img_6.png](https://raw.githubusercontent.com/davips/ldict/main/examples/img_6.png)


## Installation
### ...as a standalone lib
```bash
# Set up a virtualenv. 
python3 -m venv venv
source venv/bin/activate

# Install from PyPI...
pip install --upgrade pip
pip install -U ldict
pip install -U ldict[full]  # use this for extra functionality (recommended)

# ...or, install from updated source code.
pip install git+https://github.com/davips/ldict
```

### ...from source
```bash
git clone https://github.com/davips/ldict
cd ldict
poetry install
```

## Examples
**Merging two ldicts**
<details>
<p>

```python3
from ldict import ldict

a = ldict(x=3)
print(a)
"""
{
    "x": 3
}
"""
```

```python3

b = ldict(y=5)
print(b)
"""
{
    "y": 5
}
"""
```

```python3

print(a >> b)
"""
{
    "x": 3,
    "y": 5
}
"""
```


</p>
</details>

**Lazily applying functions to ldict**
<details>
<p>

```python3
from ldict import ldict

a = ldict(x=3)
print(a)
"""
{
    "x": 3
}
"""
```

```python3

a = a >> ldict(y=5) >> {"z": 7} >> (lambda x, y, z: {"r": x ** y // z})
print(a)
"""
{
    "x": 3,
    "y": 5,
    "z": 7,
    "r": "→(x y z)"
}
"""
```

```python3

print(a.r)
"""
34
"""
```

```python3

print(a)
"""
{
    "x": 3,
    "y": 5,
    "z": 7,
    "r": 34
}
"""
```


</p>
</details>

**Parameterized functions and sampling**
<details>
<p>

```python3
from random import Random

from ldict import empty, let


# A function provide input fields and, optionally, parameters.
# For instance:
# 'a' is sampled from an arithmetic progression
# 'b' is sampled from a geometric progression
# Here, the syntax for default parameter values is borrowed with a new meaning.
def fun(x, y, a=[-100, -99, -98, ..., 100], b=[0.0001, 0.001, 0.01, ..., 100000000]):
    return {"z": a * x + b * y}


def simplefun(x, y):
    return {"z": x * y}


# Creating an empty ldict. Alternatively: d = ldict().
d = empty >> {}
print(d)
"""
{}
"""
```

```python3

# Putting some values. Alternatively: d = ldict(x=5, y=7).
d["x"] = 5
d["y"] = 7
print(d)
"""
{
    "x": 5,
    "y": 7
}
"""
```

```python3

# Parameter values are uniformly sampled.
d1 = d >> simplefun
print(d1)
print(d1.z)
"""
{
    "x": 5,
    "y": 7,
    "z": "→(x y)"
}
35
"""
```

```python3

d2 = d >> simplefun
print(d2)
print(d2.z)
"""
{
    "x": 5,
    "y": 7,
    "z": "→(x y)"
}
35
"""
```

```python3

# Parameter values can also be manually set.
e = d >> let(fun, a=5, b=10)
print(e.z)
"""
95
"""
```

```python3

# Not all parameters need to be set.
e = d >> Random() >> let(fun, a=5)
print("e =", e.z)
"""
e = 700025.0
"""
```

```python3

# Each run will be a different sample for the missing parameters.
e = e >> Random() >> let(fun, a=5)
print("e =", e.z)
"""
e = 70000025.0
"""
```

```python3

# We can define the initial state of the random sampler.
# It will be in effect from its location place onwards in the expression.
e = d >> Random(0) >> let(fun, a=5)
print(e.z)
"""
725.0
"""
```

```python3

# All runs will yield the same result,
# if starting from the same random number generator seed.
e = e >> Random(0) >> let(fun, a=[555, 777])
print("Let 'a' be a list:", e.z)
"""
Let 'a' be a list: 700003885.0
"""
```

```python3

# Reproducible different runs are achievable by using a single random number generator.
e = e >> Random(0) >> let(fun, a=[5, 25, 125, ..., 10000])
print("Let 'a' be a geometric progression:", e.z)
"""
Let 'a' be a geometric progression: 700003125.0
"""
```

```python3
rnd = Random(0)
e = d >> rnd >> let(fun, a=5)
print(e.z)
e = d >> rnd >> let(fun, a=5)  # Alternative syntax.
print(e.z)
"""
725.0
700000025.0
"""
```

```python3

# Output fields can be defined dynamically through parameter values.
# Input fields can be defined dynamically through kwargs.
copy = lambda source=None, target=None, **kwargs: {target: kwargs[source]}
d = empty >> {"x": 5}
d >>= let(copy, source="x", target="y")
print(d)
d.evaluate()
print(d)

"""
{
    "x": 5,
    "y": "→(source target x)"
}
{
    "x": 5,
    "y": 5
}
"""
```


</p>
</details>

**Composition of sets of functions**
<details>
<p>

```python3
from random import Random

from ldict import empty


# A multistep process can be defined without applying its functions


def g(x, y, a=[1, 2, 3, ..., 10], b=[0.00001, 0.0001, 0.001, ..., 100000]):
    return {"z": a * x + b * y}


def h(z, c=[1, 2, 3]):
    return {"z": c * z}


# In the ldict framework 'data is function',
# so the alias ø represents the 'empty data object' and the 'reflexive function' at the same time.
# In other words: 'inserting nothing' has the same effect as 'doing nothing'.
fun = empty >> g >> h  # empty enable the cartesian product of the subsequent sets of functions within the expression.
print(fun)
"""
«λ{} × λ»
"""
```

```python3

# An unnapplied function has its free parameters unsampled.
# A compostition of functions results in an ordered set (Cartesian product of sets).
# It is a set because the parameter values of the functions are still undefined.
d = {"x": 5, "y": 7} >> (Random(0) >> fun)
print(d)
"""
{
    "x": 5,
    "y": 7,
    "z": "→(c z→(a b x y))"
}
"""
```

```python3

print(d.z)
"""
105.0
"""
```

```python3

d = {"x": 5, "y": 7} >> (Random(0) >> fun)
print(d.z)
"""
105.0
"""
```

```python3

# Reproducible different runs by passing a stateful random number generator.
rnd = Random(0)
e = d >> rnd >> fun
print(e.z)
"""
105.0
"""
```

```python3

e = d >> rnd >> fun
print(e.z)
"""
14050.0
"""
```

```python3

# Repeating the same results.
rnd = Random(0)
e = d >> rnd >> fun
print(e.z)
"""
105.0
"""
```

```python3

e = d >> rnd >> fun
print(e.z)
"""
14050.0
"""
```


</p>
</details>

<!--- ## Persistence
Extra dependencies can be installed to support saving data to disk or to a server in the network. 

**[still an ongoing work...]**

`poetry install -E full`
--->

## Concept

A ldict is like a common Python dict, with extra functionality and lazy. It is a mapping between string keys, called
fields, and any serializable (pickable protocol=5) object.

## Grants
This work was partially supported by Fapesp under supervision of
Prof. André C. P. L. F. de Carvalho at CEPID-CeMEAI (Grants 2013/07375-0 – 2019/01735-0).
