from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.loginUI import LoginUI     # ✅ nova tela de login
from templates.perfilUI import PerfilUI   # ✅ nova tela de perfil
import streamlit as st


class IndexUI:

    @staticmethod
    def menu_admin():
        op = st.sidebar.selectbox(
            "Menu",
            [
                "Login",                    # ✅ adicionamos login
                "Cadastro de Clientes",
                "Cadastro de Serviços",
                "Cadastro de Profissionais",
                "Cadastro de Horários",
                "Perfil"                    # ✅ adicionamos perfil
            ]
        )

        if op == "Login":
            LoginUI.main()
        elif op == "Cadastro de Clientes":
            ManterClienteUI.main()
        elif op == "Cadastro de Serviços":
            ManterServicoUI.main()
        elif op == "Cadastro de Profissionais":
            ManterProfissionalUI.main()
        elif op == "Cadastro de Horários":
            ManterHorarioUI.main()
        elif op == "Perfil":
            PerfilUI.main()

    @staticmethod
    def sidebar():
        IndexUI.menu_admin()

    @staticmethod
    def main():
        IndexUI.sidebar()


if __name__ == "__main__":
    IndexUI.main()
