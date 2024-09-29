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
