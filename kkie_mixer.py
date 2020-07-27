from random import shuffle
from collections import deque
import sys
from grupo import Dir, Unit, Grupo

#Code version 2.5

kkscsv = 'kkies_mixtos_2020.csv' #Este es el archivo que vamos a leer
unidades = {'Manada':'M','Bandada':'B','Cia':'Cia','Clan':'Clan','Tropa':'T','Pionas':'P'}


def create_things(unidades, archivo):

    #Leemos el archivo y creamos una lista de dirigentes y guiadoras
    lista_unidades = []
    kkie = kkies_mixtos_reader(archivo)

    #Creamos las unidades
    uid = 1
    for unit in unidades:
        if unit != 'Clan':
            unidades[unit] = Unit(unit, unidades[unit], id=uid)
            uid += 1
        else:
            unidades[unit] = Unit(unit, unidades)


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
        aid = 0
        for j in file:
            aid += 1
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
            dog = Dir(name, already,id=aid, new=new, assigned=assigned, assists=assists, actual=jefe[1])
            kkie.append(dog)
    return kkie

def poss_clan(grupo):
    for dir in sorted(grupo.cola, key=lambda ele: ele.priority(), reverse=True):
        #Partimos con el Clan porque es mas dificil asignar gente
        clan = grupo.unidades['Clan']
        if clan.total() < grupo.ideal:
            if grupo.valid(dir, clan):
                clan.poss(dir)
                if dir in grupo.cola:
                    grupo.cola.remove(dir)
    if clan.total() == grupo.ideal:
        return True
    else:
        print('Error al crear el clan')
        return False

def check_levels(grupo, level):
    for unit in grupo.unidades.values():
        if unit.total() < level:
            return False
    return True

def solve(grupo, level):

    if len(grupo.cola) == 0:
        grupo.generate_path()
        print('Resuelto con exito!!!')
        grupo.print_group()
        print('Resuelto !!!')
        sys.exit()
        print('Something..')

    if level >= grupo.ideal + 2:
        print('No ha sido resuelto')
        for e in grupo.cola:
            print(e.name)
        grupo.print_group()
        return False


    if check_levels(grupo, level):
        level += 1

    for dir in sorted(grupo.cola, key=lambda ele: ele.priority(), reverse=True):
        #Asignamos al dirigente (dir) a alguna unidad
        aassigned = False
        for unit in grupo.unidades.values():
            if unit.total() < level:
                if grupo.valid(dir, unit):
                    aassigned = True
                    unit.poss(dir)
                    if dir in grupo.cola:
                        grupo.cola.remove(dir)
                    if solve(grupo, level):
                        return True
        if not aassigned and level > grupo.ideal:
            #grupo.print_group()
            print(dir.name)
            print(grupo.generate_path())
            grupo.add_path()
            grupo.clean_level()

if __name__ == '__main__':

    SanFrancesco = create_things(unidades, kkscsv)
    poss_clan(SanFrancesco)
    solve(SanFrancesco, 1)





































    #Nothing by AbyssalBit


