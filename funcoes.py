import pandas as pd
import numpy as np

indices = [
          'Quantidade',
          'Média',
          'Desvio padrão',
          'Valor mínimo',
          'Q1',
          'Q2/Mediana',
          'Q3',
          'Valor máximo',
          'Moda',
          'Variância',
          'Amplitude',
          'Assimetria'    
]

def medida_assimetria(q1, q2, q3):
  return ((q3 - q2) - (q2 - q1))/(q3-q1)

def descreve_informacoes(df_referencia):
  global indices
 
  df_referencia.loc[:,'Coeficiente_de_progressao'] = df_referencia['Coeficiente_de_progressao'].astype(str).str.replace(',','.')
  df_referencia.loc[:,'Coeficiente_de_progressao'] = df_referencia['Coeficiente_de_progressao'].replace('-', np.nan).astype(float)
  #df_referencia['Coeficiente_de_progressao'] = df_referencia['Coeficiente_de_progressao'].astype(str).str.replace(',','.')
  #df_referencia['Coeficiente_de_progressao'] = df_referencia['Coeficiente_de_progressao'].replace('-', np.nan).astype(float)

  df_retorno = df_referencia.describe()  
  moda = df_referencia['Coeficiente_de_progressao'].mode()
  moda = pd.Series(data={'Coeficiente_de_progressao': tuple(moda)}, name='Moda')
  df_retorno = df_retorno._append(moda, ignore_index=False)

  variancia = df_referencia['Coeficiente_de_progressao'].var()
  variancia = pd.Series(data={'Coeficiente_de_progressao': variancia}, name='Variância')
  df_retorno = df_retorno._append(variancia, ignore_index=False)

  valor_max = df_retorno.loc['max']
  valor_min = df_retorno.loc['min']
  amplitude = pd.Series(data={'Coeficiente_de_progressao': float(valor_max['Coeficiente_de_progressao']) - float(valor_min['Coeficiente_de_progressao'])}, name='Amplitude')
  df_retorno = df_retorno._append(amplitude, ignore_index=False)

  q1 = df_retorno['Coeficiente_de_progressao'].loc['25%']
  q2 = df_retorno['Coeficiente_de_progressao'].loc['50%']
  q3 = df_retorno['Coeficiente_de_progressao'].loc['75%']
  assimetria = pd.Series(data={'Coeficiente_de_progressao': medida_assimetria(q1, q2, q3)}, name='Medida de Bowley')  
  df_retorno = df_retorno._append(assimetria, ignore_index=False)

  df_retorno.index = indices
  return df_retorno['Coeficiente_de_progressao'].to_frame()