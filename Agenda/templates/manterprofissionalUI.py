import streamlit as st
from views import View
from models.profissional import Profissional

class ManterProfissionalUI:
    @staticmethod
    def main():
        st.header("Cadastro de Profissionais")
        abas = st.tabs(["Inserir", "Listar", "Atualizar", "Excluir"])

        def tratar(acao, func, *args):
            """Executa uma ação com tratamento de erros."""
            try:
                func(*args)
                st.success(f"Profissional {acao} com sucesso!")
            except ValueError as e:
                st.error(f"Erro: {e}")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")


        with abas[0]:
            nome = st.text_input("Nome")
            esp = st.text_input("Especialidade")
            cons = st.text_input("Conselho Profissional (CRM, CRP...)")
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")

            if st.button("Inserir"):
                if not nome or not email or not senha:
                    st.error("Preencha pelo menos Nome, E-mail e Senha.")
                else:
                    tratar("inserido", View.profissional_inserir, nome, esp, cons, email, senha)

        with abas[1]:
            try:
                lista = View.profissional_listar()
                if not lista:
                    st.info("Nenhum profissional cadastrado.")
                else:
                    for p in lista:
                        st.write(p)
            except Exception as e:
                st.error(f"Erro ao listar: {e}")

        with abas[2]:
            try:
                lista = View.profissional_listar()
                if not lista:
                    st.info("Nenhum profissional cadastrado.")
                else:
                    p = st.selectbox("Selecione o profissional", lista, format_func=lambda x: f"{x.get_nome()} ({x.get_especialidade()})")
                    nome = st.text_input("Nome", p.get_nome())
                    esp = st.text_input("Especialidade", p.get_especialidade())
                    cons = st.text_input("Conselho", p.get_conselho())
                    email = st.text_input("E-mail", p.get_email())
                    senha = st.text_input("Senha", p.get_senha(), type="password")

                    if st.button("Atualizar"):
                        tratar("atualizado", View.profissional_atualizar, p.get_id(), nome, esp, cons, email, senha)
            except Exception as e:
                st.error(f"Erro ao carregar: {e}")

        with abas[3]:
            try:
                lista = View.profissional_listar()
                if not lista:
                    st.info("Nenhum profissional cadastrado.")
                else:
                    p = st.selectbox("Selecione o profissional para excluir", lista, format_func=lambda x: f"{x.get_nome()} ({x.get_especialidade()})")
                    if st.button("Excluir"):
                        tratar("excluído", View.profissional_excluir, p.get_id())
            except Exception as e:
                st.error(f"Erro ao carregar: {e}")
