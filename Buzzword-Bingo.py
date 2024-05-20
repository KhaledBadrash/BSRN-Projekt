import Log

feldG = int(input('Geben Sie die Groeße des Spielfeldes an: '))

startlog = Log.log()
startlog.logeintragstart()

#Auskommentiert bis vorarbeit geleistet
#def buzzwords():
#    w = random.randint(0, 49)  #Zufallszahl-Generator
#   print(w)
#   with open("Textdatei", "r") as file:  #Textdatei aus Github
#       content = file.readlines()  #Datei lesen
#   return content[w]  # Wort aus einer zufälligen Zeile, bestimmt vom Generator
#for buzzword in range(25): #zum Karten erstellen (test) / Es wird genau 25 mal ramdom ein Wort aus der Textdatei geprintet
#   print(buzzwords())
bspLog = Log.log()
bspLog.logeintragstep()



