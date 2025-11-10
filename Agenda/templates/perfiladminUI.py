import streamlit as st
import json
import os
from views import View

class PerfilAdminUI:
    @staticmethod
    def main():
        st.header("Perfil do Admin - Alterar Senha")

        # Carrega o usuário logado
        try:
            with open("usuario_logado.json", "r", encoding="utf-8") as f:
                usuario = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            st.warning("Nenhum usuário logado. Faça login para acessar o perfil.")
            return

        # Apenas admin
        if usuario.get("tipo") != "admin":
            st.error("Acesso restrito a administradores.")
            return

        # Busca o cliente/admin no DAO
        cli = View.cliente_listar_id(usuario["id"])
        if not cli:
            st.error("Admin não encontrado.")
            return

        # Campos do formulário
        st.text_input("E-mail do Admin (não pode ser alterado)", cli.get_email(), disabled=True)
        senha_atual = st.text_input("Senha atual", type="password")
        nova_senha = st.text_input("Nova senha", type="password")
        confirmar_senha = st.text_input("Confirmar nova senha", type="password")

        # Botão para alterar senha
        if st.button("Alterar Senha"):
            try:
                if not senha_atual or not nova_senha or not confirmar_senha:
                    st.error("Todos os campos devem ser preenchidos.")
                elif senha_atual != cli.get_senha():
                    st.error("Senha atual incorreta.")
                elif nova_senha != confirmar_senha:
                    st.error("A nova senha e a confirmação não coincidem.")
                else:
                    View.cliente_atualizar(cli.get_id(), cli.get_nome(), cli.get_email(), cli.get_fone(), nova_senha)
                    st.success("Senha alterada com sucesso!")

                    # Limpa os campos após alterar
                    senha_atual = ""
                    nova_senha = ""
                    confirmar_senha = ""

            except Exception as e:
                st.error(f"Erro ao alterar a senha: {e}")

        # Botão "Sair" — sempre aparece abaixo do formulário
        if st.button("Sair da conta"):
            if os.path.exists("usuario_logado.json"):
                os.remove("usuario_logado.json")
            st.info("Você saiu do sistema.")
