# -*- coding: cp1254 -*-
from pulp import *
def optimization(db, user_table, department, period):
    prob = LpProblem("nobetle", LpMinimize)
    DrId = [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015]
    NofDr = len(DrId)
    T = 31
    SP = 0
    Dr = DrId
    Days = range(SP, T + SP)

    WEDays = [5, 6, 12, 13, 19, 20, 26, 27]
    Fridays = [4, 11, 18, 25]
    SwF = [6, 13, 20, 27]
    deltaT = 0
    deltaTminus1 = 0

    Loc = ["ICU1", "ICU2", "SR"]
    T1 = range(SP, T - 1 + SP)
    T2 = range(SP, T - 2 + SP)

    SwFChoose = {}
    SwFChooseTemp = [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    for i in range(0, NofDr):
        print(i)
        SwFChoose[Dr[i]] = SwFChooseTemp[i]

    FridayShifts = {}
    TotalShifts = {}
    WEShifts = {}

    FridayShifts[1000] = 0
    FridayShifts[1001] = 1
    FridayShifts[1002] = 1
    FridayShifts[1003] = 1
    FridayShifts[1004] = 0
    FridayShifts[1005] = 1
    FridayShifts[1006] = 0
    FridayShifts[1007] = 0
    FridayShifts[1008] = 0
    FridayShifts[1009] = 1
    FridayShifts[1010] = 1
    FridayShifts[1011] = 1
    FridayShifts[1012] = 0
    FridayShifts[1013] = 1
    FridayShifts[1014] = 1
    FridayShifts[1015] = 2

    TotalShifts[1000] = 5
    TotalShifts[1001] = 5
    TotalShifts[1002] = 5
    TotalShifts[1003] = 5
    TotalShifts[1004] = 5
    TotalShifts[1005] = 5
    TotalShifts[1006] = 3
    TotalShifts[1007] = 6
    TotalShifts[1008] = 3
    TotalShifts[1009] = 7
    TotalShifts[1010] = 8
    TotalShifts[1011] = 8
    TotalShifts[1012] = 2
    TotalShifts[1013] = 8
    TotalShifts[1014] = 9
    TotalShifts[1015] = 9

    WEShifts[1000] = 1
    WEShifts[1001] = 1
    WEShifts[1002] = 1
    WEShifts[1003] = 1
    WEShifts[1004] = 1
    WEShifts[1005] = 1
    WEShifts[1006] = 3
    WEShifts[1007] = 1
    WEShifts[1008] = 3
    WEShifts[1009] = 1
    WEShifts[1010] = 1
    WEShifts[1011] = 1
    WEShifts[1012] = 2
    WEShifts[1013] = 1
    WEShifts[1014] = 2
    WEShifts[1015] = 3

    InfLoc = {}

    InfLoc[1000] = ['SR']
    InfLoc[1001] = ['SR']
    InfLoc[1002] = ['SR']
    InfLoc[1003] = ['SR']
    InfLoc[1004] = ['SR']
    InfLoc[1005] = ['SR']
    InfLoc[1006] = ['SR', 'ICU1']
    InfLoc[1007] = ['SR']
    InfLoc[1008] = ['SR', 'ICU1']
    InfLoc[1009] = ['SR']
    InfLoc[1010] = []
    InfLoc[1011] = []
    InfLoc[1012] = ['SR', 'ICU1']
    InfLoc[1013] = []
    InfLoc[1014] = ['ICU1', "ICU2"]
    InfLoc[1015] = ['ICU1', "ICU2"]

    ONDays = {}

    OFFDays = {1009: [1, 2, 3, 8, 9, 10, 15, 16, 17, 22, 23, 24]}

    VacationDays = {1000: [4, 5, 6, 25, 26, 27, 28, 29, 30], 1001: [4, 5, 6], 1002: [4, 5, 6, 12, 19, 26, 30],
                    1003: [4, 5, 6, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                    1004: [4, 5, 6, 28, 19, 20, 29, 30],
                    1005: [0, 11, 12, 13, 18, 19, 20, 30],
                    1010: [5], 1011: [12, 13, 29, 30], 1013: [30], 1014: [9],
                    1007: [30]}

    MustDays = {1005: [4, 6, 9], 1001: [18, 20], 1003: [11, 13],
                1002: [25, 27], 1004: [2], 1007: [17]}

    SGN = [1001, 1015, 1011]

    EGN = []

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
    CofONPos = {}
    CofONNeg = {}

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
            CofSwFPos[i, t] = 5.2
            CofSwFNeg[i, t] = 5.2
            CofTanPos[i, t] = 1.9
            CofOFFPos[i, t] = 14.4
            CofOFFNeg[i, t] = 14.4
            CofONPos[i, t] = 4
            CofONNeg[i, t] = 4


    ShiftVar = LpVariable.dicts("X", (Dr, Days, Loc), lowBound=0, upBound=1, cat=pulp.LpInteger)
    DevLocPos = LpVariable.dicts("DevLocPos", (Dr, Loc), lowBound=0, cat=pulp.LpContinuous)
    DevLocNeg = LpVariable.dicts("DevLocNeg", (Dr, Loc), lowBound=0, cat=pulp.LpContinuous)
    DevWEPos = LpVariable.dicts("DevWEPos", (Dr), lowBound=0, cat=pulp.LpContinuous)
    DevWENeg = LpVariable.dicts("DevWENeg", (Dr), lowBound=0, cat=pulp.LpContinuous)
    DevFriPos = LpVariable.dicts("DevFriPos", (Dr), lowBound=0, cat=pulp.LpContinuous)
    DevFriNeg = LpVariable.dicts("DevFriNeg", (Dr), lowBound=0, cat=pulp.LpContinuous)
    DevSatPos = LpVariable.dicts("DevSatPos", (Dr), lowBound=0, cat=pulp.LpContinuous)
    DevSatNeg = LpVariable.dicts("DevSatNeg", (Dr), lowBound=0, cat=pulp.LpContinuous)
    DevSunPos = LpVariable.dicts("DevSunPos", (Dr), lowBound=0, cat=pulp.LpContinuous)
    DevSunNeg = LpVariable.dicts("DevSunNeg", (Dr), lowBound=0, cat=pulp.LpContinuous)
    DevSwFPos = LpVariable.dicts("DevSwFPos", (Dr, Days), lowBound=0, cat=pulp.LpContinuous)
    DevSwFNeg = LpVariable.dicts("DevSwFNeg", (Dr, Days), lowBound=0, cat=pulp.LpContinuous)
    DevTanPos = LpVariable.dicts("DevTanPos", (Dr, Days), lowBound=0, cat=pulp.LpContinuous)
    DevOFFPos = LpVariable.dicts("DevOFFPos", (Dr, Days), lowBound=0, cat=pulp.LpContinuous)
    DevONNeg = LpVariable.dicts("DevONNeg", (Dr, Days), lowBound=0, cat=pulp.LpContinuous)

    prob += lpSum([CofFriPos[i] * DevFriPos[i] for i in Dr]
                  + [CofFriNeg[i] * DevFriNeg[i] for i in Dr]
                  + [CofOFFPos[i, t] * DevOFFPos[i][t] for i in Dr for t in Days]
                  + [CofONNeg[i, t] * DevONNeg[i][t] for i in Dr for t in Days]
                  + [CofSwFPos[i, t] * DevSwFPos[i][t] for i in Dr for t in Days]
                  + [CofSwFNeg[i, t] * DevSwFNeg[i][t] for i in Dr for t in Days]
                  + [CofTanPos[i, t] * DevTanPos[i][t] for i in Dr for t in Days]), ""

    for i in InfLoc:
        for l in InfLoc[i]:
            prob += lpSum([ShiftVar[i][t][l] for t in Days]) == 0, ""

    for i in Dr:
        for t in Days:
            prob += lpSum([ShiftVar[i][t][l] for l in Loc]) <= 1, ""

    for t in Days:
        prob += lpSum([ShiftVar[i][t]["ICU1"] for i in Dr]) == 1, ""

    for t in Days:
        prob += lpSum([ShiftVar[i][t]["ICU2"] for i in Dr]) == 1, ""

    for t in Days:
        prob += lpSum([ShiftVar[i][t]["SR"] for i in Dr]) >= 0, ""

    for t in Days:
        prob += lpSum([ShiftVar[i][t]["SR"] for i in Dr]) <= 1, ""

    for i in Dr:
        prob += lpSum([ShiftVar[i][t][l] for t in Days for l in Loc]) == TotalShifts[i], ""

    for i in Dr:
        prob += lpSum([ShiftVar[i][t][l] for t in WEDays for l in Loc]) == WEShifts[i], ""

    for i in Dr:
        prob += lpSum([ShiftVar[i][t][l] for t in Fridays for l in Loc]) - DevFriPos[i] + DevFriNeg[i] == FridayShifts[
            i], ""

    for i in Dr:
        for t in T1:
            prob += lpSum([ShiftVar[i][t][l] + ShiftVar[i][t + 1][l] for l in Loc]) <= 1, ""

    for i in SGN:
        prob += lpSum([ShiftVar[i][Days[0 + SP]][l] for l in Loc]) == 0, ""

    for i in Dr:
        for t in T2:
            if t not in SwF:
                prob += lpSum([ShiftVar[i][t][l] + ShiftVar[i][t + 1][l] +
                               ShiftVar[i][t + 2][l] for l in Loc]) - DevTanPos[i][t] <= 1, ""

    for i in SGN:
        if t not in SwF:
            prob += lpSum([ShiftVar[i][Days[0 + SP]][l] +
                           ShiftVar[i][Days[1 + SP]][l] for l in Loc]) - DevTanPos[i][t] == 0, ""

    for i in EGN:
        if t not in SwF:
            prob += lpSum([ShiftVar[i][Days[0 + SP]][l] for l in Loc]) - DevTanPos[i][t] == 0, ""

    for i in Dr:
        for t in SwF:
            prob += lpSum([ShiftVar[i][t - 2][l] * SwFChoose[i] - ShiftVar[i][t][l] * SwFChoose[i]
                           for l in Loc]) - DevSwFPos[i][t] <= 0, ""

    if deltaT == 1:
        for i in SGN:
            prob += lpSum([ShiftVar[i][Days[1 + SP]][l] for l in Loc]) + DevSwFNeg[i][t] == 1, ""

    if deltaTminus1 == 1:
        for i in SGN:
            prob += lpSum([ShiftVar[i][Days[0 + SP]][l] for l in Loc]) + DevSwFNeg[i][t] == 1, ""

    for i in VacationDays:
        for t in VacationDays[i]:
            prob += lpSum([ShiftVar[i][t][l] for l in Loc]) == 0, ""

    for i in MustDays:
        for t in MustDays[i]:
            prob += lpSum([ShiftVar[i][t][l] for l in Loc]) == 1, ""

    for i in OFFDays:
        for t in OFFDays[i]:
            prob += lpSum([ShiftVar[i][t][l] for l in Loc]) - DevOFFPos[i][t] == 0, ""

    for i in ONDays:
        for t in ONDays[i]:
            prob += lpSum([ShiftVar[i][t][l] for l in Loc]) + DevONNeg[i][t] == 1, ""

    prob.writeLP("nobetle.lp")
    prob.solve()
    print("Status:", LpStatus[prob.status])

    if LpStatus[prob.status] == 'Infeasible':
        print('Maalesef uygun bir cozum bulamadim, nobet sayilarini degistirip tekrar deneyin\n\n')  # Error ver
    elif LpStatus[prob.status] == 'Optimal':
        print('OPTIMAL cozumu buldum!')

    for t in Days:
        for l in Loc:
            for i in Dr:
                if ShiftVar[i][t][l].value() == 1:
                    print("gun " + str(t + 1), "lokasyon: " + str(l), "Doktor: " + str(i))