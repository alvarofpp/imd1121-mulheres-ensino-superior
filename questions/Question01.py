import altair as alt
import streamlit as st
from questions import Question


class Question01(Question):

    def __init__(self):
        self.outros_campi = {
            'Jundiai': 'ESCOLA AGRÍCOLA DE JUNDIAÍ',
            'Serido': 'CENTRO DE  ENSINO SUPERIOR DO SERIDÓ',
            'Facisa': 'FACULDADE DE CIÊNCIAS DA SAÚDE DO TRAIRI - FACISA',
        }
        self.pos_graduacao = [
            'LATO SENSU',
            'MESTRADO',
            'DOUTORADO',
            'STRICTO SENSU',
            'RESIDÊNCIA',
        ]

    def render(self, df):
        st.markdown(
            '# Porcentagem de mulheres ingressantes, por ano e por campus, em programas de graduação e pós graduação da UFRN')

        self.options = {
            'nivel_ensino': st.selectbox('Nível de Ensino', ['-', 'Graduação', 'Pós Graduação']),
        }

        df_chart = self._filter_by_nivel_ensino(df, self.options['nivel_ensino'])
        df_natal = ~df_chart['nome_unidade'].isin(list(self.outros_campi.values()))
        df_chart.loc[df_natal, 'nome_unidade'] = 'Natal'
        df_chart['nome_unidade'] = df_chart['nome_unidade'].str.title()

        df_chart = self._comparar_ingressantes(df_chart)
        df_chart = df_chart.reset_index()

        alt_chart = alt.Chart(df_chart).mark_line(point=True).encode(
            x=alt.X('ano_ingresso:N', title='Ano de ingresso'),
            y=alt.Y('sum(porcentagem):Q', title='% de mulheres ingressantes'),
            color=alt.Color('nome_unidade:N', title='Campus',
                            scale=alt.Scale(
                                domain=['Natal', 'Faculdade De Ciências Da Saúde Do Trairi - Facisa',
                                        'Escola Agrícola De Jundiaí', 'Centro De  Ensino Superior Do Seridó'],
                                range=['#5EBCB4', '#F33A4A', '#FF8100', '#4A70AA']
                            )),

            tooltip=[
                alt.Tooltip('nome_unidade', title='Campus'),
                alt.Tooltip('ano_ingresso', title='Ano'),
                alt.Tooltip('sum(porcentagem):Q', title='% de mulheres ingressantes', format='.2f'),
                alt.Tooltip('F', title='Quantidade'),
            ]
        )

        st.altair_chart(alt_chart, use_container_width=True)

    def _filter_by_nivel_ensino(self, df, value):
        if value == 'Pós Graduação':
            return df[df.nivel_ensino.isin(self.pos_graduacao)]
        elif value == 'Graduação':
            return df[df.nivel_ensino == 'GRADUAÇÃO']

        return df

    def _comparar_ingressantes(self, df):
        valores = df.groupby(by=(['ano_ingresso', 'nome_unidade', 'sexo']))['sexo'].count().unstack()
        valores.loc[:, 'porcentagem'] = valores['F'] / (valores['F'] + valores['M']) * 100
        return valores
