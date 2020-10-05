import kkie_mixer as kkm






kkscsv = 'kkies_mixtos_2020.csv' #Este es el archivo que vamos a leer
unidades = {'Manada':'M','Bandada':'B','Cia':'Cia','Clan':'Clan','Tropa':'T','Pionas':'P'}

'''
Las instrucciones del programa se encuentran en el README del repositorio
'''

SanFrancesco = kkm.create_things(unidades, kkscsv)
kkm.poss_clan(SanFrancesco)
kkm.solve(SanFrancesco, 1)
