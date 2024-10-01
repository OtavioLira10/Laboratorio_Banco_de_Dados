import pandas as pd

def transform_historicos(df_historicos):
    # Verificar e transformar todas as colunas de datas para o formato YYYYMMDD
    if 'data_reprovacao' in df_historicos.columns:
        df_historicos['data_reprovacao'] = pd.to_datetime(df_historicos['data_reprovacao']).dt.strftime('%Y%m%d')
    
    # Criar coluna indicando motivo de reprovação
    df_historicos['motivo_reprovacao'] = None  
    df_historicos.loc[df_historicos['situacao'] == 'RF', 'motivo_reprovacao'] = 'Faltas'
    df_historicos.loc[df_historicos['situacao'] == 'RM', 'motivo_reprovacao'] = 'Média'

    return df_historicos

def transform_turmas(df_turmas):
    df_turmas.rename(columns={'tot_vagas': 'total_vagas', 'vag_ocup': 'vagas_ocupadas'}, inplace=True)

    if 'vagas_ocupadas' in df_turmas.columns and 'total_vagas' in df_turmas.columns:
        df_turmas.loc[df_turmas['vagas_ocupadas'] > df_turmas['total_vagas'], 'vagas_ocupadas'] = df_turmas['total_vagas']
    
    # Criar coluna combinando Ano e Semestre
    df_turmas['Ano/Semestre'] = df_turmas['ano'].astype(str) + '.' + df_turmas['semestre'].astype(str)

    return df_turmas


def transform_cursos(df_cursos, df_professores):
    # Fazer o join para adicionar o nome do coordenador
    df_cursos = df_cursos.merge(df_professores[['cod_prof', 'nom_prof']], 
                                left_on='cod_coord', right_on='cod_prof', how='left')
    
    # Renomear a coluna para nome do coordenador
    df_cursos.rename(columns={'nom_prof': 'nome_coordenador'}, inplace=True)
    
    return df_cursos
