from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from tratamento_de_dados import geral

###########################Base de Dados###################################################
path_telematica = '/home/iasmin/Documentos/TCC-Dashboard/dados_telematica.xlsx'

df_telematica = pd.read_excel(path_telematica)
df_telematica_novo = pd.read_excel(path_telematica,sheet_name="NOVO")
#######################################TRATAMENTO DE DADOS################################
df_telematica = geral(df_telematica)
df_telematica_novo = geral(df_telematica_novo)

###############################TRATAMENTO ESPECÍFICO#######################################

df_conclusao_tel = df_telematica_novo.copy()

indexNames = df_conclusao_tel[(df_conclusao_tel['Data de conclusao'] == '-')].index

df_conclusao_tel.drop(indexNames, inplace=True)

df_conclusao_tel['Data_da_matricula'] = pd.to_datetime(df_conclusao_tel['Data_da_matricula'], format='%Y/%m/%d %H:%M:%S')
df_conclusao_tel['Data de conclusao'] = pd.to_datetime(df_conclusao_tel['Data de conclusao'], format='%Y/%m/%d %H:%M:%S')
df_conclusao_tel['Meses Conclusao'] = ((df_conclusao_tel['Data de conclusao'] - df_conclusao_tel['Data_da_matricula']).dt.days)/30
df_conclusao_tel.loc[:,'Meses Conclusao'] = df_conclusao_tel['Meses Conclusao'].astype(int)

df_agrupado_telematica = df_telematica.copy()
df_agrupado_telematica['Situacao'] = df_agrupado_telematica['Situacao'].replace( ['cancelado voluntariamente', 'cancelado compulsoriamente', 'trancado', 'evadido', 'afastado', 'trancado voluntariamente','transferido externamente', 'transferido internamente'], 'evadido/trancado')
df_agrupado_telematica['Situacao'] = df_agrupado_telematica['Situacao'].replace( ['matriculado',  'intercambio', 'vinculado'], 'matriculado')
df_agrupado_telematica['Situacao'].unique()

df_telematica_novo['Situacao'] = df_telematica_novo['Situacao'].replace( ['cancelado voluntariamente', 'cancelado compulsoriamente', 'trancado', 'evadido', 'afastado',  'trancado voluntariamente','transferido externamente', 'transferido internamente'], 'evadido/trancado')
df_telematica_novo['Situacao'] = df_telematica_novo['Situacao'].replace( ['matriculado',  'intercambio', 'vinculado'], 'matriculado')
df_telematica_novo['Situacao'].unique()
##############################PLOTANDO GRAFICOS#############################################################

#Situação Geral
df_situacao_geral_tel = df_agrupado_telematica['Situacao'].value_counts().to_frame()
colors = ['#FF6347','#6495ED','#9ACD32']

valor_absoluto1 = df_agrupado_telematica['Situacao'].value_counts()

porcentagem1 = valor_absoluto1.apply((lambda x: (x*100)/valor_absoluto1.sum()))

fig1 = px.bar(df_situacao_geral_tel,x=df_situacao_geral_tel.index,y='count',title='Situação Geral',text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem1)],color_discrete_sequence=[colors])
fig1.update_layout(yaxis={'title':'Quantidade de Alunos'},
                   xaxis={'title': 'Situacao'})

#AlunosxSexo
counts1 = df_agrupado_telematica.groupby(['Sexo','Situacao']).size()
counts1 = counts1.unstack(level=-1)

