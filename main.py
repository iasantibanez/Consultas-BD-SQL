# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 13:49:15 2018

@author: pili9 & Ivan
"""
#### ediciones a la base de datos #####
import datetime 
import sqlite3
import Crear_tablas    # este archivo.py sirve para inicializar y poblar BD

conexion = sqlite3.connect("bd_app.sqlite3")
consulta = conexion.cursor()

sql_table_app="""
INSERT INTO aplicaciones(App, Rating, Reviews, Size, Installs, Type, Price,
Content_Rating, Last_update, Current_ver, Android_Ver)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
sql_table_categorias="""
INSERT INTO categorias(id_Cat, Category)
VALUES (?,?)
"""
sql_table_generos="""
INSERT INTO generos(id_Gen, Genre)
VALUES (?,?)
"""
sql_table_reviews="""
INSERT INTO reviews(Translated_Review, Sentiment,
Sentiment_Polarity, Sentiment_subjetivity)
VALUES (? ,?, ?, ?)
"""
sql_table_aux_app_category="""
INSERT INTO aux_AppCat(id_App, id_Cat)
VALUES (?,?)
"""
sql_table_aux_app_genre="""
INSERT INTO aux_AppGen(id_App, id_Gen)
VALUES (?,?)
"""
sql_table_aux_app_reviews="""
INSERT INTO aux_AppRev(id_App, id_review)
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
    

def add_app(app_data):
    now = datetime.datetime.now()
    if isinstance(app_data["name"], str) and isinstance(app_data["category"], str) and isinstance(app_data["rating"], int) and app_data["rating"]>0 and isinstance(app_data["size"],int) and app_data["size"]>0 and isinstance(app_data["price"],int) and app_data["price"]>=0 and isinstance(app_data["version"], int) and app_data["version"]>0 and isinstance(app_data["android"], int) and app_data["android"]>0 and type(app_data["genres"]) is list:
        print("todo bien")
        #agrego a la lista de aplicaciones
        #App, Rating, Reviews, Size, Installs, Type, Price,Content_Rating, Last_update, Current_ver, Android_Ver
        argumentos = (app_data["name"], app_data["rating"], 0, app_data["size"], 0, "none", app_data["price"], "none", now.strftime("%d-%m-%Y"), app_data["version"], app_data["android"])
        add_to_sql(sql_table_app,argumentos)
        #veo si ya existe la categoria 
        categoria = app_data["category"]
        consulta.execute("SELECT * FROM categorias WHERE EXISTS(SELECT * FROM categorias WHERE Category = '{}')".format(categoria))
        # si no existe creo nueva categoria
        if consulta.fetchone() == None:
            consulta.execute("SELECT MAX(id_Cat) FROM categorias")
            numero = consulta.fetchone()[0]
            argumentos = (numero + 1, categoria)
            #agrego a la lista de categorias
            add_to_sql(sql_table_categorias, argumentos)
            #agrego a la lista auxiliar id app y ad cat
            consulta.execute("SELECT id_App FROM aplicaciones WHERE App = '{}'".format(app_data["name"]))
            idd = consulta.fetchone()[0]
            argumentos= (idd, numero + 1)
            add_to_sql(sql_table_aux_app_category,argumentos)
        #si existe el genero agrego nueva relacion de ids
        if consulta.fetchone() != None:
            consulta.execute("SELECT id_App FROM aplicaciones WHERE App = '{}'".format(app_data["name"]))
            idd = consulta.fetchone()[0]
            consulta.execute("SELECT id_Cat FROM categorias WHERE Category = '{}'".format(categoria))
            idd2 = consulta.fetchone()[0]
            argumentos = (idd, idd2)
            add_to_sql(sql_table_aux_app_category, argumentos)
        #veo si ya existen los generos 
        generos = app_data["genres"]
        for i in generos:
            consulta.execute("SELECT * FROM generos WHERE EXISTS(SELECT * FROM generos WHERE Genre = '{}')".format(i))
            #si no existe el genero lo agrego
            if consulta.fetchone() == None:
                consulta.execute("SELECT MAX(id_Gen) FROM generos")
                numero = consulta.fetchone()[0]
                argumentos = (numero + 1, i)
                add_to_sql(sql_table_generos, argumentos)
                consulta.execute("SELECT id_App FROM aplicaciones WHERE App = '{}'".format(app_data["name"]))
                idd = consulta.fetchone()[0]
                argumentos= (idd, numero + 1)
                add_to_sql(sql_table_aux_app_genre,argumentos)
            if consulta.fetchone() != None:
                consulta.execute("SELECT id_App FROM aplicaciones WHERE App = '{}'".format(app_data["name"]))
                idd = consulta.fetchone()[0]
                consulta.execute("SELECT id_Gen FROM generos WHERE Genre = '{}'".format(i))
                idd2 = consulta.fetchone()[0]
                argumentos = (idd, idd2)
                add_to_sql(sql_table_aux_app_genre, argumentos)
                conexion.commit()
        print("Aplicacion agregada correctamente")
    else:
        print("No es posible agregar la aplicacion")
        return None
    
def add_comment(app_name, text, sentiment):
    #agrego el comentario a la tabla de reviews
    dic_sent={1:'Positive', 2:'Neutral', 3: 'Negative'}
    if sentiment not in [1,2,3]:
        print("datos no sigen el formato indicado")
    else:
        print(dic_sent[sentiment])
        sentiment=dic_sent[sentiment]
        argumentos = (text, sentiment, "none" , "none")
        add_to_sql(sql_table_reviews, argumentos)
        #sumo un comentario a las reviews de las apps
        consulta.execute("UPDATE aplicaciones SET Reviews = Reviews + 1 WHERE App = '{}'".format(app_name))
        #agrego link entre id app y id review
        consulta.execute("SELECT id_App FROM aplicaciones WHERE App = '{}'".format(app_name))
        idd = consulta.fetchone()[0]
        consulta.execute("SELECT id_review FROM reviews WHERE Translated_Review = '{}'".format(text))
        idd2 = consulta.fetchone()[0]
        argumentos = (idd, idd2)
        add_to_sql(sql_table_aux_app_reviews, argumentos)
    conexion.commit()
    return None

def download_app(app_name):
    consulta.execute("UPDATE aplicaciones SET Installs = Installs + 1 WHERE App = '{}'".format(app_name))
    conexion.commit()
    return None

def delete_app(app_name): 
    #elimino las reviews asociadas a la aplicacion 
    consulta.execute("SELECT id_App FROM aplicaciones WHERE App = '{}'".format(app_name))
    if consulta.fetchone() == None:
        return print("la aplicacion no existe")
    idd = consulta.fetchone()[0]
    print(idd)
    consulta.execute("DELETE FROM reviews WHERE id_review IN (SELECT id_review FROM aux_AppRev WHERE id_App = '{}')".format(idd))
    #elimino la app de la tabla id app y id reviews
    consulta.execute("DELETE FROM aux_AppRev WHERE id_App = '{}'".format(idd))
    #elimino la app de la tabla id App y id Categoria
    consulta.execute("DELETE FROM aux_AppCat WHERE id_App = '{}'".format(idd))
    #elimino la app de la tabla id App y id genero
    consulta.execute("DELETE FROM aux_AppGen WHERE id_App = '{}'".format(idd))
    #elimino la app de la tabla aplicaciones 
    consulta.execute("DELETE FROM aplicaciones WHERE App = '{}'".format(app_name))
    conexion.commit()
    return None

conexion.commit()
consulta.close()
conexion.close()

#### CONSULTAS #######
conexion = sqlite3.connect("bd_app.sqlite3")
consulta = conexion.cursor()

def get_info(app):
    #se hace una lista de diccionarios ya que hay aplicaciones de igual nombre, 
    # pero con distintas caracteristicas 
    consulta.execute("SELECT * FROM aplicaciones WHERE App = '{}'".format(app))
    datos = consulta.fetchall()
    llaves = ["name", "category", "ratingOverall", "reviews", "size", "installs"]
    diccionarios = []
    for j in range(len(datos)):
        id_app = datos[j][0]
        consulta.execute("SELECT Category FROM categorias WHERE id_Cat = (SELECT id_Cat from aux_AppCat WHERE id_App = '{}')".format(id_app))
        categoria = consulta.fetchone()[0]
        dict = {llaves[0]: datos[j][1], llaves[1]:categoria, llaves[2]:datos[j][2], llaves[3]:datos[j][3], llaves[4]:datos[j][4], llaves[5]:datos[j][5]}
        diccionarios.append(dict)
    if len(diccionarios) == 0:
        print(app)
        dict = { "error": "la aplicacion '{}' no existe en la base de datos".format(app)}
        return dict
    return diccionarios[0]


def app_with_more_income():
    consulta.execute("SELECT * from aplicaciones")
    datos =  consulta.fetchall()
    contador = 0
    ganadores = []
    for i in datos:
        precio = int(i[7])
        instal = str(i[5])
        #instal = instal.replace(",", "")
        instal = int(instal)
        a = precio * instal
        if a > contador:
            contador = a
    for i in datos:
        precio = int(i[7])
        instal = str(i[5])
        #instal = instal.replace(",", "")
        instal = int(instal)
        a = precio * instal
        if a == contador:
            ganadores.append(i[1])
        if len(ganadores) == 5:
            break
    return ganadores


def recommend(genre, size): 
    consulta.execute("SELECT * FROM generos G WHERE G.Genre='{}'".format(genre))
    if len(consulta.fetchall()) == 0:
        return print("este genero no existe")
    else:
        #selecciono id del genero
        consulta.execute("SELECT id_Gen FROM generos WHERE Genre = '{}'".format(genre))
        id_genero = consulta.fetchone()[0]
        consulta.execute("SELECT id_App FROM aux_AppGen WHERE id_Gen = '{}'".format(id_genero))
        id_Apps = consulta.fetchall()
        lista = []
        for i in id_Apps:
            consulta.execute("SELECT Size FROM aplicaciones WHERE id_App = '{}'".format(i[0]))
            tamaño = consulta.fetchone()[0]
            if tamaño != 'Varies with device':
                tamaño = float(tamaño)
                if tamaño < size:
                    positivos = 0 
                    consulta.execute("SELECT App FROM aplicaciones WHERE id_App = '{}'".format(i[0]))
                    nombre = consulta.fetchone()[0]
                    consulta.execute("SELECT id_review FROM aux_AppRev WHERE id_App = '{}'".format(i[0]))
                    if consulta.fetchone() != None:
                        reviews = consulta.fetchall()
                        for j in reviews:
                            consulta.execute("SELECT Sentiment FROM reviews WHERE id_review = '{}'".format(j[0]))
                            sent = consulta.fetchone()[0]
                            if sent == 'Positive':
                                positivos += 1
                        lista.append((nombre, positivos))
        lista = sorted(lista, key=lambda x: x[1])
        lista = lista[::-1]
        lista_final = []
        for i in lista:
            if len(lista_final) < 5:
                lista_final.append(i[0])
        return lista_final

def best_by_genre(n,genre):
    consulta.execute("SELECT * FROM generos G WHERE G.Genre='{}'".format(genre))
    if len(consulta.fetchall()) == 0:
        return print("este genero no existe")
    else:
        consulta.execute("""SELECT id_App FROM aux_AppGen AG WHERE AG.id_Gen IN 
                     (SELECT id_Gen FROM generos G WHERE G.Genre = '{}')""".format(genre))
        #consulta.execute("SELECT * FROM generos G WHERE G.Genre='{}'".format(genre))
        #id_genero=consulta.fetchall()[0][0]
        #print(id_genero)
        #consulta.execute("SELECT * FROM aux_AppGen G WHERE G.id_Gen='{}'".format(id_genero))
        total_app_aux=consulta.fetchall()
        #print(total_app_aux)
        #print(total_app_aux)
        total_app=[]
        #saco las app coincidentes con genero
        for i in total_app_aux:
            total_app.append(i[0])
        total_app=tuple(total_app)
        #print(total_app)
        lista=[]
        #saco rating de las app y las ordeno por rating en lista
        for k in total_app:
            consulta.execute("SELECT App,Rating FROM aplicaciones A WHERE A.id_App='{}'".format(k))
            lista.append((k,consulta.fetchone()[1]))
        lista = sorted(lista, key=lambda x: x[1])
        ##saco nombre
        lista2 = []
        #while len(lista2)<20:  # pa que no se repita
        #print(lista)
        a=0
        while len(lista2)<n:
            indice=1+a
            app_id=lista[-indice][0]
            consulta.execute("SELECT App FROM aplicaciones A WHERE A.id_App='{}'".format(app_id))    
            app_name = consulta.fetchone()[0]
            if app_name not in lista2:
                lista2.append(app_name)
                #print(app_name)
            a+=1
        print(lista2)
    return lista2

def price_of_the_best_by_genre(n,genre):
    consulta.execute("SELECT id_Gen FROM generos G WHERE G.Genre = '{}'".format(genre))
    if len(consulta.fetchall()) == 0:
        print("este genero no existe")
        return -1
    else: 
        consulta.execute("SELECT AVG(price) FROM aplicaciones A WHERE A.App IN {}".format(tuple(best_by_genre(n,genre))))
        price="{0:0.2f}".format(consulta.fetchone()[0])
        print("\nel precio promedio de las apps de genero '{}' , es de $ {} USD".format(genre,price))        
        return price
   

def count_by_version(date1, date2):
    if date1 < date2 : 
        a=date1
        b=date2
    else:
        a=date2
        b=date1
    consulta.execute("SELECT DISTINCT Android_Ver FROM aplicaciones A WHERE A.Last_update BETWEEN '{}' AND '{}' ".format(a,b))
    vers_A=consulta.fetchall()
    consulta.execute("SELECT id_App Android_Ver FROM aplicaciones A WHERE A.Last_update BETWEEN '{}' AND '{}' ".format(a,b))
    app_fecha=consulta.fetchall()
    lista=[]
    for l in app_fecha:
        lista.append(l[0])
    dic_count_ver={}
    dic_max_rating_cat_ver={}
    consulta.execute("SELECT DISTINCT id_Cat FROM aux_AppCat")
    categorias=consulta.fetchall()
    for i in vers_A:
        max_rating=[0,0]
        consulta.execute("SELECT id_App FROM aplicaciones A WHERE A.Android_Ver = '{}' AND id_App IN {} ".format(i[0],tuple(lista)))
        dic_count_ver[i[0]]=len(consulta.fetchall())
        
        for k in categorias:
            consulta.execute("SELECT id_App FROM aplicaciones A WHERE A.Android_Ver = '{}' INTERSECT SELECT id_App FROM aux_AppCat AC WHERE AC.id_Cat = '{}'".format(i[0],k[0]))
            apps=consulta.fetchall()
            aux2=[]
            for j in apps:
                aux2.append(j[0])
            if len(aux2)>1:    
                consulta.execute("SELECT AVG(Rating) FROM aplicaciones A WHERE A.id_App IN {}".format(tuple(aux2)))
                rating = consulta.fetchone()[0] 
            elif len(aux2)==1:
                consulta.execute("SELECT AVG(Rating) FROM aplicaciones A WHERE A.id_App = '{}'".format(aux2[0]))
                rating = consulta.fetchone()[0]
            else:
                rating = 0
                    
            if max_rating[0] <= rating:
                max_rating[0] = rating
                max_rating[1] = k[0]
            else:
                pass
        consulta.execute("SELECT Category FROM categorias C WHERE C.id_Cat = '{}'".format(max_rating[1]))
        a=consulta.fetchone()[0]
        dic_max_rating_cat_ver[i[0]]= a
    print("Cantidad de apps por versión de Android:\n")
    print(dic_count_ver,'\n')
    print("Mejor categoria por versión de Android (Segun rating promedio)\n")
    print(dic_max_rating_cat_ver)
    
    

    
def need_update(app):
    #verifica si existe app
    consulta.execute("SELECT id_App FROM aplicaciones A WHERE A.App='{}'".format(app))
    if len(consulta.fetchall())==0:
        print("no existe app")
        return None
    
    else: # si existe, ejecuta lo demas.
    #CONSULTA ANIDADA CON 4 SUB NIVELES,
    #1) busqueda de id _app 
    #2) las categorias asociadas a la(s) app (1) 
    #3) todas las app con estas cat (2) 
    #4) todas las fechas de actualizaciones (3)        
        consulta.execute("""SELECT Last_Update FROM aplicaciones A WHERE A.id_App
                         IN (SELECT id_App FROM aux_AppCat AC WHERE AC.id_Cat
                         IN (SELECT id_Cat FROM aux_AppCat AC WHERE AC.id_App
                         IN (SELECT DISTINCT id_App FROM aplicaciones A WHERE A.App = '{}'
                         )))""".format(app))
        #recupero las fechas para las de la misma categoria.
        aux_fechas=consulta.fetchall()
        fechas=[]
        for i in aux_fechas:
            fechas.append(i[0])
        #CALCULO PROMEDIO FECHAS
        dd=0
        mm=0
        yy=0
        for k in fechas:
            aux=k.split('-')
            yy+=int(aux[0])
            mm+=int(aux[1])
            dd+=int(aux[2])
        dd=round(dd/len(fechas))
        mm=round(mm/len(fechas))
        yy=round(yy/len(fechas))
        
        consulta.execute("""SELECT Last_Update FROM aplicaciones A WHERE A.App = '{}'""".format(app))
        l_u_app=consulta.fetchone()[0].split('-')
        l_u_app=datetime.date(int(l_u_app[0]),int(l_u_app[1]),int(l_u_app[2]))
        if datetime.date(yy,mm,dd) < l_u_app :
            print("fecha promedio ", datetime.date(yy,mm,dd))
            print("fecha ultima actualizacion app:", l_u_app)
            return False
        else: 
            print("fecha promedio ", datetime.date(yy,mm,dd))
            print("fecha ultima actualizacion app:", l_u_app)
            return True

##Ejemplos
#EDICIONES A BD
#add_app(app_data)
#add_comment('Solitaire','asdasd',1)
#add_comment(app_name, text, sentiment)
#download_app(app_name)
#delete_app(app_name)
    
#CONSULTAS
#print(get_info('Superheroes Wallpapers | 4K Backgrounds'))
#print(get_info('Solitaire'))
#print(app_with_more_income())
#print(recommend('Food & Drink',20))
#best_by_genre(10,'Action')
#price_of_the_best_by_genre(10,'Action')
#count_by_version('2018-08-08','20asd-08-07')
#print(need_update('Coloring book moana'))

#print(need_update('Real Tractor Farming'))


#-------------main----------------------------------------------
#
#if __name__ == "__main__":
#    datos = get_info("Este nombre no existe")
#    print(datos["error"])
#    nombre = 'Superheroes Wallpapers | 4K Backgrounds'
#    datos_super = get_info(nombre)
#    print("{} -> {}".format(nombre, datos_super['installs']))
#    download_app(nombre)
#    datos_super = get_info(nombre)
#    print("{} -> {}".format(nombre, datos_super['installs']))


