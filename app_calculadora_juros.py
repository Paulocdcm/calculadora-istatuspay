import streamlit as st
from login import login
from pdf_utils import botao_pdf
import pandas as pd

# ------- LOGO NO TOPO ------- #
st.markdown("<div style='text-align:left'>", unsafe_allow_html=True)
st.image("logo/logo.png", width=200)
st.markdown("</div>", unsafe_allow_html=True)

# ---------- TAXAS CALCULADORA ISTATUSPAY (imagem 1) ---------- #
TAXAS_CALCULADORA = {
    "Mast/Visa": {
        "Débito": 1.99,
        "Crédito Av.": 4.39,
        "Parc 2x": 6.34,
        "Parc 3x": 7.14,
        "Parc 4x": 7.86,
        "Parc 5x": 8.54,
        "Parc 6x": 9.49,
        "Parc 7x": 10.04,
        "Parc 8x": 10.72,
        "Parc 9x": 11.51,
        "Parc 10x": 12.39,
        "Parc 11x": 12.93,
        "Parc 12x": 13.31,
        "Parc 13x": 13.79,
        "Parc 14x": 14.31,
        "Parc 15x": 15.05,
        "Parc 16x": 15.71,
        "Parc 17x": 17.51,
        "Parc 18x": 18.03,
        "Parc 19x": 18.89,
        "Parc 20x": 19.89,
        "Parc 21x": 20.99,
    },
    "Hiper/Elo": {
        "Débito": 2.24,
        "Crédito Av.": 4.39,
        "Parc 2x": 6.34,
        "Parc 3x": 7.14,
        "Parc 4x": 7.86,
        "Parc 5x": 8.54,
        "Parc 6x": 9.49,
        "Parc 7x": 10.04,
        "Parc 8x": 10.72,
        "Parc 9x": 11.51,
        "Parc 10x": 12.39,
        "Parc 11x": 12.93,
        "Parc 12x": 13.31,
        "Parc 13x": 13.79,
        "Parc 14x": 14.31,
        "Parc 15x": 15.05,
        "Parc 16x": 15.71,
        "Parc 17x": 17.51,
        "Parc 18x": 18.03,
        "Parc 19x": 18.89,
        "Parc 20x": 19.89,
        "Parc 21x": 20.99,
    },
    "Amex": {
        "Débito": None,
        "Crédito Av.": 5.00,
        "Parc 2x": 6.34,
        "Parc 3x": 7.14,
        "Parc 4x": 7.86,
        "Parc 5x": 8.54,
        "Parc 6x": 9.49,
        "Parc 7x": 10.04,
        "Parc 8x": 10.72,
        "Parc 9x": 11.51,
        "Parc 10x": 12.39,
        "Parc 11x": 12.93,
        "Parc 12x": 13.31,
        "Parc 13x": 13.79,
        "Parc 14x": 14.31,
        "Parc 15x": 15.05,
        "Parc 16x": 15.71,
        "Parc 17x": 17.51,
        "Parc 18x": 18.03,
        "Parc 19x": 18.89,
        "Parc 20x": 19.89,
        "Parc 21x": 20.99,
    },
}

# ---------- TAXAS LINKPGTO (imagem 2) ---------- #
TAXAS_LINKPGTO = {
    "Mast/Visa": {
        "Débito": 2.69,
        "Crédito Av.": 4.85,
        "Parc 2x": 6.38,
        "Parc 3x": 7.43,
        "Parc 4x": 8.22,
        "Parc 5x": 8.89,
        "Parc 6x": 9.89,
        "Parc 7x": 10.15,
        "Parc 8x": 10.91,
        "Parc 9x": 11.81,
        "Parc 10x": 12.99,
        "Parc 11x": 13.74,
        "Parc 12x": 14.97,
        "Parc 13x": 15.71,
        "Parc 14x": 16.35,
        "Parc 15x": 17.34,
        "Parc 16x": 18.16,
        "Parc 17x": 18.61,
        "Parc 18x": 19.08,
        "Parc 19x": 20.34,
        "Parc 20x": 21.39,
        "Parc 21x": 22.34,
    },
    "Hiper/Elo": {
        "Débito": 3.50,
        "Crédito Av.": 5.23,
        "Parc 2x": 6.84,
        "Parc 3x": 7.83,
        "Parc 4x": 8.81,
        "Parc 5x": 9.44,
        "Parc 6x": 10.39,
        "Parc 7x": 10.94,
        "Parc 8x": 11.55,
        "Parc 9x": 12.55,
        "Parc 10x": 13.74,
        "Parc 11x": 14.19,
        "Parc 12x": 15.49,
        "Parc 13x": 16.30,
        "Parc 14x": 17.38,
        "Parc 15x": 18.91,
        "Parc 16x": 19.18,
        "Parc 17x": 19.91,
        "Parc 18x": 20.49,
        "Parc 19x": 21.46,
        "Parc 20x": 22.09,
        "Parc 21x": 22.49,
    },
    "Amex": {
        "Débito": None,
        "Crédito Av.": 5.23,
        "Parc 2x": 6.84,
        "Parc 3x": 7.83,
        "Parc 4x": 8.81,
        "Parc 5x": 9.44,
        "Parc 6x": 10.39,
        "Parc 7x": 10.94,
        "Parc 8x": 11.55,
        "Parc 9x": 12.55,
        "Parc 10x": 13.74,
        "Parc 11x": 14.19,
        "Parc 12x": 15.49,
        "Parc 13x": 16.30,
        "Parc 14x": 17.38,
        "Parc 15x": 18.91,
        "Parc 16x": 19.18,
        "Parc 17x": 19.91,
        "Parc 18x": 20.49,
        "Parc 19x": 21.46,
        "Parc 20x": 22.09,
        "Parc 21x": 22.49,
    },
}

