import streamlit as st
import pandas as pd

# Carregar a planilha já preparada
planilha = "MISTA CALCULADORA ISTATUSPAY 2025.4 .xlsx"
df = pd.read_excel(planilha, sheet_name="Calculadora iStatusPay", header=None)

# Dados brutos da tabela - personalização das colunas
modalidades = df.loc[8:29, 1].reset_index(drop=True)
parcelas = df.loc[8:29, 3].reset_index(drop=True)
taxas = df.loc[8:29, 2].reset_index(drop=True)
valor_parcela_assumindo = df.loc[8:29, 4].reset_index(drop=True)
receber_assumindo = df.loc[8:29, 5].reset_index(drop=True)
valor_parcela_cliente = df.loc[8:29, 17].reset_index(drop=True)
valor_total_cliente = df.loc[8:29, 18].reset_index(drop=True)

# Montar DataFrame para manipulação
df_app = pd.DataFrame({
    "Modalidade": modalidades,
    "Parcelas": parcelas,
    "Taxa (%)": taxas,
    "Valor Parcela (Assumindo)": valor_parcela_assumindo,
    "Receber (Assumindo)": receber_assumindo,
    "Valor Parcela (Cliente)": valor_parcela_cliente,
    "Valor Total (Cliente)": valor_total_cliente
})

st.title("Calculadora de Juros iStatusPay")

valor_venda = st.number_input("Valor da venda", value=15000.0, min_value=1.0)
tipo_calculo = st.radio("Tipo de Cálculo", ["Assumindo Juros", "Juros ao Cliente"])
modalidade = st.selectbox("Modalidade", df_app["Modalidade"].dropna())
qtd_parcelas = st.selectbox("Quantidade de Parcelas", df_app[df_app["Modalidade"] == modalidade]["Parcelas"].unique())

# Filtra linha correta
linha = df_app[(df_app["Modalidade"] == modalidade) & (df_app["Parcelas"] == qtd_parcelas)]

if tipo_calculo == "Assumindo Juros":
    valor_parcela = linha["Valor Parcela (Assumindo)"].values[0]
    receber = linha["Receber (Assumindo)"].values[0]
    st.write(f"**Valor da Parcela:** R$ {valor_parcela:,.2f}")
    st.write(f"**Valor a Receber:** R$ {receber:,.2f}")
elif tipo_calculo == "Juros ao Cliente":
    valor_parcela = linha["Valor Parcela (Cliente)"].values[0]
    valor_total = linha["Valor Total (Cliente)"].values[0]
    st.write(f"**Valor da Parcela:** R$ {valor_parcela:,.2f}")
    st.write(f"**Valor Total:** R$ {valor_total:,.2f}")

st.info("Os dados de taxas e simulação são baseados na tabela mais recente da iStatusPay. Para atualizar, substitua a planilha Excel.")

