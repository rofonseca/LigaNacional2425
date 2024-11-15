import numpy as np
import pandas as pd
import statistics

import sys
sys.path.append('./fun/')
import more_functions

# Fecha
date = '14/11/2024'

# partido número
num = 75

# local
path = 'liga_data_0.csv'
df = more_functions.rearmar_csv(path, date)
nombre = 'data/Partido_' + str(num) + '_local.csv'
df.to_csv(nombre, index=False)

# visitante
path = 'liga_data_1.csv'
df = more_functions.rearmar_csv(path, date)
nombre = 'data/Partido_' + str(num) + '_visitante.csv'
df.to_csv(nombre, index=False)