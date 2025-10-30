from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.loginUI import LoginUI
from templates.perfilUI import PerfilUI
from templates.abriragendaUI import AbrirAgendaUI
from templates.visualizaragendaUI import VisualizarAgendaUI
from templates.visualizarservicosUI import VisualizarServicosUI   # ✅ novo import
import streamlit as st


class IndexUI:

    @staticmethod
    def menu_admin():
        usuario = st.session_state.get("usuario_logado")
        tipo_usuario = usuario["tipo"] if usuario else None

        # Menu padrão
        opcoes = [
            "Login",
            "Cadastro de Clientes",
            "Cadastro de Serviços",
            "Cadastro de Profissionais",
            "Cadastro de Horários",
            "Perfil"
        ]

        # Opções específicas por tipo de usuário
        if tipo_usuario == "profissional":
            opcoes.insert(5, "Abrir Minha Agenda")
            opcoes.insert(6, "Visualizar Minha Agenda")
        elif tipo_usuario == "cliente":
            opcoes.insert(5, "Visualizar Meus Serviços")  # ✅ cliente vê essa

        # Menu lateral
        op = st.sidebar.selectbox("Menu", opcoes)

        # Mostra usuário logado + botão de sair
        if usuario:
            st.sidebar.success(f"👤 Logado como: {usuario['nome']} ({usuario['tipo']})")
            if st.sidebar.button("Sair"):
                del st.session_state["usuario_logado"]
                st.rerun()

        # Roteamento das telas
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
        elif op == "Abrir Minha Agenda":
            AbrirAgendaUI.main()
        elif op == "Visualizar Minha Agenda":
            VisualizarAgendaUI.main()
        elif op == "Visualizar Meus Serviços":      # ✅ nova rota
            VisualizarServicosUI.main()
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
