# Copyright (c) 2022 Javier Escalada Gómez
# All rights reserved.

__version__ = '0.0.1'

# Inspiration: https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92

import json

class CustomJSONEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        if kwargs.get("indent") is None:
            kwargs.update({"indent": 2})
        if kwargs.get("separators") is None:
            kwargs.update({"separators": (",", ": ")})
        self.compact_item_separator = ", "
        self.compact_key_separator = ": "
        if "compact_separators" in kwargs:
            self.compact_item_separator, self.compact_key_separator = kwargs.pop("compact_separators")
        self.indent_hint = lambda path, collection, indent, width: True
        if "indent_hint" in kwargs:
            self.indent_hint = kwargs.pop("indent_hint")
        self.width = 0
        if "width" in kwargs:
            self.width = kwargs.pop("width")
        super().__init__(*args, **kwargs)
    
    def iterencode(self, o, *args, **kwargs):
        return self._wrap(self._iterencode(o, []))

    def encode(self, o):
        return ''.join(self.iterencode(o))
    
    def _parent_encode(self, o):
        return json.JSONEncoder.iterencode(self, o)

    def _iterencode(self, o, path):
        depth = len(path)

        if isinstance(o, (list, tuple)):
            nl_sep, ind_sep, it_sep, _ = self._config(path, o)

            yield "["
            for i, el in enumerate(o):
                if i > 0:
                    yield it_sep
                yield from (nl_sep, (depth+1)*ind_sep)
                yield from self._iterencode(el, path + [i])
            yield from (nl_sep, depth*ind_sep, "]")
            
        elif isinstance(o, dict):
            nl_sep, ind_sep, it_sep, key_sep = self._config(path, o)

            yield "{"
            for i, (k, v) in enumerate(o.items()):
                if not isinstance(k, (str, int, float, bool)) and k is not None:
                    raise TypeError(f'keys must be str, int, float, bool or None, not {k.__class__.__name__}')
                if i > 0:
                    yield it_sep
                yield from (nl_sep, (depth+1)*ind_sep)
                yield from self._parent_encode(k)
                yield self.key_separator
                yield from self._iterencode(v, path + [k])
            yield from (nl_sep, depth*ind_sep, "}")

        else:
            yield from self._parent_encode(o)
    
    def _config(self, path, collection):
        if self.indent_hint(path, collection, self.indent, self.width):
            return "\n", " " * self.indent, self.item_separator, self.key_separator
        return "", "", self.compact_item_separator, self.compact_key_separator

    def _wrap(self, tokens):
        col = 1
        prefix = ""
        for token in tokens:
            if token == "":
                continue
            
            if not self.width:
                yield token
                continue

            if token == "\n":
                col = 1
                yield token
                continue

            if col == 1 and all(c in [" ", "\t"] for c in token):
                prefix = token
                col += len(token)
                yield token
                continue

            col += len(token)
            if col > self.width + 1:
                if (token in [
                        self.compact_item_separator, self.compact_key_separator,
                        self.item_separator, self.key_separator,
                        "[", "]", "{", "}"]):
                    yield token
                    continue
                
                new_col = 1 + len(prefix) + self.indent + len(token)
                if new_col <= self.width + 1:
                    yield from ("\n", prefix, self.indent * " ")
                    col = new_col
            
            yield token