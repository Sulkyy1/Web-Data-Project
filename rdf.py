import csv
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

# Crear un grafo RDF
g = Graph()

# Definir un namespace personalizado
EX = Namespace("http://example.org/")

# Añadir prefijos al grafo
g.bind("ex", EX)

def convert_schools(filename: str):
    # Leer el CSV
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            # Crear un URI único para cada colegio
            colegio_uri = URIRef(EX + row['RBD'])  # Ajusta 'RBD' al campo clave del CSV
            
            # Añadir el tipo del recurso
            g.add((colegio_uri, RDF.type, EX.Colegio))

            # Añadir las propiedades del recurso
            g.add((colegio_uri, EX.nombre, Literal(row['NOM_RBD'])))
            g.add((colegio_uri, EX.CodDep, Literal(row['COD_DEPE'])))
            g.add((colegio_uri, EX.CodDep2, Literal(row['COD_DEPE2'])))
            g.add((colegio_uri, EX.Rural, Literal(row['RURAL_RBD'])))

def convert_sned(filename: str):
    # Leer el CSV
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            # Crear un URI único para cada colegio
            colegio_uri = URIRef(EX + row['RBD'])  # Ajusta 'RBD' al campo clave del CSV
            
            # Añadir las propiedades del recurso
            g.add((colegio_uri, EX.Promedio, Literal(row['Promedio'])))

# Guardar el RDF en un archivo
g.serialize("colegios.rdf", format="turtle")
