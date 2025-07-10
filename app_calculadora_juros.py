import streamlit as st
import pandas as pd

# Caminho da planilha
planilha = "MISTA CALCULADORA ISTATUSPAY 2025.4 .xlsx"

# Função para extrair os dados de cada calculadora
def extrair_dados(sheet):
    df = pd.read_excel(planilha, sheet_name=sheet, header=None)
    modalidades = df.loc[8:29, 1].reset_index(drop=True)
    parcelas = df.loc[8:29, 3].reset_index(drop=True)
    taxas = df.loc[8:29, 2].reset_index(drop=True)
    valor_parcela_assumindo = df.loc[8:29, 4].reset_index(drop=True)
    receber_assumindo = df.loc[8:29, 5].reset_index(drop=True)
    valor_parcela_cliente = df.loc[8:29, 17].reset_index(drop=True)
    valor_total_cliente = df.loc[8:29, 18].reset_index(drop=True)

    df_app = pd.DataFrame({
        "Modalidade": modalidades,
        "Parcelas": parcelas,
        "Taxa (%)": taxas,
        "Valor Parcela (Assumindo)": valor_parcela_assumindo,
        "Receber (Assumindo)": receber_assumindo,
        "Valor Parcela (Cliente)": valor_parcela_cliente,
        "Valor Total (Cliente)": valor_total_cliente
    })
    return df_app

# Tabs para as calculadoras
tab1, tab2 = st.tabs(["Calculadora iStatusPay", "Simulador de LinkPgto"])

# --- CALCULADORA iStatusPay ---
with tab1:
    st.title("Calculadora de Juros iStatusPay")
    df_app = extrair_dados("Calculadora iStatusPay")

    with st.form("form_simulacao_istatuspay"):
        valor_venda = st.number_input("Valor da venda", value=15000.0, min_value=1.0, step=100.0)
        tipo_calculo = st.radio("Tipo de Cálculo", ["Assumindo Juros", "Juros ao Cliente"])
        modalidade = st.selectbox("Modalidade", df_app["Modalidade"].dropna())
        parcelas_disp = df_app[df_app["Modalidade"] == modalidade]["Parcelas"].unique()
        qtd_parcelas = st.selectbox("Quantidade de Parcelas", parcelas_disp)

        executar = st.form_submit_button("Executar Simulação")

    if executar:
        linha = df_app[(df_app["Modalidade"] == modalidade) & (df_app["Parcelas"] == qtd_parcelas)].iloc[0]
        taxa = float(linha["Taxa (%)"])

        if tipo_calculo == "Assumindo Juros":
            valor_parcela = (valor_venda / qtd_parcelas) if qtd_parcelas > 0 else 0
            percentual = 1 - taxa
            receber = valor_venda * percentual

            st.subheader("Resultado da Simulação (Assumindo Juros)")
            st.write(f"**Modalidade:** {modalidade}")
            st.write(f"**Nº de Parcelas:** {qtd_parcelas}")
            st.write(f"**Taxa:** {taxa:.4f} ({taxa*100:.2f}%)")
            st.write(f"**Valor da Parcela:** R$ {valor_parcela:,.2f}")
            st.write(f"**Valor a Receber:** R$ {receber:,.2f}")

        elif tipo_calculo == "Juros ao Cliente":
            valor_total = valor_venda / (1 - taxa) if taxa < 1 else 0
            valor_parcela = valor_total / qtd_parcelas if qtd_parcelas > 0 else 0

            st.subheader("Resultado da Simulação (Juros ao Cliente)")
            st.write(f"**Modalidade:** {modalidade}")
            st.write(f"**Nº de Parcelas:** {qtd_parcelas}")
            st.write(f"**Taxa:** {taxa:.4f} ({taxa*100:.2f}%)")
            st.write(f"**Valor da Parcela:** R$ {valor_parcela:,.2f}")
            st.write(f"**Valor Total:** R$ {valor_total:,.2f}")

        st.success("Simulação realizada com sucesso!")
    else:
        st.info("Preencha os dados e clique em 'Executar Simulação' para ver o resultado.")

    st.caption("Os dados de taxas e simulação são baseados na tabela mais recente da iStatusPay.")

# --- SIMULADOR DE LINKPGTO ---
with tab2:
    st.title("Simulador de LinkPgto")
    df_app = extrair_dados("Simulador de LinkPgto")

    with st.form("form_simulacao_linkpgto"):
        valor_venda = st.number_input("Valor da venda", value=15000.0, min_value=1.0, step=100.0, key="linkpgto_venda")
        tipo_calculo = st.radio("Tipo de Cálculo", ["Assumindo Juros", "Juros ao Cliente"], key="linkpgto_tipo")
        modalidade = st.selectbox("Modalidade", df_app["Modalidade"].dropna(), key="linkpgto_modalidade")
        parcelas_disp = df_app[df_app["Modalidade"] == modalidade]["Parcelas"].unique()
        qtd_parcelas = st.selectbox("Quantidade de Parcelas", parcelas_disp, key="linkpgto_parcelas")

        executar = st.form_submit_button("Executar Simulação")

    if executar:
        linha = df_app[(df_app["Modalidade"] == modalidade) & (df_app["Parcelas"] == qtd_parcelas)].iloc[0]
        taxa = float(linha["Taxa (%)"])

        if tipo_calculo == "Assumindo Juros":
            valor_parcela = (valor_venda / qtd_parcelas) if qtd_parcelas > 0 else 0
            percentual = 1 - taxa
            receber = valor_venda * percentual

            st.subheader("Resultado da Simulação (Assumindo Juros)")
            st.write(f"**Modalidade:** {modalidade}")
            st.write(f"**Nº de Parcelas:** {qtd_parcelas}")
            st.write(f"**Taxa:** {taxa:.4f} ({taxa*100:.2f}%)")
            st.write(f"**Valor da Parcela:** R$ {valor_parcela:,.2f}")
            st.write(f"**Valor a Receber:** R$ {receber:,.2f}")

        elif tipo_calculo == "Juros ao Cliente":
            valor_total = valor_venda / (1 - taxa) if taxa < 1 else 0
            valor_parcela = valor_total / qtd_parcelas if qtd_parcelas > 0 else 0

            st.subheader("Resultado da Simulação (Juros ao Cliente)")
            st.write(f"**Modalidade:** {modalidade}")
            st.write(f"**Nº de Parcelas:** {qtd_parcelas}")
            st.write(f"**Taxa:** {taxa:.4f} ({taxa*100:.2f}%)")
            st.write(f"**Valor da Parcela:** R$ {valor_parcela:,.2f}")
            st.write(f"**Valor Total:** R$ {valor_total:,.2f}")

        st.success("Simulação realizada com sucesso!")
    else:
        st.info("Preencha os dados e clique em 'Executar Simulação' para ver o resultado.")

    st.caption("Os dados de taxas e simulação são baseados na tabela mais recente da iStatusPay.")
