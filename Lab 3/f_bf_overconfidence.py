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
import f_datosent as f_datosent

def f_bf_overconfidence(file):

    
    """
    :param file: archivo de entrada
    :return diccionario con resultado final con 4 elementos como resultado
        
    """
    
    
    df=f_datosent.f_datosent(df_datos) #archivo
    #file_type = df_datos[-4:]
    file_type = df
    
    
    if file_type == 'json': ## función sí los datos vienen en formato json
        
        df["size"]=df["size"].apply(pd.to_numeric) #convertir datos a numericos
        df["profit"]=df["profit"].apply(pd.to_numeric)
        
    

        df["closeTime"] = df["closeTime"].apply(lambda x: datetime.strptime(x, '%Y.%m.%d %H:%M:%S')) #Convertimos los numeros en formato de fecha
        weekly = df.groupby(pd.Grouper(key='closeTime', freq='W'))
        weekly = [weekly.get_group(x) for x in weekly.groups] #agrupamos por semana

        oc = 0
        w = []
        dfs = []
        c = 0
        week= []
        for z in range(len(weekly)):
            wtype = weekly[z].groupby(["type","Instrument"]) ## agrupamos por semana nuestras variables a usar
            wtype = [wtype.get_group(y) for y in wtype.groups] 
            for x in range(len(wtype)):
                for i in range(1,len(wtype[x])):
                    c += 1
                    if wtype[x].reset_index().loc[i-1,"profit"] > 0: ## condicion para observar si hubo profit y asi el sujeto es mas propenso a hacer el sesgo
                        if wtype[x].reset_index().loc[i-1,"size"] < wtype[x].reset_index().loc[i,"size"]: ## condición que muestra que el volumen ha subido ya que registro ganancia en ese mismo instrumento
                            oc += 1
                            w.append(z)
                            week.append(wtype[x]["closeTime"].iloc[0])
                            dfs.append(wtype[x].set_index(np.full(len(wtype[x]),z+1))) 
        dfs = pd.concat(dfs)           
        week = pd.DataFrame(week,columns=["closeTime"])
        fig = px.histogram(week, x="closeTime",title="Histograma de sobreconfianza")
        p = oc/c
        dfs.index.name="Week"

        return {"datos": dfs, "grafica": fig, "explicacion": "Nuestro sesgo es el de sobreconfianza el cual consiste en que gracias al exito de una persona en transacciones pasadas esta misma piensa que su habilidad es infalible por lo que empieza a tomar mas riesgo",
                "escala": "{:.1%}".format(p)}
                
    
    elif file_type == 'xlsx': ## función sí los datos vienen en formato excel

        df["closeTime"] = df["closeTime"].apply(lambda x: datetime.strptime(x, '%Y.%m.%d %H:%M:%S'))
        weekly = df.groupby(pd.Grouper(key='closeTime', freq='W'))
        weekly = [weekly.get_group(x) for x in weekly.groups]

        oc = 0
        c = 0
        w = []
        dfs = []
        week=[]
        for z in range(len(weekly)):
            wtype = weekly[z].groupby(["Type","Symbol"]) ## agrupamos por semana nuestras variables a usar
            wtype = [wtype.get_group(y) for y in wtype.groups] 
            for x in range(len(wtype)):
                for i in range(1,len(wtype[x])):
                    c += 1
                    if wtype[x].reset_index().loc[i-1,"Profit"] > 0: ## condicion para observar si hubo profit y asi el sujeto es mas propenso a hacer el sesgo
                        if wtype[x].reset_index().loc[i-1,"Size"] < wtype[x].reset_index().loc[i,"Size"]: ## condición que muestra que el volumen ha subido ya que registro ganancia en ese mismo instrumento
                            oc += 1
                            w.append(z)
                            week.append(wtype[x]["closeTime"].iloc[0])
                            dfs.append(wtype[x].set_index(np.full(len(wtype[x]),z+1)))
    dfs = pd.concat(dfs)
    week = pd.DataFrame(week,columns=["closeTime"])
    fig = px.histogram(week, x="closeTime",title="Histograma de sobreconfianza")
    p = oc/c
    dfs.index.name="Week"
    
    
    return {"datos": dfs, "grafica": fig, "explicacion": "Nuestro sesgo es el de sobreconfianza el cual consiste en que gracias al exito de una persona en transacciones pasadas esta misma piensa que su habilidad es infalible por lo que empieza a tomar mas riesgo",
                "escala": "Incurrencia por numero de transacciones {:.1%}".format(p)}

