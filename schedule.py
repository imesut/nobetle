# -*- coding: cp1254 -*-
from pulp import *
import time
from nobetle_helper import none2emp


def optimization(dr, days_number, fridays, weekends, locations):
    none2emp(dr)
    days_number=days_number+1
    places = locations
    locations = [place[0] for place in locations]
    begin_time = time.time()
    prob = LpProblem("nobetle", LpMinimize)
    s_p = 0
    days = range(s_p, days_number + s_p)
    sw_f = [6, 13, 20, 27]
    delta_t = 0
    delta_tminus1 = 0
    t1 = range(s_p, days_number - 1 + s_p)
    t2 = range(s_p, days_number - 2 + s_p)
    sw_f_choose = {}
    sw_f_choose_temp = [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    for i in range(0, len(dr)):
        sw_f_choose[dr[i]] = sw_f_choose_temp[i]

    s_g_n = []
    e_g_n = []

    for i in dr:
        if i.id in [1001, 1015, 1011]:
            s_g_n.append(i)

    cof_w_e_pos = {}
    cof_w_e_neg = {}
    cof_fri_pos = {}
    cof_fri_neg = {}
    cof_sat_pos = {}
    cof_sat_neg = {}
    cof_sun_pos = {}
    cof_sun_neg = {}
    cof_sw_f_pos = {}
    cof_sw_f_neg = {}
    cof_tan_pos = {}
    cof_o_f_f_pos = {}
    cof_o_f_f_neg = {}
    cof_o_n_pos = {}
    cof_o_n_neg = {}
    cof_loc_pos = {}
    cof_loc_neg = {}

    for i in dr:
        cof_fri_pos[i] = 5.4
        cof_fri_neg[i] = 5.4
        cof_sat_pos[i] = 1
        cof_sat_neg[i] = 1
        cof_sun_pos[i] = 1
        cof_sun_neg[i] = 1
        for t in days:
            cof_sw_f_pos[i, t] = 5.2
            cof_sw_f_neg[i, t] = 5.2
            cof_tan_pos[i, t] = 1.9
            cof_o_f_f_pos[i, t] = 14.4
            cof_o_f_f_neg[i, t] = 14.4
            cof_o_n_pos[i, t] = 4
            cof_o_n_neg[i, t] = 4

    shift_var = LpVariable.dicts("X", (dr, days, locations), lowBound=0, upBound=1, cat=pulp.LpInteger)
    DevLocPos = LpVariable.dicts("DevLocPos", (dr, locations), lowBound=0, cat=pulp.LpContinuous)
    DevLocNeg = LpVariable.dicts("DevLocNeg", (dr, locations), lowBound=0, cat=pulp.LpContinuous)
    DevWEPos = LpVariable.dicts("DevWEPos", (dr), lowBound=0, cat=pulp.LpContinuous)
    DevWENeg = LpVariable.dicts("DevWENeg", (dr), lowBound=0, cat=pulp.LpContinuous)
    DevFriPos = LpVariable.dicts("DevFriPos", (dr), lowBound=0, cat=pulp.LpContinuous)
    DevFriNeg = LpVariable.dicts("DevFriNeg", (dr), lowBound=0, cat=pulp.LpContinuous)
    DevSatPos = LpVariable.dicts("DevSatPos", (dr), lowBound=0, cat=pulp.LpContinuous)
    DevSatNeg = LpVariable.dicts("DevSatNeg", (dr), lowBound=0, cat=pulp.LpContinuous)
    DevSunPos = LpVariable.dicts("DevSunPos", (dr), lowBound=0, cat=pulp.LpContinuous)
    DevSunNeg = LpVariable.dicts("DevSunNeg", (dr), lowBound=0, cat=pulp.LpContinuous)
    DevSwFPos = LpVariable.dicts("DevSwFPos", (dr, days), lowBound=0, cat=pulp.LpContinuous)
    DevSwFNeg = LpVariable.dicts("DevSwFNeg", (dr, days), lowBound=0, cat=pulp.LpContinuous)
    DevTanPos = LpVariable.dicts("DevTanPos", (dr, days), lowBound=0, cat=pulp.LpContinuous)
    DevOFFPos = LpVariable.dicts("DevOFFPos", (dr, days), lowBound=0, cat=pulp.LpContinuous)
    DevONNeg = LpVariable.dicts("DevONNeg", (dr, days), lowBound=0, cat=pulp.LpContinuous)

    prob += lpSum([cof_fri_pos[i] * DevFriPos[i] for i in dr]
                  + [cof_fri_neg[i] * DevFriNeg[i] for i in dr]
                  + [cof_o_f_f_pos[i, t] * DevOFFPos[i][t] for i in dr for t in days]
                  + [cof_o_n_neg[i, t] * DevONNeg[i][t] for i in dr for t in days]
                  + [cof_sw_f_pos[i, t] * DevSwFPos[i][t] for i in dr for t in days]
                  + [cof_sw_f_neg[i, t] * DevSwFNeg[i][t] for i in dr for t in days]
                  + [cof_tan_pos[i, t] * DevTanPos[i][t] for i in dr for t in days]), ""

    for i in dr:
        for l in i.inf_loc:
            prob += lpSum([shift_var[i][t][l] for t in days]) == 0, ""

    for i in dr:
        for t in days:
            prob += lpSum([shift_var[i][t][l] for l in locations]) <= 1, ""

    for t in days:
        prob += lpSum([shift_var[i][t]["ICU1"] for i in dr]) == 1, ""

    for t in days:
        prob += lpSum([shift_var[i][t]["ICU2"] for i in dr]) == 1, ""

    for t in days:
        prob += lpSum([shift_var[i][t]["SR"] for i in dr]) >= 0, ""

    for t in days:
        prob += lpSum([shift_var[i][t]["SR"] for i in dr]) <= 1, ""

    for i in dr:
        prob += lpSum([shift_var[i][t][l] for t in days for l in locations]) == i.total_shifts, ""

    for i in dr:
        prob += lpSum([shift_var[i][t][l] for t in weekends for l in locations]) == i.we_shifts, ""

    for i in dr:
        prob += lpSum([shift_var[i][t][l] for t in fridays for l in locations]) - DevFriPos[i] + DevFriNeg[i] == i.friday_shifts, ""

    for i in dr:
        for t in t1:
            prob += lpSum([shift_var[i][t][l] + shift_var[i][t + 1][l] for l in locations]) <= 1, ""

    for i in s_g_n:
        prob += lpSum([shift_var[i][days[0 + s_p]][l] for l in locations]) == 0, ""

    for i in dr:
        for t in t2:
            if t not in sw_f:
                prob += lpSum([shift_var[i][t][l] + shift_var[i][t + 1][l] +
                               shift_var[i][t + 2][l] for l in locations]) - DevTanPos[i][t] <= 1, ""

    for i in s_g_n:
        if t not in sw_f:
            prob += lpSum([shift_var[i][days[0 + s_p]][l] +
                           shift_var[i][days[1 + s_p]][l] for l in locations]) - DevTanPos[i][t] == 0, ""

    for i in e_g_n:
        if t not in sw_f:
            prob += lpSum([shift_var[i][days[0 + s_p]][l] for l in locations]) - DevTanPos[i][t] == 0, ""

    for i in dr:
        for t in sw_f:
            prob += lpSum([shift_var[i][t - 2][l] * sw_f_choose[i] - shift_var[i][t][l] * sw_f_choose[i]
                           for l in locations]) - DevSwFPos[i][t] <= 0, ""

    if delta_t == 1:
        for i in s_g_n:
            prob += lpSum([shift_var[i][days[1 + s_p]][l] for l in locations]) + DevSwFNeg[i][t] == 1, ""

    if delta_tminus1 == 1:
        for i in s_g_n:
            prob += lpSum([shift_var[i][days[0 + s_p]][l] for l in locations]) + DevSwFNeg[i][t] == 1, ""

    for i in dr:
        print("i:", i)
        for t in i.vacation_days:
            print("t: ", t)
            prob += lpSum([shift_var[i][t][l] for l in locations]) == 0, ""

    for i in dr:
        for t in i.mustdays:
            prob += lpSum([shift_var[i][t][l] for l in locations]) == 1, ""

    for i in dr:
        for t in i.off_days:
            prob += lpSum([shift_var[i][t][l] for l in locations]) - DevOFFPos[i][t] == 0, ""

    for i in dr:
        for t in i.on_days:
            prob += lpSum([shift_var[i][t][l] for l in locations]) + DevONNeg[i][t] == 1, ""

    prob.writeLP("nobetle.lp")
    prob.solve()
    output = {"metadata": {}, "result": {}}
    n = 1
    for t in days:
        for l in locations:
            for i in dr:
                if shift_var[i][t][l].value() == 1:
                    output["result"]["shift"+str(n)] = {"day": t+1, "location": str(l), "doctor_id": i.id}
                    n += 1

    status = LpStatus[prob.status]
    objective_value = round(value(prob.objective), 4)
    duration = round(time.time() - begin_time, 4)
    output["metadata"] = {"status": status, "objective_value": objective_value, "calc_duration": duration}
    return output
