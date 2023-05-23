from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd


###########################Base de Dados###################################################
path_matriculado = 'matriculado.xlsx'
path_evadido = 'evadido.xlsx'

df_matriculado = pd.read_excel(path_matriculado,engine = 'openpyxl')
df_evadido= pd.read_excel(path_evadido,engine = 'openpyxl')
    
df_eng_mat = df_matriculado.loc[df_matriculado['Qual curso você está matriculado?'] == 'Engenharia de Computação']
df_tel_mat = df_matriculado.loc[df_matriculado['Qual curso você está matriculado?'] == 'Telemática']
df_eng_evd = df_evadido.loc[df_evadido['Qual curso você fazia: '] == 'Engenharia de Computação']
df_tel_evd = df_evadido.loc[df_evadido['Qual curso você fazia: '] == 'Telemática']


#####################################PLOTANDO###########################################
#Curso de Referência_matriculado
colors = ['#33e0ff','#ff3361']

fig1 = px.pie(values=df_matriculado['Qual curso você está matriculado?'].value_counts(), names=df_matriculado['Qual curso você está matriculado?'].value_counts().index,
             color_discrete_sequence=colors)

fig1.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Qual curso você está matriculado?')

fig1.update_traces(textfont_size=16)


#Curso de Referência_Evadido
colors = ['#33e0ff','#ff3361']

fig2 = px.pie(values=df_evadido['Qual curso você fazia: '].value_counts(), names=df_evadido['Qual curso você fazia: '].value_counts().index,
             color_discrete_sequence=colors)

fig2.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Qual curso você fazia: ')

fig2.update_traces(textfont_size=16)

#Semestre Ingresso Matriculado Engenharia
df_ano1 = df_eng_mat.filter(like='Ano e Semestre de ingresso no curso', axis=1).fillna(0)
df_ano1 = df_ano1.applymap(lambda x: int(x * 10) if isinstance(x, float) else int(x.replace('.', '')))

count1 = df_ano1.stack().value_counts().sort_index()
count1 = count1.drop(0)
count1.index = count1.index.astype(str)

porcentagem = count1.apply((lambda x: (x*100)/count1.value_counts().sum()))

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig3 = px.bar(count1,color_discrete_sequence=[colors],title="Ano e Semestre de ingresso em Engenharia",text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem)])
fig3.update_layout(showlegend=False,yaxis={'title':'Quantidade de Alunos'},
                   xaxis={'title': 'Semestre'})

#Semestre Ingresso Matriculado Telemática
df_ano2 = df_tel_mat.filter(like='Ano e Semestre de ingresso no curso', axis=1).fillna(0)
df_ano2 = df_ano2.applymap(lambda x: int(x * 10) if isinstance(x, float) else int(x.replace('.', '')))

count2 = df_ano2.stack().value_counts().sort_index()
count2 = count2.drop(0)
count2.index = count2.index.astype(str)

porcentagem = count2.apply((lambda x: (x*100)/count2.value_counts().sum()))

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig4 = px.bar(count2,color_discrete_sequence=[colors],title="Ano e Semestre de ingresso em Telemática",text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem)])
fig4.update_layout(showlegend=False,yaxis={'title':'Quantidade de Alunos'},
                   xaxis={'title': 'Semestre'})

#Semestre Ingresso Evadido Engenharia
df_ano3 = df_eng_evd.filter(like='Ano e Semestre de ingresso no curso', axis=1).fillna(0)
df_ano3 = df_ano3.applymap(lambda x: int(x * 10) if isinstance(x, float) else int(x.replace('.', '')))

count3 = df_ano3.stack().value_counts().sort_index()
count3 = count3.drop(0)
count3.index = count3.index.astype(str)

porcentagem = count3.apply((lambda x: (x*100)/count3.value_counts().sum()))

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig5 = px.bar(count3,color_discrete_sequence=[colors],title="Ano e Semestre de ingresso em Engenharia",text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem)])
fig5.update_layout(showlegend=False,yaxis={'title':'Quantidade de Alunos'},
                   xaxis={'title': 'Semestre'})

