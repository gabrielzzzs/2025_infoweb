import streamlit as st
import json
import os
from views import View

class ConfirmarServicoUI:
    @staticmethod
    def main():
        st.header("Confirmar Serviços Agendados")

        # --------------------------
        # Verifica se há usuário logado
        # --------------------------
        if not os.path.exists("usuario_logado.json"):
            st.warning("Acesso restrito. Faça login como profissional para confirmar serviços.")
            return

        with open("usuario_logado.json", "r", encoding="utf-8") as f:
            usuario = json.load(f)

        if usuario.get("tipo") != "profissional":
            st.warning("Acesso restrito. Esta página é apenas para profissionais.")
            return

        id_prof = usuario["id"]

        # --------------------------
        # Obtém horários cadastrados
        # --------------------------
        horarios = View.horario_listar()
        if not horarios:
            st.info("Nenhum horário cadastrado.")
            return

        # --------------------------
        # Filtra apenas os agendamentos com cliente e serviço
        # --------------------------
        agendados = [
            h for h in horarios
            if h.get_id_profissional() == id_prof and h.get_id_cliente() and h.get_id_servico()
        ]

        if not agendados:
            st.info("Nenhum serviço agendado para confirmação.")
            return

        # --------------------------
        # Exibe lista de serviços pendentes
        # --------------------------
        st.subheader("Serviços pendentes de confirmação:")

        for h in sorted(agendados, key=lambda x: x.get_data()):
            cliente = View.cliente_listar_id(h.get_id_cliente())
            servico = View.servico_listar_id(h.get_id_servico())

            nome_cliente = cliente.get_nome() if cliente else "Desconhecido"
            nome_servico = servico.get_nome() if servico else "Não informado"
            data_str = h.get_data().strftime("%d/%m/%Y %H:%M")

            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{data_str} — Cliente: {nome_cliente} — Serviço: {nome_servico}")
            with col2:
                if not h.get_confirmado():
                    if st.button("Confirmar", key=f"conf_{h.get_id()}"):
                        View.horario_atualizar(
                            h.get_id(),
                            h.get_data(),
                            True,  # confirmado = True
                            h.get_id_cliente(),
                            h.get_id_servico(),
                            h.get_id_profissional()
                        )
                        st.success(f"Serviço confirmado para {nome_cliente}.")
                        st.rerun()
                else:
                    st.info("Confirmado")
