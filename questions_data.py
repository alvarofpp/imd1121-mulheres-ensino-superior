import pandas as pd

dfs = {
    'discentes': pd.read_csv('./data/discentes.csv', index_col=None, header=0, error_bad_lines=False, sep=';'),
}
outros_campi = [
    'ESCOLA AGRÍCOLA DE JUNDIAÍ',
    'CENTRO DE  ENSINO SUPERIOR DO SERIDÓ',
    'FACULDADE DE CIÊNCIAS DA SAÚDE DO TRAIRI - FACISA',
]

dfs['graduacao'] = dfs['discentes'][dfs['discentes'].nivel_ensino == 'GRADUAÇÃO']
dfs['graduacao_natal'] = dfs['graduacao'][~dfs['graduacao'].nome_unidade.isin(outros_campi)]
#dfs['graduacao_imd'] = dfs['graduacao_natal'][dfs['graduacao_natal'].nome_unidade == 'INSTITUTO METROPOLE DIGITAL']

# Questão 02
print('Questão 02')
graduacao_imd_primeiro_ciclo = dfs['graduacao_natal'][dfs['graduacao_natal']['nome_curso'] == 'TECNOLOGIA DA INFORMAÇÃO']
graduacao_imd_segundo_ciclo = dfs['graduacao_natal'][
    dfs['graduacao_natal']['nome_curso'].isin(['ENGENHARIA DE SOFTWARE', 'CIÊNCIA DA COMPUTAÇÃO'])
]

table01 = graduacao_imd_primeiro_ciclo.groupby(by=['ano_ingresso', 'sexo'])['sexo'].count().unstack()
table02 = graduacao_imd_segundo_ciclo.groupby(by=['ano_ingresso', 'sexo'])['sexo'].count().unstack()
table01 = table01.reset_index(inplace=False)[['ano_ingresso', 'F', 'M']]
table01['ciclo'] = 'primeiro'

table02 = table02.reset_index(inplace=False)[['ano_ingresso', 'F', 'M']]
table02 = table02[table02['ano_ingresso'] > 2013]
table02['ciclo'] = 'segundo'

dataset_02 = pd.concat([
    table01,
    table02,
], axis=0, ignore_index=True)

dataset_02.to_csv('data/questoes/questao_02.csv', index=False)
