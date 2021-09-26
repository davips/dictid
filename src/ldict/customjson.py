#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the ldict project.
#  Please respect the license - more about this in the section (*) below.
#
#  ldict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ldict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ldict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
from json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """
    >>> from ldict.frozenlazydict import FrozenLazyDict
    >>> ldict = FrozenLazyDict
    >>> a = ldict(x=3)
    >>> ldict(d=a, y=5)
    {
        "d": {
            "x": 3
        },
        "y": 5
    }
    >>> from pandas.core.frame import DataFrame, Series
    >>> df = DataFrame([[1,2],[3,4]])
    >>> df
       0  1
    0  1  2
    1  3  4
    >>> b = ldict(d=a, y=5, df=df)
    >>> b
    {
        "d": {
            "x": 3
        },
        "y": 5,
        "df": "[[1 2] [3 4]]"
    }
    >>> from numpy import array
    >>> ldict(b=b, z=9, c=(c:=array([1,2,3])), d=Series(c), dd=array([[1, 2], [3, 4]]))
    """

    def default(self, obj):
        if obj is not None:
            from ldict.frozenlazydict import FrozenLazyDict
            from ldict.lazyval import LazyVal
            if isinstance(obj, FrozenLazyDict):
                return self.data
            if isinstance(obj, LazyVal):
                return str(obj)
            # if isinstance(obj, FunctionType):
            #     return str(obj)
            if not isinstance(obj, (list, set, str, int, float, bytearray, bool)):
                try:
                    from pandas.core.frame import DataFrame, Series
                    if isinstance(obj, (DataFrame, Series)):
                        return truncate("«" + str(obj.to_dict()) + "»")  # «str()» is to avoid nested identation
                    from numpy import ndarray
                    if isinstance(obj, ndarray):
                        return truncate("«" + str(obj).replace("\n", "") + "»")
                except ImportError:
                    print("Pandas or numpy may be missing.")
                return obj.asdict if hasattr(obj, "asdict") else obj.aslist
        return JSONEncoder.default(self, obj)


# class CustomJSONDecoder(JSONDecoder):
#     def __init__(self, *args, **kwargs):
#         JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
#
#     def object_hook(self, obj):
#         if obj is not None:
#             if isinstance(obj, str) and len(obj) == digits:
#                 return
#         return obj

def truncate(txt):
    return txt + "..." if len(txt) == 1000 else txt
