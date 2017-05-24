from flask import Flask, render_template, url_for, request, g, flash, redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import schedule
from nobetle_helper import integer, nobetle_time, reverse_period, periods_nextto

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
      "url": "/dashboard/stats",
      "text": "İstatistikler"
    },
    "7": {
      "url": "/logout",
      "text": "Oturumu Kapat"
    }
  },
  "dr": {
      "1": {
          "url": "/profil/profil",
          "text": "Profil"
      },
      "2": {
          "url": "/profil/stats",
          "text": "İstatistikler"
      },
      "3": {
          "url": "/logout",
          "text": "Oturumu Kapat"
      }
  }
}

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
                period = nobetle_time(1)["period"]
                current_drnobinfo = DrNobInfo.query.filter_by(Crp=current_user.Crp).filter_by(period=period).filter_by(id=id).first()
                if current_drnobinfo:
                    current_drnobinfo.friday_shifts = friday_shifts
                    current_drnobinfo.total_shifts = total_shifts
                    current_drnobinfo.we_shifts = we_shifts
                    current_drnobinfo.inf_loc = ", ".join(str(x) for x in inf_loc)
                    current_drnobinfo.vacation_days = ", ".join(str(x) for x in vacation_days)
                    current_drnobinfo.mustdays = ", ".join(str(x) for x in mustdays)
                    current_drnobinfo.on_days = ", ".join(str(x) for x in on_days)
                    current_drnobinfo.off_days = ", ".join(str(x) for x in off_days)
                else:
                    new_drnobinfo = DrNobInfo(Crp=current_user.Crp, id=id, period=period,
                                              friday_shifts=friday_shifts,
                                              total_shifts=total_shifts,
                                              we_shifts=we_shifts,
                                              inf_loc=", ".join(str(x) for x in inf_loc),
                                              vacation_days=", ".join(str(x) for x in vacation_days),
                                              mustdays=", ".join(str(x) for x in mustdays),
                                              on_days=", ".join(str(x) for x in on_days),
                                              off_days=", ".join(str(x) for x in off_days))
                    db.session.add(new_drnobinfo)
            db.session.commit()
        elif request.base_url.endswith("/dashboard/ayarlar"):
            places = Crp.query.filter_by(Crp=current_user.Crp).first().places
            for i in range(1, int(len(request.form) / 2)):
                place = request.form.get("name" + str(i), "")
                critical = request.form.get("critical" + str(i), "")
                if i:
                    places = place+","+critical+";" + places
            if places[-2] == ";":
                places = places[:-2]
            places_entry = Crp.query.filter_by(Crp=current_user.Crp).first()
            places_entry.places = places
            db.session.commit()
    if page in ["gecmis", "yeninobet", "destek", "doktorlar", "ayarlar", "stats"]:
        if page == "gecmis":
            period = nobetle_time(1)["period"]
            return redirect('/dashboard/gecmis/'+ period)
        if page == "yeninobet":
            DrList = User.query.filter_by(Crp=current_user.Crp).filter_by(type="dr").all()
            places = []
            for i in Crp.query.filter_by(Crp=current_user.Crp).first().places.split(";"):
                places.append(i.split(","))
            nobinfo = DrNobInfo.query.filter_by(Crp=current_user.Crp).filter_by(period=nobetle_time(1)["period"]).all()
            total_shift = 0
            for i in nobinfo:
                total_shift += i.total_shifts
            if total_shift == nobetle_time(1)["day_number_in_month"]*len(places):
                return render_template("yeninobet.html", status="ready",
                                       name=current_user.Name + " " + current_user.Surname, menu=menu["admin"])
            else:
                return render_template("yeninobet.html", DrList=DrList, places=places, status="notready",
                                   name=current_user.Name + " " + current_user.Surname, menu=menu["admin"])
        if page == "destek":
            return render_template("destek.html", name=current_user.Name+" "+current_user.Surname, menu=menu["admin"])
        if page == "doktorlar":
            DrList = User.query.filter_by(Crp=current_user.Crp).filter_by(type="dr").all()
            return render_template("doktorlar.html", DrList=DrList, name=current_user.Name + " " + current_user.Surname,
                                   menu=menu["admin"])
        if page == "ayarlar":
            places = []
            for i in Crp.query.filter_by(Crp=current_user.Crp).first().places.split(";"):
                places.append(i.split(","))
            return render_template("ayarlar.html", places=places, name=current_user.Name + " " + current_user.Surname,
                                   menu=menu["admin"])
        if page == "stats":
            return stats("stats.html", menu["admin"])


