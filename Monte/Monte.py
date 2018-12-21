import random
import matplotlib.pyplot as plt
import math
import csv
import numpy as np

# proizvod = [[1,2,3,4,5,6] , ["celicni lim obicni", "celicni auto-lim", "celicni brodski lim", "aluminij obicni", "dur-aluminij", "bakreni lim"], [10,7,5,4,6,8]] # id, naziv, brzina(m/sec)



def Izbornik():
    izbor = 0
    while (izbor != 1 or izbor != 2 or izbor != 3 or izbor != 9):
        izbor = int(input("\n Odaberi opciju: \n 1 = Generiranje podataka na temelju unosa parametara \n 2 = Analiza generiranih podataka iz .scv \n 9 = izlaz \n "),10)
        if izbor == 1:
            GenerateData()
        if izbor == 3:
            #PlotSigmnond()
            PlotNormalDistribution()
        if izbor == 9:
            quit()


def GenerateData():
    prevPageLevel = 0 #prethodna razina stranice
    maxNumElements = 0 #najveci broj elemenata na stranici - inicijalno
    coeficient = 1 #koeficijent složenosti stranice na bazi broja elemenata (množi se sa baznim vremenom za navigaciju među stranicama razina >0)
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
            # ako je zadana nulta razina, tada je potrebno 2sec po svakoj razini prethodne stranice za spuštanje na nultu razinu,
            # te dodatnih 5sec za prelazak na stranicu nulte razine.  
            navigTime = 2 * prevPageLevel + 5
            print("Vrijeme navigacije = " + str(navigTime))
            prevPageLevel = pageLevel # postavljanje inicijalne razine za slijedeci loop.
        elif pageLevel > 0:
            t1 = 1.5 * prevPageLevel # povratak na nultu razinu traje 2sec po svakoj razini iznad nule
            t2 = 0 
            for tepmPageLevel in range(1, pageLevel+1): # za prelazak na svaku narednu razinu, iznova se racuna koeficijent, i vrijeme reakcije
                numElements = random.randint(6,maxNumElements) # random broj elemenata na stranici (minimalno 6)
                print("Broj elemenata na stranici = " + str(numElements))
                coeficient = GetCoeficient(numElements)
                print("Koeficijent slozenosti = " + str(coeficient))
                t2 = t2 + (coeficient * 2)
                print("Vrijeme dosezanja zadane razine = " + str(t2))
            t = t1 + t2 # ukupno vrijeme potrebno da se vrati na nultu razinu, te dosegne zadanu.
            print("Ukupno vrijeme reakcije = " + str(t))
        prevPageLevel = pageLevel # postavljanje inicijalne razine za slijedeci loop/case.



def PlotSigmnond():
    x = np.arange(0, 100, 0.1) # 0=min, 100=Max, 0.1=finesa
    a = []
    for item in x:
        a.append( 1 + (4 / (1 + math.exp(-0.1*(item-50))))) # 4=L(max y os), 0.1=k(strmina), 50=x0(sredina krivulje na x osi)  
                                                            # Jedinica na početku podiže krivulju na X osi jer rezultat množi osnovnu brzinu reakcije(multiplikator je u rasponu 1-5)
    plt.plot(x,a)
    plt.show()



def PlotNormalDistribution():
    mu, sigma = 50, 10 # 50=središte distribucije, 10=prva standardna devijacja(+,- 10 od središta = 68% vrijednosti), 1000 = br uzoraka
    s = np.random.normal(mu, sigma, 1000)

    # Create the bins and histogram
    count, bins, ignored = plt.hist(s, 20, normed=True)

    # Plot the distribution curve
    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
        np.exp( - (bins - mu)**2 / (2 * sigma**2) ),       linewidth=3, color='y')
    plt.show()


def GetCoeficient(xVal):
    yVal = 1 + (4 / (1 + math.exp(-0.1*(xVal-50))))
    #plt.plot(xVal,yVal,'ro')
    #plt.show()
    return yVal


Izbornik()



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

