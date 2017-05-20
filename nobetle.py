from flask import Flask, render_template, url_for, request, g, flash, redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from apriori import *
import doktorcizelgele
import json
from nobetle_helper import integer

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:12345678@localhost/nobetle"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "BenGelmedimKaygiIcin"
bcrypt = Bcrypt(app)

#bcrypt.generate_password_hash("1234567890")


class User(db.Model):
    __tablename__ = "User"
    Crp = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String())
    Name = db.Column(db.String())
    Surname = db.Column(db.String())
    mail = db.Column(db.String())
    password = db.Column(db.String())

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __init__(self, Crp, id, type, Name, Surname, mail, password):
        self.Crp = Crp
        self.id = id
        self.type = type
        self.Name = Name
        self.Surname = Surname
        self.mail = mail
        self.password = password

    def __repr__(self):
        return "<User(name='%s', id='%s')>" % (self.Name, self.id)


class Crp(db.Model):
    __tablename__ = "Crp"
    Crp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String())
    adres = db.Column(db.String())
    places = db.Column(db.String())

    def __init__(self, Crp, Name, adres, places):
        self.Crp = Crp
        self.Name = Name
        self.adres = adres
        self.places = places

    def __repr__(self):
        return "<Crp(Name='%s', Crp='%s')>" % (self.Name, self.Crp)


class NobetleRun(db.Model):
    __tablename__ = "NobetleRun"
    Crp = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(), primary_key=True)
    run = db.Column(db.Integer, primary_key=True)
    objective = db.Column(db.Float)
    status = db.Column(db.String())
    calc_duration = db.Column(db.Float)

    def __init__(self, Crp, period, run, objective, status, calc_duration):
        self.Crp = Crp
        self.period = period
        self.run = run
        self.objective = objective
        self.status = status
        self.calc_duration = calc_duration

    def __repr__(self):
        return "<NobetleRun(Crp='%s', period='%s', run='%s')>" % (self.Crp, self.period, self.run)


class DrNobInfo(db.Model):
    __tablename__ = "DrNobInfo"
    Crp = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(), primary_key=True)
    friday_shifts = db.Column(db.Integer)
    total_shifts = db.Column(db.Integer)
    we_shifts = db.Column(db.Integer)
    inf_loc = db.Column(db.String())
    vacation_days = db.Column(db.String())
    mustdays = db.Column(db.String())
    on_days = db.Column(db.String())
    off_days = db.Column(db.String())

    def __init__(self, Crp, id, period, friday_shifts, total_shifts, we_shifts, inf_loc, vacation_days,
                 mustdays, on_days, off_days):
        self.Crp = Crp
        self.id = id
        self.period = period
        self.friday_shifts = friday_shifts
        self.total_shifts = total_shifts
        self.we_shifts = we_shifts
        self.inf_loc = inf_loc
        self.off_days = off_days
        self.vacation_days = vacation_days
        self.mustdays = mustdays
        self.on_days = on_days

    def __repr__(self):
        return "<DrNobInfo(Crp='%s', id='%s', period='%s')>" % (self.Crp, self.id, self.period)


class DrNobet(db.Model):
    __tablename__ = "DrNobet"
    Crp = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(), primary_key=True)
    day = db.Column(db.Integer, primary_key=True)

    def __init__(self, Crp, period, id, location, day):
        self.Crp = Crp
        self.period = period
        self.id = id
        self.location = location
        self.day = day

    def __repr__(self):
        return "<DrNobet(Crp='%s', period='%s', id='%s', location='%s', day='%s')>" % (self.Crp, self.period, self.id,
                                                                                       self.location, self.day)


@app.errorhandler(404)
def not_found(error):
    return "404"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


menu = {
  "admin": {
    "1": {
      "url": "/dashboard/doktorlar",
      "text": "Doktorlar"
    },
    "2": {
      "url": "/dashboard/gecmis",
      "text": "Geçmiş"
    },
    "3": {
      "url": "/dashboard/yeninobet",
      "text": "Yeni Nöbet"
    },
    "4": {
      "url": "/dashboard/destek",
      "text": "Destek"
    },
    "5": {
      "url": "/dashboard/ayarlar",
      "text": "Ayarlar"
    },
    "6": {
      "url": "/logout",
      "text": "Oturumu Kapat"
    }
  },
  "dr": {
      "1": {
          "url": "#",
          "text": "Öge1"
      },
      "2": {
          "url": "/logout",
          "text": "Oturumu Kapat"
      }
  }
}


