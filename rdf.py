import csv
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

# Crear un gráfico RDF
g = Graph()

# Definir un namespace personalizado
EX = Namespace("http://example.org/")

# Leer el CSV
with open("tu_archivo.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Crear un URI para cada fila
        subject = URIRef(EX + row['id'])  # Ajusta 'id' al campo clave de tu CSV
        
        # Añadir las propiedades
        for key, value in row.items():
            g.add((subject, URIRef(EX + key), Literal(value)))

# Guardar el RDF en un archivo
g.serialize("salida.rdf", format="turtle")  # Puedes cambiar el formato a "xml" o "nt"
