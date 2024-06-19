#--------------------------------------------------------------
# IMPORTACION COMPONENTES
#--------------------------------------------------------------
import calendar
import sqlite3
import sys
from datetime import datetime, timedelta
from colorama import Cursor, init, Fore, Style


#--------------------------------------------------------------
# DECLARACION VARIABLES GLOBALES
#--------------------------------------------------------------
now = datetime.now()
months = [month.center(20) for month in ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")]
festivos = ["  "]  # Inicializar lista de festivos



#--------------------------------------------------------------
# DECLARACION FUNCIONES
#--------------------------------------------------------------
def resaltar_dia(diaD):
    hoy = datetime.today().date()
    separador = [Style.RESET_ALL] * 2 # llenar con limpieza de estilo
    try:
        fecha_dt = datetime.strptime(diaD, '%d/%m/%Y')
        if isFestivus(diaD) == "true" or fecha_dt.weekday() == 6  : separador[0] = Fore.RED + Style.BRIGHT #Buscar festivo o domingo para ponerlo ROJO:
        if fecha_dt.date() == hoy  : separador[0] = Fore.BLUE + Style.BRIGHT # Buscar dia de hoy para pintarlo de azul
        #diaD = re.sub(r'0(\d)', r' \1', diaD[:2]) # reemplazo por patrón para que no quede 00 01 02 
        diaRs = str(fecha_dt.day).rjust(2) # justificado a la derecha
    except:
        diaRs = "  "
    return separador[0] + diaRs + separador[1]

# FUNCION ANTERIOR REVISA ARCHIVO
#def isFestivus(diaD):
#    try:
#        resp="false"
#        for linea in festivos:
#            if linea.find(diaD) >= 0: 
#                resp="true"
#                break
#    except: resp="false"
#    return resp


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
    title = '' 
    if len(ArrayMonths) == 1 : 
        dt1= ArrayMonths[0]
        month = months[dt1.month - 1]
        year = dt1.year
        title=month.strip() + ' ' +str(year)
    else :
        title = ''.join([months[dt.month - 1] + '      ' for dt in ArrayMonths])

    title2 = "Do Lu Ma Mc Ju Vi Sa      " * len(ArrayMonths)
    print(Style.BRIGHT + Fore.GREEN + title.center(20) + Style.RESET_ALL)
    print(Style.BRIGHT + title2 + Style.RESET_ALL)

 

#las funciones para generar calendario anual:

def month_array(date):
    fecha_dt = datetime.strptime(f'01/{date.month}/{date.year}', '%d/%m/%Y')
    primerdiames = (fecha_dt.isoweekday() % 7) + 1  # Convert Sunday from 7 to 1
    month_range = calendar.monthrange(date.year, date.month)[1]

    col = ["  "] * 44
    numerodeldia = 1

    for x in range(primerdiames, primerdiames + month_range):
        col[x] = f'{str(numerodeldia).zfill(2)}/{str(date.month).zfill(2)}/{date.year}'
        numerodeldia += 1

    a = [["  "] * 7 for _ in range(6)]
    for i in range(6):
        a[i] = col[(7 * i + 1):(7 * i + 8)]
    return a
  

def printByLine(ArrayMonths):
    mespintar = [month_array(M) for M in ArrayMonths]
    week = []
     
    for N in mespintar:
        #print (N)
        for y in range (6):
            week.append("")
            week[y] = week[y]+resaltar_dia(N[y][0]) +" " +resaltar_dia(N[y][1])+" " + resaltar_dia(N[y][2])+" " + resaltar_dia(N[y][3]) +" " + resaltar_dia(N[y][4]) +" " + resaltar_dia(N[y][5]) +" " + resaltar_dia(N[y][6]) +"      "
        
    for O in week:
        if(O!=""):print (O)
             
    return ""    
    
def calj_month(ArrayMonths):
    titles(ArrayMonths)
    printByLine(ArrayMonths)

def calj_year(year):
    print(f"\n{Style.BRIGHT + Fore.RED + year.center(72) + Style.RESET_ALL}\n")
    for t in range(1, 13, 3):
        calj_month([datetime.strptime(f'01/{m}/{year}', '%d/%m/%Y') for m in range(t, t + 3)])

    
#--------------------------------------------------------------
# INICIO DEL PROGRAMA
#--------------------------------------------------------------


init() # inicio COLORAMA, para colores en consola
 
try:
    #con = sqlite3.connect("C:/festivus/Festivus.db")     # antes
    con = sqlite3.connect("D:/dist/Festivus.db")
except: 
    festivos = ["  "]
 


if len(sys.argv) == 1:
    calj_month([now])
elif len(sys.argv) == 2:
    if sys.argv[1] == "-3":
        calj_month([now - timedelta(days=30), now, now + timedelta(days=30)])
    else:
        calj_year(sys.argv[1])
else:
    print("ERROR: Introdujo uno (1) o más de dos (2) argumentos")


    
    
#para compilar y probar se usa:
#C:\Users\JAC\AppData\Local\Programs\Python\Python311\python D:\dist\calj.py
#
#para volverlo ejecutable:
#pyinstaller :
#C:\Users\JAC\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller --onefile D:\dist\calj.py

# si jode por:   ImportError: No module named _bootlocale
# usar:
# pyinstaller --exclude-module _bootlocale --onefile  calj.py
