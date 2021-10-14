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
    catalog={"artists":None,"artworks":None ,"medio/tecnica":None}
    catalog['artists'] = lt.newList('SINGLE_LINKED')
    catalog['artworks'] = lt.newList('SINGLE_LINKED')
    catalog["ConstituentID-Artists"] = mp.newMap(maptype='PROBING',loadfactor=0.50)
    catalog["medio/tecnica"] = mp.newMap(maptype='PROBING',loadfactor=0.50)
    catalog["Nacionalidad"]=mp.newMap(maptype='PROBING',loadfactor=0.50)
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

# Funciones para creacion de datos

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

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpDate(obra1,obra2): 
    return ((str(obra1['Date']) < str(obra2['Date'])))

# Funciones de ordenamiento
