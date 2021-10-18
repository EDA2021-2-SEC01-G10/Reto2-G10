"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

from datetime import datetime 
import time
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog={"artists":None,"artworks":None}
    catalog['artists'] = lt.newList('SINGLE_LINKED')
    catalog['artworks'] = lt.newList('SINGLE_LINKED')
    catalog["ConstituentID-Artists"] = mp.newMap(maptype='PROBING',loadfactor=0.50)
    catalog["Nacionalidad"]=mp.newMap(maptype='PROBING',loadfactor=0.50)
    catalog["BeginDate"]=mp.newMap(numelements=1000,maptype='PROBING',loadfactor=0.50)
    catalog["DateAcquired"]=mp.newMap(maptype='PROBING',loadfactor=0.50)
    catalog["Departament"]=mp.newMap(maptype='PROBING',loadfactor=0.50)
    return catalog

# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):              
    lt.addLast(catalog['artists'], artist)
    mp.put(catalog["ConstituentID-Artists"],artist["ConstituentID"],catalog["Nacionalidad"])
def addArtwork(catalog, artwork):              
    lt.addLast(catalog['artworks'], artwork)
   
   
def addObrasPorId(catalog):  
    obras=catalog["artworks"]
    for obra in lt.iterator(obras):
       idObra=obra["ConstituentID"]
       idObra=idObra.replace("]","")
       idObra=idObra.replace("[","")
       idObra=idObra.split(",")
       for id in idObra:
           value=mp.get(catalog["ConstituentID-Artists"],id)
           if value != None: 
              valor=value["value"]
              valor.append(obra)
              mp.put(catalog["ConstituentID-Artists"],id,valor)


def addBeginDate(catalog):       
    artistas=catalog["artists"]
    fechas={}
    for artista in lt.iterator(artistas):
        beginDate=artista["BeginDate"]
        listaApp=[]
        dictArt={}
        dictArt["DisplayName"]=artista["DisplayName"]
        dictArt["BeginDate"]=beginDate
        fallecimiento=artista["EndDate"]
        if fallecimiento != "" and fallecimiento != "0" :
            dictArt["EndDate"]=fallecimiento
        else: 
            dictArt["EndDate"]="Unknown"    
        nacionalidad=artista["Nationality"]   
        if nacionalidad != "": 
            dictArt["Nationality"]=nacionalidad
        else: 
             dictArt["Nationality"]="Unknown"     
        genero=artista["Gender"]
        if genero != "": 
           dictArt["Gender"]=genero
        else: 
             dictArt["Gender"]="Unknown"   
        listaApp.append(dictArt)
        if beginDate not in fechas: 
           fechas[beginDate]=listaApp
        else: 
             valor=fechas[beginDate]
             valor.append(dictArt)
             fechas[beginDate]=valor            
    keysFechas=fechas.keys()
    keysFechasOr=sorted(keysFechas)
    for fecha in keysFechasOr:
        artistas=fechas[fecha]
        mp.put(catalog["BeginDate"],fecha,artistas)    

def addDateAcquired(catalog):
    obras=catalog["artworks"]
    fechas={}
    for obra in lt.iterator(obras):
        dateAcquired=obra["DateAcquired"]
        listaApp=[]
        dictArt={}
        dictArt["Title"]=obra["Title"]
        dictArt["ConstituentID"]=obra["ConstituentID"]
        dictArt["Date"]=obra["Date"]
        dictArt["Medium"]=obra["Medium"]
        dictArt["Dimensions"]=obra["Dimensions"]
        dictArt["CreditLine"]=obra["CreditLine"]
        listaApp.append(dictArt)
        if dateAcquired not in fechas: 
           fechas[dateAcquired]=listaApp
        else: 
             valor=fechas[dateAcquired]
             valor.append(dictArt)
             fechas[dateAcquired]=valor
    keysFechas=fechas.keys()
    keysFechasOr=sorted(keysFechas)
    for fecha in keysFechasOr:
        obras=fechas[fecha]
        mp.put(catalog["DateAcquired"],fecha,obras)             

