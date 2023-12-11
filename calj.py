#--------------------------------------------------------------
# IMPORTACION COMPONENTES
#--------------------------------------------------------------
from datetime import datetime, date, time, timedelta
import calendar
import sys
from colorama import Cursor, init, Fore, Back, Style
import sqlite3
import re


#--------------------------------------------------------------
# DECLARACION VARIABLES GLOBALES
#--------------------------------------------------------------
now = datetime.now()
#now= datetime.strptime('31/12/2020', '%d/%m/%Y')

months = ("Enero".center(20), "Febrero".center(20), "Marzo".center(20), "Abril".center(20), "Mayo".center(20), "Junio".center(20), "Julio".center(20), "Agosto".center(20), "Septiembre".center(20), "Octubre".center(20), "Noviembre".center(20), "Diciembre".center(20))
#days   = ("Do", "Lu", "Ma", "Mc", "Ju", "Vi", "Sa");




festivos = ["  "]; #inicializar lista de festivos


#--------------------------------------------------------------
# DECLARACION FUNCIONES
#--------------------------------------------------------------
def embellecedor(diaD):
	try:
		#diaD=diaD.replace("01", " 1")
		#diaD=diaD.replace("02", " 2")
		#diaD=diaD.replace("03", " 3")
		#diaD=diaD.replace("04", " 4")
		#diaD=diaD.replace("05", " 5")
		#diaD=diaD.replace("06", " 6")
		#diaD=diaD.replace("07", " 7")
		#diaD=diaD.replace("08", " 8")
		#diaD=diaD.replace("09", " 9")
		#diaD.zfill(2)
		# Utilizar una expresión regular para reemplazar '0' seguido de un dígito con ese dígito
		diaD= re.sub(r'0(\d)', r' \1', diaD)
	except: resp="  "
	return diaD

# FUNCION ANTERIOR REVISA ARCHIVO
#def isFestivus(diaD):
#	try:
#		resp="false"
#		for linea in festivos:
#			if linea.find(diaD) >= 0: 
#				resp="true"
#				break
#	except: resp="false"
#	return resp


# FUNCION NUEVA REVISA BASE DE DATOS
def isFestivus(diaD):
	resp="false"
	if (diaD!='  '):
		try:
			#print(diaD)
			cur = con.cursor()
			unsql ="select COUNT(FEST) from FESTIVUS WHERE FEST='"+diaD+"'"
			#print(unsql)
			cur.execute(unsql)
			
			unafecha = cur.fetchone()[0]
			if unafecha == 1:
				#print( unafecha )
				resp="true"
			else:
				resp="false"

		except: resp="false"
	

	return resp


def titles(ArrayMonths):
	title  = ''# 
	title2 = ''# 
	if len(ArrayMonths) == 1 :  # número de meses a pintar será 1 o 3; por ahora no se plantea otro
		dt1= ArrayMonths[0];
		month = months[dt1.month - 1]
		year = dt1.year
		#messsage = "{} {}".format(month, year)
		#longitud = len(messsage)
		#espacios = ' ' * int(10-(longitud/2))
		#messsage = "{}{} {}".format(espacios,month, year)
		messsage= month.strip() + ' ' +str(year);
		print ( Style.BRIGHT +Fore.GREEN + messsage.center(20)+ Style.RESET_ALL)
		title2 = title2+ "Do Lu Ma Mc Ju Vi Sa      "
		print(Style.BRIGHT +title2+ Style.RESET_ALL)
	else:		#entra por 3
		for M in ArrayMonths:
			title  = title + months[M.month - 1]+"      "			
			title2 = title2+ "Do Lu Ma Mc Ju Vi Sa      "
		print ( Style.BRIGHT +Fore.GREEN + title+ Style.RESET_ALL)
		print(Style.BRIGHT +title2+ Style.RESET_ALL)


	return ""

#las funciones para generar calendario anual:

