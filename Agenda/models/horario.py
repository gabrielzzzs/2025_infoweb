import json
from datetime import datetime
from models.dao import DAO

# ============================================================
# Classe Horario (modelo)
# ============================================================
class Horario:
    def __init__(self, id, data, confirmado, id_cliente, id_servico, id_profissional):
        self.set_id(id)
        self.set_data(data)
        self.set_confirmado(confirmado)
        self.set_id_cliente(id_cliente)
        self.set_id_servico(id_servico)
        self.set_id_profissional(id_profissional)

        # Novos atributos para cancelamento/reagendamento
        self.__status = "pendente"          # pendente, realizado, cancelado, remarcado
        self.__data_cancelamento = None
        self.__data_reagendamento = None

    # ---------------- Getters ----------------
    def get_id(self): return self.__id
    def get_data(self): return self.__data
    def get_confirmado(self): return self.__confirmado
    def get_id_cliente(self): return self.__id_cliente
    def get_id_servico(self): return self.__id_servico
    def get_id_profissional(self): return self.__id_profissional
    def get_status(self): return self.__status
    def get_data_cancelamento(self): return self.__data_cancelamento
    def get_data_reagendamento(self): return self.__data_reagendamento

    # ---------------- Setters ----------------
    def set_id(self, id): self.__id = id

    def set_data(self, data):
        if not isinstance(data, datetime):
            raise ValueError("Data inválida.")
        if data.year < 2025:
            raise ValueError("Data inválida: o horário não pode ser anterior ao ano de 2025.")
        self.__data = data

    def set_confirmado(self, confirmado): self.__confirmado = bool(confirmado)
    def set_id_cliente(self, id_cliente): self.__id_cliente = id_cliente
    def set_id_servico(self, id_servico): self.__id_servico = id_servico
    def set_id_profissional(self, id_profissional): self.__id_profissional = id_profissional

    def set_status(self, status):
        if status not in ["pendente", "realizado", "cancelado", "remarcado"]:
            raise ValueError("Status inválido.")
        self.__status = status

    def set_data_cancelamento(self, data): self.__data_cancelamento = data
    def set_data_reagendamento(self, data): self.__data_reagendamento = data

    # ---------------- Serialização ----------------
    def to_json(self):
        return {
            "id": self.__id,
            "data": self.__data.strftime("%d/%m/%Y %H:%M"),
            "confirmado": self.__confirmado,
            "id_cliente": self.__id_cliente,
            "id_servico": self.__id_servico,
            "id_profissional": self.__id_profissional,
            "status": self.__status,
            "data_cancelamento": self.__data_cancelamento.strftime("%d/%m/%Y %H:%M") if self.__data_cancelamento else None,
            "data_reagendamento": self.__data_reagendamento.strftime("%d/%m/%Y %H:%M") if self.__data_reagendamento else None
        }

    @staticmethod
    def from_json(dic):
        data = datetime.strptime(dic.get("data"), "%d/%m/%Y %H:%M")
        horario = Horario(
            dic.get("id"),
            data,
            dic.get("confirmado", False),
            dic.get("id_cliente"),
            dic.get("id_servico"),
            dic.get("id_profissional")
        )
        horario.set_status(dic.get("status", "pendente"))

        if dic.get("data_cancelamento"):
            horario.set_data_cancelamento(datetime.strptime(dic["data_cancelamento"], "%d/%m/%Y %H:%M"))
        if dic.get("data_reagendamento"):
            horario.set_data_reagendamento(datetime.strptime(dic["data_reagendamento"], "%d/%m/%Y %H:%M"))

        return horario

    def __str__(self):
        return f"{self.__id} - {self.__data.strftime('%d/%m/%Y %H:%M')} - Status: {self.__status} - Confirmado: {self.__confirmado}"


# ============================================================
# DAO - Herdando da classe base DAO
# ============================================================
class HorarioDAO(DAO):
    def __init__(self):
        super().__init__("horarios.json")

    def from_json(self, dic):
        return Horario.from_json(dic)

    # ---------------- CRUD ----------------
    def listar(self):
        return self.abrir()

    def listar_id(self, id):
        return next((h for h in self.abrir() if h.get_id() == id), None)

    def inserir(self, obj):
        self._objetos = self.abrir()

        # Validação: duplicidade de horário para o mesmo profissional
        for h in self._objetos:
            if h.get_id_profissional() == obj.get_id_profissional() and h.get_data() == obj.get_data():
                raise ValueError("Já existe um horário neste dia e hora para este profissional.")

        novo_id = max((h.get_id() for h in self._objetos), default=0) + 1
        obj.set_id(novo_id)
        self._objetos.append(obj)
        self.salvar()

    def atualizar(self, obj):
        self._objetos = self.abrir()

        # Validação: duplicidade ao atualizar
        for h in self._objetos:
            if (
                h.get_id() != obj.get_id()
                and h.get_id_profissional() == obj.get_id_profissional()
                and h.get_data() == obj.get_data()
            ):
                raise ValueError("Já existe um horário neste dia e hora para este profissional.")

        for i, h in enumerate(self._objetos):
            if h.get_id() == obj.get_id():
                self._objetos[i] = obj
                break

        self.salvar()

    def excluir(self, obj):
        self._objetos = self.abrir()
        target = self.listar_id(obj.get_id())

        if not target:
            return

        # Validação: não excluir se já estiver agendado por cliente
        if target.get_id_cliente() is not None:
            raise ValueError("Não é possível excluir um horário que já foi agendado por um cliente.")

        self._objetos = [h for h in self._objetos if h.get_id() != obj.get_id()]
        self.salvar()

    # ---------------- Cancelamento / Reagendamento ----------------
    def cancelar_horario(self, horario, data_cancelamento):
        horario.set_status("cancelado")
        horario.set_data_cancelamento(data_cancelamento)
        self.atualizar(horario)

    def reagendar_horario(self, horario, nova_data):
        horario.set_data(nova_data)
        horario.set_status("remarcado")
        horario.set_data_reagendamento(nova_data)
        self.atualizar(horario)
