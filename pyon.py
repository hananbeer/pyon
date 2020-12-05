import json

class PyoNoneType:
  def __bool__(self):
    return False

  # TODO: other forms of comparisons?
  # DOES NOT EXIST - works because type.__eq__...
  #def __cmp__(self, other):
  #  return type(other) == type(PyoNoneType)

  def __str__(self):
    return 'undefined'

  def __repr__(self):
    return 'PyoNone'

  def __getattr__(self, name):
    return self

  def to_prim(self):
    return None

  def to_json(self, **kwargs):
    return 'null'

PyoNone = PyoNoneType()

# TODO: I think it's not working BECAUSE it's a lambda... (function vs. method)
def mirror(obj1, obj2, attr):
  op = getattr(type(obj2), attr, None)
  if op:
    def new_op(*args):
      return op(obj1._pyon_data, *args)
    setattr(obj1, attr, new_op)
    return None

def pyon_mirror_ops1(obj1, obj2):
  # NOTE: avoiding ops *I* believe should not be used, or not yet believe they should be used.
  # leaving in comments in the meantime.
  ops = [ \
    # from dir(int):
    '__abs__', '__add__', '__and__', '__bool__', '__ceil__',
    #'__class__', '__delattr__', '__dir__',
    '__divmod__',
    # '__doc__',
    '__eq__', '__float__',
    '__floor__', '__floordiv__', '__format__', '__ge__',
    # '__getattribute__', '__getnewargs__',
    '__gt__',
    # pretty sure we don't want to mirror __hash__
    #'__hash__',
    '__index__', '__init__', '__init_subclass__',
    '__int__', '__invert__', '__le__', '__lshift__', '__lt__', '__mod__', '__mul__',
    '__ne__', '__neg__',
    # '__new__',
    '__or__', '__pos__', '__pow__', '__radd__', '__rand__',
    '__rdivmod__', '__reduce__', '__reduce_ex__',
    # '__repr__',
    '__rfloordiv__', '__rlshift__',
    '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__', '__rshift__',
    '__rsub__', '__rtruediv__', '__rxor__',
    # '__setattr__', '__sizeof__', '__str__',
    '__sub__',
    # '__subclasshook__',
    '__truediv__', '__trunc__', '__xor__',

    # from dir(str):
    '__contains__', '__getitem__', '__iter__',
    # pretty sure we want __len__
    '__len__', 
  ]

  for op in ops:
    mirror(obj1, obj2, op)

def pyon_mirror_ops2(obj1, obj2):
  # NOTE: avoiding ops *I* believe should not be used, or not yet believe they should be used.
  # leaving in comments in the meantime.
  ops = [ \
    # everything in dir(PyonObject) that we want to mirror
    # (otherwise, getattr() will take care of delegating the op)
    #'__class__', '__delattr__',
    # NOTE: __dict__ must be... well, a dict.
    #'__dict__',
    #'__dir__', '__doc__',
    '__eq__',
    #'__format__',
    '__ge__',
    #'__getattribute__',
    '__gt__',
    #'__hash__', '__init__', '__init_subclass__',
    '__le__', '__lt__',
    #'__module__',
    '__ne__', '__new__', '__reduce__', '__reduce_ex__',
    #'__repr__', '__setattr__',
    '__sizeof__',
    # TODO: maybe we should include __str__...
    #'__str__',
    #'__subclasshook__', '__weakref__'
  ]

  for op in ops:
    mirror(obj1, obj2, op)

  return None

# TODO:
# attach type to PyonObject
# register unpacker() and stuff
# mirror attributes from primitive pyon_data (e.g. Pyon(5) == 5)

