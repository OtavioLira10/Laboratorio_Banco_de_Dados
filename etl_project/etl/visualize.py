import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import numpy as np  
import seaborn as sns


def gerar_grafico_pareto(df_historicos):
    # Filtrar dados relevantes
    reprovacoes = df_historicos['motivo_reprovacao'].value_counts()
    
    # Ordenar e calcular porcentagens
    reprovacoes = reprovacoes.sort_values(ascending=False)
    cumulativo = reprovacoes.cumsum() / reprovacoes.sum() * 100
    
    fig, ax = plt.subplots()
    ax.bar(reprovacoes.index, reprovacoes.values, color='C0')
    ax2 = ax.twinx()
    ax2.plot(reprovacoes.index, cumulativo, color='C1', marker='o', linewidth=2)
    
    ax.set_ylabel('Número de Reprovações')
    ax2.set_ylabel('Porcentagem Cumulativa')
    ax.set_title('Pareto de Reprovações por Motivo')
    plt.show()


def gerar_grafico_area_empilhada(df_professores):
    # Verifica se as colunas necessárias existem
    print("Colunas disponíveis no DataFrame:", df_professores.columns)  # Para depuração

    # Agrupa por cod_curso e conta o número de professores
    professores_por_curso = df_professores['cod_curso'].value_counts().reset_index()
    professores_por_curso.columns = ['cod_curso', 'quantidade']

    # Criar gráfico de área empilhada com matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(professores_por_curso['cod_curso'], professores_por_curso['quantidade'], label='Professores', color='skyblue')
    plt.title('Quantidade de Professores por Curso')
    plt.xlabel('Código do Curso')
    plt.ylabel('Número de Professores')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Criar gráfico de área empilhada com plotly
    fig = go.Figure(data=[go.Bar(x=professores_por_curso['cod_curso'], 
                                  y=professores_por_curso['quantidade'],
                                  name='Professores')])

    fig.update_layout(
        title='Quantidade de Professores por Curso',
        xaxis_title='Código do Curso',
        yaxis_title='Número de Professores',
        legend_title='Cursos'
    )
    fig.show()


def gerar_grafico_rosca(df_historicos):
    # Filtrar apenas os alunos que não passaram na primeira tentativa
    df_reprovados = df_historicos[df_historicos['situacao'] == 'RM']
    
    # Contar o número de reprovações por disciplina
    reprovacoes_por_disciplina = df_reprovados['cod_disc'].value_counts()

    # Criar o gráfico de rosca
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(reprovacoes_por_disciplina, 
                                       labels=reprovacoes_por_disciplina.index,
                                       autopct='%1.1f%%',
                                       startangle=90,
                                       wedgeprops=dict(width=0.3))

    # Adiciona título e formato do gráfico
    ax.set_title('Proporção de Alunos que Não Passaram na Primeira Tentativa por Disciplina')
    plt.setp(autotexts, size=10, weight="bold", color="white")
    
    # Exibe o gráfico
    plt.show()


def gerar_grafico_cascata(df_historicos, periodo_coluna='motivo_reprovacao', curso_coluna='cod_disc'):
    # Agrupa os dados para contar o número de alunos por disciplina e por semestre
    alunos_por_curso = df_historicos.groupby(['ano', 'semestre', curso_coluna]).size().unstack(fill_value=0)

    # Cálculo do total acumulado para o gráfico de cascata
    total_acumulado = alunos_por_curso.cumsum()

    # Cria uma nova coluna que combina ano e semestre
    total_acumulado['ano_semestre'] = total_acumulado.index.map(lambda x: f"{x[0]}-{x[1]}")

    # Configuração do gráfico
    plt.figure(figsize=(12, 6))
    plt.title('Quantidade de Alunos por Disciplina ao Longo do Tempo')

    for curso in total_acumulado.columns[:-1]:  # Exclui a coluna 'ano_semestre'
        plt.plot(total_acumulado['ano_semestre'], total_acumulado[curso], label=curso)

    plt.xlabel('Ano/Semestre')
    plt.ylabel('Quantidade de Alunos')
    plt.xticks(rotation=45)
    plt.legend(title='Disciplinas')
    plt.grid()
    plt.tight_layout()
    plt.show()


def gerar_boxplot_seaborn(df_historicos, curso_coluna='cod_disc', media_coluna='media'):
    # Verifica se as colunas existem
    if curso_coluna not in df_historicos.columns or media_coluna not in df_historicos.columns:
        raise ValueError(f"As colunas '{curso_coluna}' ou '{media_coluna}' não foram encontradas no DataFrame.")

    # Configuração do gráfico
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=curso_coluna, y=media_coluna, data=df_historicos)
    
    plt.title('Distribuição das Médias Gerais por Curso')
    plt.xlabel('Curso')
    plt.ylabel('Média Geral')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()


def calcular_percentuais_aprovacao_reprovacao(df_historicos):
    # Contar quantos alunos estão aprovados e reprovados
    situacao_counts = df_historicos.groupby('mat_alu')['situacao'].value_counts().unstack(fill_value=0)
    
    # Calcular percentuais
    situacao_counts['total'] = situacao_counts.sum(axis=1)
    situacao_counts['percentual_aprovacao'] = (situacao_counts.get('AP', 0) / situacao_counts['total']) * 100
    situacao_counts['percentual_reprovacao'] = (situacao_counts.get('RM', 0) / situacao_counts['total']) * 100
    
    # Resetar índice para facilitar o acesso
    return situacao_counts[['percentual_aprovacao', 'percentual_reprovacao']].reset_index()


def gerar_grafico_radar(df_percentuais):
    # Gráfico de radar com Plotly
    fig = go.Figure()
    for index, row in df_percentuais.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row[['percentual_aprovacao', 'percentual_reprovacao']].tolist() + [row[['percentual_aprovacao', 'percentual_reprovacao']].iloc[0]],
            theta=['Aprovação', 'Reprovação'],
            fill='toself',
            name=str(row['mat_alu'])
        ))

    fig.update_layout(
        title='Percentuais de Aprovação e Reprovação por Aluno (Plotly)',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True
    )
    config = {'displayModeBar': False}
    fig.show()

   
