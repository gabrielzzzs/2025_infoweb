import streamlit as st
import pandas as pd
import time
from views import View

class ManterClienteUI:
    @staticmethod
    def main():
        st.header("Cadastro de Clientes 👤")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterClienteUI.listar()
        with tab2: ManterClienteUI.inserir()
        with tab3: ManterClienteUI.atualizar()
        with tab4: ManterClienteUI.excluir()

    @staticmethod
    def listar():
        clientes = View.cliente_listar()
        if len(clientes) == 0:
            st.info("Nenhum cliente cadastrado")
        else:
            df = pd.DataFrame([obj.to_json() for obj in clientes])
            st.dataframe(df)

    @staticmethod
    def inserir():
        nome = st.text_input("Nome", key="nome_inserir")
        email = st.text_input("E-mail", key="email_inserir")
        fone = st.text_input("Telefone", key="fone_inserir")
        senha = st.text_input("Senha", type="password", key="senha_inserir")  # ✅ campo com chave única
        if st.button("Inserir", key="btn_inserir"):
            if not nome or not email or not senha:
                st.error("⚠️ Preencha nome, e-mail e senha.")
            else:
                View.cliente_inserir(nome, email, fone, senha)
                st.success("✅ Cliente inserido com sucesso!")
                time.sleep(1.5)
                st.rerun()

    @staticmethod
    def atualizar():
        clientes = View.cliente_listar()
        if len(clientes) == 0:
            st.info("Nenhum cliente cadastrado")
        else:
            op = st.selectbox("Selecione o cliente para atualizar", clientes, key="sel_atualizar")
            nome = st.text_input("Nome", op.get_nome(), key=f"nome_atualizar_{op.get_id()}")
            email = st.text_input("E-mail", op.get_email(), key=f"email_atualizar_{op.get_id()}")
            fone = st.text_input("Telefone", op.get_fone(), key=f"fone_atualizar_{op.get_id()}")
            senha = st.text_input("Senha", op.get_senha(), type="password", key=f"senha_atualizar_{op.get_id()}")  # ✅ chave única
            if st.button("Atualizar", key=f"btn_atualizar_{op.get_id()}"):
                View.cliente_atualizar(op.get_id(), nome, email, fone, senha)
                st.success("✅ Cliente atualizado com sucesso!")
                time.sleep(1.5)
                st.rerun()

    @staticmethod
    def excluir():
        clientes = View.cliente_listar()
        if len(clientes) == 0:
            st.info("Nenhum cliente cadastrado")
        else:
            op = st.selectbox("Selecione o cliente para excluir", clientes, key="sel_excluir")
            if st.button("Excluir", key=f"btn_excluir_{op.get_id()}"):
                View.cliente_excluir(op.get_id())
                st.success("🗑️ Cliente excluído com sucesso!")
                time.sleep(1.5)
                st.rerun()
