import streamlit as st
import pandas as pd
from views import View
import time
from datetime import datetime

class ManterHorarioUI:
    @staticmethod
    def main():
        st.header("Cadastro de Horários")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1:
            ManterHorarioUI.listar()
        with tab2:
            ManterHorarioUI.inserir()
        with tab3:
            ManterHorarioUI.atualizar()
        with tab4:
            ManterHorarioUI.excluir()

    # ------------------------------------------------------
    @staticmethod
    def listar():
        horarios = View.horario_listar()
        if len(horarios) == 0:
            st.write("Nenhum horário cadastrado")
        else:
            dados = []
            for obj in horarios:
                cliente = View.cliente_listar_id(obj.get_id_cliente())
                servico = View.servico_listar_id(obj.get_id_servico())
                profissional = View.profissional_listar_id(obj.get_id_profissional())

                cliente_nome = cliente.get_nome() if cliente else ""
                servico_nome = servico.get_nome() if servico else ""
                profissional_nome = profissional.get_nome() if profissional else ""

                dados.append({
                    "ID": obj.get_id(),
                    "Data e Hora": obj.get_data().strftime("%d/%m/%Y %H:%M"),
                    "Confirmado": "Sim" if obj.get_confirmado() else "Não",
                    "Cliente": cliente_nome,
                    "Serviço": servico_nome,
                    "Profissional": profissional_nome
                })

            df = pd.DataFrame(dados)
            st.dataframe(df)

    # ------------------------------------------------------
    @staticmethod
    def inserir():
        clientes = View.cliente_listar()
        servicos = View.servico_listar()
        profissionais = View.profissional_listar()

        data = st.text_input("Informe a data e horário do serviço (dd/mm/aaaa HH:MM)",
                             datetime.now().strftime("%d/%m/%Y %H:%M"))
        confirmado = st.checkbox("Confirmado", key="inserir_confirmado")

        cliente = st.selectbox("Informe o cliente", clientes, index=None,
                               format_func=lambda c: c.get_nome())
        servico = st.selectbox("Informe o serviço", servicos, index=None,
                               format_func=lambda s: s.get_nome())
        profissional = st.selectbox("Informe o profissional", profissionais, index=None,
                                    format_func=lambda p: p.get_nome())

        if st.button("Inserir"):
            id_cliente = cliente.get_id() if cliente else None
            id_servico = servico.get_codigo() if servico else None
            id_profissional = profissional.get_id() if profissional else None

            try:
                data_obj = datetime.strptime(data, "%d/%m/%Y %H:%M")
                View.horario_inserir(data_obj, confirmado, id_cliente, id_servico, id_profissional)
                st.success("Horário inserido com sucesso!")
            except ValueError:
                st.error("Formato de data inválido. Use o formato dd/mm/aaaa HH:MM.")

    # ------------------------------------------------------
    @staticmethod
    def atualizar():
        horarios = View.horario_listar()
        if len(horarios) == 0:
            st.write("Nenhum horário cadastrado")
        else:
            clientes = View.cliente_listar()
            servicos = View.servico_listar()
            profissionais = View.profissional_listar()

            op = st.selectbox("Selecione o horário para atualizar", horarios,
                              format_func=lambda h: f"{h.get_id()} - {h.get_data().strftime('%d/%m/%Y %H:%M')}")
            data = st.text_input("Nova data e horário (dd/mm/aaaa HH:MM)",
                                 op.get_data().strftime("%d/%m/%Y %H:%M"))
            confirmado = st.checkbox("Confirmado", value=op.get_confirmado(),
                                     key=f"atualizar_confirmado_{op.get_id()}")

            cliente_sel = next((c for c in clientes if c.get_id() == op.get_id_cliente()), None)
            servico_sel = next((s for s in servicos if s.get_codigo() == op.get_id_servico()), None)
            prof_sel = next((p for p in profissionais if p.get_id() == op.get_id_profissional()), None)

            cliente = st.selectbox("Novo cliente", clientes,
                                   index=clientes.index(cliente_sel) if cliente_sel else None,
                                   format_func=lambda c: c.get_nome())
            servico = st.selectbox("Novo serviço", servicos,
                                   index=servicos.index(servico_sel) if servico_sel else None,
                                   format_func=lambda s: s.get_nome())
            profissional = st.selectbox("Novo profissional", profissionais,
                                        index=profissionais.index(prof_sel) if prof_sel else None,
                                        format_func=lambda p: p.get_nome())

            if st.button("Atualizar"):
                id_cliente = cliente.get_id() if cliente else None
                id_servico = servico.get_codigo() if servico else None
                id_profissional = profissional.get_id() if profissional else None

                try:
                    data_obj = datetime.strptime(data, "%d/%m/%Y %H:%M")
                    View.horario_atualizar(op.get_id(), data_obj, confirmado, id_cliente, id_servico, id_profissional)
                    st.success("Horário atualizado com sucesso!")
                except ValueError:
                    st.error("Formato de data inválido. Use o formato dd/mm/aaaa HH:MM.")

    # ------------------------------------------------------
    @staticmethod
    def excluir():
        horarios = View.horario_listar()
        if len(horarios) == 0:
            st.write("Nenhum horário cadastrado")
        else:
            op = st.selectbox("Selecione o horário para excluir", horarios,
                              format_func=lambda h: f"{h.get_id()} - {h.get_data().strftime('%d/%m/%Y %H:%M')}")
            if st.button("Excluir"):
                View.horario_excluir(op.get_id())
                st.success("Horário excluído com sucesso!")
                time.sleep(2)
                st.rerun()
