#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the garoupa project.
#  Please respect the license - more about this in the section (*) below.
#
#  garoupa is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  garoupa is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with garoupa.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
#
#  garoupa is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  garoupa is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with garoupa.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.


def extend_history(d, hosh):
    """
    >>> from ldict import ldict
    >>> d = ldict()
    >>> d.history
    {}
    >>> d["x"] = 5
    >>> d.history == {"g8_70f95e0d9b4e6e2647d114311069bdf618013": None}
    True
    >>> d["y"] = 7
    >>> d.history == {"r._102b763df082a8b575dc93e0748ce5f4cd2c4": {"bT_b0708720655fbf8f2efa3f9f5423380ea52b1", "g8_70f95e0d9b4e6e2647d114311069bdf618013"}}
    True

    Parameters
    ----------
    d
    hosh

    Returns
    -------

    """
    if not d.history or hosh.etype == "ordered" or "_" not in d.last[:3]:
        d.last = hosh.id
        d.history[d.last] = None
    else:
        many = d.history.pop(d.last)
        previous_last = d.last
        d.last = (d.last * hosh).id
        if many is None:
            d.history[d.last] = {previous_last, hosh.id}
        else:
            many.add(hosh.id)
            d.history[d.last] = many


def rewrite_history(d, hosh):
    """
    >>> from ldict import ldict
    >>> d = ldict()
    >>> d["x"] = 5
    >>> d["y"] = 7
    >>> del d["x"]
    >>> d.history == {'bT_b0708720655fbf8f2efa3f9f5423380ea52b1': None}
    True

    Parameters
    ----------
    d
    key

    Returns
    -------

    """
    lastitem = d.last and d.history[d.last]
    if d.last == hosh.id:
        del d.history[d.last]
        d.last = list(d.history.keys())[-1]
    elif isinstance(lastitem, set) and d.last in lastitem:  #TODO: check inside list?
        many = lastitem.pop(hosh.id)
        del d.history[d.last]
        d.last = (d.last / hosh).id
        d.history[d.last] = many
    else:
        d.history = {}
        hosh = d.identity.h
        many = set()
        for k, v in d.hoshes.items():
            if v.etype == "ordered":
                if hosh != d.identity.h:
                    d.history[hosh.id] = None if len(many) == 1 else many
                    hosh = d.identity.h
                    many = set()
                d.history[k] = v
            else:
                hosh *= v
                many.add(v)
        if hosh != d.identity.h:
            d.history[hosh.id] = None if len(many) == 1 else many
        d.last = list(d.history.keys())[-1]
