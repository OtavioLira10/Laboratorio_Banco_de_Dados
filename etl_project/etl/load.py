from utils.db_connection import get_db_connection

def load_data(df, table_name):
    engine = get_db_connection()
    df.to_sql(table_name, engine, if_exists='replace', index=False)  
