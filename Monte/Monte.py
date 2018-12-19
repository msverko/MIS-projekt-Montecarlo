import random
import matplotlib.pyplot as plt
import csv

# proizvod = [[1,2,3,4,5,6] , ["celicni lim obicni", "celicni auto-lim", "celicni brodski lim", "aluminij obicni", "dur-aluminij", "bakreni lim"], [10,7,5,4,6,8]] # id, naziv, brzina(m/sec)

class proizvod:
  def __init__(self, id, naziv, brzina):
    self.id = id
    self.naziv = naziv
    self.brzina = brzina

p1 = proizvod(1, "celicni lim obicni", 10)
p2 = proizvod(2, "celicni auto-lim", 7)
p2 = proizvod(3, "celicni brodski lim", 5)

prevPageLevel = 0 #prethodna razina stranice
maxNumElements = 0 #najveci broj elemenata na stranici - inicijalno

numCases = int(input("Unesi zeljeni broj ponavljanja (odvojenih slucaja) \n"),10)
#print(numSim)
maxPageLevel = int(input("Unesi najvisu mogucu razinu stranice u navigaciji \n"),10)
#print(pageLevel)
while maxNumElements < 7:
    maxNumElements = int(input("Unesi najvisi moguci broj grafickih elemenata po stranici (>6) \n"),10)
#print(numElements)



for cases in range(1, numCases+1):
    print ("case" + str(cases))
    pageLevel = random.randint(0,maxPageLevel) #random razina kriticnog dogadjaja
    print("Razina stranice = " + str(pageLevel))
    if pageLevel == 0:
        #ako je zadana nulta razina, tada je potrebno 2sec po svakoj razini prethodne stranice za spuštanje na nultu razinu,
        #te dodatnih 5sec za prelazak na stranicu nulte razine.  
        navigTime = 2 * prevPageLevel + 5 
        print("Vrijeme navigacije = " + str(navigTime))
        prevPageLevel = pageLevel # postavljanje inicijalne razine za slijedeci loop.
    elif pageLevel > 0:
        t1 = 2 * prevPageLevel #povratak na nultu razinu traje 2sec po svakoj razini iznad nule
        numElements = random.randint(10,maxNumElements) #random broj elemenata na stranici (minimalno 10)
        print("Broj elemenata na stranici = " + str(numElements))
        if numElements in range(0,10):
            coeficient = 1
        elif numElements in range(11,20):
            coeficient = 1.5
        elif numElements in range(21,30):
            coeficient = 2
        elif numElements in range(31,50):
            coeficient = 4



"""
roll_X = []
roll_Y = []


def rollDice1():
    
    roll = random.randint(1,100)
    return roll
   

def rollDice2():
    
    roll = random.randint(1,100)
    return roll
   

x = 0
while x < 10:
    rezult1 = rollDice1()
    rezult2 = rollDice2()
    roll_X.append(rezult1)
    roll_Y.append(rezult2)
    x += 1

plt.plot(roll_X, roll_Y)
plt.show()

"""


 
"""
# open file
with open('persons.csv', 'rt', newline='') as f:  #'rt'- read text   'rb' - read binary
    reader = csv.reader(f)
    header = next(reader) 
    data = [row for fow in reader]
"""

