En primer lugar para ejecutar y realizar consultas abrir "main.py" 


**[CONSIDERACIONES]**:
se debe tener en una misma carpeta;

- archivo crear_tablas requiere libreria panda
- archivos csv para crear BD en caso de no existir

**[Inicialización]**:
el programa parte llamando a crear_tablas en donde se obtienen y filtran los datos entregados.
se procede a crear y poblar la BD ("bd_app.sqlite3") con las tablas y auxiliares


En cuanto a los datos, se cambio la estructura de los siguientes:
- precio : se saco el simbolo $
- size : se saco la letra M o k -un solo caso- (asumiendo este como kilobytes)
- installs : se saco el simbolo + y se trabajo como entero
- fecha: se cambia la fecha a formato YYYY-MM-DD

**[Edición a la BD]**:

- Esto cuenta con 4 consultas en donde se asume que los parametros a agregar son correctos 
- add_app puede admitir parametros incorrectos y retorna print de fallo al agregar
- add_comment, el sentimiento puede ser 1:positivo; 2:neutral; 3:negative sino printea en consola error y retorna None
- download_app => (*) en el caso de haber mas de una app con el mismo nombre, ambas son modificadas.

**[Consultas a la BD]**

_get_info_ : 
- retorna dicc con info de app, en caso de haber 
mas de una coincidencia por simplicidad solo retorna el primero

_best_by_genre_ : 
- retorna una lista con las apps ademas de imprimirlas en consola
  
_count_by_ver_ : 
- imprime en consola el n° de apps por versión de andriod [formato diccionario]
- imprime en consola mejores categorias por versión de android [formato diccionario]
- retorna None
- (*) en caso no ingresar fecha valida, se imprimen listas vacias.
				
								
_price_of_the_best_by_genre_ : 
- según la issue #82 se utiliza best_by_genre para extraer las apps
- se guarda el valor promedio en variable precio y se extraen 2 decimales.
- retorna el precio y ademas lo imprime en consola

_recommended_:
- retorna a una lista con recomendaciones, por lo tanto se debe imprimir en consola para ver
 ej: print(recommend('Food & Drink',20))

_need_update_:
- se calcula el promedio del año, mes, dia y se aproximan para obtener un promedio de la fecha de actualizacion por las apps de dicha categoria	
- retorna True o False, 
- ademas de imprimir las fechas en consola

_app_with_more_income_:
- se consideran la app que posea el mayor valor según
 max{precio*instalaciones} para todas las apps
- retorna app o lista de app, por lo tanto se debe imprimir para ver
ej : print(app_with_more_income())

						
						
						
(*) POR ULTIMO; el archivo main fue completado
 y para efectos practicos se comentaron las consultas iniciales en el main.
 
 
 