import pandas as pd

# Cargar los datasets de delincuencia
df_delincuencia = pd.read_csv('delincuencia_clean.csv', delimiter=';')

# Sólo region y cut_region
df_regiones = df_delincuencia.drop(['comuna', 'cut_comuna', 'fecha','delito','delito_n'], axis=1)
# Sólo comuna y cut_comuna
df_comunas = df_delincuencia.drop(['region', 'fecha','delito','delito_n'], axis=1)


df_regiones = df_regiones.drop_duplicates()
df_comunas = df_comunas.drop_duplicates()

# Guardar archivos limpios
df_regiones.to_csv('regiones.csv', sep=';', index=False)
df_comunas.to_csv('comunas.csv', sep=';', index=False)