totals1 = counts1.sum(axis=1)
percentages1 = counts1.divide(totals1, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig2 = px.bar(percentages1,barmode = 'stack',color='Situacao', title='Situação dos alunos por Sexo',color_discrete_sequence=colors)
fig2.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#Situaçãoxnaturalidade
df_sem_traco1 = df_agrupado_telematica[df_agrupado_telematica.Naturalidade!='-']
counts2 = df_sem_traco1.groupby(['Naturalidade','Situacao']).size()
counts2 = counts2.unstack(level=-1)

soma2 = counts2.sum(axis=1)
counts2.insert(3, "Total", soma2, True)
counts2=counts2.sort_values(by="Total", ascending=False)
counts2=counts2.drop(columns=['Total'])
counts2=counts2.head(10)

totals2 = counts2.sum(axis=1)
percentages2 = counts2.divide(totals2, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig3 = px.bar(percentages2,barmode = 'stack',color='Situacao', title='Situação dos alunos por top 10 naturalidades',color_discrete_sequence=colors)
fig3.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#SituaçãoxBairro
df_sem_traco2 = df_agrupado_telematica[df_agrupado_telematica.Bairro!='-']
counts3 = df_sem_traco2.groupby(['Bairro','Situacao']).size()
counts3 = counts3.unstack(level=-1)

soma3 = counts3.sum(axis=1)
counts3.insert(3, "Total", soma3, True)
counts3=counts3.sort_values(by="Total", ascending=False)
counts3=counts3.drop(columns=['Total'])
counts3=counts3.head(10)

totals3 = counts3.sum(axis=1)
percentages3 = counts3.divide(totals3, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig4 = px.bar(percentages3,barmode = 'stack',color='Situacao', title='Situação dos alunos por top 10 bairros',color_discrete_sequence=colors)
fig4.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#AlunosxTipoZona
df_sem_traco3 = df_agrupado_telematica[df_agrupado_telematica.Tipo_da_zona_residencial!='-']

counts4 = df_sem_traco3.groupby(['Tipo_da_zona_residencial','Situacao']).size()
counts4 = counts4.unstack(level=-1)

totals4 = counts4.sum(axis=1)
percentages4 = counts4.divide(totals4, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig5 = px.bar(percentages4,barmode = 'stack',color='Situacao', title='Situação dos alunos por Tipo da zona residencial',color_discrete_sequence=colors)
fig5.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#SituaçãoxFormaDeIngresso
counts5 = df_agrupado_telematica.groupby(['Forma_de_ingresso','Situacao']).size()
counts5 = counts5.unstack(level=-1)

totals5 = counts5.sum(axis=1)
percentages5 = counts5.divide(totals5, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig6 = px.bar(percentages5,barmode = 'stack',color='Situacao', title='Situação dos alunos por Forma de ingresso',color_discrete_sequence=colors)
fig6.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Forma de Ingresso'})

#SituaçãoxCor/Raca
counts6 = df_agrupado_telematica.groupby(['Cor_Raca','Situacao']).size()
counts6 = counts6.unstack(level=-1)

totals6 = counts6.sum(axis=1)
percentages6 = counts6.divide(totals6, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig7 = px.bar(percentages6,barmode = 'stack',color='Situacao', title='Situação dos alunos por Cor/Raça',color_discrete_sequence=colors)
fig7.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Cor/Raca'})

#SituaçãoxEscola
df_sem_traco3 = df_agrupado_telematica[df_agrupado_telematica.Tipo_da_escola_anterior!='-']
counts7 = df_sem_traco3.groupby(['Tipo_da_escola_anterior','Situacao']).size()
counts7 = counts7.unstack(level=-1)

totals7 = counts7.sum(axis=1)
percentages7 = counts7.divide(totals7, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig20 = px.bar(percentages7,barmode = 'stack',color='Situacao', title='Situação dos alunos por Tipo da escola anterior',color_discrete_sequence=colors)
fig20.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Tipo da escola anterior'})

#FaixadeRenda
counts8 = df_agrupado_telematica.groupby(['Faixa_de_renda_(SISTEC)','Situacao']).size()
counts8 = counts8.unstack(level=-1)

totals8 = counts8.sum(axis=1)
percentages8 = counts8.divide(totals8, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig8 = px.bar(percentages8,barmode = 'stack',color='Situacao', title='Situação dos alunos por Faixa de renda (SISTEC)',color_discrete_sequence=colors)
fig8.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Faixa de renda (SISTEC)'})

#SituaçãoxIdade
df_idade_maior_30 = df_agrupado_telematica[df_agrupado_telematica.Idade>=30]
colors = ['#FF6347','#9ACD32','#6495ED','black']

fig9 = px.pie(values=df_idade_maior_30['Situacao'].value_counts(), names=df_idade_maior_30['Situacao'].value_counts().index,
             color_discrete_sequence=colors)

fig9.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Situação dos Alunos com idade maior que 30')

fig9.update_traces(textfont_size=16)

df_idade_menor_30 = df_agrupado_telematica[df_agrupado_telematica.Idade<=30]
colors = ['#FF6347','#6495ED','#9ACD32','black']

fig10 = px.pie(values=df_idade_menor_30['Situacao'].value_counts(), names=df_idade_menor_30['Situacao'].value_counts().index,
             color_discrete_sequence=colors)

fig10.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Situação dos Alunos com idade menor que 30')

fig10.update_traces(textfont_size=16)

#SituaçãoxCota
df_sem_traco4 = df_agrupado_telematica[df_agrupado_telematica.Cota_SISTEC!='-']
counts9 = df_sem_traco4.groupby(['Cota_SISTEC','Situacao']).size()
counts9 = counts9.unstack(level=-1)

totals9 = counts9.sum(axis=1)
percentages9 = counts9.divide(totals9, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig11 = px.bar(percentages9,barmode = 'stack',color='Situacao', title='Situação dos alunos por Cota SISTEC',color_discrete_sequence=colors)
fig11.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Cota SISTEC'})

#Coeficiente de progressão

df_evadidos = df_agrupado_telematica[(df_agrupado_telematica.Situacao.isin(['evadido/trancado'])) & (df_agrupado_telematica.Coeficiente_de_progressao!='-')]
df_matriculado = df_agrupado_telematica[(df_agrupado_telematica.Situacao.isin(['matriculado'])) & (df_agrupado_telematica.Coeficiente_de_progressao!='-')]
df_formado = df_agrupado_telematica[(df_agrupado_telematica.Situacao.isin(['formado'])) & (df_agrupado_telematica.Coeficiente_de_progressao!='-')]

#Evadido
df_notas_evadidos = df_evadidos['Coeficiente_de_progressao']
df_notas_evadidos =  df_notas_evadidos.astype(str).str.replace(',','.')
df_notas_evadidos = df_notas_evadidos.astype(float)
df_notas_evadidos = df_notas_evadidos.mean()

#Matriculado
df_notas_matriculados = df_matriculado['Coeficiente_de_progressao']
df_notas_matriculados =  df_notas_matriculados.astype(str).str.replace(',','.')
df_notas_matriculados = df_notas_matriculados.astype(float)
df_notas_matriculados = df_notas_matriculados.mean()

#Formado
df_notas_formados = df_formado['Coeficiente_de_progressao']
df_notas_formados =  df_notas_formados.astype(str).str.replace(',','.')
df_notas_formados = df_notas_formados.astype(float)
df_notas_formados = df_notas_formados.mean()

colors = ['#6495ED','#FF6347','#9ACD32']
fig21 = px.bar(x=['matriculado','evadido/trancado','formado'],y=[df_notas_matriculados,df_notas_evadidos,df_notas_formados], title='Situação dos alunos pelas médias do Coeficiente de Progressão',color_discrete_sequence=[colors])
fig21.update_layout(yaxis={'title':'Notas'},
                   xaxis={'title': 'Áreas'})
#SituaçãoxNotasSeleção

df_evadidos = df_agrupado_telematica[df_agrupado_telematica.Situacao.isin(['evadido/trancado'])]
df_matriculado = df_agrupado_telematica[df_agrupado_telematica.Situacao.isin(['matriculado'])]
df_formado = df_agrupado_telematica[df_agrupado_telematica.Situacao.isin(['formado'])]

#Evadido
df_notas_evadidos = df_evadidos['Notas_da_selecao'].str.split('; ', expand=True)

df_notas_evadidos.columns = ['C.N.T.', 'C.H.T.', 'L.C.T.', 'M.T.', 'RED.']
df_notas_evadidos = df_notas_evadidos.dropna()


df_notas_evadidos = df_notas_evadidos.replace(r'[a-zA-Z\.= ]+', '', regex=True)
df_notas_evadidos = df_notas_evadidos.replace(r'(?<!\d)\.(?!\d)', '', regex=True)
df_notas_evadidos = df_notas_evadidos.replace(r'.*:', '', regex=True)
df_notas_evadidos = df_notas_evadidos.astype(float).fillna(0)

df_notas_evadidos = df_notas_evadidos / 100
df_notas_evadidos = df_notas_evadidos.mean()

#Matriculado
df_notas_matriculados = df_matriculado['Notas_da_selecao'].str.split('; ', expand=True)

df_notas_matriculados.columns = ['C.N.T.', 'C.H.T.', 'L.C.T.', 'M.T.', 'RED.']
df_notas_matriculados = df_notas_matriculados.dropna()


df_notas_matriculados = df_notas_matriculados.replace(r'[a-zA-Z\.= ]+', '', regex=True)
df_notas_matriculados = df_notas_matriculados.replace(r'(?<!\d)\.(?!\d)', '', regex=True)
df_notas_matriculados = df_notas_matriculados.replace(r'.*:', '', regex=True)
df_notas_matriculados = df_notas_matriculados.astype(float).fillna(0)

df_notas_matriculados = df_notas_matriculados / 100
df_notas_matriculados = df_notas_matriculados.mean()

#Formado
df_notas_formados = df_formado['Notas_da_selecao'].str.split('; ', expand=True)

df_notas_formados.columns = ['C.N.T.', 'C.H.T.', 'L.C.T.', 'M.T.', 'RED.']
df_notas_formados = df_notas_formados.dropna()


df_notas_formados = df_notas_formados.replace(r'[a-zA-Z\.= ]+', '', regex=True)
df_notas_formados = df_notas_formados.replace(r'(?<!\d)\.(?!\d)', '', regex=True)
df_notas_formados = df_notas_formados.replace(r'.*:', '', regex=True)
df_notas_formados = df_notas_formados.astype(float).fillna(0)

df_notas_formados = df_notas_formados /10
df_notas_formados = df_notas_formados.mean()

df_concat = pd.concat([df_notas_matriculados,df_notas_evadidos,df_notas_formados], axis=1)

df_concat.rename(columns = {0:'matriculado'}, inplace = True)
df_concat.rename(columns = {1:'evadido/trancado'}, inplace = True)
df_concat.rename(columns = {2:'formado'}, inplace = True)

colors = ['#6495ED','#FF6347','#9ACD32']
fig12 = px.bar(df_concat, title='Situação dos alunos por Notas de Seleção',color_discrete_sequence=colors,barmode="group")
fig12.update_layout(yaxis={'title':'Notas'},
                   xaxis={'title': 'Áreas'})


#Situação por semestres das alunas
df_matricula_engenharia = df_telematica_novo[(df_telematica_novo.Sexo=='f')]
df_matricula_engenharia.loc[:,'Matricula'] = df_matricula_engenharia['Matricula'].astype(str)

colors = ['#FF6347','black','#9ACD32','#6495ED']

counts10 = df_matricula_engenharia.groupby(['Matricula', 'Situacao']).size()
counts10 = counts10.unstack(level=-1)

totals10 = counts10.sum(axis=1)
percentages10 = counts10.divide(totals10, axis=0)*100


fig13 = px.bar(percentages10,barmode = 'stack',color='Situacao', title='Situação dos alunos do sexo feminino por Semestre de Ingresso',color_discrete_sequence=colors)
fig13.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})

#Alunas matriculadas por Semestre
df_matricula_engenharia1 = df_telematica_novo[(df_telematica_novo.Sexo=='f')]
df_matricula_engenharia1.loc[:,'Matricula'] = df_matricula_engenharia1['Matricula'].astype(str)
grafico_matricula_engenharia1 = df_matricula_engenharia1['Matricula'].value_counts().sort_index()

colors = ['#6495ED']

fig14 = px.bar(grafico_matricula_engenharia1,barmode = 'stack', title='Quantidade de Alunas matriculadas por Semestre de Ingresso',color_discrete_sequence=colors)
fig14.update_layout(yaxis={'title':'Quantidade de alunas matriculadas'},
                   xaxis={'title': 'Semestre'},showlegend=False)

#Situação por semestres dos alunos
df_matricula_engenharia2 = df_telematica_novo[(df_telematica_novo.Sexo=='m')]
df_matricula_engenharia2.loc[:,'Matricula'] = df_matricula_engenharia2['Matricula'].astype(str)

colors = ['#FF6347','#9ACD32','#6495ED']

counts11 = df_matricula_engenharia2.groupby(['Matricula', 'Situacao']).size()
counts11 = counts11.unstack(level=-1)

totals11 = counts11.sum(axis=1)
percentages11 = counts11.divide(totals11, axis=0)*100


fig15 = px.bar(percentages11,barmode = 'stack',color='Situacao', title='Situação dos alunos do sexo masculino por Semestre de Ingresso',color_discrete_sequence=colors)
fig15.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})

#Situação por semestre
df_telematica_novo.loc[:,'Matricula'] = df_telematica_novo['Matricula'].astype(str)

counts12 = df_telematica_novo.groupby(['Matricula', 'Situacao']).size()
counts12 = counts12.unstack(level=-1)

totals12 = counts12.sum(axis=1)
percentages12 = counts12.divide(totals12, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']
fig16 = px.bar(percentages12,barmode = 'stack',color='Situacao', title='Situação dos alunos de cada semestre em Telemática',color_discrete_sequence=colors)
fig16.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})

#Meses conclusão
colors = ['orange']
fig17 = px.histogram(df_conclusao_tel,x='Meses Conclusao',color_discrete_sequence=colors,title='Meses Conclusão - Telemática')

#Tempo Conclusão

concluintes_certo = df_conclusao_tel[df_conclusao_tel['Meses Conclusao'] > 36]['Meses Conclusao'].value_counts().sum()
percent = (concluintes_certo / len(df_conclusao_tel)) * 100

labels = ['Superior 36 meses ', 'Igual ou inferior a 36 meses']
sizes = [percent, 100-percent]
colors = ["royalblue","orange"]

fig18 = px.pie(values=sizes, names=['Superior 36 meses','Igual ou inferior a 36 meses'],color_discrete_sequence=colors)

fig18.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Tempo de Conclusão - Telemática')

fig18.update_traces(textfont_size=16)

#Quantidade Alunos Engenharia
total_alunos_eng = len(df_telematica['Situacao'])
fig19 = go.Figure()
fig19 = go.Figure(go.Indicator(
    mode = "number",
    value = total_alunos_eng,))
fig19.update_layout(
    template = {'data' : {'indicator': [{
        'title': {'text': "TOTAL DE ALUNOS DO CURSO DE TELEMÁTICA "},}]
                         }})
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
                        figure=fig16)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='quantidade-total',
                        figure=fig19)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig14
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
                        figure=fig15)
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
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig7)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig8
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig5
                    )),style={"width": "100%"},
            ),width=3)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig3
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig4)
                    ),style={"width": "100%"},
        ),width=6),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig20
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig6)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig11)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig12
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig9)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig10
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig21
                    )),style={"width": "100%"},
            ),width=3)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig17
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig18)
                    ),style={"width": "100%"},
        ),width=6),
    ],style={"width": "100%"}),
    
],style={"width": "100%"})


