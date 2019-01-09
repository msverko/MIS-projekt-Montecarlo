import random
import matplotlib.pyplot as plt
import math
import csv
import numpy as np


ispunjenostArr = []
global header
global data

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
    global mu # središte mormalne distribucije
    global sigma #prva standardna devojacija
    global ispunjenost #postotak ispunjenosti stranice
    prevPageLevel = 0 #prethodna razina stranice
    maxIspunjenost = 0 #maksimalna ispunjenost stranice - inicijalno
    coeficient = 1 #koeficijent složenosti stranice na bazi broja elemenata 
                   #(množi se sa baznim vremenom za navigaciju među stranicama razina >0)
    numCases = int(input("Unesi zeljeni broj ponavljanja (odvojenih kritičnih slucaja) \n"),10)
    maxPageLevel = int(input("Unesi najvisu mogucu razinu stranice u navigaciji \n"),10)
    while maxIspunjenost < 6:
        maxIspunjenost = int(input("Unesi najvisi moguci postotak ispunjenosti stranice (>5) \n"),10)
    mu =  ((maxIspunjenost - 5)/2) + 5 # središte mormalne distribucije(pomiče se za min postotak popunjenosti stranice)
    #print("Srediste normalne distribucije = " + str(mu))
    sigma = (maxIspunjenost - 5) * 0.1 # prva standardna devijacija (10% raspona uzorka)
    #print("Prva standardna devijacija = " + str(sigma))

    with open("Rezultat.csv", mode='w') as csv_file:
            fieldnames = ['Postotak popunjenosti stranice', 'Razina stranice prikaza', 'Vrijeme reakcije operatera']
            writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            writer.writeheader()
            
    for cases in range(1, numCases+1):
        t = 0
        t1 = 0
        t2 = 0
        pageLevel = random.randint(0,maxPageLevel) #random razina stranice kriticnog dogadjaja
        if pageLevel == 0:
            # ako je zadana nulta razina, tada je potrebno 1.5sec po svakoj razini prethodne stranice za spuštanje na nultu razinu,
            # te dodatnih 5sec za prelazak na stranicu nulte razine.  
            t = 1.5 * prevPageLevel + 5
            prevPageLevel = pageLevel # postavljanje inicijalne razine za slijedeci loop.
        elif pageLevel > 0:
            t1 = 1.5 * prevPageLevel # povratak na nultu razinu traje 1.5sec po svakoj razini iznad nule
            t2 = 0 
            for tepmPageLevel in range(1, pageLevel+1): 
                # za prelazak na svaku narednu razinu, iznova se racuna koeficijent, i vrijeme reakcije
                ispunjenost = np.random.normal(mu, sigma, size=None)
                ispunjenost = int(ispunjenost)
                coeficient = GetCoeficient(ispunjenost) # izračun koeficijenta prema Sigmund krivulji
                t2 = t2 + (coeficient * 2)
            t = t1 + t2 # ukupno vrijeme potrebno da se vrati na nultu razinu, te dosegne zadanu razinu.
        prevPageLevel = pageLevel # postavljanje inicijalne razine za slijedeci loop/case.
        ispunjenostArr.append(ispunjenost)

        with open("Rezultat.csv", mode='a') as csv_file:
            fieldnames = ['Postotak popunjenosti stranice', 'Razina stranice prikaza', 'Vrijeme reakcije operatera']
            writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            writer.writerow({'Postotak popunjenosti stranice': str(ispunjenost), 'Razina stranice prikaza': str(pageLevel), 'Vrijeme reakcije operatera': str(t)})


def PlotSigmnond(): # Sigmund krivulja
    x = np.arange(0, 100, 0.1) # 0=min, 100=Max, 0.1=finesa
    a = []
    for item in x:
        a.append( 1 + (4 / (1 + math.exp(-0.1*(item-50))))) 
        # 4=L(max y os), 0.1=k(strmina), 50=x0(sredina krivulje na x osi)  
        # Jedinica na početku podiže krivulju na X osi jer rezultat množi osnovnu brzinu reakcije(multiplikator je u rasponu 1-5)
    plt.plot(x,a)
    plt.xlabel('Ispunjenost stranice[%]')
    plt.ylabel('Koeficijent složenosti stranice')
    plt.title('Multiplikator osnovne brzine navigacije na višu razinu')
    plt.grid(True)
    plt.show()


def PlotNormalDistribution(mu, sigma, IspunjenostArr): # Param: središte distribucije, prva standardna devijacja, uzorak
    #za svaki ement u IspunjenostArr:
    count, bins, ignored = plt.hist(IspunjenostArr, 20, density=True)
    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),       linewidth=3, color='y')
    plt.xlabel('Ispunjenost stranice[%]')
    plt.ylabel('Vjerojatnost')
    plt.title('Histogram grafičke složenosti HMI stranice')
    plt.text(mu, .03, "$\mu={0} , \sigma={1}$".format(mu,sigma), color="w", bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)
    plt.show()