def month_array(date):
	una_fecha = '01/'+ str(date.month)+'/'+ str(date.year)  
	fecha_dt = datetime.strptime(una_fecha, '%d/%m/%Y')
	primerdiames= fecha_dt.isoweekday() # where Monday(Lu) is 1 and Sunday(Do) is 7. For example, XX.isoweekday() == 2, a Wednesday.
	if primerdiames == 7:
		primerdiames = 1 # si resulta ser un domingo, para mi debe pasar a la linea 1
	else:
		primerdiames = primerdiames+1
	col = ["  "]#inicializar lista
	numerodeldia=1;
	monthRange = calendar.monthrange(date.year,date.month)
	for x in range(1,45): 
		col.append("  ")#agregar elemento vacio
		if primerdiames == x:
			#espacios= 2-len(str(numerodeldia))
			#if len(str(numerodeldia)) == 2: col[x]= str(numerodeldia) +'/'+ str(date.month)+'/'+ str(date.year)  #str(numerodeldia)
			#else: col[x]= ' ' + str(numerodeldia) +'/'+ str(date.month)+'/'+ str(date.year)#str(numerodeldia)
			col[x]= str(numerodeldia).zfill(2)+'/'+str(date.month).zfill(2)+'/'+ str(date.year)
			numerodeldia=numerodeldia+1
		else:
			if col[x-1]=="  ":
				col[x]="  "
			else:
				#espacios= 2-len(str(numerodeldia))
				#if len(str(numerodeldia)) == 2: col[x]=  str(numerodeldia) +'/'+ str(date.month)+'/'+ str(date.year)#str(numerodeldia)
				#else: col[x] = ' ' +  str(numerodeldia) +'/'+ str(date.month)+'/'+ str(date.year)#str(numerodeldia)			   
				col[x]= str(numerodeldia).zfill(2)+'/'+str(date.month).zfill(2)+'/'+ str(date.year)
				#print(col[x])
				#print(len(str(numerodeldia)))
				if numerodeldia <= monthRange[1]: numerodeldia = numerodeldia + 1
				else: col[x]= '  '
	#print(col)
	n = 6 #semanas
	m = 7 #dias
	a = []	
	for i in range(n):
		a.append(["  "] * m)
	nn=0
	for y in range (1,7):
		a[nn] = col[(7*y-6)] ,col[(7*y-5)], col[(7*y-4)], col[(7*y-3)], col[(7*y-2)], col[(7*y-1)], col[7*y] 
		nn=nn+1
	return a

def printByLine(ArrayMonths):
	mespintar    = []#inicializar lista
	#semanapintar = []
	week = []
	#w = ''
	for M in ArrayMonths:
		mespintar.append ( month_array(M))#
		#t1=str(M)
		#t1=t1[0:10]
		#print (mespintar)
	for N in mespintar:
		#print (N)
		for y in range (6):
			#print( y )
			m1separador0=Fore.RED + Style.BRIGHT
			m1separador1=Style.RESET_ALL
			m1separador2="";
			m1separador3="";
			m1separador4="";
			m1separador5="";
			m1separador6="";
			m1separador7="";
			#Buscar festivo en cada columna que no sea domingo MES1:

			if( isFestivus(N[y][1])=="true"):
				m1separador1=Fore.RED + Style.BRIGHT 
				m1separador2=Style.RESET_ALL 

			if( isFestivus(N[y][2])=="true"):
				m1separador2=Fore.RED + Style.BRIGHT 
				m1separador3=Style.RESET_ALL 
				
			if( isFestivus(N[y][3])=="true"):
				m1separador3=Fore.RED + Style.BRIGHT 
				m1separador4=Style.RESET_ALL 
				
			if( isFestivus(N[y][4])=="true"):
				m1separador4=Fore.RED + Style.BRIGHT 
				m1separador5=Style.RESET_ALL 
				
			if( isFestivus(N[y][5])=="true"):
				m1separador5=Fore.RED + Style.BRIGHT 
				m1separador6=Style.RESET_ALL 
				
			if( isFestivus(N[y][6])=="true"):
				m1separador6=Fore.RED + Style.BRIGHT 
				m1separador7=Style.RESET_ALL 		
				
			dayint = now.day
			monthint=now.month
			monthstr=str(monthint).zfill(2)
			#monthlen=len(monthstr)
			yearstr=str(now.year)
			#print(monthstr)

		
			daystr=str(dayint).zfill(2)
			#if len(str(dayint)) == 2:
			#else: daystr=' ' +str(dayint) 
			
			#print(N[y])
			if N[y][0][0:2] == daystr and  N[y][0][3:5]==monthstr and N[y][0][6:10]==yearstr : 
				m1separador0=Fore.BLUE + Style.BRIGHT
				m1separador1=Style.RESET_ALL 
			if N[y][1][0:2] == daystr and  N[y][1][3:5]==monthstr and N[y][1][6:10]==yearstr : 
				m1separador1=Fore.BLUE + Style.BRIGHT 
				m1separador2=Style.RESET_ALL 
			if N[y][2][0:2] == daystr and  N[y][2][3:5]==monthstr and N[y][2][6:10]==yearstr : 
				m1separador2=Fore.BLUE + Style.BRIGHT 
				m1separador3=Style.RESET_ALL 
			if N[y][3][0:2] == daystr and  N[y][3][3:5]==monthstr and N[y][3][6:10]==yearstr : 
				m1separador3=Fore.BLUE + Style.BRIGHT 
				m1separador4=Style.RESET_ALL 
			if N[y][4][0:2] == daystr and  N[y][4][3:5]==monthstr and N[y][4][6:10]==yearstr : 
				m1separador4=Fore.BLUE + Style.BRIGHT 
				m1separador5=Style.RESET_ALL 
			if N[y][5][0:2] == daystr and  N[y][5][3:5]==monthstr and N[y][5][6:10]==yearstr : 			
				m1separador5=Fore.BLUE + Style.BRIGHT 
				m1separador6=Style.RESET_ALL
			if N[y][6][0:2] == daystr and  N[y][6][3:5]==monthstr and N[y][6][6:10]==yearstr : 
				m1separador6=Fore.BLUE + Style.BRIGHT 
				m1separador7=Style.RESET_ALL
			
			week.append("")
			week[y] = week[y]+m1separador0+embellecedor(N[y][0][0:2])+m1separador1  +" " +embellecedor(N[y][1][0:2])+m1separador2 +" " + embellecedor(N[y][2][0:2])+m1separador3 +" " + embellecedor(N[y][3][0:2])+m1separador4 +" " + embellecedor(N[y][4][0:2])+m1separador5 +" " + embellecedor(N[y][5][0:2])+m1separador6 +" " + embellecedor(N[y][6][0:2])+m1separador7 +"      "
		
	for O in week:
		if(O!=""):print (O)
	 		
	return ""	
	
