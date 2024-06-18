import json
from json import JSONDecodeError

#tests zum lernen u. verstehen

# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into python:
y = json.dumps(x)

# the result is a JSON string:
print(y)