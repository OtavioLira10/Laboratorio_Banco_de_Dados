import pandas as pd
from utils.db_connection import get_db_connection

def extract_data(query):
    engine = get_db_connection()
    try:
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta: {query}")
        print(e)
        return pd.DataFrame()  

def extract_all_data():
    with open("data/queries.sql", "r") as file:
        queries = file.readlines()

    historicos = extract_data(queries[0].strip())
    turmas = extract_data(queries[1].strip())
    cursos = extract_data(queries[2].strip())
    professores = extract_data(queries[3].strip())
    disciplinas = extract_data(queries[4].strip())  

    if (historicos.empty or turmas.empty or cursos.empty or professores.empty or disciplinas.empty):
        print("Uma ou mais tabelas estão vazias ou ocorreram erros na extração.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    return historicos, turmas, cursos, professores, disciplinas  


def extract_turmas_alunos():
    engine = get_db_connection()
    query = """
        SELECT 
            t.ano,
            t.semestre,
            d.nom_disc,
            COUNT(tm.mat_alu) AS total_alunos
        FROM 
            turmas t
        LEFT JOIN 
            turmas_matriculadas tm ON t.ano = tm.ano AND t.semestre = tm.semestre AND t.cod_disc = tm.cod_disc AND t.turma = tm.turma
        LEFT JOIN 
            disciplinas d ON t.cod_disc = d.cod_disc
        GROUP BY 
            t.ano, t.semestre, d.nom_disc
        ORDER BY 
            total_alunos DESC
        LIMIT 10;  -- Ajuste este limite conforme necessário
    """
    df = pd.read_sql(query, engine)
    return df


def extract_coordenadores_professores():
    # Conectar ao banco de dados
    engine = get_db_connection()
    
    # Consultar os coordenadores (aqueles que têm cod_coord na tabela cursos)
    query_coordenadores = """
    SELECT p.cod_prof, p.nom_prof
    FROM professores p
    JOIN cursos c ON p.cod_prof = c.cod_coord
    """
    
    # Consultar todos os professores
    query_professores = """
    SELECT cod_prof, nom_prof
    FROM professores
    """

    # Ler os dados no DataFrame
    df_coordenadores = pd.read_sql(query_coordenadores, engine)
    df_professores = pd.read_sql(query_professores, engine)

    return df_coordenadores, df_professores


def extract_alunos_disciplinas_fora_do_curso():
    engine = get_db_connection()
    
    query = """
    SELECT 
        a.mat_alu,
        a.nom_alu,
        c.nom_curso,
        d.nom_disc
    FROM alunos a
    JOIN cursos c ON a.cod_curso = c.cod_curso
    JOIN turmas_matriculadas tm ON a.mat_alu = tm.mat_alu
    JOIN disciplinas d ON tm.cod_disc = d.cod_disc
    WHERE d.cod_disc NOT IN (
        SELECT cod_disc 
        FROM curriculos 
        WHERE cod_curso = a.cod_curso
    )
    """

    df_disciplinas_fora = pd.read_sql(query, engine)
    return df_disciplinas_fora