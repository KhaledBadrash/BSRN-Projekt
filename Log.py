from datetime import datetime
class Log:
    def __init__(self):
        self.now = datetime.now()
        self.date = self.now.strftime("%d/%m/%Y %H:%M:%S")
        pass

    def logEintrag(self):
        self.now = datetime.now()
        with open('\M02Mu\PycharmProjects\BSRN-Projekt\Protokoll', 'a') as file:
            file.write(self.date)
        pass
    pass