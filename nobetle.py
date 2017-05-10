from flask import Flask, render_template, url_for, request, g, flash, redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

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

    def __init__(self, Crp, Name, adres):
        self.Crp = Crp
        self.Name = Name
        self.adres = adres

    def __repr__(self):
        return "<Crp(Name='%s', Crp='%s')>" % (self.Name, self.Crp)


class NobetleRun(db.Model):
    __tablename__ = "NobetleRun"
    Crp = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(), primary_key=True)
    run = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)

    def __init__(self, Crp, period, run, score):
        self.Crp = Crp
        self.period = period
        self.run = run
        self.score = score

    def __repr__(self):
        return "<NobetleRun(Crp='%s', period='%s', run='%s')>" % (self.Crp, self.period, self.run)


class DrNobInfo(db.Model):
    __tablename__ = "DrNobInfo"
    Crp = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(), primary_key=True)
    FridayShifts = db.Column(db.Integer)
    TotalShifts = db.Column(db.Integer)
    WEShifts = db.Column(db.Integer)
    InfLoc = db.Column(db.String())
    OFFDays = db.Column(db.String())
    VacationDays = db.Column(db.String())
    MustDays = db.Column(db.String())

    def __init__(self, Crp, id, period, score, FridayShifts, TotalShifts, WEShifts, InfLoc, OFFDays, VacationDays, MustDays):
        self.Crp = Crp
        self.id = id
        self.period = period
        self.FridayShifts = FridayShifts
        self.TotalShifts = TotalShifts
        self.WEShifts = WEShifts
        self.InfLoc = InfLoc
        self.OFFDays = OFFDays
        self.VacationDays = VacationDays
        self.MustDays = MustDays

    def __repr__(self):
        return "<DrNobInfo(Crp='%s', id='%s', period='%s')>" % (self.Crp, self.id, self.period)


class DrNobet(db.Model):
    __tablename__ = "DrNobet"
    Crp = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(), primary_key=True)
    run = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(), primary_key=True)
    day = db.Column(db.Integer, primary_key=True)

    def __init__(self, Crp, period, run, id, location, day):
        self.Crp = Crp
        self.period = period
        self.run = run
        self.id = id
        self.location = location
        self.day = day

    def __repr__(self):
        return "<DrNobet(Crp='%s', period='%s', run='%s', id='%s', location='%s', day='%s')>" % (self.Crp, self.period, self.run, self.id, self.location, self.day)


@app.errorhandler(404)
def not_found(error):
    return "404"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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
                print(l_user.type)
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
    print(current_user.type)
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
    if page in ["gecmis", "yeninobet", "destek", "doktorlar"]:
        DrList = User.query.filter_by(Crp=current_user.Crp).filter_by(type="dr").all()
        return render_template(page+".html", DrList=DrList, name=current_user.Name + " " + current_user.Surname, menu={"1": {"url": "/dashboard/doktorlar", "text":"Doktorlar"},
                                                   "2": {"url": "/dashboard/gecmis", "text": "Geçmiş"},
                                                   "3": {"url": "/dashboard/yeninobet", "text": "Yeni Nöbet"},
                                                   "4": {"url": "/dashboard/destek", "text": "Destek"},
                                                   "5": {"url": "/logout", "text": "Oturumu Kapat"}})


@app.route('/panel', methods=["POST", "GET"])
@login_required
#OWNER
def panel():
    if current_user.type != "owner":
        return redirect(url_for('login'))
    if request.method == "POST":
        for i in range(1,int(len(request.form)/5)):
            name = request.form.get("name"+str(i), "")
            surname = request.form.get("surname"+str(i), "")
            mail = request.form.get("mail"+str(i), "")
            crp = request.form.get("crp"+str(i), "")
            password = request.form.get("password" + str(i), "")
            latest_user_id = User.query.order_by(User.id.desc()).first().id
            latest_crp_id = User.query.order_by(User.Crp.desc()).first().Crp
            new_crp = Crp(Crp=latest_crp_id+1, Name=crp, adres="")
            new_user = User(Crp=latest_crp_id+1, id=latest_user_id+1, type="admin", Name=name, Surname=surname, mail=mail, password=bcrypt.generate_password_hash(password))
            db.session.add(new_user)
            db.session.add(new_crp)
        db.session.commit()
        AdminList = User.query.all()
        return render_template("owner.html", message="Successfully created", liste=AdminList, title="Owner Page")
    adminlist = User.query.all()
    return render_template("owner.html", liste=adminlist, title="Owner Page")


@app.route('/profil')
#DR
@login_required
def profil():
    if current_user.type != "dr":
        return redirect(url_for('login'))
    return render_template("dr.html", name=current_user.Name + " " + current_user.Surname,
                           menu={"1": {"url": "#", "text": "Öge1"},
                                 "2": {"url": "/logout", "text": "Oturumu Kapat"}}
                           )


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