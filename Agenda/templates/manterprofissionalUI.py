import streamlit as st
from models.profissional import Profissional, ProfissionalDAO

class ManterProfissionalUI:
    @staticmethod
    def main():
        st.header("Cadastro de Profissionais")

        tab1, tab2, tab3, tab4 = st.tabs(["Inserir", "Listar", "Atualizar", "Excluir"])

        with tab1:
            nome = st.text_input("Nome")
            especialidade = st.text_input("Especialidade")
            email = st.text_input("Email")
            fone = st.text_input("Fone")
            if st.button("Inserir"):
                obj = Profissional(0, nome, especialidade, email, fone)
                ProfissionalDAO.inserir(obj)
                st.success("Profissional inserido com sucesso!")

        with tab2:
            for obj in ProfissionalDAO.listar():
                st.write(obj)

        with tab3:
            id = st.number_input("Informe o ID para atualizar", min_value=1, step=1)
            obj = ProfissionalDAO.listar_id(id)
            if obj:
                nome = st.text_input("Nome", obj.get_nome())
                especialidade = st.text_input("Especialidade", obj.get_especialidade())
                email = st.text_input("Email", obj.get_email())
                fone = st.text_input("Fone", obj.get_fone())
                if st.button("Atualizar"):
                    obj = Profissional(id, nome, especialidade, email, fone)
                    ProfissionalDAO.atualizar(obj)
                    st.success("Atualizado com sucesso!")
            else:
                st.info("ID não encontrado.")

        with tab4:
            id = st.number_input("Informe o ID para excluir", min_value=1, step=1, key="del")
            obj = ProfissionalDAO.listar_id(id)
            if obj and st.button("Excluir"):
                ProfissionalDAO.excluir(obj)
                st.success("Excluído com sucesso!")
