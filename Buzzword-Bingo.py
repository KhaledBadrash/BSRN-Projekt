import Log

eingabeBreite = int(input('Geben Sie die Breite des Spielfeldes an -xaxis: '))
eingabeHoehe = int(input('Geben Sie die Hoehe des Spielfeldes an -yaxis:  '))

#Falls Eingabe von Hoehe und Breite nicht gleich ist
if eingabeHoehe != eingabeBreite:
    print('Beide Eingaben muessen gleich sein!')

if eingabeHoehe == eingabeBreite:
    print()

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



