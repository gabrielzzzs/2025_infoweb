import streamlit as st
import json
import os
from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.loginUI import LoginUI
from templates.perfilUI import PerfilUI
from templates.perfiladminUI import PerfilAdminUI
from templates.perfilClienteUI import PerfilClienteUI
from templates.abriragendaUI import AbrirAgendaUI
from templates.visualizaragendaUI import VisualizarAgendaUI
from templates.visualizarservicosUI import VisualizarServicosUI
from templates.confirmarservicoUI import ConfirmarServicoUI
from templates.agendarservicoUI import AgendarServicoUI

class IndexUI:

    @staticmethod
    def menu():
        usuario = None
        tipo_usuario = None

        # --------------------------
        # Verifica se há login salvo
        # --------------------------
        if os.path.exists("usuario_logado.json"):
            try:
                with open("usuario_logado.json", "r", encoding="utf-8") as f:
                    usuario = json.load(f)
                    tipo_usuario = usuario.get("tipo")
            except (FileNotFoundError, json.JSONDecodeError):
                usuario = None

        # --------------------------
        # Monta o menu conforme o tipo de usuário
        # --------------------------
        if usuario is None:
            # Menu para visitantes: Login + Abrir Conta
            opcoes = ["Login", "Abrir Conta"]
            op = st.sidebar.selectbox("Menu", opcoes, key="menu_login")
        else:
            if tipo_usuario == "profissional":
                opcoes = [
                    "Cadastro de Serviços",
                    "Abrir Minha Agenda",
                    "Visualizar Minha Agenda",
                    "Confirmar Serviços",
                    "Perfil"
                ]
            elif tipo_usuario == "cliente":
                opcoes = [
                    "Agendar Serviço",
                    "Visualizar Meus Serviços",
                    "Perfil"
                ]
            elif tipo_usuario == "admin":
                opcoes = [
                    "Cadastro de Clientes",
                    "Cadastro de Serviços",
                    "Cadastro de Profissionais",
                    "Cadastro de Horários",  # só admin pode ver
                    "Perfil"
                ]
            else:
                opcoes = ["Perfil"]

            op = st.sidebar.selectbox("Menu", opcoes, key="menu_usuario")

        # --------------------------
        # Direcionamento das telas
        # --------------------------
        if usuario is None:
            if op == "Login":
                LoginUI.main()
            elif op == "Abrir Conta":
                from templates.abrircontaUI import AbrirContaUI
                AbrirContaUI.main()

        else:
            if tipo_usuario == "profissional":
                if op == "Cadastro de Serviços":
                    ManterServicoUI.main()
                elif op == "Abrir Minha Agenda":
                    AbrirAgendaUI.main()
                elif op == "Visualizar Minha Agenda":
                    VisualizarAgendaUI.main()
                elif op == "Confirmar Serviços":
                    ConfirmarServicoUI.main()
                elif op == "Perfil":
                    PerfilUI.main()

            elif tipo_usuario == "cliente":
                if op == "Agendar Serviço":
                    AgendarServicoUI.main()
                elif op == "Visualizar Meus Serviços":
                    VisualizarServicosUI.main()
                elif op == "Perfil":
                    PerfilClienteUI.main()

            elif tipo_usuario == "admin":
                if op == "Cadastro de Clientes":
                    ManterClienteUI.main()
                elif op == "Cadastro de Serviços":
                    ManterServicoUI.main()
                elif op == "Cadastro de Profissionais":
                    ManterProfissionalUI.main()
                elif op == "Cadastro de Horários":
                    ManterHorarioUI.main()
                elif op == "Perfil":
                    PerfilAdminUI.main()

    @staticmethod
    def main():
        IndexUI.menu()


if __name__ == "__main__":
    IndexUI.main()
