

class Dir:

    def __init__(self, name, already, id=0, new=False, assigned=None, assists=True, actual=None):
        self.name = name
        self.actual = actual
        self.assigned = assigned
        if id >= 10:
            self.id = str(id)
        else:
            self.id = '0' + str(id)
        if len(already) >= 6:
            self.already = already[-2:]
            self.already.append(self.actual)
        elif len(already) == 5:
            print(f'5 already: {name}')
            possible = ['B', 'M', 'T', 'Cia', 'Clan', 'P']
            uequiv = {'B':'Bandada', 'M':'Manada', 'T':'Tropa', 'Cia':'Cia',
                    'P':'Pionas', 'Clan':'Clan'}
            for b in possible:
                if b not in already and self.assigned == None:
                    print(already)
                    self.assigned = uequiv[b]
                    self.already = already
        else:
            self.already = already
        self.new = new
        self.assists = assists

    def __str__(self):
        return self.name

    def print_dir(self):
        print(self.name)
        print(f'Actual: {self.actual}')
        print(f'Estuvo: {self.already}')
        if self.new:
            print('Nuevo')
        if not self.assists:
            print('No asiste')

    def priority(self):
        return len(self.already)


class Unit:

    def __init__(self, name, key, id=0):
        #asignados: dirs forzados a dicha unidad
        #posibles: dirs que pueden rotar
        self.name = name
        self.key = key
        self.asignados = []
        self.posibles = []
        self.id = id

    def assign(self, dir):
        self.asignados.append(dir)

    def poss(self, dir):
        self.posibles.append(dir)
        dir.assigned = True

    def total(self):
        return len(self.asignados) + len(self.posibles)

    def same_unit(self, unit):
        same_unit = 0
        for dir in self.asignados:
            if dir.actual == unit:
                same_unit += 1
        for dir in self.posibles:
            if dir.actual == unit:
                same_unit += 1
        return same_unit

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
        self.solutions = []
        self.total = total
        self.paths = []
        self.cola = []
        self.kchain = []
        self.no_asisten = []
        self.asisten = 0
        self.ideal = 0
        self.backtracks = 0

    def no_asisten(self):
        return self.total - self.asisten

    def generate_path(self):
        chain = 'h'
        for unit in self.unidades.values():
            if unit.name != 'Clan':
                for dir in unit.posibles:
                    chain += dir.id
                chain += (self.ideal + 1 - len(unit.posibles) - len(unit.asignados)) * '00'
        return chain

    def add_path(self):
        chain = self.generate_path()
        self.paths.append(chain)

    def backtrack(self):
        self.backtracks += 1
        dir = self.unidades[self.kchain.pop()].posibles.pop()
        dir.assigned = False
        self.cola.append(dir)


    def no_asiste(self, dir):
        self.no_asisten.append(dir)

    def valid(self, dir, unit):
        if self.generate_path() in self.paths:
            return False
        if not dir.assigned == None:
            return False
        if unit.key in dir.already:
            return False
        if unit.same_unit(dir.actual) > 1:
            return False
        if unit.total() >= self.ideal + 1:
            return False
        if unit.name == 'Clan':
            if dir.new:
                return False
            if unit.total() >= self.ideal:
                return False
        return True

    def onemore(self):
        self.asisten += 1


    def clean_unit(self, ukey):
        unit = self.unidades[ukey]
        for dir in unit.posibles:
            self.cola.append(unit.posibles.pop())

    def clean_level(self):
        for unit in self.unidades.values():
            if unit.name != 'Clan':
                if unit.posibles:
                    dir = unit.posibles.pop()
                    dir.assigned = False
                    self.cola.append(dir)

    def pre_assign(self, dir):
        self.onemore()
        if dir.assigned:
            self.unidades[dir.assigned].asignados.append(dir)
            return 1
        else:
            self.cola.append(dir)
            return 0

    def reset(self):
        for unit in self.unidades.values():
            if unit.name != 'Clan':
                for i in range(len(unit.posibles)):
                    self.cola.append(unit.posibles.pop())



    def ideal_perunit(self):
        self.ideal =  int(self.asisten / len(self.unidades))

    def print_group(self):
        print('##### Kkie Mixto #####')
        print(f'No asisten: {len(self.no_asisten)}')
        print()
        for e in self.no_asisten:
            print(e.name)
        print()
        print(f'Asisten: {self.asisten}')
        print()
        for unit in self.unidades.values():
            print(unit)
        print()
        print(f'Backtracks: {self.backtracks}')













































#Nothing By AbyssalBit