def calj_month(ArrayMonths):
	titles(ArrayMonths)
	printByLine(ArrayMonths)
	
	return ""

	
	
def calj_year(year):
	print()
	print(Style.BRIGHT +Fore.RED + year.center(72)+ Style.RESET_ALL)
	print()
	
	#inicializar lista de fechas a pintar, enviando por trimestre
	t1 = [	datetime.strptime('01/01/'+ year   , '%d/%m/%Y'),	datetime.strptime('01/02/'+ year   , '%d/%m/%Y'),	datetime.strptime('01/03/'+ year   , '%d/%m/%Y'),	];	
	t2 = [	datetime.strptime('01/04/'+ year   , '%d/%m/%Y'),	datetime.strptime('01/05/'+ year   , '%d/%m/%Y'),	datetime.strptime('01/06/'+ year   , '%d/%m/%Y')	];
	t3 = [	datetime.strptime('01/07/'+ year   , '%d/%m/%Y'),	datetime.strptime('01/08/'+ year   , '%d/%m/%Y'),	datetime.strptime('01/09/'+ year   , '%d/%m/%Y')	];
	t4 = [	datetime.strptime('01/10/'+ year   , '%d/%m/%Y'),	datetime.strptime('01/11/'+ year   , '%d/%m/%Y'),	datetime.strptime('01/12/'+ year   , '%d/%m/%Y')	];
	
	calj_month(t1)
	calj_month(t2)
	calj_month(t3)
	calj_month(t4)
	
	return ""
	
#--------------------------------------------------------------
# INICIO DEL PROGRAMA
#--------------------------------------------------------------


init() # inicio COLORAMA, para colores en consola
# sigue: cargar archivo de festivos, lo cargo una vez y lo envío a una lista global 
#try:
#	#f = open ('C:/festivus/festivus.ini','r')
#	f = open ('./festivus.ini','r')
#	i=0;
#	for linea in f:
#		festivos[i]=linea
#		festivos.append("  ")#agregar elemento vacio
#		i=i+1
#	#print(festivos)
#	f.close()
#except: 
#	festivos = ["  "]# si no hay archivo, se envía vacio.


try:
	#con = sqlite3.connect("C:/festivus/Festivus.db")	 # antes
	con = sqlite3.connect("D:/dist/Festivus.db")
except: 
	festivos = ["  "]

if len(sys.argv) == 1:
	datess = [now]; #inicializar lista de fechas a pintar, enviando mes actual
	calj_month(datess) # se interpreta como mes actual.
elif len(sys.argv) == 2:
	if sys.argv[1]=="-3":
		datess = [
		now - timedelta(days=30),
		now,
		now + timedelta(days=30)];
		#inicializar lista de fechas a pintar, enviando mes trimestre
		calj_month(datess) # se interpreta como trimestre,
	else: 
		calj_year(sys.argv[1]) #se interpreta como año
else:
	print ("ERROR: Introdujo uno (1) o más de dos (2) argumentos")

	
	
#para compilar y probar se usa:
#C:\Users\JAC\AppData\Local\Programs\Python\Python311\python D:\dist\calj.py
#
#para volverlo ejecutable:
#pyinstaller :
#C:\Users\JAC\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller --onefile D:\dist\calj.py

# si jode por:   ImportError: No module named _bootlocale
# usar:
# pyinstaller --exclude-module _bootlocale --onefile  calj.py
