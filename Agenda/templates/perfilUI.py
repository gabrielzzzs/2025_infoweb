import streamlit as st
import json
import os
from views import View

class PerfilUI:
    @staticmethod
    def main():
        st.header("Meu Perfil")

        # Verifica se há usuário logado
        try:
            with open("usuario_logado.json", "r", encoding="utf-8") as f:
                usuario = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            st.warning("Nenhum usuário logado. Faça login para editar o perfil.")
            return

        tipo = usuario.get("tipo")

        # Exibe e permite editar conforme o tipo
        if tipo == "profissional":
            prof = View.profissional_listar_id(usuario["id"])
            if not prof:
                st.error("Profissional não encontrado.")
                return

            nome = st.text_input("Nome", prof.get_nome())
            especialidade = st.text_input("Especialidade", prof.get_especialidade())
            conselho = st.text_input("Conselho", prof.get_conselho())
            email = st.text_input("E-mail", prof.get_email())
            senha = st.text_input("Senha", prof.get_senha(), type="password")

            if st.button("Salvar alterações"):
                View.profissional_atualizar(prof.get_id(), nome, especialidade, conselho, email, senha)
                st.success("Perfil atualizado com sucesso!")

        elif tipo == "cliente" or tipo == "admin":
            cli = View.cliente_listar_id(usuario["id"])
            if not cli:
                st.error("Cliente não encontrado.")
                return

            nome = st.text_input("Nome", cli.get_nome())
            email = st.text_input("E-mail", cli.get_email())
            fone = st.text_input("Telefone", cli.get_fone())
            senha = st.text_input("Senha", cli.get_senha(), type="password")

            if st.button("Salvar alterações"):
                View.cliente_atualizar(cli.get_id(), nome, email, fone, senha)
                st.success("Perfil atualizado com sucesso!")

        # Botão "Sair" (somente nesta página)
        if os.path.exists("usuario_logado.json"):
            if st.button("Sair da conta"):
                os.remove("usuario_logado.json")
                st.info("Você saiu do sistema.")
