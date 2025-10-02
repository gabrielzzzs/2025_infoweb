import json

class Profissional:
    def __init__(self, id, nome, especialidade, email, fone):
        self.set_id(id)
        self.set_nome(nome)
        self.set_especialidade(especialidade)
        self.set_email(email)
        self.set_fone(fone)

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_especialidade(self): return self.__especialidade
    def get_email(self): return self.__email
    def get_fone(self): return self.__fone

    def set_id(self, id): self.__id = id
    def set_nome(self, nome): self.__nome = nome
    def set_especialidade(self, esp): self.__especialidade = esp
    def set_email(self, email): self.__email = email
    def set_fone(self, fone): self.__fone = fone

    def to_json(self):
        return {"id": self.__id, "nome": self.__nome,
                "especialidade": self.__especialidade,
                "email": self.__email, "fone": self.__fone}

    @staticmethod
    def from_json(dic):
        return Profissional(dic["id"], dic["nome"], dic["especialidade"], dic["email"], dic["fone"])

    def __str__(self):
        return f"{self.__id} - {self.__nome} ({self.__especialidade}) - {self.__email} - {self.__fone}"
    

class ProfissionalDAO:
    __objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        id = 0
        for aux in cls.__objetos:
            if aux.get_id() > id: id = aux.get_id()
        obj.set_id(id + 1)
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
            if obj.get_id() == id: return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux != None:
            cls.__objetos.remove(aux)
            cls.__objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux != None:
            cls.__objetos.remove(aux)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.__objetos = []
    try:
        with open("profissionais.json", mode="r") as arquivo:
            conteudo = arquivo.read().strip()
            if conteudo:  # só tenta carregar se não estiver vazio
                list_dic = json.loads(conteudo)
                for dic in list_dic:
                    obj = Profissional.from_json(dic)
                    cls.__objetos.append(obj)
    except FileNotFoundError:
        # se o arquivo não existe, apenas ignora
        pass
    except json.JSONDecodeError:
        # se o arquivo existe mas está vazio ou corrompido, ignora também
        pass


    @classmethod
    def salvar(cls):
        with open("profissionais.json", mode="w") as arquivo:
            json.dump(cls.__objetos, arquivo, default=Profissional.to_json)

