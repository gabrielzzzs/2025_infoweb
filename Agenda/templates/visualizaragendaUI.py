import streamlit as st
from views import View

class VisualizarAgendaUI:
    @staticmethod
    def main():
        st.header("📅 Visualizar Minha Agenda")

        # --- Verifica login ---
        usuario = st.session_state.get("usuario_logado")
        if not usuario or usuario.get("tipo") != "profissional":
            st.warning("⚠️ Acesso restrito! Faça login como profissional para visualizar sua agenda.")
            return

        id_prof = usuario["id"]

        # --- Obtém todos os horários ---
        horarios = View.horario_listar()
        if not horarios:
            st.info("Nenhum horário cadastrado ainda.")
            return

        # --- Filtra horários do profissional logado ---
        meus_horarios = [h for h in horarios if h.get_id_profissional() == id_prof]

        if not meus_horarios:
            st.info("Você ainda não possui horários na agenda.")
            return

        # --- Mostra lista formatada ---
        for h in sorted(meus_horarios, key=lambda x: x.get_data()):
            cliente = "Disponível"
            servico = "-"
            if h.get_id_cliente():
                cli = View.cliente_listar_id(h.get_id_cliente())
                if cli:
                    cliente = cli.get_nome()
            if h.get_id_servico():
                serv = View.servico_listar_id(h.get_id_servico())
                if serv:
                    servico = serv.get_nome()

            confirmado = "✅ Confirmado" if h.get_confirmado() else "🕒 Pendente"
            st.write(
                f"**{h.get_data().strftime('%d/%m/%Y %H:%M')}** — Cliente: {cliente} — Serviço: {servico} — {confirmado}"
            )
