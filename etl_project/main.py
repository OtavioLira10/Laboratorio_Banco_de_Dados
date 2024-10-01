from etl.extract import extract_all_data, extract_alunos_disciplinas_fora_do_curso, extract_coordenadores_professores, extract_turmas_alunos
from etl.transform import transform_historicos, transform_turmas, transform_cursos
from etl.load import load_data
import pandas as pd
from etl.visualize import (gerar_grafico_rosca, gerar_grafico_radar, 
                           gerar_boxplot_seaborn, gerar_grafico_area_empilhada, 
                           gerar_grafico_cascata, gerar_grafico_pareto, 
                           calcular_percentuais_aprovacao_reprovacao, gerar_grafico_sankey,
                           gerar_grafico_venn, gerar_heatmap_turmas) 

def main():
    # 1. Extração dos dados
    print("Iniciando a extração de dados...")
    df_historicos, df_turmas, df_cursos, df_professores, df_disciplinas = extract_all_data() 

    if df_historicos.empty or df_turmas.empty or df_cursos.empty or df_professores.empty or df_disciplinas.empty:
        print("Erro na extração de dados. Encerrando o processo.")
        return 

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

    print("Carga concluída com sucesso.")



    # #LETRA A
    # #gerar_grafico_pareto(df_historicos)
    # #LETRA B
    # #gerar_grafico_area_empilhada(df_turmas, df_professores)
    # #LETRA C
    # #gerar_grafico_rosca(df_historicos)
    # #LETRA D
    # gerar_grafico_cascata(df_historicos)
    # #LETRA E
    # gerar_boxplot_seaborn(df_historicos, curso_coluna='cod_disc', media_coluna='media')

    # #LETRA F
    # df_percentuais = calcular_percentuais_aprovacao_reprovacao(df_historicos)
    # gerar_grafico_radar(df_percentuais)

    # #LETRA G
    # calcular = calcular_percentual_aprovacao(df_historicos, cod_disciplina=200657)
    # gerar_grafico_termometro(calcular)

    # # 3 LETRA H
    # mgp = calcular_mgp(df_historicos)
    # top_10 = filtrar_top_10(mgp)
    # gerar_grafico_squarify(top_10)

    #LETRA I
    df_coordenadores, df_professores = extract_coordenadores_professores()
    gerar_grafico_venn(df_coordenadores, df_professores)

    #LETRA J
    df_historicos, df_turmas, df_cursos, df_professores, df_disciplinas = extract_all_data()
    df_turmas_alunos = extract_turmas_alunos()
    gerar_heatmap_turmas(df_turmas_alunos)

    #letra k
    # Extração dos alunos que fizeram disciplinas fora do seu curso
    df_disciplinas_fora = extract_alunos_disciplinas_fora_do_curso()
    gerar_grafico_sankey(df_disciplinas_fora)


if __name__ == "__main__":
    main()
