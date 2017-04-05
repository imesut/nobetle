# from sqlalchemy import create_engine, Column, Integer, String, PrimaryKeyConstraint
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()

class User(Base):
    __tablename__ = "User"
    Crp = Column(Integer)
    id = Column(Integer, primary_key=True)
    type = Column(String)
    Name = Column(String)
    Surname = Column(String)
    mail = Column(String)
    password = Column(String)

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return "<User(name='%s', id='%s')>" % (self.Name, self.id)

class NobetleRun(Base):
    __tablename__ = "NobetleRun"
    Crp = Column(Integer, primary_key=True)
    period = Column(String, primary_key=True)
    run = Column(Integer, primary_key=True)
    score = Column(Integer)

    def __repr__(self):
        return "<NobetleRun(Crp='%s', period='%s', run='%s')>" % (self.Crp, self.period, self.run)

class DrNobInfo(Base):
    __tablename__ = "DrNobInfo"
    Crp = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True)
    period = Column(String, primary_key=True)
    FridayShifts = Column(Integer)
    TotalShifts = Column(Integer)
    WEShifts = Column(Integer)
    InfLoc = Column(String)
    OFFDays = Column(String)
    VacationDays = Column(String)
    MustDays = Column(String)

    def __repr__(self):
        return "<DrNobInfo(Crp='%s', id='%s', period='%s')>" % (self.Crp, self.id, self.period)

file = open("sqldb_is_running.txt", "w")
file.write(" ")
file.close()

class DrNobet(Base):
    __tablename__ = "DrNobet"
    Crp = Column(Integer, primary_key=True)
    period = Column(Integer, primary_key=True)
    run = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True)
    location = Column(Integer, primary_key=True)
    day = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<DrNobet(Crp='%s', period='%s', run='%s', id='%s', location='%s', day='%s')>" % (self.Crp, self.period, self.run, self.id, self.location, self.day)

# %s: user, password, host, database
engine = create_engine("mysql+mysqldb://%s:%s@%s/%s"%("root", "12345678", "localhost", "nobetle"), echo=False)

Session = sessionmaker(bind=engine)
session = Session()

def list_all(table):
    print(type(table))
    for i in session.query(table):
        print(i)

def new_log(table, **kwargs):
    new_log = table(**kwargs)
    session.add(new_log)
    session.commit()