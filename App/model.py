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
    catalog["medio/tecnica"] = mp.newMap(maptype='PROBING',loadfactor=0.50)
    catalog["Nacionalidad"]=mp.newMap(maptype='PROBING',loadfactor=0.50)
    catalog["BeginDate"]=mp.newMap(numelements=1000,maptype='PROBING',loadfactor=0.50)
    catalog["DateAcquired"]=mp.newMap(maptype='PROBING',loadfactor=0.50)
    return catalog

# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):              
    lt.addLast(catalog['artists'], artist)
    mp.put(catalog["ConstituentID-Artists"],artist["ConstituentID"],[])
def addArtwork(catalog, artwork):              
    lt.addLast(catalog['artworks'], artwork)
    mp.put(catalog["medio/tecnica"],artwork["Medium"],artwork) 
   
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

def addNacionalidadesId(catalog):
    artistas=catalog["artists"]
    nacionalidades={}
    for artista in lt.iterator(artistas):
         nacionalidad=artista["Nationality"]
         id=artista["ConstituentID"]
         if nacionalidad not in nacionalidades: 
            nacionalidades[nacionalidad]=id
         else: 
              valor=list(nacionalidades[nacionalidad])
              valor.append(id)
              nacionalidades[nacionalidad]=valor
    keys_nacionalidades=nacionalidades.keys()
    for nacionalidad in keys_nacionalidades: 
        valor=nacionalidades[nacionalidad]
        mp.put(catalog["Nacionalidad"],nacionalidad,valor) 

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


# Funciones de consulta
def medioEspecifico(obraPorMedios,medio): 
    obrasEnMedio=mp.get(obraPorMedios,medio)
    listR=lt.newList('SINGLE_LINKED')
    for obra in lt.iterator(obrasEnMedio):
        lt.addLast(listR,obra)
    listR=merge.sort(listR, cmpDate)   
    return listR 

def obrasNacionalidad(catalog,nacionalidad):
    listR=lt.newList('SINGLE_LINKED')
    llaveValor=mp.get(catalog["Nacionalidad"],nacionalidad)
    ids=llaveValor["value"]
    for id in ids:
        if id != "0":
           llaveValorDos=mp.get(catalog["ConstituentID-Artists"],id)
           if llaveValorDos != None:
              obrasDeLaId=llaveValorDos["value"]
              for obra in obrasDeLaId:
                   lt.addLast(listR,obra)
    return listR    

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

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpDate(obra1,obra2): 
    return ((str(obra1['Date']) < str(obra2['Date'])))


