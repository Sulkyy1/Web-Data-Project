from rdflib import Graph, Namespace, URIRef, Literal, RDF, XSD
import csv
import uuid

# Crear un grafo RDF
g = Graph()

# Definir un namespace personalizado
EX = Namespace("http://example.org/")

# Añadir prefijos al grafo
g.bind("ex", EX)

# Cargar CSVs
csv_regiones = './data-clean/regiones.csv'     # regiones
csv_comunas = './data-clean/comunas.csv'       # comunas

# Diccionario para almacenar las regiones en las que está cada comuna
regiones = {}

# Crear las Regiones
with open(csv_regiones, mode='r', newline='', encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        # Crear un sujeto único para la región utilizando el cut_region
        id_region = row['cut_region']
        sujeto_region = URIRef(EX[f"Region/{id_region}"])
        
        # Añadir tripletas al grafo para la región
        g.add((sujeto_region, RDF.type, EX.Region))
        g.add((sujeto_region, EX.nombre, Literal(row['region'], datatype=XSD.string)))
        g.add((sujeto_region, EX.cut, Literal(id_region, datatype=XSD.integer)))
        
        # Guardar la referencia de la región con su id (cut_region)
        regiones[id_region] = sujeto_region

# Crear las Comunas
with open(csv_comunas, mode='r', newline='', encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        # Crear un sujeto único para la comuna utilizando el cut_comuna
        id_comuna = row['cut_comuna']
        id_region = row['cut_region']
        sujeto_comuna = URIRef(EX[f"Comuna/{id_comuna}"])
        
        # Añadir tripletas al grafo para la comuna
        g.add((sujeto_comuna, RDF.type, EX.Comuna))
        g.add((sujeto_comuna, EX.nombre, Literal(row['comuna'], datatype=XSD.string)))
        g.add((sujeto_comuna, EX.cut, Literal(id_comuna, datatype=XSD.integer)))
        
        # Relacionar la comuna con su región usando el campo 'cut_region' para buscar la región
        if id_region in regiones:
            g.add((sujeto_comuna, EX.isPartOf, regiones[id_region]))

# Guardar en un archivo en formato Turtle
with open("./output_rdf.rdf", "w", encoding='utf-8') as f:
    f.write(g.serialize(format='turtle'))

