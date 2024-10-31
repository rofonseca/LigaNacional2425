import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def analisis_libres_temporada(df, fecha):
    title_general = 'Análisis de Tiros Libres por Partido hasta la fecha \n' + fecha
    plt.figure(figsize=(12, 8))
    # Título general
    plt.suptitle(title_general, fontsize=16)
    j = 0
    for i in df['Date'].unique():
        j = j+1
        df_fec = df[df['Date'] == i]
        scored = df_fec['Free throws scored'].sum()
        not_scored = df_fec['Free throws I.P.P.'].sum() - scored
        labels = ['Tiros Libres Acertados', 'Tiros Libres Errados']
        sizes = [scored, not_scored]
        colors = ['#f2231d', '#565252']
        explode = (0.1, 0)  # Solo resaltar el primer segmento
        plt.subplot(2,4,j)
        wedges, texts, autotexts = plt.pie(sizes, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=140)
        # Personalizar los textos de los porcentajes
        for text in autotexts:
            text.set_color('white')  # Cambiar el color a blanco
            text.set_fontsize(16)    # Ajustar el tamaño de la fuente


        plt.axis('equal')
    plt.legend(wedges, labels,  loc="best",
           prop={'size': 12})
    plt.show()