#Semestre Ingresso Evadido Telemática
df_ano4 = df_tel_evd.filter(like='Ano e Semestre de ingresso no curso', axis=1).fillna(0)
df_ano4 = df_ano4.applymap(lambda x: int(x * 10) if isinstance(x, float) else int(x.replace('.', '')))

count4 = df_ano4.stack().value_counts().sort_index()
count4 = count4.drop(0)
count4.index = count4.index.astype(str)

porcentagem = count4.apply((lambda x: (x*100)/count4.value_counts().sum()))

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d','#f94b00','#f97100','#f99e00','#f9bd00']
fig6 = px.bar(count4,color_discrete_sequence=[colors],title="Ano e Semestre de ingresso em Telemática",text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem)])
fig6.update_layout(showlegend=False,yaxis={'title':'Quantidade de Alunos'},
                   xaxis={'title': 'Semestre'})

#Semestre Evasão Engenharia
df_ano5 = df_eng_evd.filter(like='Ano e Semestre da evasão', axis=1).fillna(0)
df_ano5 = df_ano5.applymap(lambda x: int(x * 10) if isinstance(x, float) else int(x.replace('.', '')))

count5 = df_ano5.stack().value_counts().sort_index()
count5 = count5.drop(0)
count5.index = count5.index.astype(str)

porcentagem = count5.apply((lambda x: (x*100)/count5.value_counts().sum()))

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig7 = px.bar(count5,color_discrete_sequence=[colors],title="Ano e Semestre de evasão em Engenharia",text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem)])
fig7.update_layout(showlegend=False,yaxis={'title':'Quantidade de Alunos'},
                   xaxis={'title': 'Semestre'})

#Semestre Evasão Telemática
df_ano6 = df_tel_evd.filter(like='Ano e Semestre da evasão', axis=1).fillna(0)
df_ano6 = df_ano6.applymap(lambda x: int(x * 10) if isinstance(x, float) else int(x.replace('.', '')))

count6 = df_ano6.stack().value_counts().sort_index()
count6 = count6.drop(0)
count6.index = count6.index.astype(str)

porcentagem = count6.apply((lambda x: (x*100)/count6.value_counts().sum()))

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d','#f94b00','#f97100','#f99e00','#f9bd00']
fig8 = px.bar(count6,color_discrete_sequence=[colors],title="Ano e Semestre de evasão em Telemática",text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem)])
fig8.update_layout(showlegend=False,yaxis={'title':'Quantidade de Alunos'},
                   xaxis={'title': 'Semestre'})

#Top Disciplinas Engenharia Matriculado
disciplinas_eng1 = df_eng_mat['Assinale 3 alternativas que apresentam as disciplinas que você teve mais dificuldade?-Eng'].str.split(',', expand=True).dropna()
disciplinas_eng1 = disciplinas_eng1.applymap(lambda x: x.strip())
count_disciplinas_eng1 = disciplinas_eng1.stack().value_counts()
porcentagem_disciplinas_eng1 = count_disciplinas_eng1 / disciplinas_eng1.shape[0] * 100
top6_disciplinas_eng1 = porcentagem_disciplinas_eng1.head(6).sort_values(ascending=True)

fig9 = px.bar(top6_disciplinas_eng1,
             orientation='h',text=[i+' ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(top6_disciplinas_eng1.index,top6_disciplinas_eng1)],color_discrete_sequence=[colors],title="Top 6 Disciplinas que os alunos matriculados em Engenharia tem dificuldade"
            )
fig9.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=35, l=0, r=0, b=10),
                  yaxis={'categoryorder':'total descending'},
                  showlegend=False
                 )
fig9.update_traces(textposition='auto')
fig9.update_xaxes(visible=False)
fig9.update_yaxes(visible=False)

