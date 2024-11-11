import numpy as np
import csv
import pandas as pd

#Cargar los datasets de Dolegios
df_2018_2019 = pd.read_csv("SNED_2018_2019.csv", delimiter=";")
df_2020_2021 = pd.read_csv("20230511_SNED_2020_2021.csv", delimiter=";")
df_2022_2023 = pd.read_csv("20230511_SNED_2022_2023.csv", delimiter=";")

#Cargar dataset de Delitos
df_delitos = pd.read_csv("cead_delincuencia_chile.csv", delimiter=";")

#Reemplazar los espacios en blanco por NaN
df = df_2022_2023.replace(r'^\s*$', np.nan, regex=True)

#Eliminar columnas que no se utilizarán
df = df.drop(['RBD_A1','RBD_A2','COD_DEPE','COD_PRO_RBD','COD_DEPROV_RBD','NOM_DEPROV_RBD'], axis=1)









#df_profile_final.to_csv('mi_dataframe2.csv', index=False) 