@app.route("/deneme/<page>")
def deneme(page):
    dr_liste = [info(id="1000", name="F", surname="", friday_shifts=0, total_shifts=5, we_shifts=1, inf_loc=["SR"],
                     vacation_days=[4, 5, 6, 25, 26, 27, 28, 29, 30], mustdays=[18, 20], on_days=[], off_days=[]),
                info(id="1001", name="E", surname="", friday_shifts=1, total_shifts=5, we_shifts=1, inf_loc=["SR"],
                     vacation_days=[4, 5, 6], mustdays=[], on_days=[], off_days=[]),
                info(id="1002", name="H", surname="", friday_shifts=1, total_shifts=5, we_shifts=1, inf_loc=["SR"],
                     vacation_days=[4, 5, 6, 12, 19, 26, 30], mustdays=[25, 27], on_days=[], off_days=[]),
                info(id="1003", name="S", surname="", friday_shifts=1, total_shifts=5, we_shifts=1, inf_loc=["SR"],
                     vacation_days=[4, 5, 6, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                     mustdays=[11, 13], on_days=[], off_days=[]),
                info(id="1004", name="İ", surname="", friday_shifts=0, total_shifts=5, we_shifts=1, inf_loc=["SR"],
                     vacation_days=[4, 5, 6, 28, 19, 20, 29, 30], mustdays=[2], on_days=[], off_days=[]),
                info(id="1005", name="H", surname="", friday_shifts=1, total_shifts=5, we_shifts=1, inf_loc=["SR"],
                     vacation_days=[0, 11, 12, 13, 18, 19, 20, 30], mustdays=[4, 6, 9], on_days=[], off_days=[]),
                info(id="1006", name="Z", surname="", friday_shifts=0, total_shifts=3, we_shifts=3,
                     inf_loc=["SR", "ICU1"], vacation_days=[], mustdays=[], on_days=[], off_days=[]),
                info(id="1007", name="B", surname="", friday_shifts=0, total_shifts=6, we_shifts=1, inf_loc=["SR"],
                     vacation_days=[30], mustdays=[17], on_days=[], off_days=[]),
                info(id="1008", name="Z", surname="", friday_shifts=0, total_shifts=3, we_shifts=3,
                     inf_loc=["SR", "ICU1"], vacation_days=[], mustdays=[], on_days=[], off_days=[]),
                info(id="1009", name="R", surname="", friday_shifts=1, total_shifts=7, we_shifts=1, inf_loc=["SR"],
                     vacation_days=[], mustdays=[], on_days=[], off_days=[1, 2, 3, 8, 9, 10, 15, 16, 17, 22, 23, 24]),
                info(id="1010", name="S", surname="", friday_shifts=1, total_shifts=8, we_shifts=1, inf_loc=[],
                     vacation_days=[5], mustdays=[], on_days=[], off_days=[]),
                info(id="1011", name="C", surname="", friday_shifts=1, total_shifts=8, we_shifts=1, inf_loc=[],
                     vacation_days=[12, 13, 29, 30], mustdays=[], on_days=[], off_days=[]),
                info(id="1012", name="P", surname="", friday_shifts=0, total_shifts=2, we_shifts=2,
                     inf_loc=["SR", "ICU1"], vacation_days=[], mustdays=[], on_days=[], off_days=[]),
                info(id="1013", name="H", surname="", friday_shifts=1, total_shifts=8, we_shifts=1, inf_loc=[],
                     vacation_days=[30], mustdays=[], on_days=[], off_days=[]),
                info(id="1014", name="A", surname="", friday_shifts=1, total_shifts=9, we_shifts=2,
                     inf_loc=["ICU1", "ICU2"], vacation_days=[9], mustdays=[], on_days=[], off_days=[]),
                info(id="1015", name="S", surname="", friday_shifts=2, total_shifts=9, we_shifts=3,
                     inf_loc=["ICU1", "ICU2"], vacation_days=[], mustdays=[], on_days=[], off_days=[])
                ]
    period = "JAN2017"
    if page == "1":
        schedule = doktorcizelgele.optimization(dr=dr_liste, days_number=31, fridays=[4, 11, 18, 25],
                                                weekends=[5, 6, 12, 13, 19, 20, 26, 27],
                                                locations=["ICU1", "ICU2", "SR"])
        for i in schedule["result"]:
            new_schedule_item = DrNobet(Crp=current_user.Crp, period=period,
                                        id=schedule["result"][i]["doctor_id"],
                                        location=schedule["result"][i]["location"],
                                        day=schedule["result"][i]["day"])
            db.session.add(new_schedule_item)
        last_run = 0
        if NobetleRun.query.filter_by(period = period).first():
            print("A schedule has found for this period")
            last_run = NobetleRun.query.filter_by(period=period).order_by(NobetleRun.run.desc()).first().run
        schedule_run_info = NobetleRun(Crp=current_user.Crp, period=period, run=last_run+1,
                                       objective=schedule["metadata"]["objective_value"],
                                       status=schedule["metadata"]["status"],
                                       calc_duration=schedule["metadata"]["calc_duration"])
        db.session.add(schedule_run_info)
        db.session.commit()
        return "deneme/1"
    elif page == "2":
        dr_nob_list = DrNobet.query.filter_by(Crp=current_user.Crp).all()
        return render_template("deneme.html", dr_nob_list = dr_nob_list)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email_form = request.form["email"]
        password_form = request.form["password"]
        l_user = User.query.filter_by(mail = email_form).first()
        if l_user:
            if bcrypt.check_password_hash(l_user.password, password_form):
                login_user(l_user)
                return redirect(url_for('dashboard'))
            else:
                flash("Parolanızı mı unuttunuz?")
        else:
            flash("Hatalı Girişi Bilgisi: kullanıcı bulunamadı.")
    elif hasattr(current_user, "type"):
        print(current_user, current_user.type)
        if current_user.type == "owner":
            return redirect(url_for('panel'))
        if current_user.type == "admin":
            return redirect(url_for('dashboard'))
        if current_user.type == "dr":
            return redirect(url_for('profil'))
    return render_template("login.html")


@app.route('/dashboard')
@login_required
#ADMIN
def dashboard():
    print(current_user.type)
    if current_user.type != "admin":
        return redirect(url_for('login'))
    return redirect(url_for("dashboard_page", page="doktorlar"))

@app.route('/dashboard/<page>', methods=["POST", "GET"])
@login_required
#ADMIN_PAGES
def dashboard_page(page):
    print(page)
    if current_user.type != "admin":
        return redirect(url_for('login'))
    if request.method == "POST":
        if request.base_url.endswith("/dashboard/doktorlar"):
            for i in range(1, int(len(request.form) / 4)):
                name = request.form.get("name" + str(i), "")
                surname = request.form.get("surname" + str(i), "")
                mail = request.form.get("mail" + str(i), "")
                password = request.form.get("password" + str(i), "")
                latest_user_id = User.query.order_by(User.id.desc()).first().id
                new_user = User(Crp=current_user.Crp, id=latest_user_id + 1, type="dr", Name=name, Surname=surname,
                                mail=mail, password=bcrypt.generate_password_hash(password))
                db.session.add(new_user)
            db.session.commit()
        elif request.base_url.endswith("/dashboard/yeninobet"):
            print(request.form)
            ids = sorted([i for i in set([str(i.split("-")[0]) for i in request.form])])
            for id in ids:
                friday_shifts = integer(request.form.get(str(id) + "-friday_shifts"))
                inf_loc = request.form.getlist(str(id)+"-inf_loc")
                mustdays = [integer(i) for i in request.form.get(str(id) + "-mustdays").split(",")]
                off_days = [integer(i) for i in request.form.get(str(id) + "-off_days").split(",")]
                on_days = [integer(i) for i in request.form.get(str(id) + "-on_days").split(",")]
                total_shifts = integer(request.form.get(str(id) + "-total_shifts"))
                vacation_days = [integer(i) for i in request.form.get(str(id) + "-vacation_days").split(",")]
                we_shifts = integer(request.form.get(str(id) + "-we_shifts"))
                print(friday_shifts, inf_loc, mustdays, off_days, on_days, total_shifts, vacation_days, we_shifts)
                new_drnobinfo = DrNobInfo(Crp=current_user.Crp, id=id, period="JUN2017", friday_shifts=friday_shifts,
                                          total_shifts=total_shifts, we_shifts=we_shifts,
                                          inf_loc=", ".join(str(x) for x in inf_loc),
                                          vacation_days=", ".join(str(x) for x in vacation_days),
                                          mustdays=", ".join(str(x) for x in mustdays),
                                          on_days=", ".join(str(x) for x in on_days),
                                          off_days=", ".join(str(x) for x in off_days))
                db.session.add(new_drnobinfo)
            db.session.commit()
        elif request.base_url.endswith("/dashboard/ayarlar"):
            places = ""
            for i in request.form:
                i = request.form.get(i)
                if i:
                    places = i + ", " + places
            places = places[:-2]
            print(places)
            places_entry = Crp.query.filter_by(Crp=current_user.Crp).first()
            places_entry.places = places
            db.session.commit()
    if page in ["gecmis", "yeninobet", "destek", "doktorlar", "ayarlar"]:
        DrList = User.query.filter_by(Crp=current_user.Crp).filter_by(type="dr").all()
        if page == "gecmis":
            return redirect('/dashboard/gecmis/JUN2017')
        if page == "yeninobet":
            return render_template("yeninobet.html", DrList=DrList, name=current_user.Name + " " + current_user.Surname,
                                   menu=menu["admin"])
        if page == "destek":
            return render_template("destek.html", name=current_user.Name+" "+current_user.Surname, menu=menu["admin"])
        if page == "doktorlar":
            return render_template("doktorlar.html", DrList=DrList, name=current_user.Name + " " + current_user.Surname,
                                   menu=menu["admin"])
        if page == "ayarlar":
            return render_template("ayarlar.html", name=current_user.Name + " " + current_user.Surname,
                                   menu=menu["admin"])


@app.route('/dashboard/gecmis/<period>')
@login_required
def history_period(period):
    period_schedule = DrNobet.query.filter_by(Crp=current_user.Crp).filter_by(period=period).all()
    if period_schedule:
        return render_template("gecmis.html", schedule=period_schedule,
                               name=current_user.Name + " " + current_user.Surname, menu=menu["admin"])
    else:
        return render_template("gecmis.html", message="No schedule info found for period of " + period,
                               name=current_user.Name + " " + current_user.Surname, menu=menu["admin"])


@app.route('/panel', methods=["POST", "GET"])
@login_required
#OWNER
def panel():
    if current_user.type != "owner":
        return redirect(url_for('login'))
    if request.method == "POST":
        for i in range(1, int(len(request.form)/6)):
            name = request.form.get("name"+str(i), "")
            surname = request.form.get("surname"+str(i), "")
            mail = request.form.get("mail"+str(i), "")
            crp = request.form.get("crp"+str(i), "")
            password = request.form.get("password" + str(i), "")
            latest_user_id = User.query.order_by(User.id.desc()).first().id
            latest_crp_id = User.query.order_by(User.Crp.desc()).first().Crp
            new_crp = Crp(Crp=latest_crp_id+1, Name=crp, adres="")
            new_user = User(Crp=latest_crp_id+1, id=latest_user_id+1, type="admin", Name=name, Surname=surname,
                            mail=mail, password=bcrypt.generate_password_hash(password))
            db.session.add(new_user)
            db.session.add(new_crp)
        db.session.commit()
        admin_list = User.query.filter_by(type="admin")
        return render_template("owner.html", message="Successfully created", liste=admin_list, title="Owner Page")
    adminlist = User.query.filter_by(type="admin")
    return render_template("owner.html", liste=adminlist, title="Owner Page")


@app.route('/profil', methods=["GET", "POST"])
#DR
@login_required
def profil():
    if current_user.type != "dr":
        return redirect(url_for('login'))
    if request.method == "POST":
        favorable_times = request.form["favorableTimes"].split(",")
        unfavorable_times = request.form["unfavorableTimes"].split(",")
        print(favorable_times, unfavorable_times)
    return render_template("dr.html", name=current_user.Name + " " + current_user.Surname,
                           menu=menu["dr"])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    current_user = ""
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()