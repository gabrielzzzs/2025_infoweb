import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
from views import View

class VisualizarAgendaUI:
    @staticmethod
    def main():
        st.header("Visualizar Minha Agenda")

        # --------------------------
        # Verifica se há usuário logado
        # --------------------------
        if not os.path.exists("usuario_logado.json"):
            st.warning("Acesso restrito. Faça login como profissional para visualizar sua agenda.")
            return

        with open("usuario_logado.json", "r", encoding="utf-8") as f:
            usuario = json.load(f)

        if usuario.get("tipo") != "profissional":
            st.warning("Acesso restrito. Esta página é apenas para profissionais.")
            return

        id_prof = usuario["id"]

        # --------------------------
        # Obtém todos os horários
        # --------------------------
        horarios = View.horario_listar()
        if not horarios:
            st.info("Nenhum horário cadastrado ainda.")
            return

        # --------------------------
        # Filtra horários do profissional logado
        # --------------------------
        meus_horarios = [h for h in horarios if h.get_id_profissional() == id_prof]

        if not meus_horarios:
            st.info("Você ainda não possui horários na agenda.")
            return

        # --------------------------
        # Monta os dados em formato de tabela
        # --------------------------
        dados = []
        for h in sorted(meus_horarios, key=lambda x: x.get_data()):
            cliente = "-"
            servico = "-"
            if h.get_id_cliente():
                cli = View.cliente_listar_id(h.get_id_cliente())
                if cli:
                    cliente = cli.get_nome()
            if h.get_id_servico():
                serv = View.servico_listar_id(h.get_id_servico())
                if serv:
                    servico = serv.get_nome()

            confirmado = "Sim" if h.get_confirmado() else "Não"

            dados.append({
                "ID": h.get_id(),
                "Data e Hora": h.get_data().strftime("%d/%m/%Y %H:%M"),
                "Cliente": cliente or "Disponível",
                "Serviço": servico or "-",
                "Confirmado": confirmado,
                "Status": h.get_status()
            })

        # --------------------------
        # Exibe tabela com Streamlit
        # --------------------------
        df = pd.DataFrame(dados)
        st.dataframe(df.style.hide(axis="index"), use_container_width=True)

        # --------------------------
        # Ações: Confirmar, Cancelar ou Reagendar
        # --------------------------
        st.subheader("Gerenciar Horários")
        # Filtra apenas horários com cliente e que não estão cancelados
        horarios_validos = [h for h in meus_horarios if h.get_id_cliente() and h.get_status() != "cancelado"]
        if horarios_validos:
            id_selecionado = st.selectbox(
                "Selecione o horário", 
                [h.get_id() for h in horarios_validos]
            )

            # Confirmar horário
            if st.button("Confirmar Horário"):
                try:
                    horario = View.horario_listar_id(id_selecionado)
                    horario.set_confirmado(True)
                    from views import HorarioDAO
                    HorarioDAO().atualizar(horario)
                    st.success("Horário confirmado com sucesso!")
                except Exception as e:
                    st.error(f"Erro: {e}")

            # Cancelar horário
            if st.button("Cancelar Horário"):
                try:
                    View.horario_cancelar(id_selecionado, datetime.now())
                    st.success("Horário cancelado com sucesso!")
                except Exception as e:
                    st.error(f"Erro: {e}")

            # Reagendar horário
            nova_data = st.time_input("Nova Data e Hora")
            if st.button("Reagendar Horário"):
                try:
                    View.horario_reagendar(id_selecionado, nova_data)
                    st.success("Horário reagendado com sucesso!")
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.info("Nenhum horário disponível para gerenciar.")