def addDepartaments(catalog):
    obras=catalog["artworks"]
    departamentos={}
    for obra in lt.iterator(obras):
        departamento=obra["Department"]
        listaObras=[]
        dictObra={}
        dictObra["Department"]=obra["Department"]
        dictObra["Title"]=obra["Title"]
        dictObra["ConstituentID"]=obra["ConstituentID"]
        dictObra["Date"]=obra["Date"]
        dictObra["Medium"]=obra["Medium"]
        dictObra["Dimensions"]=obra["Dimensions"]
        dictObra["Height (cm)"] =obra["Height (cm)"] 
        dictObra["Width (cm)"]=obra["Width (cm)"]
        dictObra["Weight (kg)"] =obra["Weight (kg)"] 
        dictObra["Depth (cm)"]=obra["Depth (cm)"]
        dictObra["Classification"]=obra["Classification"]    
        listaObras.append(dictObra)
        if departamento not in departamentos: 
            departamentos[departamento]=listaObras
        else: 
             valor=departamentos[departamento]
             valor.append(dictObra)
             departamentos[departamento]=valor    
    keysDepartamentos=departamentos.keys()
    for departamento in departamentos: 
        obras=departamentos[departamento]
        mp.put(catalog["Departament"],departamento,obras)


# Funciones de consulta
def artEnRango(catalog,añoInicial,añoFinal):   
    listR=lt.newList('SINGLE_LINKED')
    fechas=catalog["BeginDate"]
    fechasKeysSet=mp.keySet(fechas)
    fechasKeys=[]
    for fch in lt.iterator(fechasKeysSet):
        fechasKeys.append(fch)
    fechasKeys.sort()    
    for fecha in fechasKeys: 
        if int(fecha) >= añoInicial and int(fecha) <= añoFinal :
           artistas=mp.get(fechas,fecha)["value"]
           for artist in artistas:
               lt.addLast(listR,artist) 
        elif int(fecha) > añoFinal: 
             break 
    return listR    

def listarAdquisisiones(catalog,fechaInicial,fechaFinal): 
    listR=lt.newList('SINGLE_LINKED')
    fechas=catalog["DateAcquired"]
    fechasKeysSet=mp.keySet(fechas)
    fechasKeys=[]
    for fch in lt.iterator(fechasKeysSet):
        fechasKeys.append(fch)
    fechasKeys.sort()    
    fechaInDate = datetime.strptime(fechaInicial.strip(), "%Y-%m-%d")
    fechaFinDate= datetime.strptime(fechaFinal.strip(), "%Y-%m-%d")
    for fecha in fechasKeys: 
        if fecha != "":
           fechaCom=datetime.strptime(fecha.strip(), "%Y-%m-%d")
           if fechaCom >= fechaInDate and fechaCom <= fechaFinDate: 
               obras=mp.get(fechas,fecha)["value"]
               for obra in obras: 
                   lt.addLast(listR,obra)
           elif fechaCom > fechaFinDate:
                break 
    return listR      

def getObrasArt(catalog, ids):

    artists = ""
    ids1 = ids.replace("[", "").replace("]", "").split(",")
    for x in ids1:
        x = x.strip()
        NaRepetida = mp.contains(catalog["ConstituentID-Artists"], x)
        if NaRepetida:
            pareja = mp.get(catalog["ConstituentID-Artists"], x)
            value = me.getValue(pareja)
            name = value["Nombre"]
        artists += name + " "
    return artists

def obrasArtista(catalog,nombreArtista): 
    obras=lt.newList('SINGLE_LINKED')
    artistas=catalog["artists"]
    id=""
    for artist in lt.iterator(artistas):
        nombre=artist["DisplayName"]
        if nombre.strip() == nombreArtista.strip(): 
           id=artist["ConstituentID"]       
    obrasPorID=catalog["ConstituentID-Artists"]
    obrasDelArtista=mp.get(obrasPorID,id)["value"]
    for obra in obrasDelArtista:
        lt.addLast(obras,obra)
    return (obras,id)

def listaDepartamento(catalog,departamento):
    obrasPorDepartamento=lt.newList('SINGLE_LINKED')
    departamentos=catalog["Departament"] 
    depKeysSet=mp.keySet(departamentos)
    depKeys=[]
    for departament in lt.iterator(depKeysSet):
        depKeys.append(departament)
    for depar in depKeys:
        if depar == departamento :
           obras=mp.get(departamentos,depar)["value"]
           for obra in obras: 
               lt.addLast(obrasPorDepartamento,obra)          
    print (obrasPorDepartamento)           
    return obrasPorDepartamento        
    

