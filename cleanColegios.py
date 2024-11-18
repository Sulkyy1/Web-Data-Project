import numpy as np
import pandas as pd

# Cargar los datasets de colegios
df_2018_2019 = pd.read_csv('SNED_2018_2019.csv', delimiter=';')
df_2020_2021 = pd.read_csv('SNED_2020_2021.csv', delimiter=';')
df_2022_2023 = pd.read_csv('SNED_2022_2023.csv', delimiter=';')

# Eliminar columnas que no se utilizarán
df1 = df_2018_2019.drop(['RBD_A1','RBD_A2','COD_DEPE','COD_PRO_RBD','COD_DEPROV_RBD','NOM_DEPROV_RBD'], axis=1)
df2 = df_2020_2021.drop(['RBD_A1','RBD_A2','COD_DEPE','COD_PRO_RBD','COD_DEPROV_RBD','NOM_DEPROV_RBD'], axis=1)
df3 = df_2022_2023.drop(['RBD_A1','RBD_A2','COD_DEPE','COD_PRO_RBD','COD_DEPROV_RBD','NOM_DEPROV_RBD'], axis=1)

#Reemplazar los espacios en blanco por NaN
df1 = df1.replace(r'^\s*$', np.nan, regex=True)
df2 = df2.replace(r'^\s*$', np.nan, regex=True)
df3 = df3.replace(r'^\s*$', np.nan, regex=True)

df1 = df1.dropna()
df2 = df2.dropna()
df3 = df3.dropna()

# Columnas numéricas
columns = ['EFECTIVR', 'SUPERAR', 'INICIAR', 'MEJORAR', 'INTEGRAR', 'IGUALDR', 'CLUSTER', 'INDICER']

# Eliminar números negativos de las columnas numéricas
for col in columns:
    df1[col] = df1[col].astype(str).str.replace(',', '.', regex=True)
    df2[col] = df2[col].astype(str).str.replace(',', '.', regex=True)
    df3[col] = df3[col].astype(str).str.replace(',', '.', regex=True)
    df1[col] = pd.to_numeric(df1[col])
    df2[col] = pd.to_numeric(df2[col])
    df3[col] = pd.to_numeric(df3[col])
df1 = df1[df1[columns].min(axis=1) >= 0]
df2 = df2[df2[columns].min(axis=1) >= 0]
df3 = df3[df3[columns].min(axis=1) >= 0]

# Guardar archivos limpios
df1.to_csv('SNED_2018_2019_clean.csv', sep=';', index=False)
df2.to_csv('SNED_2020_2021_clean.csv', sep=';', index=False)
df3.to_csv('SNED_2022_2023_clean.csv', sep=';', index=False)