import json

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
        self.__nome = nome

    def set_email(self, email):
        if not email or email.strip() == "":
            raise ValueError("O e-mail do cliente não pode ser vazio.")
        self.__email = email

    def set_fone(self, fone): self.__fone = fone

    def set_senha(self, senha):
        if not senha or senha.strip() == "":
            raise ValueError("A senha do cliente não pode ser vazia.")
        self.__senha = senha

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
# DAO - Persistência em JSON
# ============================================================
class ClienteDAO:
    __arquivo = "clientes.json"
    __objetos = []

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open(cls.__arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                if conteudo:
                    lista = json.loads(conteudo)
                    cls.__objetos = [Cliente.from_json(dic) for dic in lista]
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    @classmethod
    def salvar(cls):
        with open(cls.__arquivo, "w", encoding="utf-8") as f:
            json.dump([obj.to_json() for obj in cls.__objetos], f, ensure_ascii=False, indent=4)

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
    def inserir(cls, obj):
        cls.abrir()
        novo_id = max((c.get_id() for c in cls.__objetos), default=0) + 1
        obj.set_id(novo_id)
        cls.__objetos.append(obj)
        cls.salvar()

    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        for i, c in enumerate(cls.__objetos):
            if c.get_id() == obj.get_id():
                cls.__objetos[i] = obj
                cls.salvar()
                return
        cls.salvar()

    @classmethod
    def excluir(cls, obj):
        cls.abrir()
        cls.__objetos = [c for c in cls.__objetos if c.get_id() != obj.get_id()]
        cls.salvar()

    @classmethod
    def autenticar(cls, email, senha):
        cls.abrir()
        for c in cls.__objetos:
            if c.get_email() == email and c.get_senha() == senha:
                return c
        return None
