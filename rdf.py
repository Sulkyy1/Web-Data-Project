import csv
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

# Crear un grafo RDF
g = Graph()

# Definir un namespace personalizado
EX = Namespace("http://example.org/")

# Añadir prefijos al grafo
g.bind("ex", EX)

# Leer el CSV
with open("tu_archivo.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Crear un URI para cada fila
        subject = URIRef(EX + row['RBD'])  # Ajusta 'RBD' al campo clave del CSV
        
        # Añadir las propiedades
        for key, value in row.items():
            if key == 'NOM_RBD':
                g.add((subject, URIRef(EX + 'nombre'), Literal(value)))
            

# Guardar el RDF en un archivo
g.serialize("salida.rdf", format="turtle")
