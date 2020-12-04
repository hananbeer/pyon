import json
from pyon import *

js = '{ "a": {"b": [0, 1.2, {"c": 3}, "pi"] }, "d": {"e": 5}, "z": 14 }'
data = json.loads(js)
p = PyonObject(**data)

def test(expr, expc=None):
  res = eval(expr, globals())
  passed = ''
  if res == expc:
    passed = 'PASSED!'
  elif expc is not None:
    raise Exception('failed: "%s" evaluated to "%s", expecting "%s"' % (expr, res, expc))

  print('%s:\r\n=> %s %s' % (expr, str(res), passed))

z = p['z']
print(z)

p['z'] = 15
print(p.z)

p.z = 16
print(p.z)

p.z *= 2
print(p.z)

test('p.a')
test('p.a.b')
test('p.a.c', PyoNone)
test('p.a.c.b', PyoNone)
test('p.a.b.c')
test('p.a.b[2]')
test('p.a.b[2].c', 3)
test('p.a.b[3]', 'pi')
test('p.d')

# TODO: should we expect int? I think PyonObject is fine, but I guess overriding __class__ might work...
#test('type(p.d.e)', int)
test('type(p.d.e)', PyonObject)

test('p.d.e', PyonObject(5))
test('p.d.e == PyonObject(4)', False)
test('p.d.e == PyonObject(5)', True)
test('p.d.e != PyonObject(5)', False)
test('p.d.e != PyonObject(6)', True)
test('p._pyon_data')
test('p.d.e == 5', True)
test('p.d.e >= 4', True)
test('p.d.e <= 6', True)
test('p.d.e > 6', False)
test('p.d.e < 4', False)
test('-p.d.e', -5)

test('type(p.d.e.to_prim())', int)
test('p.d.e.to_prim()', 5)

test('p.d.f.g.h.i.j.k == PyoNone', True)


