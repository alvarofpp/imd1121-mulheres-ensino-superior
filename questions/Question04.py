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
        st.markdown(
            '# Percentual de homens e mulheres que ingressaram, evadiram e concluíram, em cada centro da UFRN')
        st.markdown(
            'O gráfico a seguir retrata o percentual de discentes dos sexos feminino e masculino que ingressaram, concluíram e evadiram por cada centro da UFRN.')
        st.markdown('#### Como interpretar o gráfico')
        st.markdown('''
                - Cada barra representa os valores para um dos centros de ensino da UFRN;
                - Na parte superior do gráfico está representado o percentual de discentes do sexo masculino, enquanto na parte inferior está expresso o percentual de discentes do sexo feminino;
                - A barra empilhada representa o percentual dos totais de ingressantes daquele sexo que concluíram e evadiram. A parte mais próxima do eixo X corresponde a de maior valor. Exemplo: se a barra de conclusão estiver mais próximo do eixo X que a barra de evasão, significa que concluíram mais pessoas do que evadiram.
                ''')
        st.markdown(
            '**Observação**: é importante ressaltar que os valores negativos no eixo y ("% do total de discentes"), quando estamos observando o percentual de discentes do sexo feminino, não indica um valor negativo em si - esse formato foi utilizado por limitações da ferramenta.')

        dfs = []
        df = df[df['nome_unidade_gestora'].notna()]
        df = df[df['nome_unidade_gestora'].str.contains('CENTRO')]

        for campus in df.nome_unidade_gestora.unique():
            df_campus = self._calcular_percentuais_by_campus(df, campus)
            df_campus['nome_unidade_gestora'] = campus
            dfs.append(df_campus)

        df_chart = pd.concat(dfs)
        filter_f = df_chart['sexo'] == 'F'
        df_chart.loc[filter_f, 'percentual'] = df_chart[filter_f]['percentual'] * -1
        df_chart['sexo'] = df_chart['sexo'].replace({
            'F': 'Feminino',
            'M': 'Masculino',
        })
        df_chart['sort'] = abs(df_chart['percentual'])
        df_chart['nome_unidade_gestora'] = df_chart['nome_unidade_gestora'].str.title()
        df_chart = df_chart.sort_values(['sort'], ascending=False)
        df_chart = df_chart.reset_index(drop=True)

        for name, group in df_chart.groupby(by=['nome_unidade_gestora', 'sexo']):
            indexes = list(group.index)
            df_chart.at[indexes[0], 'size'] = 100
            df_chart.at[indexes[1], 'size'] = 50
            df_chart.at[indexes[2], 'size'] = 50

        chart_params = {
            'x': alt.X('nome_unidade_gestora:N', title=None, axis=alt.Axis(zindex=10)),
            'y': alt.Y('sum(percentual):Q', stack=False, title='% do total de discentes'),
            'color': alt.Color('tipo:N', title='Status',
                               scale=alt.Scale(domain=['Evasão', 'Conclusão', 'Total'],
                                               range=['#fd8060', '#b0d8a4', '#fee191'])
                               ),
            'size': alt.Size('size:Q', legend=None, scale=alt.Scale(domain=[0, 40])),
            'order': alt.Order('sort', sort='descending'),
            'tooltip': [
                alt.Tooltip('sexo:N', title='Gênero'),
                alt.Tooltip('sum(percentual):Q', title='% referente ao total', format='.2f'),
                alt.Tooltip('tipo:N', title='Status'),
                alt.Tooltip('total:Q', title='Quantidade'),
            ]
        }

        alt_chart = alt.Chart(df_chart[df_chart['tipo'] == 'Total']).mark_bar()\
            .encode(**chart_params)\
            .properties(height=600)
        chart_params['y'] = alt.Y('sum(percentual):Q', title='% do total de discentes')
        alt_chart_stacked = alt.Chart(df_chart[df_chart['tipo'] != 'Total']).mark_bar().encode(**chart_params)
        line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')

        st.altair_chart(alt_chart + alt_chart_stacked + line, use_container_width=True)

    def _calcular_percentuais_by_campus(self, df, campus):
        df_campus = df[df.nome_unidade_gestora == campus]

        df_evasao = df_campus[df_campus.status == 'CANCELADO']
        df_concluintes = df_campus[df_campus.status == 'CONCLUÍDO']

        return self._calcular_percentuais(df_campus, df_evasao, df_concluintes)

    def _calcular_percentuais(self, df_total, df_evasao, df_concluintes):
        evasao_por_sexo = df_evasao.groupby(by='sexo').count()['matricula']
        concluintes_por_sexo = df_concluintes.groupby(by='sexo').count()['matricula']

        sexos = ['F', 'M']
        dados = []

        for sexo in sexos:
            total = df_total[df_total['sexo'] == sexo].shape[0]
            percent = total / df_total.shape[0] * 100

            evasao_total = evasao_por_sexo.loc[sexo]
            evasao_percent = evasao_total / df_total.shape[0] * 100

            concluintes_total = concluintes_por_sexo.loc[sexo]
            concluintes_percent = concluintes_total / df_total.shape[0] * 100

            dados.append([sexo, total, percent, 'Total'])
            dados.append([sexo, evasao_total, evasao_percent, 'Evasão'])
            dados.append([sexo, concluintes_total, concluintes_percent, 'Conclusão'])

        return pd.DataFrame(data=dados, columns=['sexo', 'total', 'percentual', 'tipo'])
