import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
from views import View

class VisualizarServicosUI:
    @staticmethod
    def main():
        st.header("Visualizar Meus Serviços")

        # --------------------------
        # Verifica login
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
        # Função para carregar e filtrar horários
        # --------------------------
        def carregar_horarios():
            horarios = View.horario_listar()
            return [h for h in horarios if h.get_id_cliente() == id_cliente and h.get_status() != "cancelado"]

        # Inicializa a sessão para forçar refresh
        if "reload_key" not in st.session_state:
            st.session_state.reload_key = 0

        meus_horarios = carregar_horarios()
        if not meus_horarios:
            st.info("Você ainda não possui serviços agendados.")
            return

        # --------------------------
        # Monta tabela
        # --------------------------
        dados = []
        for h in sorted(meus_horarios, key=lambda x: x.get_data()):
            prof = View.profissional_listar_id(h.get_id_profissional())
            serv = View.servico_listar_id(h.get_id_servico())
            dados.append({
                "ID": h.get_id(),
                "Data": h.get_data().strftime("%d/%m/%Y %H:%M"),
                "Confirmação": "Sim" if h.get_confirmado() else "Não",
                "Serviço": serv.get_nome() if serv else "Não informado",
                "Profissional": prof.get_nome() if prof else "Não identificado",
                "Status": h.get_status()
            })

        df = pd.DataFrame(dados)
        st.dataframe(df.style.hide(axis="index"), use_container_width=True)

        # --------------------------
        # Cancelar ou reagendar
        # --------------------------
        st.subheader("Cancelar ou Reagendar Horário")
        horarios_disponiveis = [h for h in meus_horarios if h.get_status() != "cancelado"]

        if horarios_disponiveis:
            id_selecionado = st.selectbox(
                "Selecione o horário pelo ID",
                [h.get_id() for h in horarios_disponiveis],
                key=f"selectbox_{st.session_state.reload_key}"
            )

            # Cancelar
            if st.button("Cancelar Horário", key=f"cancelar_{st.session_state.reload_key}"):
                try:
                    View.horario_cancelar(id_selecionado)
                    st.success("Horário cancelado com sucesso!")
                    st.session_state.reload_key += 1  # Atualiza a sessão para recarregar a página
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao cancelar: {e}")

            # Reagendar
            st.markdown("**Reagendar Horário**")
            nova_data = st.date_input("Nova Data", key=f"data_{st.session_state.reload_key}")
            nova_hora = st.time_input("Nova Hora", key=f"hora_{st.session_state.reload_key}")
            if st.button("Reagendar Horário", key=f"reagendar_{st.session_state.reload_key}"):
                try:
                    nova_datahora = datetime.combine(nova_data, nova_hora)
                    View.horario_reagendar(id_selecionado, nova_datahora)
                    st.success("Horário reagendado com sucesso!")
                    st.session_state.reload_key += 1  # Atualiza a sessão
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao reagendar: {e}")
        else:
            st.info("Nenhum horário disponível para cancelamento ou reagendamento.")
