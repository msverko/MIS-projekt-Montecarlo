import random
import matplotlib.pyplot as plt
import math
import csv
import numpy as np

ispunjenostArr = []

def Izbornik():
    izbor = 0
    while (izbor != 1 or izbor != 2 or izbor != 3 or izbor != 9):
        izbor = int(input("\n Odaberi opciju: \n 1 = Generiranje podataka na temelju unosa parametara \n 2 = Analiza generiranih podataka iz .scv \n 9 = izlaz \n "),10)
        if izbor == 1:
            GenerateData()
            PlotNormalDistribution(mu, sigma, ispunjenostArr)
            PlotSigmnond()
        if izbor == 2:
            GetDataFromFile()
        if izbor == 9:
            quit()

def GenerateData():
    global mu
    global sigma
    global ispunjenost
    prevPageLevel = 0 #prethodna razina stranice
    maxIspunjenost = 0 #najveci broj elemenata na stranici - inicijalno
    coeficient = 1 #koeficijent složenosti stranice na bazi broja elemenata (množi se sa baznim vremenom za navigaciju među stranicama razina >0)
    numCases = int(input("Unesi zeljeni broj ponavljanja (odvojenih slucaja) \n"),10)
    #print(numSim)
    maxPageLevel = int(input("Unesi najvisu mogucu razinu stranice u navigaciji \n"),10)
    #print(pageLevel)
    while maxIspunjenost < 6:
        maxIspunjenost = int(input("Unesi najvisi moguci broj grafickih elemenata po stranici (>5) \n"),10)
    #print(numElements)
    mu =  ((maxIspunjenost - 5)/2) + 5 # središte mormalne distribucije(pomiče se za min postotak popunjenosti stranice)
    print("Središte normalne distribucije = " + str(mu))
    sigma = (maxIspunjenost - 5) * 0.1 # prva standardna devijacija (10% raspona uzorka)
    print("Prva standardna devijacija = " + str(sigma))

    with open("Rezultat.csv", mode='w') as csv_file:
            fieldnames = ['Postotak popunjenosti stranice', 'Razina stranice prikaza', 'Vrijeme reakcije operatera']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            
    for cases in range(1, numCases+1):
        print ("case" + str(cases))
        pageLevel = random.randint(0,maxPageLevel) #random razina stranice kriticnog dogadjaja
        print("Razina stranice = " + str(pageLevel))
        print("Razina prethodne stranice = " + str(prevPageLevel))
        if pageLevel == 0:
            # ako je zadana nulta razina, tada je potrebno 1.5sec po svakoj razini prethodne stranice za spuštanje na nultu razinu,
            # te dodatnih 5sec za prelazak na stranicu nulte razine.  
            navigTime = 1.5 * prevPageLevel + 5
            print("Vrijeme navigacije = " + str(navigTime))
            prevPageLevel = pageLevel # postavljanje inicijalne razine za slijedeci loop.
        elif pageLevel > 0:
            t1 = 1.5 * prevPageLevel # povratak na nultu razinu traje 1.5sec po svakoj razini iznad nule
            t2 = 0 
            for tepmPageLevel in range(1, pageLevel+1): # za prelazak na svaku narednu razinu, iznova se racuna koeficijent, i vrijeme reakcije
                ispunjenost = np.random.normal(mu, sigma, size=None)
                print("Broj elemenata na stranici = " + str(ispunjenost))
                coeficient = GetCoeficient(ispunjenost) # izračun koeficijenta prema Sigmund krivulji
                print("Koeficijent slozenosti = " + str(coeficient))
                t2 = t2 + (coeficient * 2)
                print("Vrijeme dosezanja zadane razine = " + str(t2))
            t = t1 + t2 # ukupno vrijeme potrebno da se vrati na nultu razinu, te dosegne zadanu.
            print("Ukupno vrijeme reakcije = " + str(t))
        prevPageLevel = pageLevel # postavljanje inicijalne razine za slijedeci loop/case.
        ispunjenostArr.append(ispunjenost)

        with open("Rezultat.csv", mode='a') as csv_file:
            fieldnames = ['Postotak popunjenosti stranice', 'Razina stranice prikaza', 'Vrijeme reakcije operatera']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Postotak popunjenosti stranice': str(ispunjenost), 'Razina stranice prikaza': str(pageLevel), 'Vrijeme reakcije operatera': str(t)})




def PlotSigmnond(): # primjer Sigmund krivulje
    x = np.arange(0, 100, 0.1) # 0=min, 100=Max, 0.1=finesa
    a = []
    for item in x:
        a.append( 1 + (4 / (1 + math.exp(-0.1*(item-50))))) # 4=L(max y os), 0.1=k(strmina), 50=x0(sredina krivulje na x osi)  
                                                            # Jedinica na početku podiže krivulju na X osi jer rezultat množi osnovnu brzinu reakcije(multiplikator je u rasponu 1-5)
    plt.plot(x,a)
    plt.show()


def PlotNormalDistribution(mu, sigma, IspunjenostArr): # Param: središte distribucije, prva standardna devijacja, uzorak
    for item in IspunjenostArr:
        # Create the bins and histogram
        count, bins, ignored = plt.hist(item, 20, density=True)
        plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),       linewidth=3, color='r')
    plt.show()




def GetCoeficient(xVal):    # izračun koeficijenta složenosti stranice(množiti će se sa baznom brzinom prelaska na višu razinu) 
                            # na temelju postotka ispunjenosti interaktivnim sadržajem (ovisnost prema Sigmond krivulji)
    yVal = 1 + (4 / (1 + math.exp(-0.1*(xVal-50))))
    #plt.plot(xVal,yVal,'ro')
    #plt.show()
    return yVal


def GetDataFromFile():
    file = open('persons.csv', 'rt', newline='')  #'rt'- read text   'rb' - read binary
    reader = csv.reader(file)
    header = next(reader) 
    data = [row for row in reader]
    print(header)
    print(data[0])




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


