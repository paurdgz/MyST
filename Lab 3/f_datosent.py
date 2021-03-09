#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import json #leer el archivo
from datetime import datetime #Para separar las fechas por semanas 
import matplotlib.pyplot as plt #para las graficas
import matplotlib
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime #Numeros a formato de fecha

def f_datosent(P0_archivo):
    
    """
    :param p0_archivo: archivo de entrada
    :return resultado
    
    debbuging
    p0_archivo = 'archivo_tradeview_2.xlsx'
    
    """

    
    file_type = P0_archivo[-4:]
    # Opciones para visualizar data frames en consola
    pd.set_option('display.max_rows',5000)
    pd.set_option('display.max_columns',500)
    pd.set_option('display.width',1000)
    
    # Ingreso de datos de entrada: Leer archivo JSON
    archivo = P0_archivo
    
    if file_type == 'json':
        with open(archivo, encoding='utf-8-sig') as json_file:
            datos_2 = json.load(json_file)['data']
            
        # Seleccionar la seccion de 'closedTransactions' que es la de interes
        df_datos = pd.DataFrame(datos_2['closedTransactions']['list'])
        
        # Seleccionar solo los renglones de operaciones
        df_datos = df_datos[(df_datos['type'] == 'buy') | (df_datos['type'] == 'sell') | (df_datos['type'] == 's/l') |
                (df_datos['type'] == 't/p')]
        
        # Resetear index para tener todos los numeros de indice completos
        df_datos = df_datos.reset_index()
        
        # Eliminar columnas 'info' e 'index'
        df_datos = df_datos.drop(['info', 'index'], 1)
        
        # Renombrar columnas
        df_datos.rename(columns = {'SL': 'sl', 'TP':'tp', 'price':'openPrice', 'price2':'closePrice', 'item':'Instrument'},
                        inplace=True)
        return df_datos
    elif file_type == 'xlsx':
        df_datos = pd.read_excel(archivo, sheet_name = 'Hoja1', col_header=0)
        return df_datos

