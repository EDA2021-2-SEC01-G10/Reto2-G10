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
    print("2- Listar cronológicamente los artistas(Req.1) ")
    print("3- Listar cronológicamente las adquisiciones(Req.2)")
    print("4- Clasificar las obras de un artista por técnica(Req.3)")
    print("5- Clasificar las obras por la nacionalidad de sus creadores(Req.4)  ")
    print("6- Transportar obras de un departamento (Req.5) ")
    print("7- (Req.6)")
    print("0- Salir")


def initCatalog(): 
    catalog=controller.initCatalog()
    return catalog 
def loadData(catalog): 
    controller.loadData(catalog)

def artEnRango(catalog,añoInicial,añoFinal):
    lista=controller.artEnRango(catalog,añoInicial,añoFinal)
    return lista    
def listarAdquisisionesCronologicamente(catalog,fechaInicial,fechaFinal):
    lista=controller.listarAdquisisiones(catalog,fechaInicial,fechaFinal)
    return lista

def obrasPorArtista(catalog,nombreArtista): 
    lista=controller.obrasArtista(catalog,nombreArtista)
    return lista 
def lstDepartamento(catalog,departamento):
    listDepartamento=controller.lstDepartamento(catalog,departamento)
    return listDepartamento
def ordenarPorCosto(precios): 
    listOrdenada=controller.ordenarPorCosto(precios)
    return listOrdenada
