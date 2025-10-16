import streamlit as st
from views import View

class PerfilUI:
    @staticmethod
    def main():
        if "usuario_logado" not in st.session_state:
            st.warning("Você precisa estar logado para acessar o perfil.")
            return

        usuario = st.session_state["usuario_logado"]

        st.header(f"👤 Perfil de {usuario['nome']}")

        if st.button("🚪 Sair da conta"):
            del st.session_state["usuario_logado"]
            st.success("Você saiu da conta.")
            st.rerun()
            return

        if usuario["tipo"] == "profissional":
            prof = View.profissional_listar_id(usuario["id"])
            nome = st.text_input("Nome", prof.get_nome())
            especialidade = st.text_input("Especialidade", prof.get_especialidade())
            conselho = st.text_input("Conselho", prof.get_conselho())
            email = st.text_input("E-mail", prof.get_email())
            senha = st.text_input("Senha", prof.get_senha(), type="password")

            if st.button("Salvar alterações"):
                View.profissional_atualizar(prof.get_id(), nome, especialidade, conselho, email, senha)
                st.success("Perfil atualizado com sucesso!")
