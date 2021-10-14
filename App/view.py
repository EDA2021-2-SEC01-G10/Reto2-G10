"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
import time 
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Las obras más antiguas para un medio específico(Lab.5)")
    print("3- Numero total de obras de una nacionalidad(Lab.6) ")
    print("0- Salir ")
def initCatalog(): 
    catalog=controller.initCatalog()
    return catalog 
def loadData(catalog): 
    controller.loadData(catalog)

def listMasAntiguas(catalog,medio): 
    list=controller.listMasAntiguas(catalog,medio) 
    return list     
def contarPorNacionalidad(catalog,nacionalidad):
    obrasPorNacionalidad=controller.contarPorNacionalidad(catalog,nacionalidad)
    return obrasPorNacionalidad

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        start_time = time.process_time()
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print('Artistas cargados: ' + str(lt.size(catalog['artists'])))
        print('Obras cargadas: ' + str(lt.size(catalog['artworks'])))
        stop_time = time.process_time()
        timeT=(stop_time - start_time)*1000
        print("Tiempo:",timeT)

    elif int(inputs[0]) == 2:
        medio=input("Ingrese el medio especifico que desea consultar: ")
        masAntiguas=listMasAntiguas(catalog,medio)
        print(lt.size(masAntiguas))
    elif int(inputs[0]) == 3:    
        nacionalidad=(input("Ingrese la nacionalidad que desea consultar: ")).strip()
        obrasPorNacionalidad=contarPorNacionalidad(catalog,nacionalidad)
        numeroObras=str(lt.size(obrasPorNacionalidad))
        print("Hay "+numeroObras+" obras catalogadas,hechas por artistas con nacionalidad de: "+nacionalidad)
    elif int(inputs[0]) == 0:    
         sys.exit(0)
    else:
        sys.exit(0)
sys.exit(0)