#Top Disciplinas Engenharia Evadido
disciplinas_eng2 = df_eng_evd['Assinale as três disciplinas que você teve mais dificuldade.-Eng'].str.split(',', expand=True).dropna()
disciplinas_eng2 = disciplinas_eng2.applymap(lambda x: x.strip())
count_disciplinas_eng2 = disciplinas_eng2.stack().value_counts()
porcentagem_disciplinas_eng2 = count_disciplinas_eng2 / disciplinas_eng2.shape[0] * 100
top6_disciplinas_eng2 = porcentagem_disciplinas_eng2.head(6).sort_values(ascending=True)

fig10 = px.bar(top6_disciplinas_eng2,
             orientation='h',text=[i+' ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(top6_disciplinas_eng2.index,top6_disciplinas_eng2)],color_discrete_sequence=[colors],title="Top 6 Disciplinas que os alunos evadidos em Engenharia tiveram dificuldade"
            )
fig10.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=35, l=0, r=0, b=10),
                  yaxis={'categoryorder':'total descending'},
                  showlegend=False
                 )
fig10.update_traces(textposition='auto')
fig10.update_xaxes(visible=False)
fig10.update_yaxes(visible=False)

#Top Disciplinas Telemática Matriculado
disciplinas_tel1 = df_tel_mat['Assinale 3 alternativas que apresentam as disciplinas que você teve mais dificuldade?-Tel'].str.split(',', expand=True).dropna()
disciplinas_tel1 = disciplinas_tel1.applymap(lambda x: x.strip())
count_disciplinas_tel1 = disciplinas_tel1.stack().value_counts()


porcentagem_disciplinas_tel1 = count_disciplinas_tel1 / disciplinas_tel1.shape[0] * 100
top6_disciplinas_tel1 = porcentagem_disciplinas_tel1.head(6).sort_values(ascending=True)

fig11 = px.bar(top6_disciplinas_tel1,
             orientation='h',text=[i+' ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(top6_disciplinas_tel1.index,top6_disciplinas_tel1)],color_discrete_sequence=[colors],title="Top 6 Disciplinas que os alunos matriculados em Telemática tiveram dificuldade"
            )
fig11.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=40, l=0, r=0, b=10),
                  yaxis={'categoryorder':'total descending'},
                  showlegend=False
                 )
fig11.update_traces(textposition='auto')
fig11.update_xaxes(visible=False)
fig11.update_yaxes(visible=False)

#Top Disciplinas Telemática Evadido
disciplinas_tel2 = df_tel_evd['Assinale as três disciplinas que você teve mais dificuldade.-Tel'].str.split(',', expand=True).dropna()
disciplinas_tel2 = disciplinas_tel2.applymap(lambda x: x.strip())
count_disciplinas_tel2 = disciplinas_tel2.stack().value_counts()
porcentagem_disciplinas_tel2 = count_disciplinas_tel2 / disciplinas_tel2.shape[0] * 100 
top6_disciplinas_tel2 = porcentagem_disciplinas_tel2.head(6).sort_values(ascending=True)

fig12 = px.bar(top6_disciplinas_tel2,
             orientation='h',text=[i+' ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(top6_disciplinas_tel2.index,top6_disciplinas_tel2)],color_discrete_sequence=[colors],title="Top 6 Disciplinas que os alunos evadidos em Telemática tiveram dificuldade"
            )
fig12.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=40, l=0, r=0, b=10),
                  yaxis={'categoryorder':'total descending'},
                  showlegend=False
                 )
fig12.update_traces(textposition='auto')
fig12.update_xaxes(visible=False)
fig12.update_yaxes(visible=False)

#Escolha do Curso Engenharia Matriculado
cols1 = df_eng_mat.filter(like='Assinale a coluna que representa a intensidade de influência do fator para a escolha do curso.', axis=1)
col_labels1 = [col.split('[', 1)[1].replace(']', '') for col in cols1]
mapeamento1 = {'Não influenciou': 0, 'Pouca influência': 1, 'Muita influência': 2}