def GetCoeficient(xVal):    # izračun koeficijenta složenosti stranice(množiti će se sa baznom brzinom prelaska na višu razinu) 
                            # na temelju postotka ispunjenosti interaktivnim sadržajem (ovisnost prema Sigmond krivulji)
    yVal = 1 + (4 / (1 + math.exp(-0.1*(xVal-50))))
    #plt.plot(xVal,yVal,'ro')
    #plt.show()
    return yVal


def GetDataFromFile():
    ispunjenost = []
    razina = []
    brzinaReakcije = []
    with open("Rezultat.csv", mode='rt') as csv_file:
        #file = open('rezultat.csv', 'rt', newline='')  #'rt'- read text   'rb' - read binary
        reader = csv.reader(csv_file, delimiter=',')
        header = next(reader) 
        data = [row for row in reader]

    # Ovisnost brzine reakcije o ispunjenosti stranice
    # analiza za max. 10 razina i max. 100% ispunjenosti
    for eachLine in data:
        ispunjenost.append(int(eachLine[0])) # ispunjenost
        razina.append(int(eachLine[1])) # razina staranice
        brzinaReakcije.append(float(eachLine[2])) # brzina reakcije
    brPonavljanja = len(ispunjenost)
    plt.scatter(ispunjenost,brzinaReakcije)
    plt.xlabel('Ispunjenost stranice[%]')
    plt.ylabel('Brzina reakcije')
    plt.title('Ovisnost brzine reakcije o ispunjenosti stranice (max.10raz. i 100%)' )
    plt.text(30, 10, "Broj ponavljanja =" + str(brPonavljanja), color="w", bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)
    plt.show()
    ispunjenost.clear()
    razina.clear()
    brzinaReakcije.clear()

    # Ovisnost brzine reakcije o ispunjenosti stranice
    # analiza za max. 6 razina i max. 100% ispunjenosti
    for eachLine in data:
        if int(eachLine[1]) < 7:
            ispunjenost.append(int(eachLine[0])) # ispunjenost
            razina.append(int(eachLine[1])) # razina staranice
            brzinaReakcije.append(float(eachLine[2])) # brzina reakcije
    brPonavljanja = len(ispunjenost)
    plt.scatter(ispunjenost,brzinaReakcije)
    plt.xlabel('Ispunjenost stranice[%]')
    plt.ylabel('Brzina reakcije')
    plt.title('Ovisnost brzine reakcije o ispunjenosti stranice (max.6raz. i 100%)' )
    plt.text(30, 10, "Broj ponavljanja =" + str(brPonavljanja), color="w", bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)
    plt.show()
    ispunjenost.clear()
    razina.clear()
    brzinaReakcije.clear()

    # Ovisnost brzine reakcije o razini stranice
    # analiza za max. 10 razina i max. 100% ispunjenosti
    for eachLine in data:
        ispunjenost.append(int(eachLine[0])) # ispunjenost
        razina.append(int(eachLine[1])) # razina staranice
        brzinaReakcije.append(float(eachLine[2])) # brzina reakcije
    brPonavljanja = len(ispunjenost)
    plt.scatter(razina,brzinaReakcije)
    plt.xlabel('Razina stranice')
    plt.ylabel('Brzina reakcije')
    plt.title('Ovisnost brzine reakcije o razini stranice (max.10raz. i 100%)' )
    plt.text(2, 10, "Broj ponavljanja =" + str(brPonavljanja), color="w", bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)
    plt.show()
    ispunjenost.clear()
    razina.clear()
    brzinaReakcije.clear()

    # Ovisnost brzine reakcije o razini stranice
    # analiza za max. 10 razina i max. 50% ispunjenosti
    for eachLine in data:
        if int(eachLine[0]) < 51:
            ispunjenost.append(int(eachLine[0])) # ispunjenost
            razina.append(int(eachLine[1])) # razina staranice
            brzinaReakcije.append(float(eachLine[2])) # brzina reakcije
    brPonavljanja = len(ispunjenost)
    plt.scatter(razina,brzinaReakcije)
    plt.xlabel('Razina stranice')
    plt.ylabel('Brzina reakcije')
    plt.title('Ovisnost brzine reakcije o razini stranice (max.10raz. i 50%)' )
    plt.text(2, 10, "Broj ponavljanja =" + str(brPonavljanja), color="w", bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)
    plt.show()
    ispunjenost.clear()
    razina.clear()
    brzinaReakcije.clear()

Izbornik()