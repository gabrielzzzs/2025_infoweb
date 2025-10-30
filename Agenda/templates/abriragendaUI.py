import streamlit as st
from datetime import datetime
from views import View

class AbrirAgendaUI:
    @staticmethod
    def main():
        st.header("🗓️ Abrir Minha Agenda")

        # --------------------------
        # Verificar login
        # --------------------------
        usuario = st.session_state.get("usuario_logado")

        if not usuario or usuario.get("tipo") != "profissional":
            st.warning(" Acesso restrito! Faça login como profissional para abrir sua agenda.")
            return  # interrompe aqui, não mostra o resto da tela

        # --------------------------
        # Pegar o profissional logado
        # --------------------------
        prof_id = usuario["id"]
        prof = View.profissional_listar_id(prof_id)

        st.subheader(f" Profissional: {prof.get_nome()}")

        # --------------------------
        # Campos da agenda
        # --------------------------
        data = st.date_input("Dia do atendimento", datetime.now().date())
        hora_inicio = st.time_input("Hora inicial", datetime.strptime("08:00", "%H:%M").time())
        hora_fim = st.time_input("Hora final", datetime.strptime("12:00", "%H:%M").time())
        intervalo = st.number_input("Intervalo entre atendimentos (minutos)", min_value=10, step=5, value=30)

        # --------------------------
        # Gerar horários
        # --------------------------
        if st.button("Gerar horários"):
            qtd = View.abrir_agenda(prof.get_id(), data, hora_inicio, hora_fim, intervalo)
            st.success(f" {qtd} horários adicionados à agenda de {prof.get_nome()}!")
