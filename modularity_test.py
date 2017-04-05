from sqldb import *
from doktorcizelgele import solve

#solve()


"""
Functions
---------
list_all(table)
new_log(table, **kwargs)
"""

#list_all(User)

"""
List_all from: NobetleRun, DrNobet, DrNobInfo, User
list_all(NobetleRun)
"""

"""
new_log(User,
        Crp = 10000,
        id=123,
        type = "Dr",
        Name = "ali",
        Surname = "sism",
        mail = "alisism@mail.com",
        password = "1234566543211234")

new_log(NobetleRun,
        Crp = 10000,
        period="APR2017",
        run = 1000,
        score = 5700)

new_log(DrNobInfo,
        Crp = 100,
        id=100,
        period="APR2017",
        FridayShifts = 5,
        TotalShifts = 50,
        WEShifts = 10,
        InfLoc="Loc1",
        OFFDays = "1, 3, 5",
        VacationDays = "5, 7, 9, 11",
        MustDays = "10, 13, 17")
"""