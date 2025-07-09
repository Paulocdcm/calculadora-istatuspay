import streamlit as st
import pandas as pd

# Carregar a planilha já preparada
planilha = "MISTA CALCULADORA ISTATUSPAY 2025.4 .xlsx"
df = pd.read_excel(planilha, sheet_name="Calculadora iStatusPay", header=None)

# Dados da tabela
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

with st.form("form_simulacao"):
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
        # Simula proporcional ao valor informado
        valor_parcela = (valor_venda / qtd_parcelas) if qtd_parcelas > 0 else 0
        # Ajuste usando a mesma lógica da tabela original
        percentual = 1 - taxa  # ex: taxa=0.0714 (7,14%) --> percentual = 0.9286
        receber = valor_venda * percentual

        st.subheader("Resultado da Simulação (Assumindo Juros)")
        st.write(f"**Modalidade:** {modalidade}")
        st.write(f"**Nº de Parcelas:** {qtd_parcelas}")
        st.write(f"**Taxa:** {taxa:.4f} ({taxa*100:.2f}%)")
        st.write(f"**Valor da Parcela:** R$ {valor_parcela:,.2f}")
        st.write(f"**Valor a Receber:** R$ {receber:,.2f}")

    elif tipo_calculo == "Juros ao Cliente":
        # Aqui o cliente paga o valor bruto mais o juro sobre o total
        # Lógica: valor total = valor_venda / (1 - taxa)
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

st.caption("Os dados de taxas e simulação são baseados na tabela mais recente da iStatusPay. Para atualizar, basta substituir a planilha Excel no repositório.")

