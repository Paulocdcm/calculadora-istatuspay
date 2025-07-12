import streamlit as st

def login():
    st.markdown(
        """
        <h2 style="text-align:center;margin-bottom:30px;">
            Simulador de Juros
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
