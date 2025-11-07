import streamlit as st
import json
import os
import pandas as pd
from views import View

class VisualizarServicosUI:
    @staticmethod
    def main():
        st.header("Visualizar Meus Serviços")

        # --------------------------
        # Verifica se há login ativo
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
        # Monta tabela com colunas solicitadas
        # --------------------------
        dados = []
        for h in sorted(meus_horarios, key=lambda x: x.get_data()):
            prof = View.profissional_listar_id(h.get_id_profissional())
            serv = View.servico_listar_id(h.get_id_servico())

            nome_prof = prof.get_nome() if prof else "Não identificado"
            nome_serv = serv.get_nome() if serv else "Não informado"
            confirmacao = "Sim" if h.get_confirmado() else "Não"

            dados.append({
                "ID": h.get_id(),
                "Data": h.get_data().strftime("%d/%m/%Y %H:%M"),
                "Confirmação": confirmacao,
                "Serviço": nome_serv,
                "Profissional": nome_prof
            })

        # --------------------------
        # Exibe tabela formatada
        # --------------------------
        df = pd.DataFrame(dados, columns=["ID", "Data", "Confirmação", "Serviço", "Profissional"])
        st.dataframe(df.style.hide(axis="index"), use_container_width=True)
