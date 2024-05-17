from datetime import datetime
class log:
    def __init__(self):
        self.now = datetime.now()
        self.date = self.now.strftime("%d/%m/%Y %H:%M:%S")
        pass

    def logeintragstep(self):
        self.now = datetime.now()
        with open(r'C:\Users\khaled\PycharmProjects\BSRN-Projekt\Protokoll', 'a') as file:
            return file.write('Step: '+self.date + '\n')
        pass

    def logeintragstart(self):
        self.now = datetime.now()
        with open(r'C:\Users\khaled\PycharmProjects\BSRN-Projekt\Protokoll', 'a') as file:
            return file.write('Start: '+self.date + '\n')
        pass
