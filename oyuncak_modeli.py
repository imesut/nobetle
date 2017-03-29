# -*- coding: cp1254 -*-
from pulp import *

prob = LpProblem("DENEME",LpMinimize)

oyuncak = [0,1]
limit_marangoz = 100
limit_boyama = 200
saat_marangoz = [3,1]
saat_boyama = [1,3]
profit = [-10,-15]

X = LpVariable.dicts("X",(oyuncak), lowBound=0, upBound=1000, cat=pulp.LpInteger)

prob += lpSum([X[i]*profit[i] for i in oyuncak]), ""
prob += lpSum([X[i]*saat_marangoz[i] for i in oyuncak])   <= limit_marangoz, ""
prob += lpSum([X[i]*saat_boyama[i] for i in oyuncak])   <= limit_boyama, ""

prob.writeLP("ozcan.lp")
prob.solve()

print("Status:", LpStatus[prob.status])

print(X[0].value())
print(X[1].value())
