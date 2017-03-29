# -*- coding: cp1254 -*-
"""
v3:
Henuz V2'ye ek olarak birsey eklemedim. 
V2:
======= DICT ve VERi YAPILARI ==============
1. Nobet sayilari ve ONDAYS gibi isteklerin yapilari birbirinden farklılasabiliyor. 
2. Tum nobet sayilarini dict olarak yazdim. Ancak key'ler hem isim, hem de ID olabilir. 
3. ONdays, OFFdays, MustDays, Vacations, InfLoc: Bunlari dictionary olarak yazdım.
   - Dictionary'nin key'leri doktor ismi de olabilir, direk rakam da olabilir.
   - Kritik bir konu ise, mesela bir doktorun hic ONDays'i yoksa onu o listeye eklemedim.
     Böylece kocaman bir matrix tutmaktansa, icabinda hic istek yoksa, hic verisi olmayan bir
     dictionary tutmus oldum. Bu yapi, dictionary olmana bir yerde ise yaramayacak. Ancak
     kolaylikla matrixlik bir yapiya cevrilebilir. Cevrilirken su iki seye dikkat etmek gerek:
       -> ONDAYS' (ve digerilerinin) yapisi dict'ten DrxDays yapili bir matrixe donusecek
       -> Kisitlari yazdiran looplar bu matrixli yapiya uygun sekilde yazilacak. 

======= SOFT CONSTRAINT YAPILARI ==============
Soft Constraint ile ilgili aklıma iki yapı geliyor. 
1. Soft constraint başına ceza
   - Herkes için, mesela, OFF günlerin belli bir cezası olsun.
   - Kıdeme göre bu ceza değişsin.
   - Eğer birden fazla OFF gun secerse bu cezayı boleyim.
   - Benzer sekilde bu ceza puanlarini gunler arasinda kendi istedikleri
     gibi dagitabilsin. 
2. Toplam ceza
   - Herkes için toplam bir ceza puanı olsun
   - insanlar ellerindeki toplam ceza puanini istedigi gibi dagitsin.
   ! Burada şu problem olabilir. Çocuk bütün cezasını bir gune yatirirsa,
     kidemlinin istedigi olmayabilir. Buna soyle bir onlem alabiliriz.
     Kidemlinin istedigi illa olacaksa, orayi izin gunu ya da zorunlu gun yapabiliriz,
     boylece kidemlinin istedigi olur. Dolayisiyla bu puanlama işi de olabilir gibi.

- - - - COZUM - - - - - - - 

1. Simdilik soft constraintler ile calisan bir kodumuz olsun
2. Bu katsayilari ayarlama isi bir sonraki iş olacak


======= DiGER DURUMLAR ==============

Bu arada doktor isimleri ile ilgili su problemim var
1. isimler olsun istiyorum cunku kisa vadede emine ile yaptigim nobet listelerinin
   okunabilmesini istiyorum.
2. Ancak uzun vadede isimler olsun istemiyorum. Bu turkce karakterler karistirir diye
   dusunuyorum. Bu nednele de isimler olsun istemiyorum.
   Simdilik rakamlarla bi devam edelim hele.

9. Soft constraint cezalarini yazarken suna dikkat edelim:
   Kisit for all Doctor mu, for all Doctor, Gun mu? Cok farkediyor!!!
"""

# Import PuLP modeler functions
from pulp import *

# Create the 'prob' variable to contain the problem data
prob = LpProblem("BAVU_AR",LpMinimize)

#Burada hic isim tutmasak, isim isini arada bir layer olsa
#o layer halletse herseyi, nasil olur? Yani turkce karakter meselesi olabilir
#isim isinden emin olamadigim icin birkac farkli liste olusturdum.

DrAd  =  ["Fatma", "Emine", "Harun", "Selcuk", "Ismail",
          "Hakki", "Zehra", "Betul", "Zeynep", "Rabia",
          "Shainaz", "Celal", "Pervin", "Hazan", "Ayse", "Tural"]