soma1 = cols1.apply(lambda x: x.map(mapeamento1).sum(), axis=0)
soma1 = soma1.rename(index=dict(zip(cols1, col_labels1)))
soma1 = soma1.sort_values()

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig13 = px.bar(soma1,color_discrete_sequence=[colors],title="Fatores que influêciam para a escolha do curso dos matriculados em Engenharia",orientation="h",text=[i for i in (soma1.index)])
fig13.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Fatores'},
                   xaxis={'title': 'Pontos'})
fig13.update_traces(textposition='auto')
fig13.update_xaxes(visible=False)
fig13.update_yaxes(visible=False)

#Escolha do Curso Telemática Matriculado
cols2 = df_tel_mat.filter(like='Assinale a coluna que representa a intensidade de influência do fator para a escolha do curso.', axis=1)

col_labels2 = [col.split('[', 1)[1].replace(']', '') for col in cols2]
print(col_labels2)
mapeamento2 = {'Não influenciou': 0, 'Pouca influência': 1, 'Muita influência': 2}

soma2 = cols2.apply(lambda x: x.map(mapeamento2).sum(), axis=0)
soma2 = soma2.rename(index=dict(zip(cols2, col_labels2)))
soma2 = soma2.sort_values()

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig14 = px.bar(soma2,color_discrete_sequence=[colors],title="Fatores que influêciam para a escolha do curso dos matriculados em Telemática",orientation="h",text=[i for i in (soma2.index)])
fig14.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Fatores'},
                   xaxis={'title': 'Pontos'})
fig14.update_traces(textposition='auto')
fig14.update_xaxes(visible=False)
fig14.update_yaxes(visible=False)

#Escolha do Curso Engenharia Evadido
cols3 = df_eng_evd.filter(like='Assinale a coluna que representa a intensidade de influência do fator para a sua escolha do curso.', axis=1)
col_labels3 = [col.split('[', 1)[1].replace(']', '') for col in cols3]
mapeamento3 = {'Não influenciou': 0, 'Pouca influência': 1, 'Muita influência': 2}

soma3 = cols3.apply(lambda x: x.map(mapeamento3).sum(), axis=0)
soma3 = soma3.rename(index=dict(zip(cols3, col_labels3)))
soma3 = soma3.sort_values()
soma3 = soma3.drop('Linha 6')

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig15 = px.bar(soma3,color_discrete_sequence=[colors],title="Fatores que influêciam para a escolha do curso dos evadidos em Engenharia",orientation="h",text=[i for i in (soma3.index)])
fig15.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Fatores'},
                   xaxis={'title': 'Pontos'})
fig15.update_traces(textposition='auto')
fig15.update_xaxes(visible=False)
fig15.update_yaxes(visible=False)

#Escolha do Curso Telemática Evadido
cols4 = df_tel_evd.filter(like='Assinale a coluna que representa a intensidade de influência do fator para a sua escolha do curso.', axis=1)
col_labels4 = [col.split('[', 1)[1].replace(']', '') for col in cols4]
mapeamento4 = {'Não influenciou': 0, 'Pouca influência': 1, 'Muita influência': 2}

soma4 = cols4.apply(lambda x: x.map(mapeamento4).sum(), axis=0)
soma4 = soma4.rename(index=dict(zip(cols4, col_labels4)))
soma4 = soma4.sort_values()
soma4 = soma4.drop('Linha 6')

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig16 = px.bar(soma4,color_discrete_sequence=[colors],title="Fatores que influêciam para a escolha do curso dos evadidos em Telemática",orientation="h",text=[i for i in (soma4.index)])
fig16.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Fatores'},
                   xaxis={'title': 'Pontos'})
fig16.update_traces(textposition='auto')
fig16.update_xaxes(visible=False)
fig16.update_yaxes(visible=False)

#Influência permanência/abandono matriculado eng
cols5 = df_eng_mat.filter(like='Assinale a coluna que representa a intensidade de influência do fator para a sua permanência do curso.', axis=1)

col_labels5 = [col.split('[', 1)[1].replace(']', '') for col in cols5]

