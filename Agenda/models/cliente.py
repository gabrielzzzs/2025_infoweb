import json
from models.dao import DAO

# ============================================================
# Classe Cliente (modelo)
# ============================================================
class Cliente:
    def __init__(self, id, nome, email, fone, senha):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_fone(fone)
        self.set_senha(senha)

    # -------- Getters --------
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_email(self): return self.__email
    def get_fone(self): return self.__fone
    def get_senha(self): return self.__senha

    # -------- Setters --------
    def set_id(self, id): self.__id = id

    def set_nome(self, nome):
        if not nome or nome.strip() == "":
            raise ValueError("O nome do cliente não pode ser vazio.")
        self.__nome = nome.strip()

    def set_email(self, email):
        if not email or email.strip() == "":
            raise ValueError("O e-mail do cliente não pode ser vazio.")
        self.__email = email.strip()

    def set_fone(self, fone):
        self.__fone = fone.strip() if fone else ""

    def set_senha(self, senha):
        if not senha or senha.strip() == "":
            raise ValueError("A senha do cliente não pode ser vazia.")
        self.__senha = senha.strip()

    # -------- JSON --------
    def to_json(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "email": self.__email,
            "fone": self.__fone,
            "senha": self.__senha
        }

    @staticmethod
    def from_json(dic):
        return Cliente(
            dic.get("id", 0),
            dic.get("nome", ""),
            dic.get("email", ""),
            dic.get("fone", ""),
            dic.get("senha", "")
        )

    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__email} - {self.__fone}"


# ============================================================
# DAO - Herdando da classe base DAO
# ============================================================
class ClienteDAO(DAO):
    def __init__(self):
        super().__init__("clientes.json")

    def from_json(self, dic):
        return Cliente.from_json(dic)

    # -------- CRUD --------
    def listar(self):
        return self.abrir()

    def listar_id(self, id):
        return next((c for c in self.abrir() if c.get_id() == id), None)

    def inserir(self, obj):
        self._objetos = self.abrir()

        # Validação: e-mail duplicado
        for c in self._objetos:
            if c.get_email().lower() == obj.get_email().lower():
                raise ValueError("E-mail já cadastrado.")

        novo_id = max((c.get_id() for c in self._objetos), default=0) + 1
        obj.set_id(novo_id)
        self._objetos.append(obj)
        self.salvar()

    def atualizar(self, obj):
        self._objetos = self.abrir()

        # Validação: e-mail duplicado (exceto o próprio)
        for c in self._objetos:
            if c.get_email().lower() == obj.get_email().lower() and c.get_id() != obj.get_id():
                raise ValueError("E-mail já cadastrado.")

        for i, c in enumerate(self._objetos):
            if c.get_id() == obj.get_id():
                self._objetos[i] = obj
                self.salvar()
                return
        self.salvar()

    def excluir(self, obj):
        self._objetos = [c for c in self.abrir() if c.get_id() != obj.get_id()]
        self.salvar()

    def autenticar(self, email, senha):
        for c in self.abrir():
            if c.get_email() == email and c.get_senha() == senha:
                return c
        return None
