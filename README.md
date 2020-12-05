# Pyon - Python Object Notation
## Really?
Not really. *Pyon* is **not** a new data format.

*Pyon* is a python module that provides an interface similar to JavaScript.

Example:
```python
# JSON...
json_data = json.loads('{"a": {"b": 3.14}}')
print(json_data['a']['b'])

# PYON!
pyon_data = PyonObject(json_data)
print(pyon_data.a.b)
```
