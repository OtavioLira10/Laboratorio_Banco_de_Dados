import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import numpy as np  
import seaborn as sns
import matplotlib.patches as patches
import plotly.express as px
import squarify
from matplotlib_venn import venn2

#Terceira-A -V
def gerar_grafico_pareto(df_historicos):

    reprovacoes = df_historicos['motivo_reprovacao'].value_counts()
    

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

#LETRA B
def gerar_grafico_area_empilhada(df_turmas, df_professores):

    df_merged = df_turmas.merge(df_professores, on="cod_prof")
    

    print("Dados mesclados:")
    print(df_merged.head())


    if df_merged.empty:
        print("DataFrame mesclado está vazio. Verifique os dados de entrada.")
        return


    df_grouped = df_merged.groupby(["ano", "semestre", "cod_curso"]).size().unstack().fillna(0)


    print("Dados agrupados após o merge:")
    print(df_grouped)

    anos_semestres = [f'{ano}.{semestre}' for ano, semestre in zip(df_grouped.index.get_level_values('ano'), df_grouped.index.get_level_values('semestre'))]
    cursos = df_grouped.columns

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.stackplot(anos_semestres, df_grouped.T, labels=cursos)
    ax.set_title("Quantidade de Professores por Curso ao Longo do Tempo")
    ax.set_xlabel("Ano.Semestre")
    ax.set_ylabel("Número de Professores")
    ax.legend(title="cod_curso", loc="upper right")
    plt.xticks(rotation=45) 
    plt.tight_layout()
    plt.show()



#TERCEIRA C- V
def gerar_grafico_rosca(df_historicos):
    df_reprovados = df_historicos[df_historicos['situacao'] == 'RM']
    
    reprovacoes_por_disciplina = df_reprovados['cod_disc'].value_counts()

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(reprovacoes_por_disciplina, 
                                       labels=reprovacoes_por_disciplina.index,
                                       autopct='%1.1f%%',
                                       startangle=90,
                                       wedgeprops=dict(width=0.3))

    ax.set_title('Proporção de Alunos que Não Passaram na Primeira Tentativa por Disciplina')
    plt.setp(autotexts, size=10, weight="bold", color="white")
    
    plt.show()

#LETRA D- V
def gerar_grafico_cascata(df_historicos, periodo_coluna='motivo_reprovacao', curso_coluna='cod_disc'):
    alunos_por_curso = df_historicos.groupby(['ano', 'semestre', curso_coluna]).size().unstack(fill_value=0)

    total_acumulado = alunos_por_curso.cumsum()

    total_acumulado['ano_semestre'] = total_acumulado.index.map(lambda x: f"{x[0]}-{x[1]}")

    plt.figure(figsize=(12, 6))
    plt.title('Quantidade de Alunos por Disciplina ao Longo do Tempo')

    for curso in total_acumulado.columns[:-1]:  
        plt.plot(total_acumulado['ano_semestre'], total_acumulado[curso], label=curso)

    plt.xlabel('Ano/Semestre')
    plt.ylabel('Quantidade de Alunos')
    plt.xticks(rotation=45)
    plt.legend(title='Disciplinas')
    plt.grid()
    plt.tight_layout()
    plt.show()

#LETRA E
def gerar_boxplot_seaborn(df_historicos, curso_coluna='cod_disc', media_coluna='media'):
    if curso_coluna not in df_historicos.columns or media_coluna not in df_historicos.columns:
        raise ValueError(f"As colunas '{curso_coluna}' ou '{media_coluna}' não foram encontradas no DataFrame.")

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
    situacao_counts = df_historicos.groupby('mat_alu')['situacao'].value_counts().unstack(fill_value=0)
    
    situacao_counts['total'] = situacao_counts.sum(axis=1)
    situacao_counts['percentual_aprovacao'] = (situacao_counts.get('AP', 0) / situacao_counts['total']) * 100
    situacao_counts['percentual_reprovacao'] = (situacao_counts.get('RM', 0) / situacao_counts['total']) * 100
    
    return situacao_counts[['percentual_aprovacao', 'percentual_reprovacao']].reset_index()


def gerar_grafico_radar(df_percentuais):
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




def calcular_percentual_aprovacao(df_historicos, cod_disciplina):
    df_disciplina = df_historicos[df_historicos['cod_disc'] == cod_disciplina]
    
    total_alunos = len(df_disciplina)
    aprovados = len(df_disciplina[df_disciplina['situacao'] == 'AP'])
    
    if total_alunos > 0:
        percentual_aprovacao = (aprovados / total_alunos) * 100
    else:
        percentual_aprovacao = 0
    
    return percentual_aprovacao

