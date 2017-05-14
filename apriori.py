class info():
    def __init__(self, id, name, surname, friday_shifts, total_shifts, we_shifts, inf_loc, vacation_days, mustdays, on_days, off_days):
        self.id = id
        self.name = name
        self.surname = surname
        self.friday_shifts = friday_shifts
        self.total_shifts = total_shifts
        self.we_shifts = we_shifts
        self.inf_loc = inf_loc
        self.vacation_days = vacation_days
        self.mustdays = mustdays
        self.on_days = on_days
        self.off_days = off_days

    def __repr__(self):
        return "<info(id='%s', name='%s')>" % (self.id, self.name)

"""
Dr = [info(id=1000, name="Mesut", surname="Yılmaz", friday_shifts=0, total_shifts=5, we_shifts=3, inf_loc=['ICU1', "ICU2"], vacation_days=[4, 5, 6, 25], mustdays=[26, 29]),
      info(id=1001, name="Oğulcan", surname="Yılmaz", friday_shifts=0, total_shifts=5, we_shifts=3, inf_loc=['ICU1'], vacation_days=[4, 5, 6, 25], mustdays=[26, 29]),
      info(id=1002, name="Mehmet", surname="Yılmaz", friday_shifts=0, total_shifts=5, we_shifts=3, inf_loc=['ICU1', "ICU2"], vacation_days=[4, 5, 6, 25], mustdays=[26, 29])
      ]


for i in Dr:
    for j in i.inf_loc:
        print(j)
"""