@app.route('/dashboard/yeninobet/nobetle')
@login_required
def nobetle():
    if current_user.type != "admin":
        return redirect(url_for('login'))
    nobinfo = DrNobInfo.query.filter_by(Crp=current_user.Crp).filter_by(period=nobetle_time(1)["period"]).all()
    total_shift = 0
    for i in nobinfo:
        total_shift += i.total_shifts
    places = []
    for i in Crp.query.filter_by(Crp=current_user.Crp).first().places.split(";"):
        places.append(i.split(","))
    lp_time = nobetle_time(1)
    if total_shift == lp_time["day_number_in_month"] * len(places):
        result = schedule.optimization(dr=nobinfo, days_number=lp_time["day_number_in_month"],
                                       fridays=lp_time["friday_days"], weekends=lp_time["weekend_days"],
                                       locations=places)
        db.session.remove()
        for i in result["result"]:
            new_dr_nobet = DrNobet(Crp=str(current_user.Crp),
                                   period=lp_time["period"],
                                   id=str(result["result"][i]["doctor_id"]),
                                   location=str(result["result"][i]["location"]),
                                   day=str(result["result"][i]["day"]))
            db.session.add(new_dr_nobet)
        db.session.commit()
        new_schedule_stat = NobetleRun(Crp=current_user.Crp,
                                       period=lp_time["period"],
                                       run=1,
                                       objective=result["metadata"]["objective_value"],
                                       status=result["metadata"]["status"],
                                       calc_duration=result["metadata"]["calc_duration"])
        db.session.add(new_schedule_stat)
        db.session.commit()
        return redirect("/dashboard/gecmis")
    else:
        return redirect("/dashboard/yeninobet")


@app.route('/dashboard/gecmis/<period>')
@login_required
def history_period(period):
    if current_user.type != "admin":
        return redirect(url_for('login'))
    if period.endswith("-prev"):
        return redirect("/dashboard/gecmis/"+periods_nextto(period[:-5])["prev"])
    elif period.endswith("-next"):
        return redirect("/dashboard/gecmis/"+periods_nextto(period[:-5])["next"])
    period_schedule = DrNobet.query.filter_by(Crp=current_user.Crp).filter_by(period=period).all()
    DrList = User.query.filter_by(Crp=current_user.Crp).filter_by(type="dr").all()
    if period_schedule:
        return render_template("gecmis.html", period_numbers=reverse_period(period), schedule=period_schedule,
                               name=current_user.Name + " " + current_user.Surname,
                               link=request.path, menu=menu["admin"])
    else:
        return render_template("gecmis.html", message= period + " dönemi için kayıtlı bir nöbet çizelgesi bulunamadı.",
                               name=current_user.Name + " " + current_user.Surname, menu=menu["admin"])


@app.route('/stats')
@login_required
def stats(*args):
    period = nobetle_time(1)["period"]
    dr = DrNobet.query.filter_by(id=current_user.id)
    department = DrNobet.query.filter_by(Crp=current_user.Crp)
    period_dr_shift_number = len(dr.filter_by(period=period).all())
    period_department_shift_number = len(department.filter_by(period=period).all())
    doctor_number = len(User.query.filter_by(Crp=current_user.Crp).filter_by(type="dr").all())
    all_dr_shift_number = len(dr.all())
    all_department_shift_number = len(department.all())
    menu = ""
    if not args:
        page = "stats.html"
    else:
        for i in args:
            if str(i).endswith(".html"):
                page = str(i)
            else:
                menu = i
    return render_template(page, menu=menu,
                           pdrn=period_dr_shift_number,
                           pden=period_department_shift_number,
                           dn=doctor_number,
                           adrn=all_department_shift_number,
                           aden=all_dr_shift_number)


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


@app.route('/profil')
#DR
@login_required
def profil():
    return redirect("/profil/profil")


@app.route('/profil/<page>', methods=["POST", "GET"])
@login_required
def profil_page(page):
    if current_user.type != "dr":
        return redirect(url_for('login'))
    if request.method == "POST":
        if request.base_url.endswith("/profil/profil"):
            favorable_times = request.form["favorableTimes"].split(",")
            unfavorable_times = request.form["unfavorableTimes"].split(",")
    if page == "profil":
        return render_template("dr.html", name=current_user.Name + " " + current_user.Surname,
                           menu=menu["dr"])
    elif page == "stats":
        return stats("stats.html", menu["dr"])


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