import json
from models.cliente import ClienteDAO
from models.horario import HorarioDAO

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
# DAO - Data Access Object (Persistência em JSON)
# ============================================================
class ProfissionalDAO:
    __arquivo = "profissionais.json"
    __objetos = []

    # ---------- CRUD ----------
    @classmethod
    def inserir(cls, obj):
        cls.abrir()

        # Valida e-mail duplicado (clientes + profissionais) e admin
        clientes = ClienteDAO.listar()
        for c in clientes:
            if c.get_email().lower() == obj.get_email().lower() or obj.get_email().lower() == "admin":
                raise ValueError("E-mail já cadastrado ou reservado para admin.")
        for p in cls.__objetos:
            if p.get_email().lower() == obj.get_email().lower():
                raise ValueError("E-mail já cadastrado.")

        # ID
        obj.set_id(max((p.get_id() for p in cls.__objetos), default=0) + 1)
        cls.__objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.__objetos

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for obj in cls.__objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        cls.abrir()

        # Valida e-mail duplicado (clientes + profissionais) e admin
        clientes = ClienteDAO.listar()
        for c in clientes:
            if c.get_email().lower() == obj.get_email().lower() or obj.get_email().lower() == "admin":
                raise ValueError("E-mail já cadastrado ou reservado para admin.")
        for p in cls.__objetos:
            if p.get_email().lower() == obj.get_email().lower() and p.get_id() != obj.get_id():
                raise ValueError("E-mail já cadastrado.")

        for i, p in enumerate(cls.__objetos):
            if p.get_id() == obj.get_id():
                cls.__objetos[i] = obj
                cls.salvar()
                return
        cls.salvar()

    @classmethod
    def excluir(cls, obj):
        cls.abrir()

        # Impede exclusão de profissional com horários cadastrados
        for h in HorarioDAO.listar():
            if h.get_id_profissional() == obj.get_id():
                raise ValueError("Não é possível excluir profissional com horários cadastrados.")

        cls.__objetos = [p for p in cls.__objetos if p.get_id() != obj.get_id()]
        cls.salvar()

    # ---------- Persistência ----------
    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open(cls.__arquivo, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read().strip()
                if conteudo:
                    list_dic = json.loads(conteudo)
                    cls.__objetos = [Profissional.from_json(dic) for dic in list_dic]
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    @classmethod
    def salvar(cls):
        with open(cls.__arquivo, "w", encoding="utf-8") as arquivo:
            json.dump([obj.to_json() for obj in cls.__objetos], arquivo, ensure_ascii=False, indent=4)

    # ---------- Autenticação ----------
    @classmethod
    def autenticar(cls, email, senha):
        cls.abrir()
        for p in cls.__objetos:
            if p.get_email() == email and p.get_senha() == senha:
                return p
        return None
