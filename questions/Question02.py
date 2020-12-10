import altair as alt
import pandas as pd
import streamlit as st
from questions import Question


class Question02(Question):

    def __init__(self):
        self.ciclos = {
            'primeiro': ['TECNOLOGIA DA INFORMAÇÃO', ],
            'segundo': ['ENGENHARIA DE SOFTWARE', 'CIÊNCIA DA COMPUTAÇÃO', ]
        }
        self.outros_campi = {
            'Jundiai': 'ESCOLA AGRÍCOLA DE JUNDIAÍ',
            'Serido': 'CENTRO DE  ENSINO SUPERIOR DO SERIDÓ',
            'Facisa': 'FACULDADE DE CIÊNCIAS DA SAÚDE DO TRAIRI - FACISA',
        }

    def render(self, df):
        st.markdown('# Porcentagem de mulheres ingressantes, por ano de ingresso e ciclo do IMD')

        df_graduacao = df[df.nivel_ensino == 'GRADUAÇÃO']
        df_graduacao_natal = df_graduacao[~df_graduacao.nome_unidade.isin(self.outros_campi)]

        df_chart = self._filter_by_ciclo(df_graduacao_natal)
        df_chart = self._comparar_ingressantes(df_chart)
        df_chart = df_chart.reset_index()

        alt_chart = alt.Chart(df_chart).mark_bar().encode(
            x=alt.X('ciclo:O', title=None),
            y=alt.Y('porcentagem:Q', title='% de mulheres ingressantes'),
            color=alt.Color('ciclo:N', title='Ciclo'),
            column=alt.Column('ano_ingresso:N', title='Ano de ingresso'),
            tooltip=[
                alt.Tooltip('ciclo', title='Ciclo'),
                alt.Tooltip('sum(porcentagem):Q', title='% de ingressantes', format='.2f'),
            ]
        ).properties(width=47)

        st.altair_chart(alt_chart)

    def _filter_by_ciclo(self, df):
        df_primeiro = df[df.nome_curso.isin(self.ciclos['primeiro'])]
        df_primeiro.loc[:, 'ciclo'] = 'Primeiro'
        df_segundo = df[df.nome_curso.isin(self.ciclos['segundo'])]
        df_segundo = df_segundo[df_segundo.ano_ingresso > 2013]
        df_segundo.loc[:, 'ciclo'] = 'Segundo'

        return pd.concat([df_primeiro, df_segundo])

    def _comparar_ingressantes(self, df):
        valores = df.groupby(by=(['ciclo', 'ano_ingresso', 'sexo']))['sexo'].count().unstack()
        valores.loc[:, 'porcentagem'] = valores['F']/(valores['F']+valores['M']) * 100
        return valores
