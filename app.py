import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from odufrn_downloader import ODUFRNDownloader
import glob
import os



@st.cache
def load_data():

	ufrn_data = ODUFRNDownloader()
	ufrn_data.download_package('discentes')

	path = r'./discentes' 
	all_files = glob.glob(path + "/*.csv")

	li = []

	for filename in all_files:
	    df = pd.read_csv(filename, index_col=None, header=0, error_bad_lines=False, sep=";")
	    li.append(df)

	discentesUFRN = pd.concat(li, axis=0, ignore_index=True)
	return discentesUFRN

def clean_data(df):
	discentesUFRN = df[df['sexo'].isin(['M', 'F'])]
	discentesUFRN.groupby('sexo')['matricula'].count()
	return discentesUFRN

def questao_01(opc_nivel, opc_campus, discentesUFRN):
	outros_campi = ['ESCOLA AGRÍCOLA DE JUNDIAÍ','CENTRO DE  ENSINO SUPERIOR DO SERIDÓ',
                'FACULDADE DE CIÊNCIAS DA SAÚDE DO TRAIRI - FACISA']

	campi_dict_graduacao: {' - ': graduacao_ufrn, 'Natal': graduacao_natal, 'Serido':graduacao_serido,
							'Facisa':graduacao_facisa, 'Jundiai':graduacao_facisa}

	campi_dict_pos: {' - ': pos_ufrn, 'Natal': pos_natal, 'Serido':pos_serido,
							'Facisa':pos_facisa,'Jundiai':pos_facisa}


	if(opc_nivel == "Graduação"):
		# Separando recortes dos dados graduação
		graduacao_ufrn = discentesUFRN[discentesUFRN.nivel_ensino == "GRADUAÇÃO"]

		graduacao_natal = graduacao_ufrn[~graduacao_ufrn.nome_unidade.isin(outros_campi)]

		graduacao_serido = graduacao_ufrn[graduacao_ufrn.nome_unidade == 'CENTRO DE  ENSINO SUPERIOR DO SERIDÓ']

		graduacao_facisa = graduacao_ufrn[graduacao_ufrn.nome_unidade == 'FACULDADE DE CIÊNCIAS DA SAÚDE DO TRAIRI - FACISA']

		graduacao_jundiai = graduacao_ufrn[graduacao_ufrn.nome_unidade == 'ESCOLA AGRÍCOLA DE JUNDIAÍ']

		return(campi_dict_graduacao[opc_campus])

	if(opc_nivel == "Pós Graduação"):
		# Separando recorte dos dados pós graduação
		pos_ufrn = discentesUFRN[discentesUFRN.nivel_ensino.isin(['LATO SENSU','MESTRADO',
		                                                          'DOUTORADO','STRICTO SENSU',
		                                                          'RESIDÊNCIA'])]

		pos_natal = pos_ufrn[~pos_ufrn.nome_unidade.isin(outros_campi)]

		pos_serido = pos_ufrn[pos_ufrn.nome_unidade == 'CENTRO DE  ENSINO SUPERIOR DO SERIDÓ']

		pos_facisa = pos_ufrn[pos_ufrn.nome_unidade == 'FACULDADE DE CIÊNCIAS DA SAÚDE DO TRAIRI - FACISA']

		pos_jundiai = pos_ufrn[pos_ufrn.nome_unidade == 'ESCOLA AGRÍCOLA DE JUNDIAÍ']

		return(campi_dict_pos[opc_campus])

	else:
		return (discentesUFRN)



def main():
	# TODO app
	discentesUFRN = load_data()
	discentesUFRN = clean_data(discentesUFRN)

	st.title("Mulheres na UFRN")
	st.subheader("Comparação no número de homens e mulheres ingressantes, por ano")

	
	col1, col2 = st.beta_columns(2)

	opc_nivel = col1.selectbox("Nível de Ensino", [' - ', 'Graduação', 'Pós Graduação'])
	opc_campus = col2.selectbox("Campus", [' - ', 'Natal', 'Serido', 'Facisa', 'Jundiai'])

	dados_q1 = questao_01(opc_nivel, opc_campus, discentesUFRN)


	st.write(dados_q1)



if __name__ == "__main__":
    main()
