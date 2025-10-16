import streamlit as st
from models.profissional import Profissional, ProfissionalDAO

class ManterProfissionalUI:
    @staticmethod
    def main():
        st.header("Cadastro de Profissionais 👨‍⚕️")

        tab1, tab2, tab3, tab4 = st.tabs(["Inserir", "Listar", "Atualizar", "Excluir"])

        # --------------------------
        # INSERIR
        # --------------------------
        with tab1:
            nome = st.text_input("Nome")
            especialidade = st.text_input("Especialidade")
            conselho = st.text_input("Conselho Profissional (ex: CRM, CRP, etc.)")
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")

            if st.button("Inserir"):
                if not nome or not email or not senha:
                    st.error("Preencha pelo menos Nome, E-mail e Senha.")
                else:
                    obj = Profissional(0, nome, especialidade, conselho, email, senha)
                    ProfissionalDAO.inserir(obj)
                    st.success("✅ Profissional inserido com sucesso!")

        # --------------------------
        # LISTAR
        # --------------------------
        with tab2:
            lista = ProfissionalDAO.listar()
            if len(lista) == 0:
                st.info("Nenhum profissional cadastrado.")
            else:
                for obj in lista:
                    st.write(obj)

        # --------------------------
        # ATUALIZAR
        # --------------------------
        with tab3:
            lista = ProfissionalDAO.listar()
            if len(lista) == 0:
                st.info("Nenhum profissional cadastrado.")
            else:
                op = st.selectbox(
                    "Selecione o profissional",
                    lista,
                    format_func=lambda p: f"{p.get_nome()} ({p.get_especialidade()})"
                )
                nome = st.text_input("Nome", op.get_nome())
                especialidade = st.text_input("Especialidade", op.get_especialidade())
                conselho = st.text_input("Conselho", op.get_conselho())
                email = st.text_input("E-mail", op.get_email())
                senha = st.text_input("Senha", op.get_senha(), type="password")

                if st.button("Atualizar"):
                    obj = Profissional(op.get_id(), nome, especialidade, conselho, email, senha)
                    ProfissionalDAO.atualizar(obj)
                    st.success("✅ Profissional atualizado com sucesso!")

        # --------------------------
        # EXCLUIR
        # --------------------------
        with tab4:
            lista = ProfissionalDAO.listar()
            if len(lista) == 0:
                st.info("Nenhum profissional cadastrado.")
            else:
                op = st.selectbox(
                    "Selecione o profissional para excluir",
                    lista,
                    format_func=lambda p: f"{p.get_nome()} ({p.get_especialidade()})"
                )
                if st.button("Excluir"):
                    ProfissionalDAO.excluir(op)
                    st.success("🗑️ Profissional excluído com sucesso!")
