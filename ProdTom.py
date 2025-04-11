import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Leitura do arquivo
df = pd.read_excel('consulta_0.xlsx')
df = df.replace('-', '0')

# Conversão da coluna de produção para número
df['prod_ton'] = pd.to_numeric(
    df['prod_ton'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False),
    errors='coerce'
)

# Pivoteia os dados para ter os anos como colunas
df_pivot = df.pivot_table(index=None, columns='ano', values='prod_ton', aggfunc='first')
df_pivot = df_pivot.reset_index(drop=True)

# Arredonda os valores
numeric_cols = df_pivot.select_dtypes(include=['float', 'int']).columns
df_pivot[numeric_cols] = df_pivot[numeric_cols].round(2)

# Adiciona coluna com a média da produção por linha
df_pivot["prod_ton"] = df_pivot.mean(axis=1)
df_pivot["prod_ton"] = df_pivot["prod_ton"].round(2)

# Configuração da página
st.set_page_config(layout="wide")
st.title('Produção de tomate')
st.write('Produção de tomate')

# Mostra a tabela completa
st.dataframe(df_pivot.style.format({'prod_ton': '{:.2f}'}))

# Criando filtro por ano
anos = df_pivot.columns[:-1].tolist()  # exclui a coluna "prod_ton"
opcoes_anos = ['Todos'] + [str(ano) for ano in anos]
ano_selecionado = st.sidebar.selectbox("Selecione o ano:", opcoes_anos)

# Filtro e gráficos
col1, col2 = st.columns(2)

with col1:
    if ano_selecionado == "Todos":
        st.write("Média da produção por ano (Todos os dados):")
        media_ano = df_pivot[anos].mean()
        st.bar_chart(media_ano)
    else:
        ano = float(ano_selecionado)  # transforma o ano em float para indexar a coluna corretamente
        st.write(f"Produções do ano {ano_selecionado}:")
        st.dataframe(df_pivot[[ano]])
        st.write(f"Estatísticas do ano {ano_selecionado}: média, min, max")
        st.write(df_pivot[ano].describe().round(2))

with col2:
    st.write("### Gráfico de linhas: Evolução das produções")
    if ano_selecionado == "Todos":
        media_por_ano = df_pivot[anos].mean()
        st.line_chart(media_por_ano)
    else:
        ano = float(ano_selecionado)
        st.line_chart(df_pivot[[ano]])

