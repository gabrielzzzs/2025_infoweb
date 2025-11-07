import streamlit as st
import json
import os
from views import View

class VisualizarServicosUI:
    @staticmethod
    def main():
        st.header("Visualizar Meus Serviços")

        # --------------------------
        # Verifica se há usuário logado
        # --------------------------
        if not os.path.exists("usuario_logado.json"):
            st.warning("Acesso restrito. Faça login como cliente para visualizar seus serviços.")
            return

        with open("usuario_logado.json", "r", encoding="utf-8") as f:
            usuario = json.load(f)

        if usuario.get("tipo") not in ["cliente", "admin"]:
            st.warning("Acesso restrito. Esta página é apenas para clientes.")
            return

        id_cliente = usuario["id"]
        st.success(f"Bem-vindo, {usuario['nome']}")

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
        meus_horarios = [h for h in horarios if h.get_id_cliente() == id_cliente]

        if not meus_horarios:
            st.info("Você ainda não possui serviços agendados.")
            return

        # --------------------------
        # Mostra lista formatada
        # --------------------------
        st.subheader("Meus Serviços Agendados")
        for h in sorted(meus_horarios, key=lambda x: x.get_data()):
            prof = View.profissional_listar_id(h.get_id_profissional())
            serv = View.servico_listar_id(h.get_id_servico())

            nome_prof = prof.get_nome() if prof else "Desconhecido"
            nome_serv = serv.get_nome() if serv else "Não informado"
            status = "Confirmado" if h.get_confirmado() else "Aguardando confirmação"

            st.write(
                f"{h.get_data().strftime('%d/%m/%Y %H:%M')} — Profissional: {nome_prof} — Serviço: {nome_serv} — {status}"
            )
