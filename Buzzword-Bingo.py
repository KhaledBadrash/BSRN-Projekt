import math

print("Welcome to Bingo!")
print("Test")
print("Test2")
print("Test3")
print("Test4")

import random

w = random.randint(1, 50)
print(w)

with open("C:\\Users\\M02Mu\\Documents - Kopie\\2. Semester\\BSRN\\buzzwords.txt", "r") as file:
    content = file.readlines()
    print(content[w-1])