NofDr = len(DrAd)
DrID  = range(0,len(DrAd))

#Doktorların numaralarini veriyor. 
DrDict2 ={}
j=0
for i in DrAd:
    DrDict2[i] = DrID[j]
    j=j+1

#Number of days, number days-1 and number of days-2
#For calculating the block shifts
############################################
## Defining the parameters      ############
## Doctors, Days, Weekends, Locations ######
############################################

T      = 31
#Henuz gunleri birden mi, sifirdan mi baslaticam, bilemedim. Bu asagidaki degisken buna yariyor. 
SP     = 0
Dr     = DrAd #Dr'lari simdilik numara ile tutuyorum. 
Days   = range(SP,T+SP)
WEDays = [5,6,12,13,19,20,26,27] #haftasonu gunleri
Fridays= [4,11,18,25] #haftasonu gunleri
SwF    = [6,13,20,27]
#Shows whether day T or T-1 of the previous month is Friday. 
deltaT       = 0
deltaTminus1 = 0

Loc  = ["ICU1", "ICU2", "SR"]
T1   = range(SP,T-1+SP)
T2   = range(SP,T-2+SP)

############################################
## Choosing Constraints         ############
## Kısıt Secimi                 ############
############################################
SwFChoose={}
SwFChooseTemp   = [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
for i in range(0,NofDr):
    print i
    SwFChoose[Dr[i]] = SwFChooseTemp[i]


############################################
## Number of shifts(Nobet adedi):   ########
## DAYS (gun'lere ozel              ########
############################################

#Her doktorun CUma, C.tesi, Pazar, HS ve Toplam nobet sayilari farkli. 

#Initialization

FridayShiftsTemp  = [0 for a in Dr]
WEShiftsTemp      = [0 for a in Dr]
TotalShiftsTemp   = [0 for a in Dr]
SatShiftsTemp     = [0 for a in Dr]
SanShiftsTemp     = [0 for a in Dr]




FridayShifts["Fatma"] = 0
FridayShifts["Emine"] = 1
FridayShifts["Harun"] = 1
FridayShifts["Selcuk"] = 1
FridayShifts["Ismail"] = 0
FridayShifts["Hakki"] = 1
FridayShifts["Zehra"] = 0
FridayShifts["Betul"] = 0
FridayShifts["Zeynep"] = 0
FridayShifts["Rabia"] = 1
FridayShifts["Shainaz"] = 1
FridayShifts["Celal"] = 1
FridayShifts["Pervin"] = 0
FridayShifts["Hazan"] = 1
FridayShifts["Ayse"] = 1
FridayShifts["Tural"] = 2



TotalShifts["Fatma"] = 5
TotalShifts["Emine"] = 5
TotalShifts["Harun"] = 5
TotalShifts["Selcuk"] = 5
TotalShifts["Ismail"] = 5
TotalShifts["Hakki"] = 5
TotalShifts["Zehra"] = 3
TotalShifts["Betul"] = 6
TotalShifts["Zeynep"] = 3
TotalShifts["Rabia"] = 7
TotalShifts["Shainaz"] = 8
TotalShifts["Celal"] = 8
TotalShifts["Pervin"] = 2
TotalShifts["Hazan"] = 8
TotalShifts["Ayse"] =9
TotalShifts["Tural"] = 9



WEShifts["Fatma"] = 1
WEShifts["Emine"] = 1
WEShifts["Harun"] = 1
WEShifts["Selcuk"] = 1
WEShifts["Ismail"] = 1
WEShifts["Hakki"] = 1
WEShifts["Zehra"] = 3
WEShifts["Betul"] = 1
WEShifts["Zeynep"] = 3
WEShifts["Rabia"] = 1
WEShifts["Shainaz"] = 1
WEShifts["Celal"] = 1
WEShifts["Pervin"] = 2
WEShifts["Hazan"] = 1
WEShifts["Ayse"] =2
WEShifts["Tural"] = 3



#my_file = open("FridayShifts.txt","r")
#FridayShift2 = my_file.read()
#print my_file.readline() #tek satir okur
#my_file.close()



############################################
## Infeasible Locations             ########
## Uygun olmayan yerler              #######
## (Her doktor her yerde tutamaz      ######
############################################
'''
InfLocTemp  = [['SR'], ['SR'] ,['SR'] ,['SR'] ,['SR'] ,['SR'],
               ['SR','ICU1'],['SR'] ,['SR','ICU1'] ,['SR'] ,['SR'],
               [] ,['SR', 'ICU1'] ,[] , ['ICU1','ICU2'], ['ICU1','ICU2'] ]

InfLoc ={}
for i in range(0,NofDr):
    InfLoc[Dr[i]] = InfLocTemp[i]
'''
InfLoc["Fatma"] = ['SR']
InfLoc["Emine"] = ['SR']
InfLoc["Harun"] = ['SR']
InfLoc["Selcuk"] = ['SR']
InfLoc["Ismail"] = ['SR']
InfLoc["Hakki"] = ['SR']
InfLoc["Zehra"] = ['SR', 'ICU1']
InfLoc["Betul"] = ['SR']
InfLoc["Zeynep"] = ['SR', 'ICU1']
InfLoc["Rabia"] = ['SR']
InfLoc["Shainaz"] = []
InfLoc["Celal"] = []
InfLoc["Pervin"] = ['SR', 'ICU1']
InfLoc["Hazan"] = []
InfLoc["Ayse"] = ['ICU1',"ICU2"]
InfLoc["Tural"] = ['ICU1',"ICU2"]


############################################
## Number of shifts:            ############
## LOCATIONS                    ############
############################################
'''
ICU1ShiftsTemp  = [[3], [3], [3], [4], [4], [3], [0], [3], [0], [3], [4], [0], [0], [0], [0]]
ICU2ShiftsTemp  = [[1], [1], [1], [0], [0], [2], [0], [3], [0], [5], [3], [5], [3], [3], [3]] 
SRShiftsTemp    = [[], [], [], [], [], [], [4], [], [5], 0, [1], [3], [5], [6], [5]]
    
LocationShifts = {}
for i in range(0,NofDr):
    LocationShifts[Dr[i],'ICU1'] = ICU1ShiftsTemp[i]
    LocationShifts[Dr[i],'ICU2'] = ICU2ShiftsTemp[i]
    LocationShifts[Dr[i],'SR']   = SRShiftsTemp[i]

#LocationShifts.keys()[
'''


############################################
## Izınli Gunler, istekler      ############
## ON, MUST, OFF, VACATIONS     ############
############################################
## Initialization
#ONDays   = [[0 for x in range(len(Days))] for x in range(len(Dr))]
#OFFDays, VACATION, MUSTON da bu sekilde tanimlanabilir. 
#Nasıl tutacagim, bunu dusunuyorum,
#En basiti bir matrix sekilde tanimlamak.
#ama bu sekilde is yuku olarak bilgisayara cok az sey veriyoruz.
#SU anda dict ozelligini kullaniyoruz. 
ONDays   = {}

OFFDays      ={'Rabia':[1,2,3,8,9,10,15,16,17,22,23,24]}

VacationDays = {'Fatma':[4,5,6,25,26,27,28,29,30], 'Emine':[4,5,6], 'Harun':[4,5,6,12,19,26,30],
                "Selcuk":[4,5,6,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
                'Ismail':[4,5,6,28,19,20,29,30],
                'Hakki': [0,11,12,13,18,19,20,30],
                'Shainaz': [5], 'Celal': [12,13,29,30], 'Hazan':[30], 'Ayse':[9],
                'Betul':[30]}

MustDays     = {'Hakki': [4,6,9], 'Emine':[18,20], 'Selcuk':[11,13],
                'Harun':[25,27], 'Ismail':[2], 'Betul':[17]}



############################################
## Info from Previos Month      ############
## On duty on day T and T-1     ############
############################################

#People who are on shift on day T of previous month
SGN = ['Emine', 'Tural','Celal']
#[DrDict["Harun"],DrDict["Betul"], DrDict["Pervin"] ]

#People who are on shift on day T-1 of previous month
EGN = []


############################################
##                              ############
## COEFFICIENTS                 ############
## KATSAYILAR                   ############
##                              ############
############################################
#YB ve AML'deki nobetlerden saparsa uygulanacak cezalar
CofWEPos = {}
CofWENeg = {}
CofFriPos = {}
CofFriNeg = {}
CofSatPos = {}
CofSatNeg = {}
CofSunPos = {}
CofSunNeg = {}

CofSwFPos = {}
CofSwFNeg = {}
CofTanPos = {}
CofOFFPos = {}
CofOFFNeg = {}
CofONPos  = {}
CofONNeg  = {}


CofLocPos = {}
CofLocNeg = {}


    
for i in Dr:
#    CofWEPos[i]  = 1
#    CofWENeg[i]  = 1
    CofFriPos[i] = 5.4
    CofFriNeg[i] = 5.4
    CofSatPos[i] = 1
    CofSatNeg[i] = 1
    CofSunPos[i] = 1
    CofSunNeg[i] = 1
    for t in Days:
        CofSwFPos[i,t] = 5.2
        CofSwFNeg[i,t] = 5.2
        CofTanPos[i,t] = 1.9
        CofOFFPos[i,t] = 14.4
        CofOFFNeg[i,t] = 14.4
        CofONPos[i,t]  = 4
        CofONNeg[i,t]  = 4
#    for l in Loc:
#        CofLocPos[i,l] = 7
#        CofLocNeg[i,l] = 5
        


        



############################################
##                              ############
## VARIABLES                    ############
##                              ############
############################################
#Degiskenleri kümeler uzerinden tanimlayabiliyoruz.

ShiftVar = LpVariable.dicts("X",(Dr,Days,Loc),
                           lowBound=0,
                           upBound=1,
                           cat=pulp.LpInteger)



#Soft constraint'ler için değişkenler
DevLocPos = LpVariable.dicts("DevLocPos",(Dr,Loc),
                           lowBound=0,
                           cat=pulp.LpContinuous)

DevLocNeg = LpVariable.dicts("DevLocNeg",(Dr,Loc),
                           lowBound=0,
                           cat=pulp.LpContinuous)


DevWEPos  = LpVariable.dicts("DevWEPos",(Dr),
                           lowBound=0,
                           cat=pulp.LpContinuous)

DevWENeg  = LpVariable.dicts("DevWENeg",(Dr),
                           lowBound=0,
                           cat=pulp.LpContinuous)

DevFriPos = LpVariable.dicts("DevFriPos",(Dr),
                           lowBound=0,
                           cat=pulp.LpContinuous)

DevFriNeg = LpVariable.dicts("DevFriNeg",(Dr),
                           lowBound=0,
                           cat=pulp.LpContinuous)

DevSatPos = LpVariable.dicts("DevSatPos",(Dr),
                           lowBound=0,
                           cat=pulp.LpContinuous)

DevSatNeg = LpVariable.dicts("DevSatNeg",(Dr),
                           lowBound=0,
                           cat=pulp.LpContinuous)


DevSunPos = LpVariable.dicts("DevSunPos",(Dr),
                           lowBound=0,
                           cat=pulp.LpContinuous)

DevSunNeg = LpVariable.dicts("DevSunNeg",(Dr),
                           lowBound=0,
                           cat=pulp.LpContinuous)


DevSwFPos = LpVariable.dicts("DevSwFPos",(Dr,Days),
                           lowBound=0,
                           cat=pulp.LpContinuous)

DevSwFNeg = LpVariable.dicts("DevSwFNeg",(Dr,Days),
                           lowBound=0,
                           cat=pulp.LpContinuous)


DevTanPos = LpVariable.dicts("DevTanPos",(Dr,Days),
                           lowBound=0,
                           cat=pulp.LpContinuous)

#DevTanNeg = LpVariable.dicts("DevTanNeg",(Dr,Days),
#                           lowBound=0,
#                           cat=pulp.LpContinuous)


DevOFFPos = LpVariable.dicts("DevOFFPos",(Dr,Days),
                           lowBound=0,
                           cat=pulp.LpContinuous)

#DevOFFNeg = LpVariable.dicts("DevOFFNeg",(Dr,Days),
#                           lowBound=0,
#                           cat=pulp.LpContinuous)


#DevONPos = LpVariable.dicts("DevONPos",(Dr,Days),
#                           lowBound=0,
#                           cat=pulp.LpContinuous)

DevONNeg = LpVariable.dicts("DevONNeg",(Dr,Days),
                           lowBound=0,
                           cat=pulp.LpContinuous)



############################################
##                              ############
## OBJECTIVE FUNCTION           ############
##                              ############
############################################

prob += lpSum([CofFriPos[i]*DevFriPos[i] for i in Dr ]
            + [CofFriNeg[i]*DevFriNeg[i] for i in Dr ]
 + [CofOFFPos[i,t]*DevOFFPos[i][t] for i in Dr for t in Days]
 + [CofONNeg[i,t]*DevONNeg[i][t] for i in Dr for t in Days]
 + [CofSwFPos[i,t]*DevSwFPos[i][t] for i in Dr for t in Days]
 + [CofSwFNeg[i,t]*DevSwFNeg[i][t] for i in Dr for t in Days]
 + [CofTanPos[i,t]*DevTanPos[i][t] for i in Dr for t in Days]), ""

#[CofLocPos[i,l]*DevLocPos[i][l] for i in Dr for l in Loc ]
#              + [CofLocNeg[i,l]*DevLocNeg[i][l] for i in Dr for l in Loc] 

#prob += 0, "Arbitrary Objective Function"



############################################
##                              ############
## CONSTRAINTS                  ############
##                              ############
############################################


#There are infeasible dr-location matches which should be eliminated
#Bazı doktorlar bazı lokasyonlarda nobet tutamaz. Kıdemsizler YB'de, YB rotasyonu olanlar
# Constraint 1
for i in InfLoc:
    for l in InfLoc[i]:
        prob += lpSum([ShiftVar[i][t][l] for t in Days ]) == 0, ""

#Every doctor can be at a single location at a particular day
#Her doktor en fazla bir yerde nobetci olabilir
# Constraint 2
for i in Dr:
    for t in Days:
        prob += lpSum([ShiftVar[i][t][l] for l in Loc])   <= 1, ""

#YB'de bir doktor olabilir
#There can be a single doctor at ICU1 and ICU2
# Constraint 3
for t in Days:
    prob += lpSum([ShiftVar[i][t]["ICU1"] for i in Dr]) == 1, ""

for t in Days:
    prob += lpSum([ShiftVar[i][t]["ICU2"] for i in Dr]) == 1, ""

#Ameliyathane de en az bir doktor olabilir
#There should be at least one Dr at Surgery
# Constraint 4
for t in Days:
    prob += lpSum([ShiftVar[i][t]["SR"] for i in Dr]) >= 0, ""


#Ameliyathanede en fazla bir doktor olabilir. 
#There should be at most one Dr at Surgery
# Constraint 5
for t in Days:
    prob += lpSum([ShiftVar[i][t]["SR"] for i in Dr]) <= 1, ""


#Toplam nöbet sayısı
#Number of shifts - TotalShifts
# Constraint 6
for i in Dr:
    prob += lpSum([ShiftVar[i][t][l] for t in Days for l in Loc])  == TotalShifts[i], ""

#Haftasonu nöbet sayısı
#Number of shifts - WEShifts
# Constraint 7
for i in Dr:
    prob += lpSum([ShiftVar[i][t][l] for t in WEDays for l in Loc])   == WEShifts[i], ""
#    prob += lpSum([ShiftVar[i][t][l] for t in WEDays for l in Loc]) -DevWEPos[i] + DevWENeg[i]  == WEShifts[i], ""

'''
#YB nobet sayisi
#Number of shifts - ICU
for i in Dr:
    prob += lpSum([ShiftVar[i][t]["ICU1"] for t in Days]) == LocationShifts[i,'ICU1'], ""
    prob += lpSum([ShiftVar[i][t]["ICU2"] for t in Days])  == LocationShifts[i,'ICU2'] , ""
    prob += lpSum([ShiftVar[i][t]["SR"] for t in Days])  == LocationShifts[i,'SR'] , ""

#    prob += lpSum([ShiftVar[i][t]["ICU1"] for t in Days]) -DevLocPos[i]["ICU1"] + DevLocNeg[i]["ICU1"] == LocationShifts[i,'ICU1'], ""
#    prob += lpSum([ShiftVar[i][t]["ICU2"] for t in Days]) -DevLocPos[i]["ICU2"] + DevLocNeg[i]["ICU2"] == LocationShifts[i,'ICU2'] , ""
'''

#Cuma nobet sayısı
#Number of shifts - FridayShifts
# Constraint 8
for i in Dr:
    #prob += lpSum([ShiftVar[i][t][l]  for t in Fridays for l in Loc])   == FridayShifts[i], ""
    prob += lpSum([ShiftVar[i][t][l]  for t in Fridays for l in Loc])-DevFriPos[i] + DevFriNeg[i]  == FridayShifts[i], ""



##############################
#   Blok nobetler       ######
#   Block Shift         ######
##############################
# Constraint 9
for i in Dr:
    for t in T1:
        prob += lpSum([ShiftVar[i][t][l] + ShiftVar[i][t+1][l] for l in Loc])  <= 1, ""


#Evvelki ayın T. günü icin blok nobet      
#Block Shifts for T
# Constraint 10
for i in SGN:
    prob += lpSum([ShiftVar[i][Days[0+SP]][l]  for l in Loc])  == 0, ""
      


##############################
#  Gunasiri nobetler    ######
# Tandem Shifts         ######
##############################
# Constraint 11
for i in Dr:
    for t in T2:
        if t not in SwF:
            prob += lpSum([ShiftVar[i][t][l] + ShiftVar[i][t+1][l]+
                       ShiftVar[i][t+2][l] for l in Loc]) -DevTanPos[i][t]  <= 1, ""


#Evvelki ayın T. günü icin gunasiri nobet
#Tandem Shifts
# Constraint 12
for i in SGN:
    if t not in SwF:
        prob += lpSum([ShiftVar[i][Days[0+SP]][l]+
                   ShiftVar[i][Days[1+SP]][l] for l in Loc])-DevTanPos[i][t]   == 0, ""

#Evvelki ayın T-1. günü icin gunasiri nobet
#Tandem Shifts
# Constraint 13
for i in EGN:
    if t not in SwF:
        prob += lpSum([ShiftVar[i][Days[0+SP]][l] for l in Loc])-DevTanPos[i][t] == 0, ""


#############################
#Cumalı pazarlar        ######
#Sundays with Friday    ######
##############################
#Bu kisiti biraz degistirdim.
#Onceliklesag tarafı kucuk esit yaptım. Boylece sol taraf istedigi kadar
#negatif olabilir.
#İkinci olarak cuma ile pazar'ın yerini degistirdim. Boylece, istedigi kadar
#pazar nobeti yazsin, cuma nobeti yazmayacaktır. Ama cuma nobeti varsa
#oraya mutlaka bir pazar nobeti koymaya calisacak. Bu, sunun icin onemli
#Haftasonu sayılarını fixliyoruz. Bu nedenle pazar sayısı 3 asagi 5 yukari belli
#Ama tersi oldugunda, yani pazar varsa cuma da koysun diyince bu kez cuma
#kalabilecekken oraya nobet koyabiliyor. Simdilik boyle dursun bakalim
# Constraint 14
for i in Dr:
    for t in SwF:
        prob += lpSum([ShiftVar[i][t-2][l]*SwFChoose[i]  - ShiftVar[i][t][l]*SwFChoose[i]
                       for l in Loc]) -DevSwFPos[i][t]   <= 0, ""

#Evvelki ayın T. günü icin cumalı pazar
#Sundays with Friday for T
# Constraint 15
if deltaT ==1:
    for i in SGN:
        prob += lpSum([ShiftVar[i][Days[1+SP]][l] for l in Loc]) + DevSwFNeg[i][t]  == 1, ""


#Evvelki ayın T-1. günü icin cumalı pazar
#Sundays with Friday for T-1
# Constraint 16
if deltaTminus1 ==1:
    for i in SGN:
        prob += lpSum([ShiftVar[i][Days[0+SP]][l] for l in Loc]) + DevSwFNeg[i][t]  == 1, ""


##############################
# Izinler ve istekler     ####
# Vacation, OFF, ON, Must ####
##############################
'''
Burada belki her gune ayri bir agirlik verdirebiliriz.
O yuzden hepsini toplayıp sıfıra eşitlemek yerine,
ayri ayri kodlamak daha verimli olacaktır.
'''

#Izinli oldugu gunler
#Vacation Days
# Constraint 17
for i in VacationDays:
    for t in VacationDays[i]:
        prob += lpSum([ShiftVar[i][t][l] for l in Loc ]) == 0, ""

#Mecbur Nobet Gunleri
#Must Days
# Constraint 18
for i in MustDays:
    for t in MustDays[i]:
        prob += lpSum([ShiftVar[i][t][l] for l in Loc ])  == 1, ""

#Istenmeyen Nobet Gunleri
#OFF Days
# Constraint 19
for i in OFFDays:
    for t in OFFDays[i]:
        prob += lpSum([ShiftVar[i][t][l] for l in Loc ]) - DevOFFPos[i][t] == 0, ""

#Istenen Nobet Gunleri
#ON Days
# Constraint 20
for i in ONDays:
    for t in ONDays[i]:
        prob += lpSum([ShiftVar[i][t][l] for l in Loc ])  + DevONNeg[i][t] == 1, ""



# The problem data is written to an .lp file
prob.writeLP("BAVU.lp")
# The problem is solved using PuLP’s choice of Solver
prob.solve()
# The status of the solution is printed to the screen
print "Status:", LpStatus[prob.status]

'''
for v in prob.variables():
    print v.name, "=", v.varValue
'''

f = open('Guray.txt', 'w')
f.write('Bezmialem Anestezi ve Yogun Bakim Nobet Cizelgesi\n')
if LpStatus[prob.status]=='Infeasible':
    f.write('Maalesef uygun bir cozum bulamadim, nobet sayilarini degistirip tekrar deneyin\n\n')
elif LpStatus[prob.status]=='Optimal':
    f.write('OPTIMAL cozumu buldum! \n\n')
    

for t in Days:
    Temp = Days[t]+1
    f.write("%s\t" % Temp )
    for l in Loc:
        for i in Dr:
            if ShiftVar[i][t][l].value() == 1:
                f.write("%s\t" % i )
        
    f.write("\n")
f.close()

#name = raw_input("Guray")
