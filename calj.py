#--------------------------------------------------------------
# IMPORTACION COMPONENTES
#--------------------------------------------------------------
import calendar
#import sqlite3 #ya no se requiere base de datos, se calculan los festivos
import sys
from datetime import datetime, timedelta, date
from colorama import Cursor, init, Fore, Style


#--------------------------------------------------------------
# DECLARACION VARIABLES GLOBALES
#--------------------------------------------------------------
now = datetime.now()
months = [month.center(20) for month in ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")]
festivos = set()  # Inicializar conjunto de festivos



#--------------------------------------------------------------
# DECLARACION FUNCIONES
#--------------------------------------------------------------
def resaltar_dia(diaD):
    hoy = datetime.today().date()
    separador = [Style.RESET_ALL] * 2 # llenar con limpieza de estilo
    try:
        fecha_dt = datetime.strptime(diaD, '%d/%m/%Y')
        #if isFestivus(diaD) == "true" or fecha_dt.weekday() == 6  : separador[0] = Fore.RED + Style.BRIGHT #Buscar festivo o domingo para ponerlo ROJO:
        if isFestivus(diaD) == True or fecha_dt.weekday() == 6  : separador[0] = Fore.RED + Style.BRIGHT #Buscar festivo o domingo para ponerlo ROJO:
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
#def isFestivus(diaD):
#    resp="false"
#    if (diaD!='  '):
#        try:
#            #print(diaD)
#            cur = con.cursor()
#            unsql ="select COUNT(FEST) from FESTIVUS WHERE FEST='"+diaD+"'"
#            #print(unsql)
#            cur.execute(unsql)
#            
#            unafecha = cur.fetchone()[0]
#            if unafecha == 1:
#                #print( unafecha )
#                resp="true"
#            else:
#                resp="false"
#
#        except: resp="false"
    

#    return resp
# FUNCION NUEVA calcula los festivos
def isFestivus(diaD):
    #print(diaD)
    fecha_obj = datetime.strptime(diaD, "%d/%m/%Y")
    fecha_dt =date(fecha_obj.year,fecha_obj.month,fecha_obj.day)
    #return fecha_dt in obtener_festivos_colombia(fecha_dt.year)    
    #print(f"¿{fecha_dt} está en festivos? {'Sí' if fecha_dt in festivos else 'No'}")
    #print(fecha_dt in festivos)

    return fecha_dt in festivos


def calcular_pascua(anio):
    a = anio % 19
    b = anio // 100
    c = anio % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(anio, mes, dia)

def siguiente_lunes(fecha):
    return fecha + timedelta(days=(7 - fecha.weekday()) % 7)


def obtener_festivos_colombia(anio):
    global festivos
    #print(anio)
    pascua = calcular_pascua(anio)

    festivos = {
        date(anio, 1, 1),    # Año Nuevo
        date(anio, 5, 1),    # Día del Trabajo
     date(anio, 7, 20),   # Independencia
        date(anio, 8, 7),    # Batalla de Boyacá
        date(anio, 12, 8),   # Inmaculada Concepción
        date(anio, 12, 25),  # Navidad
    } 
     

    trasladables = [
        date(anio, 1, 6),    # Reyes Magos
        date(anio, 3, 19),   # San José
        date(anio, 6, 29),   # San Pedro y San Pablo
        date(anio, 8, 15),   # Asunción de la Virgen
        date(anio, 10, 12),  # Día de la Raza
        date(anio, 11, 1),   # Todos los Santos
        date(anio, 11, 11),  # Independencia de Cartagena
    ]
    festivos.update(siguiente_lunes(f) for f in trasladables)

    festivos.update({
        pascua - timedelta(days=3),   # Jueves Santo
        pascua - timedelta(days=2),   # Viernes Santo
    })

    trasladables_religiosos = [
        pascua + timedelta(days=43),  # Ascensión del Señor
        pascua + timedelta(days=64),  # Corpus Christi
        pascua + timedelta(days=71),  # Sagrado Corazón
    ]
    festivos.update(siguiente_lunes(f) for f in trasladables_religiosos)
    #print(festivos)
    # return eliminado, ahora se actualiza la variable global







########################################################
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
 
#try:
    #con = sqlite3.connect("C:/dist/Festivus.db")     # antes
    #con = sqlite3.connect("D:/dist/Festivus.db")
    #festivos=obtener_festivos_colombia(now.year)
    #print( festivos)
#except: 
   #festivos = set()
 


if len(sys.argv) == 1:
    obtener_festivos_colombia(now.year)
    calj_month([now])
elif len(sys.argv) == 2:
    if sys.argv[1] == "-3":
        obtener_festivos_colombia((now - timedelta(days=30)).year)
        obtener_festivos_colombia((now.year))
        obtener_festivos_colombia((now + timedelta(days=30)).year)
        calj_month([now - timedelta(days=30), now, now + timedelta(days=30)])
    else:
        obtener_festivos_colombia(datetime.strptime(f'01/01/{sys.argv[1]}', '%d/%m/%Y').year)
        calj_year(sys.argv[1])
        
        input()  # Espera a que el usuario presione Enter
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