def buscar_taxa(bandeira, modalidade, tabela_taxas):
    taxa = tabela_taxas.get(bandeira, {}).get(modalidade)
    if taxa is None or taxa == "X":
        return None
    return taxa / 100  # decimal

def simular(valor_venda, tipo_calculo, modalidade, bandeira, tabela_taxas):
    taxa = buscar_taxa(bandeira, modalidade, tabela_taxas)
    if taxa is None:
        return None, "Modalidade não disponível para esta bandeira."
    if "Parc" in modalidade:
        qtd_parcelas = int(modalidade.replace("Parc", "").replace("x", "").strip())
    else:
        qtd_parcelas = 1

    if tipo_calculo == "Assumindo Juros":
        valor_receber = valor_venda * (1 - taxa)
        valor_parcela = valor_venda / qtd_parcelas if qtd_parcelas > 0 else valor_venda
        resultado = {
            "Modalidade": modalidade,
            "Bandeira": bandeira,
            "Tipo de Cálculo": tipo_calculo,
            "Valor da Venda": f"R$ {valor_venda:,.2f}",
            "Parcelas": qtd_parcelas,
            "Taxa (%)": f"{(taxa*100):.2f}%",
            "Valor da Parcela": f"R$ {valor_parcela:,.2f}",
            "Valor a Receber": f"R$ {valor_receber:,.2f}",
        }
    elif tipo_calculo == "Juros ao Cliente":
        valor_total = valor_venda / (1 - taxa) if taxa < 1 else 0
        valor_parcela = valor_total / qtd_parcelas if qtd_parcelas > 0 else 0
        resultado = {
            "Modalidade": modalidade,
            "Bandeira": bandeira,
            "Tipo de Cálculo": tipo_calculo,
            "Valor da Venda": f"R$ {valor_total:,.2f}",      # Valor cobrado do cliente
            "Parcelas": qtd_parcelas,
            "Taxa (%)": f"{(taxa*100):.2f}%",
            "Valor da Parcela": f"R$ {valor_parcela:,.2f}",
            "Valor a Receber": f"R$ {valor_venda:,.2f}",     # Sempre o líquido garantido ao lojista
        }
    else:
        return None, "Tipo de cálculo inválido."
    return resultado, None

