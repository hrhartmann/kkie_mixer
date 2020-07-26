

class Dir:


    def __init__(self, name, already, new=False, assigned=None, assists=True, actual=None):
        self.name = name
        self.actual = actual
        self.assigned = assigned
        if len(already) >= 6:
            self.already = already[-2:]
            self.already.append(self.actual)
        elif len(already) == 5:
            possible = ['B', 'M', 'T', 'Cia', 'Clan', 'P']
            uequiv = {'B':'Bandada', 'M':'Manada', 'T':'Tropa', 'Cia':'Cia',
                    'P':'Pionas', 'Clan':'Clan'}
            for b in possible:
                if b not in already and self.assigned == None:
                    self.assigned = uequiv[b]
                    self.already = already
        else:
            self.already = already
        self.new = new
        self.assists = assists

    def __str__(self):
        return self.name

class Unit:

    def __init__(self, name, key):
        #asignados: dirs forzados a dicha unidad
        #posibles: dirs que pueden rotar
        self.name = name
        self.key = key
        self.asignados = []
        self.posibles = []
        self.min = min

    def assign(self, dir):
        self.asignados.append(dir)

    def total(self):
        return len(self.asignados) + len(self.posibles)

    def __str__(self):
        text = '-----' + self.name + '-----\n'
        for a in self.asignados:
            text += a.name + '\n'
        for a in self.posibles:
            text += a.name + '\n'
        return text


class Grupo:

    def __init__(self, unidades, total):
        self.unidades = unidades
        self.total = total
        self.no_asisten = []
        self.asisten = 0

    def no_asisten(self):
        return self.total - self.asisten

    def onemore(self):
        self.asisten += 1

    def pre_assign(self, dir):
        if dir.assigned:
            self.unidades[dir.assigned].asignados.append(dir)
        self.onemore()

    def print_group(self):
        print('##### Kkie Mixto #####')
        print('No asisten: ')
        for e in self.no_asisten:
            print(e.name)
        print()
        for unit in self.unidades.values():
            print(unit)
