import altair as alt
import pandas as pd
import streamlit as st
from questions import Question


class Question04(Question):

    def __init__(self):
        self.outros_campi = {
            'Jundiai': 'ESCOLA AGRÍCOLA DE JUNDIAÍ',
            'Serido': 'CENTRO DE  ENSINO SUPERIOR DO SERIDÓ',
            'Facisa': 'FACULDADE DE CIÊNCIAS DA SAÚDE DO TRAIRI - FACISA',
        }

    def render(self, df):
        st.markdown('# Evasão e Conclusão por centro')
        dfs = []

        campis = {**self.outros_campi, **{'Natal': 'Natal',}}
        for key, campus in campis.items():
            df_campus = self._calcular_percentuais_by_campus(df.copy(), campus)
            df_campus['nome_unidade'] = campus
            dfs.append(df_campus)

        df_chart = pd.concat(dfs)
        df_chart['sexo'] = df_chart['sexo'].replace({
            'F': 'Feminino',
            'M': 'Masculino',
        })
        df_chart = df_chart.sort_values('percentual', ascending=False)

        alt_chart = alt.Chart(df_chart).mark_bar().encode(
            x=alt.X('nome_unidade:N', title=None),
            y=alt.Y('sum(percentual):Q', stack=False, title='% dos ingressantes'),
            column=alt.Column('tipo:N', title=None),
            color=alt.Color('sexo', title='Gênero'),
            tooltip=[
                alt.Tooltip('sexo', title='Gênero'),
                alt.Tooltip('sum(percentual):Q', title='% dos ingressantes')
            ],
        )
        st.altair_chart(alt_chart)

    def _calcular_percentuais_by_campus(self, df, campus):
        if campus == 'Natal':
            df_campus = df[~df.nome_unidade.isin(self.outros_campi)]
        else:
            df_campus = df[df.nome_unidade == campus]

        df_evasao = df_campus[df_campus.status == 'CANCELADO']
        df_concluintes = df_campus[df_campus.status == 'CONCLUÍDO']

        return self._calcular_percentuais(df_campus, df_evasao, df_concluintes)

    def _calcular_percentuais(self, df_total, df_evasao, df_concluintes):
        evasao_por_sexo = df_evasao.groupby(by='sexo').count()['matricula']
        concluintes_por_sexo = df_concluintes.groupby(by='sexo').count()['matricula']

        sexos = ['F', 'M']
        dados = []
        dados_diff = {}

        for sexo in sexos:
            evasao_total = evasao_por_sexo.loc[sexo]
            evasao_percent = evasao_por_sexo.loc[sexo] / evasao_por_sexo.sum() * 100

            concluintes_total = concluintes_por_sexo.loc[sexo]
            concluintes_percent = concluintes_por_sexo.loc[sexo] / concluintes_por_sexo.sum() * 100

            dados.append([sexo, evasao_total, evasao_percent, 'Evasão'])
            dados.append([sexo, concluintes_total, concluintes_percent, 'Conclusão'])
            dados_diff[sexo] = {
                'concluintes_total': concluintes_total,
                'concluintes_percent': concluintes_percent,
                'evasao_total': evasao_total,
                'evasao_percent': evasao_percent,
            }
        df_sexo = pd.DataFrame(data=dados, columns=['sexo', 'total', 'percentual', 'tipo'])
        df_sexo = df_sexo.append({
            'sexo': 'Diferença',
            'total': abs(dados_diff['M']['evasao_total'] - dados_diff['F']['evasao_total']),
            'percentual': abs(dados_diff['M']['evasao_percent'] - dados_diff['F']['evasao_percent']),
            'tipo': 'Evasão',
        }, ignore_index=True)

        return df_sexo.append({
            'sexo': 'Diferença',
            'total': abs(dados_diff['M']['concluintes_total'] - dados_diff['F']['concluintes_total']),
            'percentual': abs(dados_diff['M']['concluintes_percent'] - dados_diff['F']['concluintes_percent']),
            'tipo': 'Conclusão',
        }, ignore_index=True)
