import altair as alt
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
        st.markdown('# Segundos ciclos IMD')

        self.options = {
            'ciclo': st.selectbox('Ciclo', ['Primeiro', 'Segundo', ]),
        }

        df_graduacao = df[df.nivel_ensino == 'GRADUAÇÃO']
        df_graduacao_natal = df_graduacao[~df_graduacao.nome_unidade.isin(self.outros_campi)]

        df_chart = self._filter_by_ciclo(df_graduacao_natal, self.options['ciclo'])
        df_chart['sexo'] = df_chart['sexo'].replace({
            'F': 'Feminino',
            'M': 'Masculino',
        })

        alt_chart = alt.Chart(df_chart).mark_bar().encode(
            x=alt.X('sexo:O', title=None),
            y=alt.Y('count(sexo):Q', title='Quantidade de ingressantes'),
            color='sexo:N',
            column=alt.Column('ano_ingresso:N', title='Ano de ingresso'),
            tooltip=[alt.Tooltip('count(sexo):Q', title='Quantidade de ingressantes'), alt.Tooltip('sexo', title='Gênero'),]
        )

        st.altair_chart(alt_chart)

    def _filter_by_ciclo(self, df, value):
        df_filter = df[df.nome_curso.isin(self.ciclos[value.lower()])]

        if value == 'Segundo':
            df_filter = df_filter[df_filter.ano_ingresso > 2013]

        return df_filter
