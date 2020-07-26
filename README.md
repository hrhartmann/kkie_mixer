# kkie_mixer by AbyssalBit
**Program created to distribute objects in groups with restrictions**

**Instrucciones**

Archivo __nombre del archivo a ejecutar__:
kkscsv: nombre del documento csv para el historial y las unidades actuales
ejecutar el archivo con Python3.6+.

Instrucciones del archivo CSV:

La columna Asignad@ se utiliza para determinar si el dirigente o guiadora en 
cuestión debe permanecer en su unidad actual (Casi siempre se queda uno).
La columna Nuev@ se utiliza para determinar si el dirigente o guiadora entró al kkie
ese mismo año.
La columna Actual indica la unidad actual del dirigetne o guiadora.
La columna Asiste indica si asistirá a los kkies mixtos que se realizarán en la ocasión.
Las columnas de historial y las columnas siguientes indican por cuales unidades ya ha 
pasado el dirigetne o guiadora en kkies mixtos anteriores.


**Las columnas pueden tener los siguientes valores:**

Asignad@: defecto = no / asignar = si

Nuev@: defecto = no / nuev@ = si

*Actual: {Manada, Bandada, Tropa, Cia, Pioneros, Clan}

Asiste: defecto = si / ausente = no

historial: * = vacío / {M, B, T, Cia, P, Clan}

otro (parte del historial): * = vacío / {M, B, T, Cia, P, Clan}


