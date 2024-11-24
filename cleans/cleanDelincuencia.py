import numpy as np
import pandas as pd

# Cargar los datasets de delincuencia
df_delincuencia = pd.read_csv('./data/cead_delincuencia_chile.csv', delimiter=';')

# Reemplazar los espacios en blanco por NaN
df_delincuencia = df_delincuencia.replace(r'^\s*$', np.nan, regex=True)
df_delincuencia = df_delincuencia.dropna()

# Reemplazar ',' por '.' para convertir a numérico
df_delincuencia['delito_n'] = df_delincuencia['delito_n'].astype(str).str.replace(',', '.', regex=True)
# Convertir parámetros a numéricos
df_delincuencia['delito_n'] = pd.to_numeric(df_delincuencia['delito_n'])
df_delincuencia['cut_comuna'] = pd.to_numeric(df_delincuencia['cut_comuna'])
df_delincuencia['cut_region'] = pd.to_numeric(df_delincuencia['cut_region'])

# Guardar archivo limpio
df_delincuencia.to_csv('./data-clean/delincuencia_clean.csv', sep=';', index=False)