def ordenarPorFecha(precios): 
    listOrdenada=controller.ordenarPorFecha(precios)
    return listOrdenada


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
        añoInicial=int(input("Ingrese el año de nacimiento para el rango inicial de artistas deseado:"))
        añoFinal=int(input("Ingrese el año de nacimiento para el rango final de artistas deseado:"))
        artistasEnRango=artEnRango(catalog,añoInicial,añoFinal)
        print("") 
        print("Hay " + str(lt.size(artistasEnRango)) +" artistas nacidos entre "+str(añoInicial)+" y "+str(añoFinal))
        print("")
        print("Los primeros y ultimos 3 artistas nacidos en este rango son: ")
        print("")
        artistsMostrar=(list(lt.iterator(artistasEnRango)))
        if lt.size(artistasEnRango) >=3:
            for i in range (0,3):       
                print("|Nombre: "+artistsMostrar[i]["DisplayName"]+"|FechaDeNacimiento: "+artistsMostrar[i]["BeginDate"]+"|FechaDeFallecimiento: "+artistsMostrar[i]["EndDate"]+"|Nacionalidad: "+artistsMostrar[i]["Nationality"]+"|Genero: "+artistsMostrar[i]["Gender"])
                print("")
                
            for i in range (lt.size(artistasEnRango)-3,lt.size(artistasEnRango)):
                print("|Nombre: "+artistsMostrar[i]["DisplayName"]+"|FechaDeNacimiento: "+artistsMostrar[i]["BeginDate"]+"|FechaDeFallecimiento: "+artistsMostrar[i]["EndDate"]+"|Nacionalidad: "+artistsMostrar[i]["Nationality"]+"|Genero: "+artistsMostrar[i]["Gender"])
                print("")    
        else: 
             for i in lt.iterator(artistasEnRango):
                 print("|Nombre: "+i["DisplayName"]+"|FechaDeNacimiento: "+i["BeginDate"]+"|FechaDeFallecimiento: "+i["EndDate"]+"|Nacionalidad: "+i["Nationality"]+"|Genero: "+i["Gender"]) 
        
    elif int(inputs[0]) == 3:
        start_time = time.process_time()
        fechaInicial=input("Ingrese la fecha que desee consultar como rango inicial de las adquisisiones: ")
        fechaFinal=input("Ingrese la fecha que desee consultar como rango final de las adquisisiones: ")
        listAdquisisiones=listarAdquisisionesCronologicamente(catalog,fechaInicial,fechaFinal)
        print("") 
        print("El MoMA adquirio "+str(lt.size(listAdquisisiones))+" piezas unicas entre "+fechaInicial+" y "+fechaFinal) 
        compradas=0          
        for i in lt.iterator(listAdquisisiones):
            creditLine=i["CreditLine"]
            if creditLine == "Purchase":
               compradas+=1
        print("")     
        print("Con un total de "+str(compradas)+" obras compradas.")  
        print("")
        print("Las primeras y ultimas 3 obras en este rango son: ")
        print("")
        artworksMostrar=(list(lt.iterator(listAdquisisiones)))
        for i in range (0,3):
             print("|Titulo: "+artworksMostrar[i]["Title"]+"|Artista(s): "+artworksMostrar[i]["ConstituentID"]+"|Fecha: "+artworksMostrar[i]["Date"]+"|Medio: "+artworksMostrar[i]["Medium"]+"|Dimensiones: "+artworksMostrar[i]["Dimensions"])
             print("")
        for i in range (lt.size(listAdquisisiones)-3,lt.size(listAdquisisiones)):
             print("|Titulo: "+artworksMostrar[i]["Title"]+"|Artista(s): "+artworksMostrar[i]["ConstituentID"]+"|Fecha: "+artworksMostrar[i]["Date"]+"|Medio: "+artworksMostrar[i]["Medium"]+"|Dimensiones: "+artworksMostrar[i]["Dimensions"])
             print("")
    elif int(inputs[0]) == 4:
         nombreArtista=input("Ingrese el nombre del artista que desea consultar: ") 
         listObrasPorArtista=obrasPorArtista(catalog,nombreArtista)
         obras=listObrasPorArtista[0]
         id=listObrasPorArtista[1]
         print("")
         print (nombreArtista+" con MoMA ID "+id+" tiene "+str(lt.size(obras))+" piezas con su nombre en el museo.")
         tecniques={}
         for i in lt.iterator(obras):
             tecnique=i["Medium"]
             if tecnique not in tecniques: 
                 tecniques[tecnique]=1
             else:
                  tecniques[tecnique]+=1
         print("")
         print("Hay "+str(len(tecniques))+" diferentes tecnicas/medios en sus trabajos.")
         tecniquesValues=list(tecniques.values())
         tecniquesKeys=list(tecniques.keys())
         maxTecnique=max(tecniquesValues)
         maxTecniqueName=""
         for i in tecniquesKeys: 
             num=tecniques[i]
             if num == maxTecnique :
                maxTecniqueName=i 
                print("")
                print("La tecnica más usada por el/la artista es "+ i +",con la cual tiene los siguientes ejemplares:")
                print("")
                break
         for obra in lt.iterator(obras):   
             tecnique=obra["Medium"]
             if tecnique == maxTecniqueName: 
                print("|Titulo: "+obra["Title"]+"|Fecha: "+obra["Date"]+"|Medio: "+obra["Medium"]+"|Dimensiones: "+obra["Dimensions"])
                print("")

    elif int(inputs[0]) == 6:     
         departamento=input("Ingrese el nombre del departamento que quiere consultar: ")
         departamento=departamento.strip()
         listDepartamento=lstDepartamento(catalog,departamento)
         print("")
         print("El MoMA va a transportar "+str(lt.size(listDepartamento))+" obras del departamento de "+departamento)
         pesoTotalEstimado=0.0 
         for i in lt.iterator(listDepartamento):
             pesoPorObra=i["Weight (kg)"]
             if pesoPorObra != "": 
                pesoPorObra=float(pesoPorObra) 
                pesoTotalEstimado += pesoPorObra 
         print("")       
         print("El peso estimado de la carga en Kg es :" + str(pesoTotalEstimado))
         precioTotalEstimado=0.0
         for j in lt.iterator(listDepartamento):
             precio=j["CostoObra"]
             precioTotalEstimado+=precio
         print("")       
         print("El costo estimado de la carga en USD es :" + str(round(precioTotalEstimado,3)))
         preciosOrdenadosFecha=ordenarPorFecha(listDepartamento)
         preciosOrdenadosCosto=ordenarPorCosto(listDepartamento)
         print("")       
         print("Las 5 obras más antiguas para transportar son:")
         print("")   
         obrasMostrar=list(lt.iterator(preciosOrdenadosFecha))
         mostradas=0
         i=0
         while i < len(obrasMostrar) and mostradas <5 :
              fecha= obrasMostrar[i]["Date"]
              if fecha != "":
                 print("|Titulo: "+obrasMostrar[i]["Title"]+"|Artista(s): "+obrasMostrar[i]["ConstituentID"]+"|Clasificación: "+obrasMostrar[i]["Classification"]+"|Fecha: "+obrasMostrar[i]["Date"]+"|Medio: "+obrasMostrar[i]["Medium"]+"|Dimensiones: "+obrasMostrar[i]["Dimensions"]+"|Costo(USD): "+str(round(obrasMostrar[i]["CostoObra"],3)))
                 print("")
                 mostradas+=1
                 i+=1
              else:
                   i+=1   
         print("")       
         print("Las 5 obras más costosas para transportar son:")
         print("")   
         obrasMostrar=list(lt.iterator(preciosOrdenadosCosto))
         mostradas=0
         i=len(obrasMostrar)-1
         while i > 0 and mostradas <5 :
              costo= obrasMostrar[i]["CostoObra"]
              if costo != "":
                 print("|Titulo: "+obrasMostrar[i]["Title"]+"|Artista(s): "+obrasMostrar[i]["ConstituentID"]+"|Clasificación: "+obrasMostrar[i]["Classification"]+"|Fecha: "+obrasMostrar[i]["Date"]+"|Medio: "+obrasMostrar[i]["Medium"]+"|Dimensiones: "+obrasMostrar[i]["Dimensions"]+"|Costo(USD): "+str(round(obrasMostrar[i]["CostoObra"],3)))
                 print("")
                 mostradas+=1
                 i-=1
              else:
                   i-=1   
 
    elif int(inputs[0]) == 0:    
         sys.exit(0)
    else:
        sys.exit(0)
sys.exit(0)
