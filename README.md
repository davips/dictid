![test](https://github.com/davips/ldict/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/ldict/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/ldict)
<div style="background-color: rgb(15, 20, 25);">

# ldict
Uniquely identified lazy dict.

[Latest version as a package](https://pypi.org/project/ldict)

[Current code](https://github.com/davips/ldict)

[API documentation](https://davips.github.io/ldict)

## Overview
We consider that every value is generated by a process, starting from `empty`. The process is a sequence of
transformation steps that can be of two types:
value insertion and function application. Value insertion is done using dict-like objects as shown below. The
operator `>>` concatenates the steps chronologically. Each value and each function have unique deterministic
identifiers. Identifiers for future values are predictable through the magic
available [here](https://pypi.org/project/garoupa).
![img.png](https://raw.githubusercontent.com/davips/ldict/main/examples/img.png)

Function application is done in the same way. The parameter names define the input fields, while the keys in the
returned dict define the output fields:
![img_1.png](https://raw.githubusercontent.com/davips/ldict/main/examples/img_1.png)

Similarly, for anonymous functions:
![img_5.png](https://raw.githubusercontent.com/davips/ldict/main/examples/img_5.png)

Finally, the result is only evaluated at request:
![img_6.png](https://raw.githubusercontent.com/davips/ldict/main/examples/img_6.png)
![img_7.png](https://raw.githubusercontent.com/davips/ldict/main/examples/img_7.png)


## Installation
### ...as a standalone lib
```bash
# Set up a virtualenv. 
python3 -m venv venv
source venv/bin/activate

# Install from PyPI...
pip install --upgrade pip
pip install -U ldict

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
    "id": "kr_4aee5c3bcac2c478be9901d57fd1ef8a9d002",
    "ids": "kr_4aee5c3bcac2c478be9901d57fd1ef8a9d002",
    "x": 3
}
"""
```

```python3

b = ldict(y=5)
print(b)
"""
{
    "id": "Uz_0af6d78f77734fad67e6de7cdba3ea368aae4",
    "ids": "Uz_0af6d78f77734fad67e6de7cdba3ea368aae4",
    "y": 5
}
"""
```

```python3

print(a >> b)
"""
{
    "id": "c._2b0434ca422114262680df425b85cac028be6",
    "ids": "kr_4aee5c3bcac2c478be9901d57fd1ef8a9d002 Uz_0af6d78f77734fad67e6de7cdba3ea368aae4",
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
    "id": "kr_4aee5c3bcac2c478be9901d57fd1ef8a9d002",
    "ids": "kr_4aee5c3bcac2c478be9901d57fd1ef8a9d002",
    "x": 3
}
"""
```

```python3

a = a >> ldict(y=5) >> {"z": 7} >> (lambda x, y, z: {"r": x ** y // z})
print(a)
"""
{
    "id": "8jopGVdtSEyCk1NSKcrEF-Lfv8up9MQBdvkLxU2o",
    "ids": "J3tsy4vUXPELySBicaAy-h-UK7Dp9MQBdvkLxU2o... +2 ...Ss_7dff0a161ba7462725cac7dcee71b67669f69",
    "r": "→(x y z)",
    "x": 3,
    "y": 5,
    "z": 7
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
    "id": "8jopGVdtSEyCk1NSKcrEF-Lfv8up9MQBdvkLxU2o",
    "ids": "J3tsy4vUXPELySBicaAy-h-UK7Dp9MQBdvkLxU2o... +2 ...Ss_7dff0a161ba7462725cac7dcee71b67669f69",
    "r": 34,
    "x": 3,
    "y": 5,
    "z": 7
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

from ldict import Ø
from ldict.cfg import cfg


# A function provide input fields and, optionally, parameters.
# For instance:
# 'a' is sampled from an arithmetic progression
# 'b' is sampled from a geometric progression
# Here, the syntax for default parameter values is borrowed with a new meaning.
def fun(x, y, a=[-100, -99, -98, ..., 100], b=[0.0001, 0.001, 0.01, ..., 100000000]):
    return {"z": a * x + b * y}


# Creating an empty ldict. Alternatively: d = ldict().
d = Ø >> {}
d.show(colored=False)
"""
{
    "id": "0000000000000000000000000000000000000000",
    "ids": {}
}
"""
```

```python3

# Putting some values. Alternatively: d = ldict(x=5, y=7).
d["x"] = 5
d["y"] = 7
d.show(colored=False)
"""
{
    "id": "I0_39c94b4dfbc7a8579ca1304eba25917204a5e",
    "ids": {
        "x": "Tz_d158c49297834fad67e6de7cdba3ea368aae4",
        "y": "Rs_92162dea64a7462725cac7dcee71b67669f69"
    },
    "x": 5,
    "y": 7
}
"""
```

```python3

# Parameter values are uniformly sampled.
d1 = d >> fun
d1.show(colored=False)
print(d1.z)
"""
{
    "id": "TwXk--hgpglNTWhyEiUtwH8CMjkiw-qXN50iHMux",
    "ids": {
        "z": "C3c9VYF4V7gvpr1FY7znWGAfy8kiw-qXN50iHMux",
        "x": "Tz_d158c49297834fad67e6de7cdba3ea368aae4",
        "y": "Rs_92162dea64a7462725cac7dcee71b67669f69"
    },
    "z": "→(a b x y)",
    "x": 5,
    "y": 7
}
70000330.0
"""
```

```python3

d2 = d >> fun
d2.show(colored=False)
print(d2.z)
"""
{
    "id": "IM4WSDgRQc6iYuIR-mR74uCOulMN4WbfS8QsAyVi",
    "ids": {
        "z": "w7TZ8-6pQ3ch6YrYicw1ut2sgaMN4WbfS8QsAyVi",
        "x": "Tz_d158c49297834fad67e6de7cdba3ea368aae4",
        "y": "Rs_92162dea64a7462725cac7dcee71b67669f69"
    },
    "z": "→(a b x y)",
    "x": 5,
    "y": 7
}
69999720.0
"""
```

```python3

# Parameter values can also be manually set.
e = d >> cfg(a=5, b=10) >> fun
print(e.z)
"""
95
"""
```

```python3

# Not all parameters need to be set.
e = d >> cfg(a=5) >> fun
print(e.z)
"""
7025.0
"""
```

```python3

# Each run will be a different sample for the missing parameters.
e = e >> cfg(a=5) >> fun
print(e.z)
"""
25.07
"""
```

```python3

# We can define the initial state of the random sampler.
# It will be in effect from its location place onwards in the expression.
e = d >> cfg(a=5) >> Random(0) >> fun
print(e.z)
"""
699999990.0
"""
```

```python3

# All runs will yield the same result,
# if starting from the same random number generator seed.
e = e >> cfg(a=5) >> Random(0) >> fun
print(e.z)
"""
699999990.0
"""
```

```python3

# Reproducible different runs are achievable by using a single random number generator.
rnd = Random(0)
e = d >> cfg(a=5) >> rnd >> fun
print(e.z)
e = d >> cfg(a=5) >> rnd >> fun  # Alternative syntax.
print(e.z)
"""
699999990.0
35.0007
"""
```


</p>
</details>

**Composition of sets of functions**
<details>
<p>

```python3
from random import Random

from ldict import Ø


# A multistep process can be defined without applying its functions


def g(x, y, a=[1, 2, 3, ..., 10], b=[0.00001, 0.0001, 0.001, ..., 100000]):
    return {"z": a * x + b * y}


def h(z, c=[1, 2, 3]):
    return {"z": c * z}


# In the ldict framework 'data is function',
# so the alias ø represents the 'empty data object' and the 'reflexive function' at the same time.
# In other words: 'inserting nothing' has the same effect as 'doing nothing'.
# The operator '*' is an alias for '>>', used just to make the context clearer.
fun = Ø * g * h  # ø enable the cartesian product of the subsequent sets of functions within the expression.
print(fun)
"""
«g × h»
"""
```

```python3

# The difference between 'ø * g * h' and 'ldict(x=3) >> g >> h' is that the functions in the latter are already applied
# (resulting in an ldict object). The former still has its free parameters unsampled,
# and results in an ordered set of composite functions.
# It is a set because the parameter values of the functions are still undefined.
d = {"x": 5, "y": 7} >> fun
print(d)
"""
{
    "id": "onL-iTnl8YQZa2nktD9nrjj.6GeWGCOjgQu3Qk37",
    "ids": "EErwUz.qB6B2qy6rNsQgRiLEUueWGCOjgQu3Qk37... +1 ...Rs_92162dea64a7462725cac7dcee71b67669f69",
    "z": "→(c z→(a b x y))",
    "x": 5,
    "y": 7
}
"""
```

```python3

print(d.z)
"""
70025.0
"""
```

```python3

d = {"x": 5, "y": 7} >> fun
print(d.z)
"""
100.0
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

**Transparent persistence**
<details>
<p>

```python3
import shelve
from collections import namedtuple
from pprint import pprint

from ldict import ldict, Ø
# The cache can be set globally.
# It is as simple as a dict, or any dict-like implementation mapping str to serializable content.
# Implementations can, e.g., store data on disk or in a remote computer.
from ldict.cfg import cfg
from ldict.config import setcache

setcache({})


def fun(x, y):
    print("Calculated!")  # Watch whether the value had to be calculated.
    return {"z": x ** y}


# The operator '^' indicates a relevant point during the process, i.e., a point where data should be stored.
# It is mostly intended to avoid costly recalculations or log results.
# The symbol points upwards, meaning data can momentarily come from or go outside of the process.
# When the same process is repeated, only the first request will trigger calculation.
# Local caching objects (dicts or dict-like database servers) can also be used.
# They should be wrapped by square brackets to avoid ambiguity.
# The list may contain many different caches, e.g.: [RAM, local, remote].
mycache = {}
remote = {}
d = Ø >> {"x": 3, "y": 2} >> fun >> [mycache, remote]
print(d)
print(d.z, d.id)
"""
{
    "id": "dpWeC4tFX.7oD1PMWLoyNAaH6gtNSvzvAw2XMZVi",
    "ids": "GsDJe8CjPiVCEoJEoNzyfKAyyirNSvzvAw2XMZVi... +1 ...yI_a331070d4bcdde465f28ba37ba1310e928122",
    "z": "→(^ x y)",
    "x": 3,
    "y": 2
}
Calculated!
9 dpWeC4tFX.7oD1PMWLoyNAaH6gtNSvzvAw2XMZVi
"""
```

```python3

# The second request just retrieves the cached value.
d = ldict(y=2, x=3) >> fun >> [remote]
print(d.z, d.id)
"""
9 dpWeC4tFX.7oD1PMWLoyNAaH6gtNSvzvAw2XMZVi
"""
```

```python3

# The caching operator can appear in multiple places in the expression, if intermediate values are of interest.
# The ø is used as ldict-inducer when needed.
d = ldict(y=2, x=3) >> fun ^ Ø >> (lambda x: {"x": x ** 2}) >> Ø >> {"w": 5, "k": 5} >> Ø >> [mycache]
print(d.z, d.id)
"""
9 QaRWaaqyTLRqBDzvIff.HdTGQVDeSMDamXXwaYMA
"""
```

```python3

# Persisting to disk is easily done via Python shelve.
P = namedtuple("P", "x y")
a = [3, 2]
b = [1, 4]


def measure_distance(a, b):
    from math import sqrt
    return {"distance": sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)}


with shelve.open("/tmp/my-cache-file.db") as db:
    d = ldict(a=a, b=b) >> measure_distance >> [db]
    pprint(dict(db))  # Cache is initially empty.
    print(d.distance)
    pprint(dict(db))
    #  ...

    # '^' syntax is also possible.
    a = [7, 1]
    b = [4, 3]
    copy = lambda source=None, target=None, **kwargs: {target: kwargs[source]}
    mean = lambda distance, other_distance: {"m": (distance + other_distance) / 2}
    e = (
            ldict(a=a, b=b)
            >> measure_distance
            >> {"other_distance": d.distance}
            >> mean
            ^ Ø
            ^ cfg(source="m", target="m0")
            >> copy
            >> (lambda m: {"m": m ** 2})
    )
    print(e.m0, e.m)

"""
{'3Q_85403c3464883af128dc24eef54294173d8ef': [1, 4],
 'E0_45bf7de0dcdfc012da8a0f556492e8880b09d': [3, 2],
 'KBQMiN2gHLwCewlu6HC67I1R2-m8hIbZ8IXI2c0c': 2.8284271247461903,
 'uSytg7O3BaGIggOzqYSBO3ees4KQw0Bf1SouJQht': 2.8284271247461903}
2.8284271247461903
{'3Q_85403c3464883af128dc24eef54294173d8ef': [1, 4],
 'E0_45bf7de0dcdfc012da8a0f556492e8880b09d': [3, 2],
 'KBQMiN2gHLwCewlu6HC67I1R2-m8hIbZ8IXI2c0c': 2.8284271247461903,
 'uSytg7O3BaGIggOzqYSBO3ees4KQw0Bf1SouJQht': 2.8284271247461903}
3.2169892001050897 10.349019513592784
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
A ldict is like a common Python dict, with extra functionality and lazy.
It is a mapping between string keys, called fields, and any serializable object.
The ldict `id` (identifier) and the field `ids` are also part of the mapping.  

The user can provide a unique identifier ([hosh](https://pypi.org/project/garoupa))
for each function or value object.
Otherwise, they will be calculated through blake3 hashing of the content of data or bytecode of function.
For this reason, such functions should be simple, i.e.,
with minimal external dependencies, to avoid the unfortunate situation where two
functions with identical local code actually perform different calculations through
calls to external code that implement different algorithms with the same name.
<!--- Alternatively, a Hosh object can be passed inside the dict that is returned by the function, under the key "_id". --->

## Grants
This work was partially supported by Fapesp under supervision of
Prof. André C. P. L. F. de Carvalho at CEPID-CeMEAI (Grants 2013/07375-0 – 2019/01735-0).

</div>
