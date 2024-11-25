import csv
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

# Crear un grafo RDF
g = Graph()

# Definir los namespaces
EX = Namespace("http://example.org/")
QB = Namespace("http://purl.org/linked-data/cube#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

# Añadir prefijos al grafo
g.bind("ex", EX)
g.bind("qb", QB)

METRICAS = [
    "EFECTIVR", "SUPERAR", "INICIAR", "MEJORAR", "INTEGRAR", "IGUALDR", "INDICER", "SEL"
]
METRICAS_RELATIONS = {
    "EFECTIVR": EX.efectividad,
    "SUPERAR": EX.superacion,
    "INICIAR": EX.iniciativa,
    "MEJORAR": EX.mejoramiento,
    "INTEGRAR": EX.integracion,
    "IGUALDR": EX.igualdad,
    "INDICER": EX.indiceSNED,
    "SEL": EX.seleccionado
}

METRICAS_NAMES = {
    "EFECTIVR": "efectividad",
    "SUPERAR": "superacion",
    "INICIAR": "iniciativa",
    "MEJORAR": "mejoramiento",
    "INTEGRAR": "integracion",
    "IGUALDR": "igualdad",
    "INDICER": "indiceSNED",
    "SEL": "seleccionado"
}

dataset_uris = {}
for metrica in METRICAS:
    # Crear el conjunto de datos Data Cube para cada metrica
    dataset_uris[metrica] = EX[f'{metrica}_Dataset']
    g.add((dataset_uris[metrica], RDF.type, QB.DataSet))
    g.add((dataset_uris[metrica], EX['title'], Literal(f"{METRICAS_NAMES[metrica]} de colegios por año")))

dataset_uris["codDep"] = EX[f'codDep_Dataset']
g.add((dataset_uris["codDep"], RDF.type, QB.DataSet))
g.add((dataset_uris["codDep"], EX['title'], Literal(f"código de dependencia de colegios por año")))

dataset_uris["rural"] = EX[f'rural_Dataset']
g.add((dataset_uris["rural"], RDF.type, QB.DataSet))
g.add((dataset_uris["rural"], EX['title'], Literal(f"ruralidad de colegios por año")))

def convert_schools(filename: str, anio: int):
    # Leer el CSV
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            # Crear un URI único para cada colegio
            colegio_uri = URIRef((EX[f"colegio/{row['RBD']}"]))  # Ajusta 'RBD' al campo clave del CSV
            
            # Añadir el tipo del recurso
            g.add((colegio_uri, RDF.type, EX.Colegio))

            # Añadir las propiedades del recurso
            g.add((colegio_uri, EX.rbd, Literal(row['RBD'])))
            g.add((colegio_uri, EX.nombre, Literal(row['NOM_RBD'])))

            # Añadir observaciones para las métricas
            for metrica in METRICAS:

                obs_uri = URIRef((EX[f"obs/{row['RBD']}/{anio}/{metrica}"]))

                # Añadir el tipo de la observación y su dataset
                g.add((obs_uri, RDF.type, QB.Observation))
                g.add((obs_uri, QB.dataSet, dataset_uris[metrica]))

                # Añadir las tripletas de la observación
                g.add((obs_uri, EX.colegio, colegio_uri))
                g.add((obs_uri, EX.anio, Literal(anio, datatype=XSD.gyear)))
                g.add((obs_uri, METRICAS_RELATIONS[metrica], Literal(row[metrica], datatype=XSD.float)))

            # Observacion para el codigo de dependencia
            obs_uri = URIRef((EX[f"obs/{row['RBD']}/{anio}/codDep"]))

            # Añadir el tipo de la observación y su dataset
            g.add((obs_uri, RDF.type, QB.Observation))
            g.add((obs_uri, QB.dataSet, dataset_uris["codDep"]))

            # Añadir las tripletas de la observación
            g.add((obs_uri, EX.colegio, colegio_uri))
            g.add((obs_uri, EX.anio, Literal(anio, datatype=XSD.gyear)))
            g.add((obs_uri, EX.codDep, Literal(row['COD_DEPE2'], datatype=XSD.int)))

            # Observacion para ruralidad
            obs_uri = URIRef((EX[f"obs/{row['RBD']}/{anio}/rural"]))

            # Añadir el tipo de la observación y su dataset
            g.add((obs_uri, RDF.type, QB.Observation))
            g.add((obs_uri, QB.dataSet, dataset_uris["rural"]))

            # Añadir las tripletas de la observación
            g.add((obs_uri, EX.colegio, colegio_uri))
            g.add((obs_uri, EX.anio, Literal(anio, datatype=XSD.gyear)))
            g.add((obs_uri, EX.rural, Literal(row['RURAL_RBD'], datatype=XSD.int)))

filenames = ['./data-clean/SNED_2018_2019_clean.csv', './data-clean/SNED_2020_2021_clean.csv', './data-clean/SNED_2022_2023_clean.csv']

for filename in filenames:
    anio = int(filename.split('_')[2])
    print(f"Convirtiendo colegios del archivo {filename}")
    convert_schools(filename, anio)

# Guardar el RDF en un archivo
g.serialize("colegios.rdf", format="turtle")
