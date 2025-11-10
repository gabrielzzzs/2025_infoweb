import json
from models.dao import DAO
from models.cliente import ClienteDAO
from models.horario import HorarioDAO


# ============================================================
# Classe Profissional (modelo)
# ============================================================
class Profissional:
    def __init__(self, id, nome, especialidade, conselho, email, senha):
        self.set_id(id)
        self.set_nome(nome)
        self.set_especialidade(especialidade)
        self.set_conselho(conselho)
        self.set_email(email)
        self.set_senha(senha)

    # ----------- Getters -----------
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_especialidade(self): return self.__especialidade
    def get_conselho(self): return self.__conselho
    def get_email(self): return self.__email
    def get_senha(self): return self.__senha

    # ----------- Setters -----------
    def set_id(self, id): self.__id = id

    def set_nome(self, nome):
        if not nome:
            raise ValueError("O nome do profissional não pode ser vazio.")
        self.__nome = nome

    def set_especialidade(self, esp): self.__especialidade = esp
    def set_conselho(self, conselho): self.__conselho = conselho

    def set_email(self, email):
        if not email:
            raise ValueError("O e-mail do profissional não pode ser vazio.")
        self.__email = email

    def set_senha(self, senha):
        if not senha:
            raise ValueError("A senha do profissional não pode ser vazia.")
        self.__senha = senha

    # ----------- Serialização -----------
    def to_json(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "especialidade": self.__especialidade,
            "conselho": self.__conselho,
            "email": self.__email,
            "senha": self.__senha
        }

    @staticmethod
    def from_json(dic):
        return Profissional(
            dic.get("id", 0),
            dic.get("nome", ""),
            dic.get("especialidade", ""),
            dic.get("conselho", ""),
            dic.get("email", ""),
            dic.get("senha", "")
        )

    def __str__(self):
        return f"{self.__id} - {self.__nome} ({self.__especialidade}) - {self.__conselho} - {self.__email}"


# ============================================================
# DAO - Herdando da classe base DAO
# ============================================================
class ProfissionalDAO(DAO):
    def __init__(self):
        super().__init__("profissionais.json")

    def from_json(self, dic):
        return Profissional.from_json(dic)

    # ---------- CRUD ----------
    def inserir(self, obj):
        self._objetos = self.abrir()

        # Valida e-mail duplicado (clientes + profissionais) e admin
        clientes = ClienteDAO.listar()
        for c in clientes:
            if c.get_email().lower() == obj.get_email().lower() or "admin" in obj.get_email().lower():
                raise ValueError("E-mail já cadastrado ou reservado para admin.")

        for p in self._objetos:
            if p.get_email().lower() == obj.get_email().lower():
                raise ValueError("E-mail já cadastrado.")

        obj.set_id(max((p.get_id() for p in self._objetos), default=0) + 1)
        self._objetos.append(obj)
        self.salvar()

    def listar(self):
        return self.abrir()

    def listar_id(self, id):
        return next((p for p in self.abrir() if p.get_id() == id), None)

    def atualizar(self, obj):
        self._objetos = self.abrir()

        clientes = ClienteDAO.listar()
        for c in clientes:
            if c.get_email().lower() == obj.get_email().lower() or "admin" in obj.get_email().lower():
                raise ValueError("E-mail já cadastrado ou reservado para admin.")

        for p in self._objetos:
            if p.get_email().lower() == obj.get_email().lower() and p.get_id() != obj.get_id():
                raise ValueError("E-mail já cadastrado.")

        for i, p in enumerate(self._objetos):
            if p.get_id() == obj.get_id():
                self._objetos[i] = obj
                self.salvar()
                return

        self.salvar()

    def excluir(self, obj):
        self._objetos = self.abrir()

        # Impede exclusão de profissional com horários cadastrados
        for h in HorarioDAO.listar():
            if h.get_id_profissional() == obj.get_id():
                raise ValueError("Não é possível excluir profissional com horários cadastrados.")

        self._objetos = [p for p in self._objetos if p.get_id() != obj.get_id()]
        self.salvar()

    # ---------- Autenticação ----------
    def autenticar(self, email, senha):
        self._objetos = self.abrir()
        for p in self._objetos:
            if p.get_email() == email and p.get_senha() == senha:
                return p
        return None
