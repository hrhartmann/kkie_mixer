from random import shuffle
from collections import deque
from grupo import Dir, Unit, Grupo

#Code version 2.5


kkscsv = 'kkies_mixtos_2020.csv' #Este es el archivo que vamos a leer
unidades = {'Manada':'M','Bandada':'B','Cia':'Cia','Clan':'Clan','Tropa':'T','Pionas':'P'}


def create_things(unidades, archivo):

    #Leemos el archivo y creamos una lista de dirigentes y guiadoras
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
        else:
            SanFrancesco.no_asiste(dir)
        #dir.print_dir()

    #SanFrancesco.print_group()
    SanFrancesco.ideal_perunit()
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

def solve(grupo, level):

    if level >= grupo.ideal + 2 or len(grupo.cola) == 0:
        for e in grupo.cola:
            print(e.name)
        grupo.print_group()
        return

    for dir in sorted(grupo.cola, key=lambda ele: ele.priority(), reverse=True):
        if 'Clan' not in dir.already and not dir.new:
            print(dir.name)
        #Partimos con el Clan porque es mas dificil asignar gente
        clan = grupo.unidades['Clan']
        if clan.total() < grupo.ideal:
            if grupo.valid(dir, clan):
                clan.poss(dir)
                if dir in grupo.cola:
                    grupo.cola.remove(dir)

        #Asignamos al dirigente a alguna unidad
        for unit in grupo.unidades.values():
            if unit.total() < level:
                if grupo.valid(dir, unit):
                    unit.poss(dir)
                    if dir in grupo.cola:
                        grupo.cola.remove(dir)
    solve(grupo, level + 1)





if __name__ == '__main__':

    SanFrancesco = create_things(unidades, kkscsv)
    solve(SanFrancesco, 1)




































    #Nothing code by AbyssalBit
