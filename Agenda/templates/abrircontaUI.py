import streamlit as st 
from views import View

class AbrirContaUI:

    @staticmethod
    def main():
        st.header("Abrir Conta - Cliente")

        # Campos do formulário
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        fone = st.text_input("Telefone")
        senha = st.text_input("Senha", type="password")

        if st.button("Cadastrar"):
            try:
                View.cliente_inserir(nome, email, fone, senha)
                st.success(f"Cliente '{nome}' cadastrado com sucesso!")
            except ValueError as e:
                st.error(f"Erro: {e}")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")
