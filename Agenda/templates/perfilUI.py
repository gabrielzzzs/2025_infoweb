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

        # ----- Profissional -----
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
                # Limpa senha
                senha = ""

        # ----- Cliente e Admin -----
        elif tipo == "cliente" or tipo == "admin":
            cli = View.cliente_listar_id(usuario["id"])
            if not cli:
                st.error("Cliente não encontrado.")
                return

            nome = st.text_input("Nome", cli.get_nome())
            fone = st.text_input("Telefone", cli.get_fone())

            # Email editável somente para cliente, admin não pode alterar
            if tipo == "admin":
                email = cli.get_email()
                st.text_input("E-mail do Admin (não pode ser alterado)", email, disabled=True)
            else:
                email = st.text_input("E-mail", cli.get_email())

            senha_atual = st.text_input("Senha atual", type="password")
            nova_senha = st.text_input("Nova senha", type="password")
            confirmar_senha = st.text_input("Confirmar nova senha", type="password")

            if st.button("Alterar senha"):
                # Validação simples
                if senha_atual != cli.get_senha():
                    st.error("Senha atual incorreta.")
                elif nova_senha != confirmar_senha:
                    st.error("Nova senha e confirmação não coincidem.")
                elif not nova_senha:
                    st.error("A nova senha não pode ser vazia.")
                else:
                    View.cliente_atualizar(cli.get_id(), nome, cli.get_email(), fone, nova_senha)
                    st.success("Senha alterada com sucesso!")
                    # Limpar campos
                    senha_atual = ""
                    nova_senha = ""
                    confirmar_senha = ""

        # ----- Botão Sair -----
        if os.path.exists("usuario_logado.json"):
            if st.button("Sair da conta"):
                os.remove("usuario_logado.json")
                st.info("Você saiu do sistema.")
                st.rerun() # volta para menu de login