mapeamento5 = {'Não influenciou.': 0, 'Pouca influência.': 1, 'Muita influência.': 2}

soma5 = cols5.apply(lambda x: x.map(mapeamento5).sum(), axis=0)
soma5 = soma5.rename(index=dict(zip(cols5, col_labels5)))
soma5 = soma5.sort_values()

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig17 = px.bar(soma5,color_discrete_sequence=[colors],title="Fatores que influêciam para a permanência no curso de Engenharia",orientation="h",text=[i for i in (soma5.index)])
fig17.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Fatores'},
                   xaxis={'title': 'Pontos'})
fig17.update_traces(textposition='auto')
fig17.update_xaxes(visible=False)
fig17.update_yaxes(visible=False)
#Influência permanência/abandono matriculado tel
cols6 = df_tel_mat.filter(like='Assinale a coluna que representa a intensidade de influência do fator para a sua permanência do curso.', axis=1)

col_labels6 = [col.split('[', 1)[1].replace(']', '') for col in cols6]

mapeamento6 = {'Não influenciou.': 0, 'Pouca influência.': 1, 'Muita influência.': 2}

soma6 = cols6.apply(lambda x: x.map(mapeamento6).sum(), axis=0)
soma6 = soma6.rename(index=dict(zip(cols6, col_labels6)))
soma6 = soma6.sort_values()

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig18 = px.bar(soma6,color_discrete_sequence=[colors],title="Fatores que influêciam para a permanência no curso de Telemática",orientation="h",text=[i for i in (soma6.index)])
fig18.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Fatores'},
                   xaxis={'title': 'Pontos'})
fig18.update_traces(textposition='auto')
fig18.update_xaxes(visible=False)
fig18.update_yaxes(visible=False)

#Influência permanência/abandono evadidos eng
cols7 = df_eng_evd.filter(like='Assinale a coluna que representa a intensidade de influência do fator para a desistência ou abandono do curso. ', axis=1)

col_labels7 = [col.split('[', 1)[1].replace(']', '') for col in cols7]

mapeamento7 = {'Não influenciou': 0, 'Pouca influência': 1, 'Muita influência': 2}

soma7 = cols7.apply(lambda x: x.map(mapeamento7).sum(), axis=0)
soma7 = soma7.rename(index=dict(zip(cols7, col_labels7)))
soma7 = soma7.sort_values()
soma7 = soma7.drop('Linha 10')

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig19 = px.bar(soma7,color_discrete_sequence=[colors],title="Fatores que influêciam para a desistência ou abandono no curso de Engenharia",orientation="h",text=[i for i in (soma7.index)])
fig19.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Fatores'},
                   xaxis={'title': 'Pontos'})
fig19.update_traces(textposition='auto')
fig19.update_xaxes(visible=False)
fig19.update_yaxes(visible=False)

#Influência permanência/abandono evadidos tel
cols8 = df_tel_evd.filter(like='Assinale a coluna que representa a intensidade de influência do fator para a desistência ou abandono do curso. ', axis=1)

col_labels8 = [col.split('[', 1)[1].replace(']', '') for col in cols8]

mapeamento8 = {'Não influenciou': 0, 'Pouca influência': 1, 'Muita influência': 2}

soma8 = cols8.apply(lambda x: x.map(mapeamento8).sum(), axis=0)
soma8 = soma8.rename(index=dict(zip(cols8, col_labels8)))
soma8 = soma8.sort_values()
soma8 = soma8.drop('Linha 10')

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d']
fig20 = px.bar(soma8,color_discrete_sequence=[colors],title="Fatores que influêciam para a desistência ou abandono no curso de Telemática",orientation="h",text=[i for i in (soma8.index)])
fig20.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Fatores'})
fig20.update_traces(textposition='auto')
fig20.update_xaxes(visible=False)
fig20.update_yaxes(visible=False)

