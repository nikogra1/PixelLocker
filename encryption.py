class Encryption():
    def __init__(self) -> None:
        pass
    def encrypt(self,leter,PIN:str):
        c = 0
        PIn = 0
        for i in range(400):
            if leter == chr(i):
                c = i
        for i in list(PIN):
            for j in range(400):
                if i == chr(j):
                    PIn += j
        d = str(c)
        d = int(d)
        d = d * int(PIn)
        return d
    def decrypt(self,PIN:str,d):
        PIn = 0
        for i in list(PIN):
            for j in range(400):
                if i == chr(j):
                    PIn += j
        d = int(d) // int(PIn)
        d = int(d)
        d = chr(d)
        return d