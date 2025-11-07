import streamlit as st
import json
from datetime import datetime
from views import View

class AbrirAgendaUI:
    @staticmethod
    def main():
        st.header("Abrir Minha Agenda")

        # Verifica se há um profissional logado
        try:
            with open("usuario_logado.json", "r", encoding="utf-8") as f:
                usuario = json.load(f)
        except FileNotFoundError:
            usuario = None

        if not usuario or usuario.get("tipo") != "profissional":
            st.warning("Acesso restrito. Faça login como profissional para abrir sua agenda.")
            return

        id_prof = usuario["id"]

        # Campos da agenda
        data = st.date_input("Dia do atendimento", datetime.now().date())
        hora_inicio = st.time_input("Hora inicial", datetime.strptime("08:00", "%H:%M").time())
        hora_fim = st.time_input("Hora final", datetime.strptime("12:00", "%H:%M").time())
        intervalo = st.number_input("Intervalo entre atendimentos (minutos)", min_value=10, step=5, value=30)

        # Gerar horários
        if st.button("Gerar horários"):
            qtd = View.abrir_agenda(id_prof, data, hora_inicio, hora_fim, intervalo)
            st.success(f"{qtd} horários adicionados à sua agenda com sucesso!")
