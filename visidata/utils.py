import operator

'Various helper classes and functions.'

__all__ = ['AttrDict', 'joinSheetnames', 'moveListItem', 'namedlist']


class AttrDict(dict):
    'Augment a dict with more convenient .attr syntax.'
    def __getattr__(self, k):
        return self[k]

    def __setattr__(self, k, v):
        self[k] = v

    def __dir__(self):
        return self.keys()


def joinSheetnames(*sheetnames):
    'Concatenate sheet names in a standard way'
    return '_'.join(str(x) for x in sheetnames)


def moveListItem(L, fromidx, toidx):
    "Move element within list `L` and return element's new index."
    toidx = max(toidx, 0)
    r = L.pop(fromidx)
    L.insert(toidx, r)
    return toidx


class OnExit:
    '"with OnExit(func, ...):" calls func(...) when the context is exited'
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self.func(*self.args, **self.kwargs)
        except Exception as e:
            exceptionCaught(e)


def itemsetter(i):
    def g(obj, v):
        obj[i] = v
    return g


def namedlist(objname, fieldnames):
    'like namedtuple but editable'
    class NamedListTemplate(list):
        __name__ = objname
        _fields = fieldnames

        def __init__(self, L=None, **kwargs):
            if L is None:
                L = [None]*len(fieldnames)
            super().__init__(L)
            for k, v in kwargs.items():
                setattr(self, k, v)

        @classmethod
        def length(cls):
            return len(cls._fields)

        def __getattr__(self, k):
            'to enable .fieldname'
            try:
                return self[self._fields.index(k)]
            except ValueError:
                raise AttributeError

        def __setattr__(self, k, v):
            'to enable .fieldname ='
            try:
                self[self._fields.index(k)] = v
            except ValueError:
                super().__setattr__(k, v)

    for i, attrname in enumerate(fieldnames):
        # create property getter/setter for each field
        setattr(NamedListTemplate, attrname, property(operator.itemgetter(i), itemsetter(i)))

    return NamedListTemplate
