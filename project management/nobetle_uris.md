#Nobetle URIs

##```/panel```
- **WHO** nobetle owner can log in
- **HOW** will be a single page
- **WHAT** new admin = new crp

##```/login```
- **WHO** admins and drs can log in
- **HOW** will be redirected to Login page
 - Form -> ```/dashboard```
- **WHAT** Password encrypted and submitted as ```POST```

##```/dashboard```
- **WHO** Who logged in and rediretcted from ```/login```
- **HOW** by checking;
	- _Login & session_ check
	- Check _user type_
 		- dr
 		- admin
- **WHAT** different rendered pages according to _user type_


###User: "admin" can do;
- Add/delete doctors
	- Warning message visible 
- Enter nobet numbers by next period
- Enter offdays, vacationdays, mustdays etc for next period.

###User: "dr" can do;
- Enter favorable time
- Enter unfavorable time
- View nobets

 