def gerar_grafico_termometro(percentual_aprovacao):
    fig, ax = plt.subplots(figsize=(2, 6))  

    bulbo = patches.Circle((0.5, 0.1), 0.15, color='red', ec='black', lw=1.5)
    ax.add_patch(bulbo)

    corpo = patches.Rectangle((0.4, 0.1), 0.2, 0.7, color='lightgray', ec='black', lw=1.5)
    ax.add_patch(corpo)

    altura_percentual = percentual_aprovacao / 100 * 0.7 
    preenchimento = patches.Rectangle((0.4, 0.1), 0.2, altura_percentual, color='red', ec='black', lw=1.5)
    ax.add_patch(preenchimento)

    ax.text(0.5, 0.85, f'{percentual_aprovacao:.1f}%', ha='center', fontsize=16, color='black', fontweight='bold')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')  

    plt.title('Percentual de Aprovação')
    plt.show()


    
def calcular_mgp(df_historicos):
    """
    Função para calcular as Médias Gerais Ponderadas (MGP) de cada aluno.
    A função espera que o DataFrame contenha as colunas 'mat_alu' e 'media'.
    """
    mgp = df_historicos.groupby('mat_alu')['media'].mean().reset_index()
    mgp.columns = ['mat_alu', 'MGP']
    
    return mgp

def filtrar_top_10(mgp):
    """
    Filtra os 10 alunos com as maiores MGPs.
    """
    top_10 = mgp.nlargest(10, 'MGP')
    return top_10


def gerar_grafico_squarify(mgp):
    """
    Gera um gráfico Treemap usando a biblioteca squarify.
    """
    plt.figure(figsize=(10, 6))
    squarify.plot(sizes=mgp['MGP'], label=mgp['mat_alu'], alpha=0.8)
    plt.title('Top 10 Alunos com Maiores Médias Gerais Ponderadas (MGP)', fontsize=15)
    plt.axis('off')  
    plt.show()

#Letra I
def gerar_grafico_venn(coordenadores, professores):
    set_coordenadores = set(coordenadores['cod_prof'])
    set_professores = set(professores['cod_prof'])

    plt.figure(figsize=(8, 8))
    venn2([set_coordenadores, set_professores], ('Coordenadores', 'Professores'))
    plt.title('Interseção entre Coordenadores e Professores')
    plt.show()


    
def gerar_heatmap_turmas(df_turmas):

    heatmap_data = (
        df_turmas.groupby(['disciplinas', 'ano', 'semestre'])
        .agg(num_alunos=('num_alunos', 'sum')) 
        .reset_index()
    )
    
    heatmap_data = heatmap_data.nlargest(10, 'num_alunos')

    pivot_table = heatmap_data.pivot('disciplinas', 'ano_semestre', 'num_alunos')

    # Gerar o heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlGnBu")  
    plt.title('Heatmap das 10 Turmas com Mais Alunos por Disciplina/Ano/Semestre')
    plt.ylabel('Disciplinas')
    plt.xlabel('Ano/Semestre')
    plt.show()


def gerar_heatmap_turmas(df_turmas_alunos):

    heatmap_data = df_turmas_alunos.pivot(index="ano", columns="nom_disc", values="total_alunos")
    
    plt.figure(figsize=(10, 3))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", cbar_kws={'label': 'Total de Alunos'})
    plt.title('Heatmap das Turmas com Mais Alunos por Disciplina e Ano')
    plt.xlabel('Disciplina')
    plt.ylabel('Ano')
    plt.show()


def gerar_grafico_sankey(df):
    # Obter cursos e disciplinas
    cursos = df['nom_curso'].unique()
    disciplinas = df['nom_disc'].unique()

    # Criar dicionários para mapear os nomes para índices
    curso_to_index = {curso: i for i, curso in enumerate(cursos)}
    disc_to_index = {disc: i + len(cursos) for i, disc in enumerate(disciplinas)}  # Offset para disciplinas

    # Criar listas para os dados do gráfico
    source = []
    target = []
    value = []

    # Preencher as listas com os dados do DataFrame
    for _, row in df.iterrows():
        source.append(curso_to_index[row['nom_curso']])
        target.append(disc_to_index[row['nom_disc']])
        value.append(1)  # Cada linha representa um fluxo de 1

    # Criar o gráfico de Sankey
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=list(cursos) + list(disciplinas)
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    ))

    fig.update_layout(title_text='Fluxo de Alunos entre Cursos e Disciplinas', font_size=10)
    fig.show()