import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta
from views import View

class VisualizarServicosUI:
    @staticmethod
    def main():
        st.header("Visualizar Meus Serviços")

        # --------------------------
        # Verifica se há login ativo
        # --------------------------
        if not os.path.exists("usuario_logado.json"):
            st.warning("Acesso restrito. Faça login como cliente para visualizar seus serviços.")
            return

        with open("usuario_logado.json", "r", encoding="utf-8") as f:
            usuario = json.load(f)

        if usuario.get("tipo") != "cliente":
            st.warning("Acesso restrito. Esta página é apenas para clientes.")
            return

        id_cliente = usuario["id"]

        # --------------------------
        # Obtém todos os horários
        # --------------------------
        horarios = View.horario_listar()
        if not horarios:
            st.info("Nenhum horário cadastrado ainda.")
            return

        # --------------------------
        # Filtra horários do cliente logado
        # --------------------------
        meus_horarios = [h for h in horarios if h.get_id_cliente() == id_cliente and h.get_status() != "cancelado"]

        if not meus_horarios:
            st.info("Você ainda não possui serviços agendados.")
            return

        # --------------------------
        # Monta tabela com colunas solicitadas
        # --------------------------
        dados = []
        for h in sorted(meus_horarios, key=lambda x: x.get_data()):
            prof = View.profissional_listar_id(h.get_id_profissional())
            serv = View.servico_listar_id(h.get_id_servico())

            nome_prof = prof.get_nome() if prof else "Não identificado"
            nome_serv = serv.get_nome() if serv else "Não informado"
            confirmacao = "Sim" if h.get_confirmado() else "Não"

            dados.append({
                "ID": h.get_id(),
                "Data": h.get_data().strftime("%d/%m/%Y %H:%M"),
                "Confirmação": confirmacao,
                "Serviço": nome_serv,
                "Profissional": nome_prof,
                "Status": h.get_status()
            })

        # --------------------------
        # Exibe tabela com Streamlit
        # --------------------------
        df = pd.DataFrame(dados)
        st.dataframe(df.style.hide(axis="index"), use_container_width=True)

        # --------------------------
        # Ações: Cancelar ou Reagendar
        # --------------------------
        st.subheader("Cancelar ou Reagendar Horário")
        horario_ids = [h.get_id() for h in meus_horarios if h.get_status() not in ["cancelado", "remarcado"]]
        if horario_ids:
            id_selecionado = st.selectbox("Selecione o horário", horario_ids)

            # Cancelar
            if st.button("Cancelar Horário"):
                try:
                    View.horario_cancelar(id_selecionado, datetime.now())
                    st.success("Horário cancelado com sucesso!")
                except Exception as e:
                    st.error(f"Erro: {e}")

            # Reagendar
            nova_data = st.time_input("Nova Data e Hora")
            if st.button("Reagendar Horário"):
                try:
                    View.horario_reagendar(id_selecionado, nova_data)
                    st.success("Horário reagendado com sucesso!")
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.info("Nenhum horário disponível para cancelamento ou reagendamento.")
