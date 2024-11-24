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
csv_delincuencia = '../data-clean/cead_delincuencia_chile_random_sample.csv'  
with open(csv_delincuencia, mode='r', newline='', encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=';') 
    for row in reader:
        # Crear un sujeto único utilizando un UUID
        id = uuid.uuid4()
        sujeto = URIRef((EX[f"Delito/{id}"]))
        
        #Añadir tripletas al grafo
        g.add((sujeto, RDF.type, EX.Delito))
        g.add((sujeto, EX.tipo, Literal(row['delito'], datatype=XSD.string)))
        g.add((sujeto, EX.cantidad, Literal(row['delito_n'], datatype=XSD.int)))
        g.add((sujeto, EX.fecha, Literal(row['fecha'], datatype=XSD.date)))
        
        
# Guardar en un archivo en formato Turtle
with open("../output_delincuencia.rdf", "w", encoding='utf-8') as f:
    f.write(g.serialize(format='turtle'))

# Mostrar el grafo RDF en pantalla
print(g.serialize(format='turtle'))

