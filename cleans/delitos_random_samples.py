import pandas as pd

# Lee todo el archivo CSV especificando el separador
data = pd.read_csv('../data-clean/delincuencia_clean.csv', sep=';')

# Toma una muestra aleatoria de 1,000 filas
data_sample = data.sample(n=1000, random_state=42)  # random_state para reproducibilidad

# Guarda la muestra en un nuevo archivo CSV con ';' como separador
data_sample.to_csv('../data-clean/cead_delincuencia_chile_random_sample.csv', sep=';', index=False)

print("Nuevo archivo creado con 1,000 filas.")
