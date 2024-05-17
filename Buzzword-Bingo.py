print("Welcome to Bingo!")
print("Test")
print("Test2")
print("Test3")
print("Test4")

import random


def buzzwords():
    w = random.randint(1, 50)  #Zufallszahl-Generator
    print(w)
    with open("C:\\Users\\M02Mu\\Documents - Kopie\\2. Semester\\BSRN\\buzzwords.txt", "r") as file:  #Datei
        content = file.readlines()  #Datei lesen
    return content[w - 1]  # Wort aus einer zufälligen Zeile, bestimmt vom Generator


for buzzword in range(25): #zum Karten erstellen (test)
   i = 0
   i = i + 1
   print(buzzwords())



print("Hello")
