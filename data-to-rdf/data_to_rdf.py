from rdflib import BNode, Graph, Namespace, URIRef, Literal, RDF, XSD
import csv
import uuid

# Crear un grafo RDF
g = Graph()

# Definir un namespace personalizado
EX = Namespace("http://example.org/")
QB = Namespace("http://purl.org/linked-data/cube#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

# Añadir prefijos al grafo
g.bind("ex", EX)
g.bind("qb", QB)

# Cargar CSVs
csv_regiones = './data-clean/regiones.csv'                 # regiones
csv_comunas = './data-clean/comunas.csv'                   # comunas
csv_delincuencia = './data-clean/delincuencia_clean.csv'   # delincuencia

# Diccionario para almacenar las regiones en las que está cada comuna
regiones = {}
# Diccionario para almacenar las comunas en las que ocurre cada delito y colegio
comunas ={}

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

        # Guardar la referencia de la comuna con su id (cut_comuna)
        comunas[id_comuna] = sujeto_comuna

# Crear los Delitos
with open(csv_delincuencia, mode='r', newline='', encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=';') 
    for row in reader:
        # Crear un sujeto único utilizando un UUID
        id_comuna = row['cut_comuna']
        id = uuid.uuid4()
        sujeto_delito = URIRef((EX[f"Delito/{id}"]))
        
        #Añadir tripletas al grafo
        g.add((sujeto_delito, RDF.type, EX.Delito))
        g.add((sujeto_delito, EX.tipo, Literal(row['delito'], datatype=XSD.string)))
        g.add((sujeto_delito, EX.cantidad, Literal(row['delito_n'], datatype=XSD.int)))
        g.add((sujeto_delito, EX.fecha, Literal(row['fecha'], datatype=XSD.date)))

        # Relacionar el delito con su comuna usando el campo 'cut_comuna' para buscar la comuna
        if id_comuna in comunas:
            g.add((sujeto_delito, EX.happenedIn, comunas[id_comuna]))

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

'''
# Definición de la estructura del conjunto de datos
ex:gdpStructure a qb:DataStructureDefinition ;
    qb:component [ qb:dimension ex:country ] ;
    qb:component [ qb:dimension ex:year ] ;
    qb:component [ qb:measure ex:gdp ] ;
    qb:component [ qb:attribute ex:currency ] .
'''

dataset_uris = {}
structure_uris = {}
for metrica in METRICAS:
    # Crear el conjunto de datos Data Cube para cada metrica
    dataset_uris[metrica] = URIRef((EX[f'{metrica}_Dataset']))
    g.add((dataset_uris[metrica], RDF.type, QB.DataSet))
    g.add((dataset_uris[metrica], EX['title'], Literal(f"{METRICAS_NAMES[metrica]} de colegios por año")))

    # Vincular el conjunto de datos con su estructura
    structure_uris[metrica] = URIRef((EX[f'{metrica}_Structure']))
    g.add((dataset_uris[metrica], QB.structure, structure_uris[metrica]))

    # Definir la estructura del conjunto de datos
    g.add((structure_uris[metrica], RDF.type, QB.DataStructureDefinition))
    
    # Crear nodos anónimos para los componentes
    component_colegio = BNode()
    component_anio = BNode()
    component_measure = BNode()

    # Componentes de la estructura
    # Dimensión: Colegio
    g.add((structure_uris[metrica], QB.component, component_colegio))
    g.add((component_colegio, QB.dimension, EX.colegio))

    # Dimensión: Año
    g.add((structure_uris[metrica], QB.component, component_anio))
    g.add((component_anio, QB.dimension, EX.anio))

    # Medida: metrica
    g.add((structure_uris[metrica], QB.component, component_measure))
    g.add((component_measure, QB.measure, METRICAS_RELATIONS[metrica]))

dataset_uris["codDep"] = URIRef((EX[f'codDep_Dataset']))
g.add((dataset_uris["codDep"], RDF.type, QB.DataSet))
g.add((dataset_uris["codDep"], EX['title'], Literal(f"código de dependencia de colegios por año")))

# Vincular el conjunto de datos con su estructura
structure_uris["codDep"] = URIRef((EX['codDep_Structure']))
g.add((dataset_uris["codDep"], QB.structure, structure_uris["codDep"]))

# Definir la estructura del conjunto de datos
g.add((structure_uris["codDep"], RDF.type, QB.DataStructureDefinition))

# Crear nodos anónimos para los componentes
component_colegio = BNode()
component_anio = BNode()
component_codDep = BNode()

# Componentes de la estructura
# Dimensión: Colegio
g.add((structure_uris["codDep"], QB.component, component_colegio))
g.add((component_colegio, QB.dimension, EX.colegio))

# Dimensión: Año
g.add((structure_uris["codDep"], QB.component, component_anio))
g.add((component_anio, QB.dimension, EX.anio))

# Medida: "codDep"
g.add((structure_uris["codDep"], QB.component, component_codDep))
g.add((component_codDep, QB.measure, EX.codDep))

dataset_uris["rural"] = URIRef((EX[f'rural_Dataset']))
g.add((dataset_uris["rural"], RDF.type, QB.DataSet))
g.add((dataset_uris["rural"], EX['title'], Literal(f"ruralidad de colegios por año")))

# Vincular el conjunto de datos con su estructura
structure_uris["rural"] = URIRef((EX['rural_Structure']))
g.add((dataset_uris["rural"], QB.structure, structure_uris["rural"]))

# Definir la estructura del conjunto de datos
g.add((structure_uris["rural"], RDF.type, QB.DataStructureDefinition))

# Crear nodos anónimos para los componentes
component_colegio = BNode()
component_anio = BNode()
component_rural = BNode()

# Componentes de la estructura
# Dimensión: Colegio
g.add((structure_uris["rural"], QB.component, component_colegio))
g.add((component_colegio, QB.dimension, EX.colegio))

# Dimensión: Año
g.add((structure_uris["rural"], QB.component, component_anio))
g.add((component_anio, QB.dimension, EX.anio))

# Medida: "rural"
g.add((structure_uris["rural"], QB.component, component_rural))
g.add((component_rural, QB.measure, EX.rural))

def convert_schools(filename: str, anio: int):
    # Leer el CSV
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            # Crear un URI único para cada colegio
            colegio_uri = URIRef((EX[f"colegio/{row['RBD']}"]))  # Ajusta 'RBD' al campo clave del CSV
            id_comuna = row['COD_COM_RBD']
            
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

            # Relacionar el colegio con su comuna usando el campo 'COD_COM_RBD' para buscar la comuna
            if id_comuna in comunas:
                g.add((colegio_uri, EX.locatedIn, comunas[id_comuna]))

filenames = ['./data-clean/SNED_2018_2019_clean.csv', './data-clean/SNED_2020_2021_clean.csv', './data-clean/SNED_2022_2023_clean.csv']

for filename in filenames:
    anio = int(filename.split('_')[2])
    print(f"Convirtiendo colegios del archivo {filename}")
    convert_schools(filename, anio)

# Guardar en un archivo en formato Turtle
with open("./output_rdf.rdf", "w", encoding='utf-8') as f:
    f.write(g.serialize(format='turtle'))

