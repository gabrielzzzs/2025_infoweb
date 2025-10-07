import streamlit as st
import pandas as pd
import time
from views import View

class ManterServicoUI:
    @staticmethod
    def main():
        st.header("Cadastro de Serviços")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterServicoUI.listar()
        with tab2: ManterServicoUI.inserir()
        with tab3: ManterServicoUI.atualizar()
        with tab4: ManterServicoUI.excluir()

    @staticmethod
    def listar():
        servicos = View.servico_listar()
        if len(servicos) == 0:
            st.write("Nenhum serviço cadastrado")
        else:
            list_dic = [obj.to_json() for obj in servicos]
            df = pd.DataFrame(list_dic)
            st.dataframe(df)

    @staticmethod
    def inserir():
        nome = st.text_input("Informe o nome do serviço")
        preco = st.number_input("Informe o preço do serviço", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Inserir"):
            View.servico_inserir(nome, preco) 
            st.success("Serviço inserido com sucesso")
            time.sleep(2)
            st.rerun()

    @staticmethod
    def atualizar():
        servicos = View.servico_listar()
        if len(servicos) == 0:
            st.write("Nenhum serviço cadastrado")
        else:
            op = st.selectbox("Atualização de Serviços", servicos, format_func=lambda s: f"{s.get_nome()} (R$ {s.get_preco():.2f})")
            nome = st.text_input("Novo nome", op.get_nome())
            preco = st.number_input("Novo preço", value=op.get_preco(), step=0.01, format="%.2f")
            if st.button("Atualizar"):
                View.servico_atualizar(op.get_codigo(), nome, preco)
                st.success("Serviço atualizado com sucesso")
                time.sleep(2)
                st.rerun()

    @staticmethod
    def excluir():
        servicos = View.servico_listar()
        if len(servicos) == 0:
            st.write("Nenhum serviço cadastrado")
        else:
            op = st.selectbox("Exclusão de Serviços", servicos, format_func=lambda s: f"{s.get_nome()} (R$ {s.get_preco():.2f})")
            if st.button("Excluir"):
                View.servico_excluir(op.get_codigo())
                st.success("Serviço excluído com sucesso")
                time.sleep(2)
                st.rerun()
