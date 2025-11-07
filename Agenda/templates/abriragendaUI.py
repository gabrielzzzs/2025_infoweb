import streamlit as st
from datetime import datetime
import json
import os
from views import View

class AbrirAgendaUI:
    @staticmethod
    def main():
        st.header("Abrir Minha Agenda")

        # --------------------------
        # Verifica se há usuário logado
        # --------------------------
        if not os.path.exists("usuario_logado.json"):
            st.warning("Acesso restrito. Faça login como profissional para abrir sua agenda.")
            return

        with open("usuario_logado.json", "r", encoding="utf-8") as f:
            usuario = json.load(f)

        if usuario.get("tipo") != "profissional":
            st.warning("Acesso restrito. Esta página é apenas para profissionais.")
            return

        id_prof = usuario["id"]
        nome_prof = usuario["nome"]

        # --------------------------
        # Campos da agenda
        # --------------------------
        data = st.date_input("Dia do atendimento", datetime.now().date())
        hora_inicio = st.time_input("Hora inicial", datetime.strptime("08:00", "%H:%M").time())
        hora_fim = st.time_input("Hora final", datetime.strptime("12:00", "%H:%M").time())
        intervalo = st.number_input("Intervalo entre atendimentos (minutos)", min_value=10, step=5, value=30)

        # --------------------------
        # Gerar horários automaticamente
        # --------------------------
        if st.button("Gerar horários"):
            qtd = View.abrir_agenda(id_prof, data, hora_inicio, hora_fim, intervalo)
            st.success(f"{qtd} horários adicionados à agenda de {nome_prof} com sucesso.")
