from random import shuffle
from collections import deque
from grupo import Dir, Unit, Grupo


kkscsv = 'kkies_mixtos_2020.csv' #Este es el archivo que vamos a leer
unidades = {'Manada':'M','Bandada':'B','Cia':'Cia','Clan':'Clan','Tropa':'T','Pionas':'P'}


def create_things(unidades, archivo):

    lista_unidades = []
    kkie = kkies_mixtos_reader(archivo)
    #Creamos las unidades
    for unit in unidades:
        unidades[unit] = Unit(unit, unidades[unit])


    #Creamos el grupo
    SanFrancesco = Grupo(unidades, len(kkie))

    #Asignamos a los dirigentes y guiadoras que ya estan asignados
    for dir in kkie:
        if dir.assists:
            SanFrancesco.pre_assign(dir)

    SanFrancesco.print_group()


    return SanFrancesco


def kkies_mixtos_reader(archivo):
    uequiv = {'B':'Bandada', 'M':'Manada', 'T':'Tropa', 'Cia':'Cia',
            'P':'Pionas', 'Clan':'Clan'}
    invequiv = {'Bandada':'B', 'Manada': 'M', 'Tropa':'T', 'Cia':'Cia',
            'Pionas': 'P', 'Clan':'Clan'}
    with open(archivo, 'r') as file:
        fline = file.readline()
        data = fline.split(',')
        possible = ['B', 'M', 'T', 'Cia', 'Clan', 'P']
        kkie = []
        for j in file:
            jefe = j.split(',')
            already = []
            assigned = None
            new = False
            name = jefe[0]
            assists = True
            already.append(invequiv[jefe[1]])
            for option in jefe[5:]:
                if option not in already and option != '*' and option != '\n':
                    already.append(option)
            unidades = ['Manada', 'Tropa', 'Pionas', 'Cia', 'Clan', 'Bandada']
            if jefe[3].lower() == 'si':
                assigned = jefe[1]
            else:
                assigned = None
            if jefe[2].lower() == 'si':
                new = True
            if 'no' in jefe[4].lower():
                assists = False
            dog = Dir(name, already, new=new, assigned=assigned, assists=assists, actual=jefe[1])
            kkie.append(dog)
    return kkie



if __name__ == '__main__':

    SanFrancesco = create_things(unidades, kkscsv)




































    #Nothing
