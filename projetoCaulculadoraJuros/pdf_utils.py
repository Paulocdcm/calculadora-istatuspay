from fpdf import FPDF
import base64
import streamlit as st
from datetime import datetime

def gerar_pdf(titulo, valor_venda, modalidade, tipo_calculo, resultados):
    pdf = FPDF(orientation='L')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Faixa preta no topo
    largura_pagina = pdf.w
    altura_faixa = 22
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, largura_pagina, altura_faixa, 'F')

    # Logo
    try:
        pdf.image("logo/logo.png", x=8, y=3, w=38)
    except Exception as e:
        print(f"Erro ao inserir logo: {e}")

    # Título centralizado
    pdf.set_xy(0, altura_faixa + 8)
    pdf.set_font("Arial", "B", 22)
    pdf.cell(largura_pagina, 12, titulo, align='C', ln=True)

    # Subtítulo (opcional)
    pdf.set_font("Arial", "I", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Dados principais com destaque
    pdf.set_font("Arial", "", 13)
    pdf.cell(0, 8, f"Valor da venda: R$ {valor_venda}", ln=True)
    pdf.cell(0, 8, f"Modalidade: {modalidade}", ln=True)
    pdf.cell(0, 8, f"Tipo de Cálculo: {tipo_calculo}", ln=True)
    pdf.ln(8)

    # Tabela
    page_width = pdf.w - 2 * pdf.l_margin
    colunas = list(resultados.columns)
    dados = resultados.values.tolist()
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
    total_width = sum(larguras)
    if total_width > page_width:
        proporcao = page_width / total_width
        larguras = [w * proporcao for w in larguras]

    # Cabeçalho da tabela (preto)
    pdf.set_fill_color(0, 0, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 11)
    for i, col in enumerate(colunas):
        pdf.cell(larguras[i], 10, str(col), border=1, align="C", fill=True)
    pdf.ln()

    # Dados da tabela (zebrado cinza e branco)
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

    # Rodapé com data
    pdf.set_y(-18)
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(150, 150, 150)
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(0, 10, f"Relatório gerado em {data}", 0, 0, 'R')

    pdf.set_text_color(0, 0, 0)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

def botao_pdf(titulo, valor_venda, modalidade, tipo_calculo, resultados):
    pdf_bytes = gerar_pdf(titulo, valor_venda, modalidade, tipo_calculo, resultados)
    b64 = base64.b64encode(pdf_bytes).decode()
    st.markdown(
        f'''
        <a href="data:application/pdf;base64,{b64}" download="simulacao.pdf" 
        style="background:#222;color:white;padding:14px 28px;
        border-radius:8px;text-decoration:none;display:inline-block;margin-top:18px;
        font-size:17px;font-weight:600;">
        📄 Baixar Simulação em PDF
        </a>
        ''',
        unsafe_allow_html=True
    )