#Situação empregaticia matriculados eng
valor_absoluto3 = df_eng_mat['Qual a sua situação atualmente? '].value_counts()
porcentagem3 = valor_absoluto3.apply((lambda x: (x*100)/valor_absoluto3.sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig21 = px.bar(porcentagem3,title='Situação empregatícia atual dos matriculados em Engenharia',
             orientation='h',text=[i+' ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto3.index,porcentagem3)],color_discrete_sequence=[colors],
            )
fig21.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=35, l=10, r=0, b=10),showlegend=False)
fig21.update_traces(textposition='auto')
fig21.update_xaxes(visible=False)
fig21.update_yaxes(visible=False)


#periodo do vinculo empregaticio matriculados eng
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig22 = px.pie(values=df_eng_mat['Em qual período foi o seu primeiro vínculo empregatício ou de estágio?'].value_counts(), names=df_eng_mat['Em qual período foi o seu primeiro vínculo empregatício ou de estágio?'].value_counts().index,
             color_discrete_sequence=colors)

fig22.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Período em que se iniciou o vínculo empregatício - Engenharia')

fig22.update_traces(textfont_size=16)

#Situação empregaticia matriculados tel
valor_absoluto = df_tel_mat['Qual a sua situação atualmente? '].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/valor_absoluto.sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig23 = px.bar(porcentagem,title='Situação empregatícia atual dos matriculados em Telemática',
             orientation='h',text=[i+' ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto.index,porcentagem)],color_discrete_sequence=[colors],
            )
fig23.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=35, l=10, r=0, b=10),showlegend=False)
fig23.update_traces(textposition='auto')
fig23.update_xaxes(visible=False)
fig23.update_yaxes(visible=False)

#periodo do vinculo empregaticio matriculados tel
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig24 = px.pie(values=df_tel_mat['Em qual período foi o seu primeiro vínculo empregatício ou de estágio?'].value_counts(), names=df_tel_mat['Em qual período foi o seu primeiro vínculo empregatício ou de estágio?'].value_counts().index,
             color_discrete_sequence=colors)

fig24.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Período em que se iniciou o vínculo empregatício - Telemática')

fig24.update_traces(textfont_size=16)

#Situação empregaticio evadidos eng
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig25 = px.pie(values=df_eng_evd['Trabalha em qual área atualmente:'].value_counts(), names=df_eng_evd['Trabalha em qual área atualmente:'].value_counts().index,
             color_discrete_sequence=colors)

fig25.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Área em que trabalha atualmente - Engenharia')

fig25.update_traces(textfont_size=16)

#Situação empregaticio evadidos Tel
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig26 = px.pie(values=df_tel_evd['Trabalha em qual área atualmente:'].value_counts(), names=df_tel_evd['Trabalha em qual área atualmente:'].value_counts().index,
             color_discrete_sequence=colors)

fig26.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Área em que trabalha atualmente - Telemática')

fig26.update_traces(textfont_size=16)

#Avaliação matriculados eng
aval1 = df_eng_mat.filter(like='Qual a nota você atribui para o quanto os seguintes aspectos influenciam na sua permanência no curso? Considerando 1 como a nota mínima e 5 a nota máxima.', axis=1)
col_labels1 = [col.split('[', 1)[1].replace(']', '') for col in aval1]

soma9 = aval1.sum()
soma9 = soma9.rename(index=dict(zip(aval1, col_labels1)))
soma9 = soma9.sort_values()

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d','#f94b00','#f97100','#f99e00','#f9bd00']
fig27 = px.bar(soma9,color_discrete_sequence=[colors],title="Avaliação do curso de Engenharia, pelos matriculados",orientation="h",text=[i for i in (soma9.index)])
fig27.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Áreas'},
                   xaxis={'title': 'Pontos'})
fig27.update_traces(textposition='auto')
fig27.update_xaxes(visible=False)
fig27.update_yaxes(visible=False)

#Avaliação matriculados tel

aval2 = df_tel_mat.filter(like='Qual a nota você atribui para o quanto os seguintes aspectos influenciam na sua permanência no curso? Considerando 1 como a nota mínima e 5 a nota máxima.', axis=1)
col_labels2 = [col.split('[', 1)[1].replace(']', '') for col in aval2]

