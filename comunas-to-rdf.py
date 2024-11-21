import csv
import uuid
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD, RDFS


# Crear un grafo RDF
g = Graph()

# Definir un namespace personalizado
EX = Namespace("http://example.org/")

# Añadir prefijos al grafo
g.bind("ex", EX)

# Cargar el CSV de delincuencia
csv_comunas = './comunas.csv'  
with open(csv_comunas, mode='r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';') 
    for row in reader:
        # Crear un sujeto único utilizando el cut de la comuna
        id = uuid.uuid4()
        sujeto = URIRef((EX[f"Comuna/{id}"]))
        
        #Añadir tripletas al grafo
        g.add((sujeto, RDF.type, EX.Comuna))
        g.add((sujeto, EX.nombre, Literal(row['comuna'], datatype=XSD.string)))
        g.add((sujeto, EX.cut, Literal(row['cut_comuna'], datatype=XSD.integer)))
            
# Guardar en un archivo en formato Turtle
with open("output_comuna.rdf", "w", encoding='utf-8') as f:
    f.write(g.serialize(format='turtle'))

# Mostrar el grafo RDF en pantalla
print(g.serialize(format='turtle'))