class PyonBase(object):
  # IMPORTANT NOTE: declaring attributes with double-underscores, therefore making them private,
  # will cause Python-voodoo because the class name is appended - but ONLY for in some cases,
  # confusing __getattr__.
  # in short, internal attributes need to be unique "just enough".
  # HOWEVER, maybe it is desireable to have private internal data...
  #__slots = ('_pyon_data', '_pyon_prim')
  #_pyon_data = None
  #_pyon_prim = None
  def __init__(self):
    self._pyon_data = None
    self._pyon_prim = None

  def __eq__(self, other):
    # allow comparing PyonObject(5) == PyonObject(5)
    if type(other) == PyonObject:
      other = other.to_prim()

    return self._pyon_data.__eq__(other)

  def __ne__(self, other):
    # allow comparing PyonObject(5) != PyonObject(6)
    if type(other) == PyonObject:
      other = other.to_prim()

    return self._pyon_data.__ne__(other)

  def __lt__(self, other):
    return self._pyon_data.__lt__(other)

  def __le__(self, other):
    return self._pyon_data.__le__(other)

  def __gt__(self, other):
    return self._pyon_data.__gt__(other)

  def __ge__(self, other):
    return self._pyon_data.__ge__(other)


  def __add__(self, other):
    return self._pyon_data.__add__(other)

  def __sub__(self, other):
    return self._pyon_data.__sub__(other)

  def __mul__(self, other):
    return self._pyon_data.__mul__(other)

  def __div__(self, other):
    return self._pyon_data.__div__(other)

  def __floordiv__(self, other):
    return self._pyon_data.__floordiv__(other)

  def __mod__(self, other):
    return self._pyon_data.__mod__(other)

  def __pow__(self, other):
    return self._pyon_data.__pow__(other)

  def __lshift__(self, other):
    return self._pyon_data.__lshift__(other)

  def __rshift__(self, other):
    return self._pyon_data.__rshift__(other)

  def __and__(self, other):
    return self._pyon_data.__and__(other)

  def __xor__(self, other):
    return self._pyon_data.__xor__(other)

  def __or__(self, other):
    return self._pyon_data.__or__(other)

  # screw supporting i-ops
  """
  def __iadd__(self, other):
    return self._pyon_data.__iadd__(other)

  def __isub__(self, other):
    return self._pyon_data.__isub__(other)

  def __imul__(self, other):
    return self._pyon_data.__imul__(other)

  def __idiv__(self, other):
    return self._pyon_data.__idiv__(other)

  def __ifloordiv__(self, other):
    return self._pyon_data.__ifloordiv__(other)

  def __imod__(self, other):
    return self._pyon_data.__imod__(other)

  def __ipow__(self, other):
    return self._pyon_data.__ipow__(other)

  def __ilshift__(self, other):
    return self._pyon_data.__ilshift__(other)

  def __irshift__(self, other):
    return self._pyon_data.__irshift__(other)

  def __iand__(self, other):
    return self._pyon_data.__iand__(other)

  def __ixor__(self, other):
    return self._pyon_data.__ixor__(other)

  def __ior__(self, other):
    return self._pyon_data.__ior__(other)
  """

  # unary operators
  def __neg__(self):
    return self._pyon_data.__neg__()

  def __pos__(self):
    return self._pyon_data.__pos__()

  def __abs__(self):
    return self._pyon_data.__abs__()

  def __invert__(self):
    return self._pyon_data.__invert__()

  def __complex__(self):
    return self._pyon_data.__complex__()

  def __int__(self):
    return self._pyon_data.__int__()

  def __long__(self):
    return self._pyon_data.__long__()

  def __float__(self):
    return self._pyon_data.__float__()

  def __oct__(self):
    return self._pyon_data.__oct__()

  def __hex__(self):
    return self._pyon_data.__hex__()

  # also override some magic funcs
  def __len__(self):
    return self._pyon_data.__len__()

  def __hash__(self):
    return self._pyon_data.__hash__()

class PyonObject(PyonBase):
  def __init__(self, arg=PyoNone, **kwargs):
    # so that __getattr__ won't trigger on PyonBase attributes
    # EDIT: so apparently self.__init__ must finish first... use deferred_setattr method
    super(PyonBase, self).__init__()

    self.__set_data(arg, **kwargs)

  def __set_data(self, arg=PyoNone, **kwargs):
    # NOTE: because of __setattr__ we have to set _pyon_* attributes via super class
    if arg is not PyoNone and type(arg) != dict:
      if len(kwargs) > 0:
        raise Exception('PyonObject cannot accept both primitive argument and complex data')
          
      super(PyonBase, self).__setattr__('_pyon_prim', True)
      # TODO: chain to parent element?

      if type(arg) == list:
        super(PyonObject, self).__setattr__('_pyon_data', [PyonObject(x) for x in arg])
      else:
        # neither a dict nor a list - assume primitive (int, float, str, null)
        super(PyonObject, self).__setattr__('_pyon_data', arg)
    else:
      if type(arg) == dict:
        # ie. PyonObject({'val': 69}, val=420, l33t='c0d3'))
        # provides: { "val": 69, "l33t": "c0d3" }
        
        # NOTE: kwargs override positional arg:
        arg.update(kwarg)
        # for positional arguments to override kwargs:
        #kwargs.update(arg)

      super(PyonBase, self).__setattr__('_pyon_prim', False)

      # local var, deffer self._pyon_data to be set atomically below
      _pyon_data = {}

      # convert kwargs dict to Pyon chain
      for key, val in kwargs.items():
        if type(val) == dict:
          _pyon_data[key] = PyonObject(**val)
        else:
          # primitive Pyon (int, string, float, list - TODO: check the rest?)
          _pyon_data[key] = PyonObject(val)

      # and finally set self._pyon_data atomically
      super(PyonObject, self).__setattr__('_pyon_data', _pyon_data)

    # TODO: should be done for both prim and complex?
    #pyon_mirror_ops2(self, self._pyon_data)

  # TODO: delegate __ops__ to pyon_data?
  #def __getattribute__(self, name):
  #  pass

  def __getattr__(self, name):
    # NOTE: __getattr__ will be called only if `self` has no attribute `name`
    if self._pyon_prim:
      return getattr(self._pyon_data, name, PyoNone)

    # JSON's null (None in python) is a valid value, so default to PyoNone
    return self._pyon_data.get(name, PyoNone)

  def __setattr__(self, name, val):
    return self._pyon_data.__setitem__(name, val)

  def __getitem__(self, name):
    # TODO: check if prmitive for errors, complex for PyoNone
    return self._pyon_data[name]

  def __setitem__(self, name, val):
    # TODO: check prim?
    return self._pyon_data.__setitem__(name, PyonObject(val))

  def __dir__(self):
    if self._pyon_prim:
      return []

    return self._pyon_data.keys()

  def __repr__(self):
    if self._pyon_prim:
      return 'Pyon:%s' % repr(self._pyon_data)

    return 'PyonObject(type=%s, decendants=%s)' % (type(self._pyon_data), len(self._pyon_data))

  def __str__(self):
    # TODO: check prim?
    return str(self._pyon_data)

  def to_prim(self):
    if self._pyon_prim:
      return self._pyon_data

    # convert sub PyonObject's recursively
    res = { key: val.to_primitive() for (key, val) in self._pyon_data.items() }
    return res

  def to_json(self, **kwargs):
    return json.dumps(self.to_prim(), **kwargs)
