import streamlit as st
import json
import os
import pandas as pd
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
                "Data e Hora": h.get_data().strftime("%d/%m/%Y %H:%M"),
                "Cliente": cliente or "Disponível",
                "Serviço": servico or "-",
                "Confirmado": confirmado
            })

        # --------------------------
        # Exibe tabela com Streamlit
        # --------------------------
        df = pd.DataFrame(dados)
        st.dataframe(df, use_container_width=True)
