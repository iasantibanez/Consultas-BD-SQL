# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 04:45:13 2018

@author: ivans
"""

import pandas as pd 
import sqlite3 
import datetime as dt

csv_app=pd.read_csv("googleplaystore.csv")  #10841 datos
csv_reviews=pd.read_csv("googleplaystore_user_reviews.csv") 

#csv filtrada de cualquier fila con al menos un valor NaN
# el csv de app
csv_app_f = csv_app.dropna(axis=0)  
csv_app_f = csv_app_f.reset_index(drop=True)   #9360 datos
#el csv de reviews
csv_app_reviews = csv_reviews.dropna(axis=0)
csv_app_reviews = csv_app_reviews.reset_index(drop=True) #37427

    
#nombre de las columnas
columna=[]
columna2=[]
for i in csv_app_f:
    columna.append(i)
for j in csv_app_reviews:
    columna2.append(j)
#N°TOTAL INDICES(FILAS)
N_filas=len(csv_app_f.index)
N_filas_reviews=len(csv_app_reviews.index)

#print(set(csv_app_f[columna[1]])) # categorias
#print(set(csv_app_f[columna[9]])) # generos
categorias=list(set(csv_app_f[columna[1]]))
a=set(csv_app_f[columna[9]])
generos=[]
aux=[]
for i in a:
    #print(i.split(";"))
    a=i.split(";")
    for k in a:
        aux.append(k)
generos=list(set(aux))

# creo dicc pa linkear los reviews despues
d_app={}
for i in range(N_filas):
    d_app[csv_app_f[columna[0]][i]]=i+1


##SQL
##---conectar a la base de datos---
conexion = sqlite3.connect("bd_app.sqlite3")
#seleccionar el cursor para realizar consulta
consulta = conexion.cursor()



#primera tabla de info_apps
tabla_apps="""
CREATE TABLE IF NOT EXISTS aplicaciones(id_App INTEGER PRIMARY KEY AUTOINCREMENT,
App VARCHAR(30),
Rating FLOAT,
Reviews INTERGER,
Size FLOAT,
Installs INTERGER,
Type VARCHAR(30),
Price FLOAT,
Content_Rating VARCHAR(30),
Last_update DATE,
Current_Ver VARCHAR(30),
Android_Ver VARCHAR(30))"""

if (consulta.execute(tabla_apps)): pass #print("Tabla creada con éxito")
else: print("ha ocurrido un error al crear la tabla")

#2da tabla de reviews.
tabla_reviews="""
CREATE TABLE IF NOT EXISTS reviews(
id_review INTEGER PRIMARY KEY AUTOINCREMENT,
Translated_Review VARCHAR(50),
Sentiment VARCHAR(30),
Sentiment_Polarity FLOAT,
Sentiment_subjetivity FLOAT)"""

if (consulta.execute(tabla_reviews)): pass #print("Tabla creada con éxito")
else: print("ha ocurrido un error al crear la tabla")


tabla_categorias="""
CREATE TABLE IF NOT EXISTS categorias(
id_Cat INTEGER PRIMARY KEY,
Category VARCHAR(30))"""

if (consulta.execute(tabla_categorias)): pass #print("Tabla creada con éxito")
else: print("ha ocurrido un error al crear la tabla")

tabla_generos="""
CREATE TABLE IF NOT EXISTS generos(
id_Gen INTEGER PRIMARY KEY,
Genre VARCHAR(30))"""

if (consulta.execute(tabla_generos)): pass #print("Tabla creada con éxito")
else: print("ha ocurrido un error al crear la tabla")

#-------- TABLAS AUXILIARES-------------------------------

tabla_AppGen="""
CREATE TABLE IF NOT EXISTS aux_AppGen(
id_App INTEGER,
id_Gen VARCHAR(30),
FOREIGN KEY (id_App) REFERENCES aplicaciones,
FOREIGN KEY (id_Gen) REFERENCES generos)"""
if (consulta.execute(tabla_AppGen)):  pass #print("Tabla auxiliar creada con éxito")
else: print("ha ocurrido un error al crear la tabla")
        
tabla_AppCat="""
CREATE TABLE IF NOT EXISTS aux_AppCat(
id_App INTEGER,
id_Cat VARCHAR(30),
FOREIGN KEY (id_App) REFERENCES aplicaciones,
FOREIGN KEY (id_Cat) REFERENCES categorias)"""
if (consulta.execute(tabla_AppCat)): pass #print("Tabla auxiliar creada con éxito")
else: print("ha ocurrido un error al crear la tabla")
        
tabla_AppRev="""
CREATE TABLE IF NOT EXISTS aux_AppRev(
id_App INTEGER,
id_review VARCHAR(30),
FOREIGN KEY (id_App) REFERENCES aplicaciones,
FOREIGN KEY (id_review) REFERENCES reviews)"""
if (consulta.execute(tabla_AppRev)): pass #print("Tabla auxiliar creada con éxito")
else: print("ha ocurrido un error al crear la tabla")
        

consulta.close()
conexion.close()


#-----------------PLANTILLAS PARA INSERT DATOS---------------------------------
conexion = sqlite3.connect("bd_app.sqlite3")
consulta = conexion.cursor()

sql_table_app="""
INSERT INTO aplicaciones(App, Rating, Reviews, Size, Installs, Type, Price,
Content_Rating, Last_update, Current_ver, Android_Ver)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, date(?), ?, ?)
"""

sql_table_reviews="""
INSERT INTO reviews(Translated_Review, Sentiment,
Sentiment_Polarity, Sentiment_subjetivity)
VALUES (? ,?, ?, ?)
"""
        

sql_table_categorias="""
INSERT INTO categorias(id_Cat, Category)
VALUES (?,?)
"""


sql_table_generos="""
INSERT INTO generos(id_Gen, Genre)
VALUES (?,?)
"""

# INSERT TABLAS AUXILIARES

sql_table_aux_app_category="""
INSERT INTO aux_AppCat(id_App, id_Cat)
VALUES (?,?)
"""

sql_table_aux_app_reviews="""
INSERT INTO aux_AppRev(id_App, id_review)
VALUES (?,?)
"""
sql_table_aux_app_genre="""
INSERT INTO aux_AppGen(id_App, id_Gen)
VALUES (?,?)
"""

def add_to_sql(base,argumentos):
    #realizar consulta
    if (consulta.execute(base,argumentos)):
        pass
        return True
    else: 
        print("ha ocurrido un error al guardar registro")
        return False
    
#print(csv_app_f[columna[7]][1])
#a = csv_app_f[columna[4]][1]
#print(a)
#if 'M' in a:
 #   print("hola")
 #   #a.remove('M')
#    b=a.replace("M","")
#print(a)
#print(b)

def date_transform(date):
    dic_month = { 'January': 1, 'February' : 2, 'March' : 3, 'April': 4, 'May' : 5, 'June' : 6, 'July' : 7, 'August' : 8, 'September' :  9, 'October' : 10, 'November' : 11, 'December': 12  }
    a=date.replace(",","")
    b=a.split(" ")
    #return str(b[2])+'-'+str(dic_month[b[0]])+"-"+str(b[1])
    return dt.date(int(b[2]),int(dic_month[b[0]]),int(b[1]))
#print(date_transform(csv_app_f[columna[10]][1]))
    
#_----------------------------------POBLAR TABLAS-----------------
#agrego datos a la tabla_aplicaciones
def poblar():
    a=0
    for i in range(N_filas): #App, Rating, Reviews, Size, Installs, Type, Price,Content_Rating, Last_update, Current_ver, Android_Ver)
        #SIZE XXM to XX (MB)
        if 'M' in csv_app_f[columna[4]][i]:
            aux1=csv_app_f[columna[4]][i].replace("M","")
        else:
            aux1=csv_app_f[columna[4]][i] 
        if 'k' in aux1:
            aux1=float(aux1.replace("k",""))/1000
        #PRICE $XX to XX ($)
        if '$' in csv_app_f[columna[7]][i]:
            aux2=csv_app_f[columna[7]][i].replace("$","")
        else:
            aux2=csv_app_f[columna[7]][i]
        #installs to XX+ to xx
        if '+' in csv_app_f[columna[5]][i]:
            aux3=csv_app_f[columna[5]][i].replace("+","")
            aux3=aux3.replace(",","")
        else:
            aux3=csv_app_f[columna[5]][i]
            aux3=aux3.replace(",","")
        
        date=date_transform(csv_app_f[columna[10]][i])    
        arg=(csv_app_f[columna[0]][i],csv_app_f[columna[2]][i],csv_app_f[columna[3]][i],
            aux1,aux3,csv_app_f[columna[6]][i],aux2,
            csv_app_f[columna[8]][i],date,csv_app_f[columna[11]][i],
            csv_app_f[columna[12]][i])
        #agrego a tabla
        
        if (add_to_sql(sql_table_app,arg)):
            a+=1
    print("se han cargado {} datos a la tabla {} ".format(a,'app'))
    a=0
    #agrego datos a la tabla_reviews
    for i in range(N_filas_reviews):
        arg=(csv_app_reviews[columna2[1]][i],csv_app_reviews[columna2[2]][i],csv_app_reviews[columna2[3]][i],
            csv_app_reviews[columna2[4]][i])
        if (add_to_sql(sql_table_reviews,arg)):
            a+=1
    print("se han cargado {} datos a la tabla {} ".format(a,'reviews'))
    a=0
            
    #agrego datos a la tabla_categorias  #
    
    for i in range(len(categorias)):
       arg=((i+1),categorias[i])
       if (add_to_sql(sql_table_categorias,arg)):
            a+=1
    print("se han cargado {} datos a la tabla {} ".format(a,'categorias'))
    a=0
         
    #agrego datos a la tabla_generos   
    for i in range(len(generos)): 
       arg=((i+1),generos[i])
       if (add_to_sql(sql_table_generos,arg)):
            a+=1
    print("se han cargado {} datos a la tabla {} ".format(a,'generos'))
    a=0
    
    #agrego datos a tablas auxiliares
    #tabla aux app-category
    
    for i in range(N_filas):
       idapp=(i+1)
       cat=csv_app_f[columna[1]][i]
       consulta.execute("SELECT id_Cat FROM categorias C WHERE C.Category='{}'".format(cat))
       idcat=consulta.fetchall()[0][0]
       arg=(idapp,idcat)
       if (add_to_sql(sql_table_aux_app_category,arg)):
            a+=1
    print("se han cargado {} datos a la tabla auxiliar {} ".format(a,'aux_AppCat'))
    a=0
    
    for i in range(N_filas):
       idapp=i+1
       generos_de_app=csv_app_f[columna[9]][i].split(';')
       for k in generos_de_app:
            consulta.execute("SELECT id_Gen FROM generos G WHERE G.Genre='{}'".format(k))
            idgen=consulta.fetchone()[0]
            arg=(idapp,idgen)
            add_to_sql(sql_table_aux_app_genre,arg)
            a+=1
    print("se han cargado {} datos a la tabla auxiliar {} ".format(a,'aux_AppGen'))
    a=0
    
    for i in range(N_filas_reviews):
        idrev=i+1
        nameapp=csv_app_reviews[columna2[0]][i]
        #idapp=d_app[app]
        #print(app)
        #consulta.execute("SELECT id_App FROM aplicaciones A WHERE A.App='{}'.format(app))
        #check=consulta.fetchone()
        #print(idapp)
        if nameapp not in d_app.keys():
            pass
        else:
            idapp=d_app[nameapp]
            arg=(idapp,idrev)
            add_to_sql(sql_table_aux_app_reviews,arg)
            a+=1
            
        
    print("se han cargado {} datos a la tabla auxiliar {} ".format(a,'aux_AppRev'))
    a=0
    
    return None


consulta.execute("SELECT count(*) FROM aplicaciones")
if (consulta.fetchone()[0])==0:
    poblar()
    print("-------------BD creada exitosamente, lista para usar--------------\n\n")
    
else:
    print("-------BD encontrada---------\n\n")
    pass

conexion.commit()
consulta.close()
conexion.close()