def addPrecios(listaDepartamento):  
    preciosObras=lt.newList("ARRAY_LIST")
    for i in lt.iterator(listaDepartamento): 
        dimension=i["Dimensions"]
        if dimension != "":
            dimensiones=[]
            alturaObra=i["Height (cm)"] 
            anchuraObra=i["Width (cm)"]    
            profundidadObra=i["Depth (cm)"]  
            if alturaObra != "" and alturaObra != "0": 
                alturaObra=float(alturaObra)/100
                dimensiones.append(alturaObra)
            if anchuraObra != "" and anchuraObra != "0": 
                anchuraObra=float(anchuraObra)/100
                dimensiones.append(anchuraObra) 
            if profundidadObra != "" and profundidadObra != "0": 
                profundidadObra=float(profundidadObra)/100
                dimensiones.append(profundidadObra) 
            productoDimensiones=1   
            for dimension in dimensiones:
                productoDimensiones*=dimension        
            preciosObra=[]   
            preciosObra.append(productoDimensiones * 72.00)
            peso=i["Weight (kg)"]   
            if peso != "" and peso != "0": 
               peso=float(peso)  
               preciosObra.append(peso*72.00)
            precioMayor=max(preciosObra)
            i["CostoObra"]=precioMayor             
            lt.addLast(preciosObras,i)  
        else: 
             i["CostoObra"]=48.00        
             lt.addLast(preciosObras,i)      

    return preciosObras   
#Funciones de ordenamiento 
def ordenarPorCosto(precios):
    obrasConPrecio=lt.newList("ARRAY_LIST")  
    for obra in lt.iterator(precios):
         lt.addLast(obrasConPrecio,obra)
    obrasConPrecioOrdenados=merge.sort(obrasConPrecio,cmpArtworkByCost)    
    return obrasConPrecioOrdenados 

def ordenarPorFecha(precios):     
    obrasPorFecha=lt.newList("ARRAY_LIST")  
    for obra in lt.iterator(precios):
         lt.addLast(obrasPorFecha,obra)
    obrasPorFechaOrdenadas=merge.sort(obrasPorFecha,cmpArtworkByDate)    
    return obrasPorFechaOrdenadas 


def ordenarArtNac (catalog):
    sub_list1 = lt.subList(catalog, 1, lt.size(catalog))
    sub_list1 = sub_list1.copy()
    sort_list = merge.sort(sub_list1, cmpArtNum)
    return sort_list


# Funciones utilizadas para comparar elementos dentro de una lista

def cmpArtworkByCost (artwork1,artwork2): 
    """
     Devuelve verdadero (True) si el 'CostoObra' de artwork1 es menor que el de artwork2
     Args:
     artwork1: informacion del primer artwork que incluye su valor 'CostoObra'
     artwork2: informacion del segundo artwork que incluye su valor 'CostoObra'
    """
    return ((float(artwork1['CostoObra']) < float(artwork2['CostoObra'])))

def cmpArtworkByDate(artwork1,artwork2): 
    """
     Devuelve verdadero (True) si el 'Date' de artwork1 es menor que el de artwork2
     Args:
     artwork1: informacion del primer artwork que incluye su valor 'Date'
     artwork2: informacion del segundo artwork que incluye su valor 'Date'
    """    
    return ((str(artwork1['Date']) < str(artwork2['Date'])))

def cmpArtNum(n1, n2):
    num1 = n1["Artworks"]
    num2 = n2["Artworks"]

    if num1 > num2:
        return True
    else:
        return False

def searchCID (list_art, idAw):

    size = lt.size(list_art)
    x = 1

    id_com = idAw.strip("[]")

    while x < size:
        element1 = lt.getElement(list_art, x)
        co_id = element1["ConstituentID"]
        if co_id in id_com:
            return element1["DisplayName"]
        x += 1

def first3(list):
    first = lt.subList(list,1,3)
    return first

def last3(lista):
    last = lt.subList(lista,lt.size(lista)-2,3)
    return last


def compSize(n1, n2):
    return (lt.size(n1["artworks"]) > lt.size(n2["artworks"]))

def topNat(catalog):

    keys = mp.keySet(catalog["Nacionalidad"])
    topNa = lt.newList()
    for x in lt.iterator(keys):
        entry = mp.get(catalog["Nacionalidad"], x)
        nac = me.getValue(entry)
        lt.addLast(topNa, nac)
    merge.sort(topNa, cmpfunction = compSize)

    return topNa


