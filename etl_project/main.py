from etl.extract import extract_all_data
from etl.transform import transform_historicos, transform_turmas, transform_cursos
from etl.load import load_data
from etl.visualize import gerar_grafico_rosca, gerar_grafico_radar, gerar_boxplot_seaborn, gerar_grafico_area_empilhada, gerar_grafico_cascata, gerar_grafico_pareto, calcular_percentuais_aprovacao_reprovacao

def main():
    # 1. Extração dos dados
    print("Iniciando a extração de dados...")
    df_historicos, df_turmas, df_cursos, df_professores, df_disciplinas = extract_all_data()  # Capture df_disciplinas

    if df_historicos.empty or df_turmas.empty or df_cursos.empty or df_professores.empty or df_disciplinas.empty:
        print("Erro na extração de dados. Encerrando o processo.")
        return  # Encerra a função se a extração falhar

    print("Extração concluída.")

    # 2. Transformação dos dados
    print("Iniciando a transformação de dados...")
    df_historicos = transform_historicos(df_historicos)
    df_turmas = transform_turmas(df_turmas)
    df_cursos = transform_cursos(df_cursos, df_professores)

    print("---" * 50)
    print("Imprimindo os dataframes:")
    print("DATA_FRAME HISTORICOS")
    print(df_historicos.head())
    print("---" * 50)
    print("DATA_FRAME TURMAS")
    print(df_turmas.head())
    print("---" * 50)
    print("DATA_FRAME CURSOS")
    print(df_cursos.head())
    print("---" * 50)
    print("DATA_FRAME PROFESSORES")
    print(df_professores.head())
    print("---" * 50)
    print("DATA_FRAME DISCIPLINAS")
    print(df_disciplinas.head())
    print("---" * 50)

    print("Transformação concluída.")

    print("Iniciando a carga de dados no Data Mart...")
    load_data(df_historicos, 'historico_data_mart')
    load_data(df_turmas, 'turmas_data_mart')
    load_data(df_cursos, 'cursos_data_mart')
    print("Carga concluída com sucesso.")


    gerar_grafico_pareto(df_historicos)
    gerar_grafico_rosca(df_historicos)
    gerar_boxplot_seaborn(df_historicos, curso_coluna='cod_disc', media_coluna='media')

    gerar_grafico_cascata(df_historicos)
    gerar_grafico_area_empilhada(df_professores)
    df_percentuais = calcular_percentuais_aprovacao_reprovacao(df_historicos)
    gerar_grafico_radar(df_percentuais)




if __name__ == "__main__":
    main()
