import streamlit as st
from questions import Question


class Question01(Question):

    def __init__(self):
        self.outros_campi = {
            'Jundiai' : 'ESCOLA AGRÍCOLA DE JUNDIAÍ',
            'Serido' : 'CENTRO DE  ENSINO SUPERIOR DO SERIDÓ',
            'Facisa' : 'FACULDADE DE CIÊNCIAS DA SAÚDE DO TRAIRI - FACISA',
        }
        self.pos_graduacao = [
            'LATO SENSU',
            'MESTRADO',
            'DOUTORADO',
            'STRICTO SENSU',
            'RESIDÊNCIA',
        ]

    def render(self, df):
        st.markdown("# Comparação no número de homens e mulheres ingressantes, por ano")

        col1, col2 = st.beta_columns(2)
        self.options = {
            'nivel_ensino': col1.selectbox("Nível de Ensino", ['-', 'Graduação', 'Pós Graduação']),
            'campus': col2.selectbox("Campus", ['-', 'Natal', 'Serido', 'Facisa', 'Jundiai']),
        }

        df_chart = self._filter_by_nivel_ensino(df, self.options['nivel_ensino'])
        df_chart = self._filter_by_campus(df_chart, self.options['campus'])
        if not df_chart.empty:
            df_result = self._comparar_ingressantes(df_chart)
            st.dataframe(df_result)

    def _filter_by_nivel_ensino(self, df, value):
        if value == 'Pós Graduação':
            return df[df.nivel_ensino.isin(self.pos_graduacao)]
        elif value == 'Graduação':
            return df[df.nivel_ensino == 'GRADUAÇÃO']

        return df

    def _filter_by_campus(self, df, value):
        if value == 'Natal':
            return df[~df.nome_unidade.isin(list(self.outros_campi.values()))]
        elif value in ['Jundiai', 'Serido', 'Facisa',]:
            return df[df.nome_unidade == self.outros_campi[value]]

        return df

    def _comparar_ingressantes(self, df):
        valores = df.groupby(by=(['ano_ingresso', 'sexo']))['sexo'].count().unstack()
        valores['porcentagem'] = valores['F']/(valores['F']+valores['M']) * 100
        return valores