soma10 = aval2.sum()
soma10 = soma10.rename(index=dict(zip(aval2, col_labels2)))
soma10 = soma10.sort_values()

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d','#f94b00','#f97100','#f99e00','#f9bd00']
fig28 = px.bar(soma10,color_discrete_sequence=[colors],title="Avaliação do curso de Telemática, pelos matriculados",orientation="h",text=[i for i in (soma10.index)])
fig28.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Áreas'},
                   xaxis={'title': 'Pontos'})
fig28.update_traces(textposition='auto')
fig28.update_xaxes(visible=False)
fig28.update_yaxes(visible=False)

#Avaliação evadidos eng
aval3 = df_eng_evd.filter(like='Qual a nota você atribui para os seguintes aspectos durante sua permanência no curso? Considerando 1 como a nota mínima e 5 a nota máxima.', axis=1)
col_labels3 = [col.split('[', 1)[1].replace(']', '') for col in aval3]

soma11 = aval3.sum()
soma11 = soma11.rename(index=dict(zip(aval3, col_labels3)))
soma11 = soma11.sort_values()

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d','#f94b00','#f97100','#f99e00','#f9bd00']
fig29 = px.bar(soma11,color_discrete_sequence=[colors],title="Avaliação do curso de Engenharia, pelos evadidos",orientation="h",text=[i for i in (soma11.index)])
fig29.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Áreas'},
                   xaxis={'title': 'Pontos'})
fig29.update_traces(textposition='auto')
fig29.update_xaxes(visible=False)
fig29.update_yaxes(visible=False)

#Avaliação evadidos tel
aval4 = df_tel_evd.filter(like='Qual a nota você atribui para os seguintes aspectos durante sua permanência no curso? Considerando 1 como a nota mínima e 5 a nota máxima.', axis=1)
col_labels4 = [col.split('[', 1)[1].replace(']', '') for col in aval4]

soma12 = aval4.sum()
soma12 = soma12.rename(index=dict(zip(aval4, col_labels4)))
soma12 = soma12.sort_values()

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361','#f9002d','#f94b00','#f97100','#f99e00','#f9bd00']
fig30 = px.bar(soma12,color_discrete_sequence=[colors],title="Avaliação do curso de Telemática, pelos evadidos",orientation="h",text=[i for i in (soma12.index)])
fig30.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',showlegend=False,yaxis={'title':'Áreas'},
                   xaxis={'title': 'Porcentagem'})
fig30.update_traces(textposition='auto')
fig30.update_xaxes(visible=False)
fig30.update_yaxes(visible=False)

###################################LAYOUT###################################################################


layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig1
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig3)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig4)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig2
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig5)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig6)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig7
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig8)
                    ),style={"width": "100%"},
        ),width=6)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig9
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig13)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig17)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig11
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig14)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig18)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig10
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            figure=fig15)
                        ),style={"width": "100%"},
            ),width=4),
	    dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig19)
                    ),style={"width": "100%"},
        ),width=4)
    ],style={"width": "100%"}),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig12
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            figure=fig16)
                        ),style={"width": "100%"},
            ),width=4),
	    dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig20)
                    ),style={"width": "100%"},
        ),width=4)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig21
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            figure=fig22)
                        ),style={"width": "100%"},
            ),width=3),
	    dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig23)
                    ),style={"width": "100%"},
        ),width=3),
	    dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            figure=fig24)
                        ),style={"width": "100%"},
            ),width=3)
    ],style={"width": "100%"}),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig25
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig26)
                    ),style={"width": "100%"},
        ),width=6),
    ],style={"width": "100%"}),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig27
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            figure=fig29)
                        ),style={"width": "100%"},
            ),width=6)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig28
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            figure=fig30)
                        ),style={"width": "100%"},
            ),width=6)
    ],style={"width": "100%"})
    
],style={"width": "100%"})