def main_app():
    tab1, tab2 = st.tabs(["Calculadora iStatusPay", "Simulador de LinkPgto"])

    # --- CALCULADORA iStatusPay --- (TABELA 1)
    with tab1:
        st.markdown("### Calculadora de Juros iStatusPay")
        bandeiras = list(TAXAS_CALCULADORA.keys())
        bandeira = st.selectbox("Bandeira", bandeiras)
        modalidades = list(TAXAS_CALCULADORA[bandeira].keys())
        simular_todas = st.checkbox("Simular todas as modalidades")

        if simular_todas:
            modalidade = None
        else:
            modalidade = st.selectbox("Modalidade", modalidades)

        if "simulacoes_istatuspay" not in st.session_state:
            st.session_state.simulacoes_istatuspay = []

        with st.form("form_simulacao_istatuspay"):
            valor_venda = st.number_input("Valor da venda", min_value=1.0, step=100.0, format="%.2f")
            tipo_calculo = st.radio("Tipo de Cálculo", ["Assumindo Juros", "Juros ao Cliente"])
            executar = st.form_submit_button("Executar Simulação")

        if st.button("Apagar todas as simulações", key="clear_sim_istatuspay"):
            st.session_state.simulacoes_istatuspay = []
            st.rerun()

        if executar:
            if simular_todas:
                resultados = []
                for mod in modalidades:
                    resultado, erro = simular(
                        valor_venda, tipo_calculo, mod, bandeira, TAXAS_CALCULADORA
                    )
                    if resultado:
                        resultados.append(resultado)
                if not resultados:
                    st.warning("Nenhuma modalidade disponível para simulação.")
                else:
                    st.session_state.simulacoes_istatuspay.extend(resultados)
                    st.success("Simulações adicionadas à lista!")
            else:
                if not modalidade or modalidade == "" or not valor_venda:
                    st.warning("Selecione a modalidade e informe o valor da venda.")
                else:
                    resultado, erro = simular(
                        valor_venda, tipo_calculo, modalidade, bandeira, TAXAS_CALCULADORA
                    )
                    if erro:
                        st.warning(erro)
                    else:
                        st.session_state.simulacoes_istatuspay.append(resultado)
                        st.success("Simulação adicionada à lista!")

        if st.session_state.simulacoes_istatuspay:
            todas = pd.DataFrame(st.session_state.simulacoes_istatuspay)
            st.markdown("#### Simulações realizadas nesta sessão:")
            st.dataframe(todas, use_container_width=True, hide_index=True)
            botao_pdf("Simulação IstatusPay", valor_venda, modalidade if not simular_todas else "Todas", tipo_calculo, todas)

    # --- SIMULADOR DE LINKPGTO --- (TABELA 2)
    with tab2:
        st.markdown("### Simulador de LinkPgto")
        bandeiras = list(TAXAS_LINKPGTO.keys())
        bandeira = st.selectbox("Bandeira", bandeiras, key="link_bandeira")
        modalidades = list(TAXAS_LINKPGTO[bandeira].keys())
        simular_todas_link = st.checkbox("Simular todas as modalidades", key="simular_todas_linkpgto")

        if simular_todas_link:
            modalidade = None
        else:
            modalidade = st.selectbox("Modalidade", modalidades, key="linkpgto_modalidade")

        if "simulacoes_linkpgto" not in st.session_state:
            st.session_state.simulacoes_linkpgto = []

        with st.form("form_simulacao_linkpgto"):
            valor_venda = st.number_input("Valor da venda", min_value=1.0, step=100.0, format="%.2f", key="linkpgto_venda")
            tipo_calculo = st.radio("Tipo de Cálculo", ["Assumindo Juros", "Juros ao Cliente"], key="linkpgto_tipo")
            executar = st.form_submit_button("Executar Simulação")

        if st.button("Apagar todas as simulações", key="clear_sim_linkpgto"):
            st.session_state.simulacoes_linkpgto = []
            st.rerun()

        if executar:
            if simular_todas_link:
                resultados = []
                for mod in modalidades:
                    resultado, erro = simular(
                        valor_venda, tipo_calculo, mod, bandeira, TAXAS_LINKPGTO
                    )
                    if resultado:
                        resultados.append(resultado)
                if not resultados:
                    st.warning("Nenhuma modalidade disponível para simulação.")
                else:
                    st.session_state.simulacoes_linkpgto.extend(resultados)
                    st.success("Simulações adicionadas à lista!")
            else:
                if not modalidade or modalidade == "" or not valor_venda:
                    st.warning("Selecione a modalidade e informe o valor da venda.")
                else:
                    resultado, erro = simular(
                        valor_venda, tipo_calculo, modalidade, bandeira, TAXAS_LINKPGTO
                    )
                    if erro:
                        st.warning(erro)
                    else:
                        st.session_state.simulacoes_linkpgto.append(resultado)
                        st.success("Simulação adicionada à lista!")

        if st.session_state.simulacoes_linkpgto:
            todas = pd.DataFrame(st.session_state.simulacoes_linkpgto)
            st.markdown("#### Simulações realizadas nesta sessão:")
            st.dataframe(todas, use_container_width=True, hide_index=True)
            botao_pdf("Simulação LinkPgto", valor_venda, modalidade if not simular_todas_link else "Todas", tipo_calculo, todas)
        st.caption("Os dados de taxas e simulação são baseados na tabela mais recente da IstatusPay.")

if __name__ == "__main__":
    if login():
        main_app()
    else:
        st.stop()
