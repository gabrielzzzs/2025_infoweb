import streamlit as st
import json
import os

class LoginUI:
    @staticmethod
    def main():
        st.title("Login no Sistema")

        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            usuario = None
            tipo_usuario = None

            # Verifica se é profissional
            try:
                with open("profissionais.json", "r", encoding="utf-8") as f:
                    profissionais = json.load(f)
            except FileNotFoundError:
                profissionais = []

            profissional = next((p for p in profissionais if p["email"] == email and p["senha"] == senha), None)
            if profissional:
                usuario = profissional
                tipo_usuario = "profissional"

            # Se não for profissional, tenta cliente
            if not usuario:
                try:
                    with open("clientes.json", "r", encoding="utf-8") as f:
                        clientes = json.load(f)
                except FileNotFoundError:
                    clientes = []

                cliente = next((c for c in clientes if c["email"] == email and c["senha"] == senha), None)
                if cliente:
                    usuario = cliente
                    tipo_usuario = "cliente"

            # Se achou usuário
            if usuario:
                if tipo_usuario == "cliente" and usuario["email"].lower() == "admin@admin.com":
                    tipo_usuario = "admin"

                # Salva o usuário logado
                with open("usuario_logado.json", "w", encoding="utf-8") as f:
                    json.dump({
                        "id": usuario["id"],
                        "nome": usuario["nome"],
                        "tipo": tipo_usuario
                    }, f, ensure_ascii=False, indent=4)

                st.success(f"Login bem-sucedido. Bem-vindo, {usuario['nome']} ({tipo_usuario}).")
            else:
                st.error("E-mail ou senha incorretos.")
