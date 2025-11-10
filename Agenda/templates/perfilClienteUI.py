import streamlit as st
import json
import os
from views import View

class PerfilClienteUI:

    @staticmethod
    def main():
        st.header("Perfil do Cliente")

        # Verifica usuário logado
        try:
            with open("usuario_logado.json", "r", encoding="utf-8") as f:
                usuario = json.load(f)
        except FileNotFoundError:
            st.warning("Acesso restrito. Faça login como cliente.")
            return

        if usuario.get("tipo") != "cliente":
            st.warning("Acesso restrito. Esta página é apenas para clientes.")
            return

        id_cliente = usuario["id"]

        # Obtém dados do cliente
        cliente = View.cliente_listar_id(id_cliente)
        if not cliente:
            st.error("Cliente não encontrado.")
            return

        # Campos do formulário
        st.text_input("E-mail (não pode ser alterado)", value=cliente.get_email(), disabled=True)
        nome = st.text_input("Nome", value=cliente.get_nome())
        fone = st.text_input("Telefone", value=cliente.get_fone())
        senha_atual = st.text_input("Senha atual", type="password")
        nova_senha = st.text_input("Nova senha", type="password")
        confirmar_senha = st.text_input("Confirmar nova senha", type="password")

        # Botão Atualizar
        if st.button("Atualizar"):
            try:
                # Valida senha atual
                if senha_atual != cliente.get_senha():
                    raise ValueError("Senha atual incorreta.")

                # Valida nova senha
                if nova_senha != confirmar_senha:
                    raise ValueError("Nova senha e confirmação não conferem.")

                # Atualiza cliente
                View.cliente_atualizar(
                    id_cliente,
                    nome,
                    cliente.get_email(),  # e-mail não muda
                    fone,
                    nova_senha if nova_senha else cliente.get_senha()
                )

                st.success("Dados atualizados com sucesso!")

            except ValueError as e:
                st.error(f"Erro: {e}")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")
                
        if st.button("Sair"):
            try:
                os.remove("usuario_logado.json")
                st.success("Você saiu da sua conta com sucesso!")
                st.info("Recarregue a página para voltar à tela de login.")
            except Exception as e:
                st.error(f"Erro ao sair: {e}")
