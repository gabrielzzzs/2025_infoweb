import streamlit as st
import json
import os
from views import View
from datetime import datetime

class AgendarServicoUI:
    @staticmethod
    def main():
        st.header("Agendar Serviço")

        # --------------------------
        # Verifica se o cliente está logado
        # --------------------------
        if not os.path.exists("usuario_logado.json"):
            st.warning("Acesso restrito. Faça login como cliente para agendar serviços.")
            return

        with open("usuario_logado.json", "r", encoding="utf-8") as f:
            usuario = json.load(f)

        if usuario.get("tipo") != "cliente":
            st.warning("Acesso restrito. Esta página é apenas para clientes.")
            return

        id_cliente = usuario["id"]

        # --------------------------
        # Selecionar profissional
        # --------------------------
        profs = View.profissional_listar()
        if not profs:
            st.info("Nenhum profissional cadastrado.")
            return

        prof_opcoes = {p.get_nome(): p.get_id() for p in profs}
        nome_prof = st.selectbox("Escolha o profissional", list(prof_opcoes.keys()))
        id_prof = prof_opcoes[nome_prof]

        # --------------------------
        # Selecionar serviço
        # --------------------------
        servicos = View.servico_listar()
        if not servicos:
            st.info("Nenhum serviço cadastrado.")
            return

        serv_opcoes = {s.nome: s.codigo for s in servicos}
        nome_serv = st.selectbox("Escolha o serviço", list(serv_opcoes.keys()))
        id_serv = serv_opcoes[nome_serv]

        # --------------------------
        # Selecionar horário disponível
        # --------------------------
        horarios = View.horario_listar()

        hora_opcoes = []
        hora_map = {}  # Mapa do texto para o objeto horário

        for h in horarios:
            if h.get_id_profissional() != id_prof:
                continue

            texto = h.get_data().strftime("%d/%m/%Y %H:%M")
            if h.get_id_cliente() is None and h.get_data() > datetime.now():
                # horário disponível
                hora_opcoes.append(texto)
            else:
                # horário ocupado ou passado
                texto += " (Indisponível)"
                hora_opcoes.append(texto)

            hora_map[texto] = h

        if not hora_opcoes:
            st.info("Nenhum horário disponível para este profissional.")
            return

        horario_str = st.selectbox("Escolha o horário", hora_opcoes)

        # --------------------------
        # Botão de agendamento
        # --------------------------
        horario = hora_map[horario_str]
        if horario.get_id_cliente() is not None or horario.get_data() < datetime.now():
            st.warning("Este horário não está disponível. Escolha outro.")
        else:
            if st.button("Confirmar Agendamento"):
                # Impede o mesmo cliente de agendar o mesmo horário duas vezes
                for h in horarios:
                    if (
                        h.get_id_cliente() == id_cliente and
                        h.get_data() == horario.get_data() and
                        h.get_id_profissional() == id_prof
                    ):
                        st.error("Você já possui um agendamento neste mesmo horário.")
                        return

                # Atualiza o horário com cliente e serviço
                horario.set_id_cliente(id_cliente)
                horario.set_id_servico(id_serv)
                horario.set_confirmado(False)
                View.horario_atualizar(
                    horario.get_id(),
                    horario.get_data(),
                    horario.get_confirmado(),
                    horario.get_id_cliente(),
                    horario.get_id_servico(),
                    horario.get_id_profissional()
                )

                st.success("Serviço agendado com sucesso!")
