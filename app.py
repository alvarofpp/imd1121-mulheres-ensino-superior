import streamlit as st
import pandas as pd
from questions import Question01, Question02


@st.cache
def load_data():
    return {
        'discentes': pd.read_csv('data/discentes.csv', sep=';'),
    }


def main():
    st.title("Mulheres no Ensino Superior da UFRN")

    st.markdown("""
    Trabalho realizado por:
    - [Álvaro Ferreira Pires de Paiva](https://github.com/alvarofpp)
        - Matrícula: 2016039162
        - E-mail: alvarofepipa@gmail.com
    - [Carmem Stefanie da Silva Cavalcante](https://github.com/carmems)
        - Matrícula: 20180063434
        - E-mail: cstefanie.16@gmail.com
    - [Jonas de Oliveira Freire Filho](https://github.com/usrjonas)
        - Matrícula: 20200038865
        - E-mail: jonas.oliveira1402@outlook.com
    - [Pedro Avelino Ferreira Nogueira](#)
        - Matrícula: 20180062339
        - E-mail: pdnog@ufrn.edu.br
    """)

    st.markdown('# Motivação')
    st.markdown('Nos dias de hoje, existem muitas discussões acerca da igualdade de gênero e da representatividade feminina em diversos contextos, como política, mercado de trabalho, área de atuação, cargos de liderança, salários, etc. Dentre eles, definimos explorar a participação feminina no ensino superior.')
    st.markdown('O problema não é visto quando analisamos a quantidade de mulheres presentes no ensino superior, mas em sua distribuição nos cursos ofertados, normalmente essa distribuição revela muitas vezes a prevalência da tradicional divisão sexual do trabalho, no qual homens assumem determinados postos (exemplo: cursos de exatas) e mulheres outros (exemplo: cursos de biológicas).')
    st.markdown('Um exemplo claro dessa distribuição é o fato de que, na Universidade Federal do Rio Grande do Norte (UFRN), ingressaram, nos últimos três anos, cerca de 80% mais homens do que mulheres no curso de Bacharelado em Tecnologia da Informação - dado obtido através da lista de ingressantes disponibilizada pelo Sisu.')
    st.markdown('Com isso em mente, o presente trabalho tem como objetivo realizar uma análise minuciosa sobre a representatividade feminina no ensino superior, tendo como corte a UFRN, de forma que possa incentivar o debate sobre representatividade feminina dentro da própria instituição.')

    st.markdown('# Pesquisa de base de dados')
    st.markdown('Inicialmente, realizamos pesquisas em bases de dados nacionais da educação, como dados do Instituto Nacional de Estudos e Pesquisas Educacionais (INEP), da Universidade Federal do Rio Grande do Norte (UFRN) e da Universidade Federal do Ceará. Porém, definimos o escopo do nosso projeto como sendo a UFRN, então selecionamos três bases de dados dos [dados abertos da UFRN](http://dados.ufrn.br/):')
    st.markdown("""
    - [Discentes](http://dados.ufrn.br/dataset/discentes);
    - [Bolsas de Apoio](http://dados.ufrn.br/dataset/bolsas-de-apoio);
    - [Bolsas de Iniciação Científica](http://dados.ufrn.br/dataset/bolsistas-de-iniciacao-cientifica).
    """)
    st.markdown('----------')

    datasets = load_data()

    # Questão 1
    question_01 = Question01()
    question_01.render(datasets['discentes'])

    # Questão 2
    question_02 = Question02()
    question_02.render(datasets['discentes'])


if __name__ == "__main__":
    main()
