from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.manterhorarioUI import ManterHorarioUI  
import streamlit as st

class IndexUI:

    def menu_admin():
        op = st.sidebar.selectbox(
            "Menu",
            [
                "Cadastro de Clientes",
                "Cadastro de Serviços",
                "Cadastro de Profissionais",
                "Cadastro de Horários"  
            ]
        )

        if op == "Cadastro de Clientes":
            ManterClienteUI.main()
        elif op == "Cadastro de Serviços":
            ManterServicoUI.main()
        elif op == "Cadastro de Profissionais":
            ManterProfissionalUI.main()
        elif op == "Cadastro de Horários":  
            ManterHorarioUI.main()

    def sidebar():
        IndexUI.menu_admin()

    def main():
        IndexUI.sidebar()

IndexUI.main()
