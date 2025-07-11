import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# --------- LOGIN ---------
def login():
    st.markdown(
        """
        <h2 style="text-align:center;margin-bottom:30px;">
            Simulação IstatusPay
        </h2>
        """,
        unsafe_allow_html=True
    )
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        with st.form("login_form"):
            user = st.text_input("Usuário")
            pwd = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
        if submit:
            if user == "teste" and pwd == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
    return st.session_state.logged_in

# --------- PDF COM FPDF (Preto e Branco, Profissional) ---------
def gerar_pdf(titulo, valor_venda, modalidade, tipo_calculo, resultados):
    pdf = FPDF(orientation='L')  # paisagem, cabe tabela grande
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, titulo, ln=True, align='C')
    pdf.ln(2)
    pdf.set_font("Arial", "", 13)
    pdf.cell(0, 8, f"Valor da venda: {valor_venda}", ln=True)
    pdf.cell(0, 8, f"Modalidade: {modalidade}", ln=True)
    pdf.cell(0, 8, f"Tipo de Cálculo: {tipo_calculo}", ln=True)
    pdf.ln(8)

    # Margens e tabela responsiva
    page_width = pdf.w - 2 * pdf.l_margin
    colunas = list(resultados.columns)
    dados = resultados.values.tolist()
    # Calcular largura ideal para cada coluna
    pdf.set_font("Arial", "B", 11)
    min_width = 28
    max_width = 60
    larguras = []
    for idx, col in enumerate(colunas):
        larg = pdf.get_string_width(str(col)) + 10
        larg = max(larg, min_width)
        larg = min(larg, max_width)
        for row in dados:
            cell_len = pdf.get_string_width(str(row[idx])) + 10
            if cell_len > larg:
                larg = min(cell_len, max_width)
        larguras.append(larg)
    # Corrige se a soma ultrapassa a página
    total_width = sum(larguras)
    if total_width > page_width:
        proporcao = page_width / total_width
        larguras = [w * proporcao for w in larguras]

    # Cabeçalho mais destacado
    pdf.set_fill_color(0, 0, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 11)
    for i, col in enumerate(colunas):
        pdf.cell(larguras[i], 10, str(col), border=1, align="C", fill=True)
    pdf.ln()

    # Corpo zebrado cinza/branco, fonte proporcional
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)
    fill = False
    for idx, row in enumerate(dados):
        fill = not fill
        pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
        for i, item in enumerate(row):
            txt = str(item)
            pdf.cell(larguras[i], 9, txt, border=1, align="C", fill=True)
        pdf.ln()
    pdf.ln(2)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

def botao_pdf(titulo, valor_venda, modalidade, tipo_calculo, resultados):
    pdf_bytes = gerar_pdf(titulo, valor_venda, modalidade, tipo_calculo, resultados)
    b64 = base64.b64encode(pdf_bytes).decode()
    st.markdown(
        f'<a href="data:application/pdf;base64,{b64}" download="simulacao.pdf" '
        f'style="background:#222;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;display:inline-block;margin-top:20px;background:#111;">'
        f'📄 Baixar Simulação em PDF</a>',
        unsafe_allow_html=True
    )

# --------- EXTRAI DADOS DA PLANILHA ---------
def extrair_dados(planilha, sheet):
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

