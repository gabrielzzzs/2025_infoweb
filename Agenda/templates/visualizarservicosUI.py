import streamlit as st
from views import View

class VisualizarServicosUI:
    @staticmethod
    def main():
        st.header("📅 Visualizar Meus Serviços")

        # --- Verifica login ---
        usuario = st.session_state.get("usuario_logado")
        if not usuario or usuario.get("tipo") != "cliente":
            st.warning("⚠️ Acesso restrito! Faça login como cliente para visualizar seus serviços.")
            st.info("Vá até o menu **Login** e entre com seu e-mail e senha de cliente.")
            return

        id_cliente = usuario["id"]

        # --- Obtém todos os horários ---
        horarios = View.horario_listar()
        if not horarios:
            st.info("Nenhum horário cadastrado ainda.")
            return

        # --- Filtra horários do cliente logado ---
        meus_horarios = [h for h in horarios if h.get_id_cliente() == id_cliente]

        if not meus_horarios:
            st.info("Você ainda não possui serviços agendados.")
            return

        # --- Mostra lista formatada ---
        for h in sorted(meus_horarios, key=lambda x: x.get_data()):
            prof = View.profissional_listar_id(h.get_id_profissional())
            serv = View.servico_listar_id(h.get_id_servico())

            nome_prof = prof.get_nome() if prof else "Desconhecido"
            nome_serv = serv.get_nome() if serv else "Não informado"
            status = "✅ Confirmado" if h.get_confirmado() else "🕒 Aguardando Confirmação"

            st.write(
                f"**{h.get_data().strftime('%d/%m/%Y %H:%M')}** — Profissional: {nome_prof} — Serviço: {nome_serv} — {status}"
            )
