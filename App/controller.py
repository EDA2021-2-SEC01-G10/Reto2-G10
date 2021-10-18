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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog
# Funciones para la carga de datos
def loadData(catalog):
    loadArtists(catalog)
    loadArtworks(catalog)
    loadArtworksID(catalog)
    loadBeginDates(catalog)
    loadDateAcquired(catalog)
    loadDepartaments(catalog)

def loadArtists(catalog):
    artistsfile = cf.data_dir + 'MoMA/Artists-utf8-large.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist) 

def loadArtworks(catalog):
    artworksfile = cf.data_dir + 'MoMA/Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(artworksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)  

def loadArtworksID(catalog):
    model.addObrasPorId(catalog)

def loadBeginDates(catalog):
    model.addBeginDate(catalog)    
def loadDateAcquired(catalog):
    model.addDateAcquired(catalog) 
def loadDepartaments(catalog):
    model.addDepartaments(catalog)



# Funciones de consulta sobre el catálogo
def artEnRango(catalog,añoInicial,añoFinal):
    lista=model.artEnRango(catalog,añoInicial,añoFinal)
    return lista
def listarAdquisisiones(catalog,fechaInicial,fechaFinal):
    listR=model.listarAdquisisiones(catalog,fechaInicial,fechaFinal)    
    return listR
def obrasArtista(catalog,nombreArtista): 
    listR=model.obrasArtista(catalog,nombreArtista)
    return listR 
       
def lstDepartamento(catalog,departamento):
    listaDepartamento=obtenerLista(catalog,departamento)
    agregarPrecio=preciosObras(listaDepartamento)
    return agregarPrecio

def obtenerLista(catalog,departamento):
    listR=model.listaDepartamento(catalog,departamento)
    return listR

def first3(lista):
    return model.first3(lista)

def last3(lista):
    return model.last3(lista)

def getObrasArt(catalog, ids):

    return model.getObrasArt(catalog, ids)

def firulais123(catalog):
    
    return model.topNat(catalog)

def preciosObras(listaDepartamento):
    listConPrecios=model.addPrecios(listaDepartamento)  
    return listConPrecios

# Funciones de ordenamiento 
def ordenarPorCosto(precios):
    listOrdenada=model.ordenarPorCosto(precios)   
    return listOrdenada

def ordenarPorFecha(precios):
    listOrdenada=model.ordenarPorFecha(precios)
    return listOrdenada 
    


def searchCID (list_art, idAw):
    return model.searchCID (list_art, idAw)