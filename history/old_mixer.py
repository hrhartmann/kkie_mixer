from grupo import Dir
from collections import deque
from random import shuffle
from kkie_mixer import kkies_mixtos_reader, kkscsv


MAX_ATTEMPTS = 20

def kkies_mixtos(lista):
    everyone = []
    for j in lista:
        everyone.append(j.name)
    corres = {'Manada':'M','Bandada':'B','Cia':'Cia','Clan':'Clan','Tropa':'T','Pionas':'P'}
    numxkkie = int(len(lista)/len(corres))
    corresnumxkkie = {'Manada':numxkkie,'Bandada':numxkkie,'Cia':numxkkie-1,'Clan':numxkkie-1,'Tropa':numxkkie-1,'Pionas':numxkkie-1}
    kkiemix = {'Bandada':deque([]),
    'Manada':deque([]),
    'Tropa':deque([]),
    'Cia':deque([]),
    'Pionas':deque([]),
    'Clan':deque([])}
    cola = lista.copy()
    no_asignados = deque([])
    ya_asignados = deque([])
    asignar_dps = deque([])
    asignacion_lista = []
    no_asiste = []
    shuffle(cola)
    priority_line = [[],[],[],[],[]]



    # Asignacion de linea de prioridad y asignacion obligatoria
    while cola:
        pdir = cola.pop()
        if pdir.assigned != None:
            ya_asignados.append(pdir)
        else:
            priority_line[len(pdir.already) - 1].append(pdir)

    # Asignacion obligatoria
    print('Ya asignados: ')
    for j in ya_asignados:
        if j.assigned != None and j.assigned != True:
            kkiemix[j.assigned].append(j)
        else:
            print('Error of assigned: {}'.format(j.name))

    #############################################################
    ########## Asignacion por kkie ##############################
    #############################################################
    while priority_line:
        for line in priority_line:
            if len(priority_line[-1]) > 0:
                j = priority_line[-1].pop()
            else:
                priority_line.pop()
            if j.assigned == None and j.assists:
                asignacion_lista.append(j)
                for kkie in corres:
                    if kkie not in j.already and len(kkiemix[kkie]) < corresnumxkkie[kkie] and j not in kkiemix[kkie]:
                        if j.assigned == True:
                            pass
                        elif kkie == 'Clan' and not j.new:
                            kkiemix['Clan'].appendleft(j)
                            j.assigned = True
                        else:
                            kkiemix[kkie].appendleft(j)
                            j.assigned = True

                    else:
                        if j not in no_asignados:

                            no_asignados.append(j)

            else:
                if j.assists == False:
                    if j.name not in no_asiste:
                        no_asiste.append(j.name)
                elif j.assigned == 'later' and j not in asignar_dps:
                    asignar_dps.append(j)
                else:
                    pass
    cambios = 0

    # Asignacion a quienes faltaron
    print('No asignados:')
    for k in no_asignados:
        print(f'{k.name} no fue asignad@')
    while no_asignados:
        cambios += 1
        if cambios > 10:
            break
        j = no_asignados.pop()
        assigned = False
        for unit in kkiemix:
            if corres[unit] not in j.already and len(kkiemix[unit]) < corresnumxkkie[unit] + 2 and not assigned:
                if (unit == 'Clan' and j.new) or (j.assigned == True):
                    pass
                else:
                    if j not in kkiemix[unit]:
                        kkiemix[unit].append(j)
                        j.assigned = True
                        assigned = True
        if not assigned:
            for unit in kkiemix:
                if corres[unit] not in j.already and len(kkiemix[unit]) > corresnumxkkie[unit] + 2 and not assigned:
                    if (unit == 'Clan' and j.new) or (j.assigned == True):
                        pass
                    else:
                        if j not in kkiemix[unit]:
                            enroque = kkiemix[unit][0]
                            if enroque.assigned == True:
                                no_asignados.appendleft(kkiemix[unit].popleft())
                                kkiemix[unit].append(j)
                                j.assigned = True
                                assigned = True
        if not assigned and j not in asignar_dps:
            asignar_dps.append(j)

    # Asignacion tardia y cambios
    print('Asignar dps: ')
    for k in asignar_dps:
        print(k.name)
    while asignar_dps:
        cambios += 1
        if cambios > 40:
            break
        j = asignar_dps.pop()
        assigned = False
        for unit in kkiemix:
            if corres[unit] not in j.already and not assigned:
                if (unit == 'Clan' and j.new) or (j.assigned == True):
                    pass
                else:
                    if j not in kkiemix[unit]:
                        kkiemix[unit].append(j)
                        j.assigned = True
                        assigned = True
        if not assigned:
            for unit in kkiemix:
                if corres[unit] not in j.already and not assigned:
                    if (unit == 'Clan' and j.new) or (j.assigned == True):
                        pass
                    else:
                        if j not in kkiemix[unit]:
                            if enroque.assigned == True:
                                no_asignados.appendleft(kkiemix[unit].popleft())
                                kkiemix[unit].append(j)
                                j.assigned = True
                                assigned = True



    # Resultado
    count = 0
    k_asignados = []
    for key in kkiemix:
        print('############################')
        print(key)
        for b in kkiemix[key]:
            print(f'   {b.name} ({b.actual})')
            count += 1
            k_asignados.append(b.name)
    print()
    never_assigned = []

    # No asignados
    print(f'Total: {count}')
    for j in lista:
        if j.name not in k_asignados and j.assists != False:
            print(f'{j.name} no fue k asignad@')
            if j.assists:
                never_assigned.append(j)

    #Zona critica de verificacion
    critic = 0
    misma_unidad_critic = False
    for unit in kkiemix.values():
        for unit_name in corres.values():
            misma_unidad = 0
            for j in unit:
                if j.actual == unit_name:
                    misma_unidad += 1
            if misma_unidad > 2:
                critic += 1
                misma_unidad_critic = True
    if len(never_assigned) > 0:
        critic += 1
    if not critic:
        print('No asisten:')
        for dir in no_asiste:
            print(dir)
    print()
    print('Critic: {}'.format(critic))
    if misma_unidad_critic:
        print('Mas de dos personas de la misma unidad quedaron juntos')

    return critic

if __name__ == '__main__':
    #kkies_mixtos(kkies_mixtos_reader(kkscsv)

    attempts = 0
    while True:
        attempts += 1
        print(f'******* ATTEMPT {attempts} **********')
        if not kkies_mixtos(kkies_mixtos_reader(kkscsv)):
            print(f'Total attempts: {attempts}')
            break

        if attempts >= MAX_ATTEMPTS:
            break
