import json
from datetime import datetime

class Horario:
    def __init__(self, id, data, confirmado, id_cliente, id_servico, id_profissional):
        self.set_id(id)
        self.set_data(data)
        self.set_confirmado(confirmado)
        self.set_id_cliente(id_cliente)
        self.set_id_servico(id_servico)
        self.set_id_profissional(id_profissional)

    # Getters
    def get_id(self): return self.__id
    def get_data(self): return self.__data
    def get_confirmado(self): return self.__confirmado
    def get_id_cliente(self): return self.__id_cliente
    def get_id_servico(self): return self.__id_servico
    def get_id_profissional(self): return self.__id_profissional

    # Setters
    def set_id(self, id): self.__id = id

    def set_data(self, data):
        # validação: não aceitar ano anterior a 2025
        if not isinstance(data, datetime):
            raise ValueError("Data inválida.")
        if data.year < 2025:
            raise ValueError("Data inválida: o horário não pode ser anterior ao ano de 2025.")
        self.__data = data

    def set_confirmado(self, confirmado): self.__confirmado = bool(confirmado)
    def set_id_cliente(self, id_cliente): self.__id_cliente = id_cliente
    def set_id_servico(self, id_servico): self.__id_servico = id_servico
    def set_id_profissional(self, id_profissional): self.__id_profissional = id_profissional

    # JSON helpers
    def to_json(self):
        return {
            "id": self.__id,
            "data": self.__data.strftime("%d/%m/%Y %H:%M"),
            "confirmado": self.__confirmado,
            "id_cliente": self.__id_cliente,
            "id_servico": self.__id_servico,
            "id_profissional": self.__id_profissional
        }

    @staticmethod
    def from_json(dic):
        data = datetime.strptime(dic["data"], "%d/%m/%Y %H:%M")
        return Horario(dic["id"], data, dic.get("confirmado", False), dic.get("id_cliente"), dic.get("id_servico"), dic.get("id_profissional"))

    def __str__(self):
        return f"{self.__id} - {self.__data.strftime('%d/%m/%Y %H:%M')} - Confirmado: {self.__confirmado}"

# DAO (persistência em horarios.json) com validações (duplicidade/exclusão)
class HorarioDAO:
    __objetos = []

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("horarios.json", "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read().strip()
                if conteudo:
                    lista = json.loads(conteudo)
                    for dic in lista:
                        cls.__objetos.append(Horario.from_json(dic))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    @classmethod
    def salvar(cls):
        with open("horarios.json", "w", encoding="utf-8") as arquivo:
            json.dump([h.to_json() for h in cls.__objetos], arquivo, ensure_ascii=False, indent=2)

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
        # valida duplicidade: mesmo profissional e mesma data/hora
        for h in cls.__objetos:
            if h.get_id_profissional() == obj.get_id_profissional() and h.get_data() == obj.get_data():
                raise ValueError("Já existe um horário neste dia e hora para este profissional.")
        # inicializa como disponível
        obj.set_id_cliente(None)
        obj.set_id_servico(None)
        obj.set_confirmado(False)
        novo_id = max([h.get_id() for h in cls.__objetos], default=0) + 1
        obj.set_id(novo_id)
        cls.__objetos.append(obj)
        cls.salvar()

    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        # valida duplicidade ao atualizar (outro id com mesma data/profissional)
        for h in cls.__objetos:
            if h.get_id() != obj.get_id() and h.get_id_profissional() == obj.get_id_profissional() and h.get_data() == obj.get_data():
                raise ValueError("Já existe um horário neste dia e hora para este profissional.")
        aux = cls.listar_id(obj.get_id())
        if aux:
            cls.__objetos.remove(aux)
            cls.__objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        cls.abrir()
        # não permite excluir se já agendado por cliente
        target = cls.listar_id(obj.get_id())
        if not target:
            return
        if target.get_id_cliente() is not None:
            raise ValueError("Não é possível excluir um horário que já foi agendado por um cliente.")
        cls.__objetos = [h for h in cls.__objetos if h.get_id() != obj.get_id()]
        cls.salvar()
