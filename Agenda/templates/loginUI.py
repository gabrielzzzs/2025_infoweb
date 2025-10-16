import streamlit as st
from views import View

class LoginUI:
    @staticmethod
    def main():
        st.title("🔐 Login no Sistema")

        tipo = st.radio("Entrar como:", ["Cliente", "Profissional"])
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if tipo == "Profissional":
                prof = View.profissional_autenticar(email, senha)
                if prof:
                    st.session_state["usuario_logado"] = {
                        "tipo": "profissional",
                        "id": prof.get_id(),
                        "nome": prof.get_nome()
                    }
                    # ✅ marca o sucesso antes de recarregar
                    st.session_state["login_sucesso"] = True
                    st.session_state["nome_logado"] = prof.get_nome()
                    st.rerun()
                else:
                    st.error("❌ E-mail ou senha incorretos.")
            else:
                st.info("🔧 Login de cliente ainda não implementado.")

        if st.session_state.get("login_sucesso"):
            st.success(f"✅ Login realizado com sucesso! Bem-vindo, {st.session_state['nome_logado']} 👋")
            del st.session_state["login_sucesso"]
            del st.session_state["nome_logado"]