# --------- APP PRINCIPAL ---------
def main_app():
    planilha = "MISTA CALCULADORA ISTATUSPAY 2025.4 .xlsx"
    tab1, tab2 = st.tabs(["Calculadora iStatusPay", "Simulador de LinkPgto"])

    # --- CALCULADORA iStatusPay ---
    with tab1:
        st.markdown("### Calculadora de Juros iStatusPay")
        df_app = extrair_dados(planilha, "Calculadora iStatusPay")
        modalidades_unicas = df_app["Modalidade"].dropna().unique()
        modalidade_opcoes = ["Selecione a modalidade"] + list(modalidades_unicas)

        if "simulacoes_istatuspay" not in st.session_state:
            st.session_state.simulacoes_istatuspay = []

        with st.form("form_simulacao_istatuspay"):
            valor_venda = st.number_input("Valor da venda", min_value=1.0, step=100.0, format="%.2f")
            tipo_calculo = st.radio("Tipo de Cálculo", ["Assumindo Juros", "Juros ao Cliente"])
            modalidade = st.selectbox("Modalidade", modalidade_opcoes, index=0)
            executar = st.form_submit_button("Executar Simulação")

        if executar:
            if modalidade == "Selecione a modalidade" or not valor_venda:
                st.warning("Selecione a modalidade e informe o valor da venda.")
            else:
                linhas = df_app[df_app["Modalidade"] == modalidade]
                resultados = []
                for _, linha in linhas.iterrows():
                    qtd_parcelas = int(linha["Parcelas"])
                    taxa = float(linha["Taxa (%)"])
                    if tipo_calculo == "Assumindo Juros":
                        valor_parcela = (valor_venda / qtd_parcelas) if qtd_parcelas > 0 else 0
                        percentual = 1 - taxa
                        receber = valor_venda * percentual
                        resultados.append({
                            "Simulação": len(st.session_state.simulacoes_istatuspay) + 1,
                            "Modalidade": modalidade,
                            "Tipo de Cálculo": tipo_calculo,
                            "Valor da Venda": f"R$ {valor_venda:,.2f}",
                            "Parcelas": qtd_parcelas,
                            "Taxa (%)": f"{taxa*100:.2f}%",
                            "Valor da Parcela": f"R$ {valor_parcela:,.2f}",
                            "Valor a Receber": f"R$ {receber:,.2f}"
                        })
                    elif tipo_calculo == "Juros ao Cliente":
                        valor_total = valor_venda / (1 - taxa) if taxa < 1 else 0
                        valor_parcela = valor_total / qtd_parcelas if qtd_parcelas > 0 else 0
                        resultados.append({
                            "Simulação": len(st.session_state.simulacoes_istatuspay) + 1,
                            "Modalidade": modalidade,
                            "Tipo de Cálculo": tipo_calculo,
                            "Valor da Venda": f"R$ {valor_venda:,.2f}",
                            "Parcelas": qtd_parcelas,
                            "Taxa (%)": f"{taxa*100:.2f}%",
                            "Valor da Parcela": f"R$ {valor_parcela:,.2f}",
                            "Valor Total": f"R$ {valor_total:,.2f}"
                        })
                st.session_state.simulacoes_istatuspay.append(pd.DataFrame(resultados))
                st.success("Simulação adicionada à lista!")

        if st.session_state.simulacoes_istatuspay:
            todas = pd.concat(st.session_state.simulacoes_istatuspay, ignore_index=True)
            st.markdown("#### Simulações realizadas nesta sessão:")
            st.dataframe(todas, use_container_width=True, hide_index=True)
            botao_pdf("Simulação IstatusPay", valor_venda, modalidade, tipo_calculo, todas)

    # --- SIMULADOR DE LINKPGTO ---
    with tab2:
        st.markdown("### Simulador de LinkPgto")
        df_app = extrair_dados(planilha, "Simulador de LinkPgto")
        modalidades_unicas = df_app["Modalidade"].dropna().unique()
        modalidade_opcoes = ["Selecione a modalidade"] + list(modalidades_unicas)

        if "simulacoes_linkpgto" not in st.session_state:
            st.session_state.simulacoes_linkpgto = []

        with st.form("form_simulacao_linkpgto"):
            valor_venda = st.number_input("Valor da venda", min_value=1.0, step=100.0, format="%.2f", key="linkpgto_venda")
            tipo_calculo = st.radio("Tipo de Cálculo", ["Assumindo Juros", "Juros ao Cliente"], key="linkpgto_tipo")
            modalidade = st.selectbox("Modalidade", modalidade_opcoes, index=0, key="linkpgto_modalidade")
            executar = st.form_submit_button("Executar Simulação")

        if executar:
            if modalidade == "Selecione a modalidade" or not valor_venda:
                st.warning("Selecione a modalidade e informe o valor da venda.")
            else:
                linhas = df_app[df_app["Modalidade"] == modalidade]
                resultados = []
                for _, linha in linhas.iterrows():
                    qtd_parcelas = int(linha["Parcelas"])
                    taxa = float(linha["Taxa (%)"])
                    if tipo_calculo == "Assumindo Juros":
                        valor_parcela = (valor_venda / qtd_parcelas) if qtd_parcelas > 0 else 0
                        percentual = 1 - taxa
                        receber = valor_venda * percentual
                        resultados.append({
                            "Simulação": len(st.session_state.simulacoes_linkpgto) + 1,
                            "Modalidade": modalidade,
                            "Tipo de Cálculo": tipo_calculo,
                            "Valor da Venda": f"R$ {valor_venda:,.2f}",
                            "Parcelas": qtd_parcelas,
                            "Taxa (%)": f"{taxa*100:.2f}%",
                            "Valor da Parcela": f"R$ {valor_parcela:,.2f}",
                            "Valor a Receber": f"R$ {receber:,.2f}"
                        })
                    elif tipo_calculo == "Juros ao Cliente":
                        valor_total = valor_venda / (1 - taxa) if taxa < 1 else 0
                        valor_parcela = valor_total / qtd_parcelas if qtd_parcelas > 0 else 0
                        resultados.append({
                            "Simulação": len(st.session_state.simulacoes_linkpgto) + 1,
                            "Modalidade": modalidade,
                            "Tipo de Cálculo": tipo_calculo,
                            "Valor da Venda": f"R$ {valor_venda:,.2f}",
                            "Parcelas": qtd_parcelas,
                            "Taxa (%)": f"{taxa*100:.2f}%",
                            "Valor da Parcela": f"R$ {valor_parcela:,.2f}",
                            "Valor Total": f"R$ {valor_total:,.2f}"
                        })
                st.session_state.simulacoes_linkpgto.append(pd.DataFrame(resultados))
                st.success("Simulação adicionada à lista!")

        if st.session_state.simulacoes_linkpgto:
            todas = pd.concat(st.session_state.simulacoes_linkpgto, ignore_index=True)
            st.markdown("#### Simulações realizadas nesta sessão:")
            st.dataframe(todas, use_container_width=True, hide_index=True)
            botao_pdf("Simulação IstatusPay", valor_venda, modalidade, tipo_calculo, todas)
        st.caption("Os dados de taxas e simulação são baseados na tabela mais recente da IstatusPay.")

# --------- RODA O APP COM LOGIN ---------
if login():
    main_app()
else:
    st.stop()
