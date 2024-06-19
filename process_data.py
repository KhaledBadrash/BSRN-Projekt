import json
from json import JSONDecodeError

#tests zum lernen u. verstehen.

# a Python object (dict):
x = [{
    "name": "John",
    "age": 30,
    "city": "New York"
},
    {
        "name": "Matilda",
        "age": 35,
        "city": "Hamburg",
        "adresse": {  #multivalued, mengenwertig
            "city": "New York",
            "PLZ": 77777
        },
        "hobbies": ["Schach", "Lesen", "Zocken"]  #arr
    }
]

# convert into python:
y = json.dumps(x)

# the result is a JSON string:
print(y)

import json

# Deine Python-Daten:
x = [{
    "name": "John",
    "age": 30,
    "city": "New York"
},
    {
        "name": "Matilda",
        "age": 35,
        "city": "Hamburg",
        "adresse": {  #multivalued, mengenwertig
            "city": "New York",
            "PLZ": 77777
        },
        "hobbies": ["Schach", "Lesen", "Zocken"]  #arr
    }
]

# Konvertiere in JSON-String:
y = json.dumps(x)
print("JSON-String:")
print(y)

# Konvertiere JSON-String zurück in ein Python-Objekt:
python_obj = json.loads(y)

# Finde die Adresse von Matilda:
matilda_adresse = None
for person in python_obj:
    if person.get("name") == "Matilda":
        matilda_adresse = person.get("adresse").get("city")
        break

# Ausgabe der Adresse von Matilda:
print("\nAdresse von Matilda:")
print(matilda_adresse)

# Finde Matilda und greife auf das 0te Element ihrer Hobbies zu:
matilda_hobby_0 = None
for person in python_obj:
    if person.get("name") == "Matilda":
        matilda_hobby_0 = person.get("hobbies")[0]
        break

# Ausgabe des 0ten Elements der Hobbies von Matilda:
print("\nDas 0te Element der Hobbies von Matilda:")
print(matilda_hobby_0)

