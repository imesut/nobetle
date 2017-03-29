from flask import Flask, render_template, url_for, request, g
from pulp import *
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("/html/demo/index.html")

@app.route('/demo')
def demo():
    return render_template("/html/demo/demo.html")

@app.route('/sonuc', methods=["POST", "GET"])
def sonuc():
    if request.method == "POST":
        marangoz = request.form["marangoz"]
        boyama = request.form["boyama"]
    else:
        print("alamadım")

    prob = LpProblem("DENEME", LpMinimize)

    oyuncak = [0, 1]
    limit_marangoz = int(marangoz)
    limit_boyama = int(boyama)
    saat_marangoz = [3, 1]
    saat_boyama = [1, 3]
    profit = [-10, -15]

    X = LpVariable.dicts("X", (oyuncak), lowBound=0, upBound=1000, cat=pulp.LpInteger)

    prob += lpSum([X[i] * profit[i] for i in oyuncak]), ""
    prob += lpSum([X[i] * saat_marangoz[i] for i in oyuncak]) <= limit_marangoz, ""
    prob += lpSum([X[i] * saat_boyama[i] for i in oyuncak]) <= limit_boyama, ""

    prob.writeLP("ozcan.lp")
    prob.solve()

    return("Status: " + LpStatus[prob.status] + " Tren: " + str(X[0].value()) + " Asker: " + str(X[1].value()))

database = "/Users/mesut/Desktop/nobetle_db.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)g
    return db

@app.route('/deneme')
def deneme():
    cur = get_db().execute("select * from DrInfo")
    output = cur.fetchall()
    print(type(output))
    for i in output:
        print(i)
        print(type(i))
    return str(output)



if __name__ == '__main__':
    app.run()
